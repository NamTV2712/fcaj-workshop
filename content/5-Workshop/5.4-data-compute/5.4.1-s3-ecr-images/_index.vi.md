---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.1-prepare/"]
title: "S3, ECR và build image ARM64"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

## 1. Xác nhận bucket của bạn

Trên **S3 → General purpose buckets**, tìm tên `StagingRecordingsBucket` trong output stack `tina-staging`. Bucket được tạo riêng trong tài khoản này; để **Block all public access** bật. Trong **Properties → Lifecycle rules**, xác nhận quy tắc hết hạn tiền tố `runtime-invocations/`. Không tải lên dữ liệu riêng tư để chụp ảnh.

{{< workshop-screenshot file="07-s3-lab.png" description="Bucket recordings của tài khoản thực hành, chế độ chặn truy cập công khai và lifecycle rule." >}}

## 2. Tạo các ECR repository còn thiếu

Foundation đã tạo `tina-staging/bot`, `tina-staging/runtime`, `tina-staging/meeting-api`. Trong CloudShell tạo bốn repository cần thêm:

```bash
for name in terminal gateway admin-api viegem; do
  aws ecr create-repository --region "$AWS_REGION" \
    --repository-name "tina-staging/$name" \
    --image-tag-mutability IMMUTABLE --encryption-configuration encryptionType=AES256
done
```

Nếu một repository đã tồn tại trong tài khoản của bạn, kiểm tra đúng tên/quyền và bỏ tên đó khỏi vòng lặp rồi chạy các tên còn thiếu. Không thay tiền tố `tina-staging`: một số execution role trong phiên bản template cố định cho phép đọc đúng tiền tố này.

## 3. Tạo IAM instance profile cho builder

Lệnh dưới đây tạo role dùng tạm cho EC2, gắn policy Systems Manager và quyền push ECR có giới hạn trong các repository `tina-staging/*`. Chạy một lần trong CloudShell bằng danh tính có quyền quản lý IAM:

```bash
cat > "$HOME/tina-workshop/builder-trust.json" <<'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}
EOF
cat > "$HOME/tina-workshop/builder-ecr.json" <<EOF
{"Version":"2012-10-17","Statement":[
  {"Effect":"Allow","Action":"ecr:GetAuthorizationToken","Resource":"*"},
  {"Effect":"Allow","Action":["ecr:DescribeRepositories","ecr:DescribeImages","ecr:BatchCheckLayerAvailability","ecr:InitiateLayerUpload","ecr:UploadLayerPart","ecr:CompleteLayerUpload","ecr:PutImage","ecr:BatchGetImage","ecr:GetDownloadUrlForLayer"],"Resource":"arn:aws:ecr:${AWS_REGION}:${TINA_ACCOUNT}:repository/tina-staging/*"}
]}
EOF
aws iam create-role --role-name tina-workshop-builder-role --assume-role-policy-document "file://$HOME/tina-workshop/builder-trust.json"
aws iam attach-role-policy --role-name tina-workshop-builder-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
aws iam put-role-policy --role-name tina-workshop-builder-role --policy-name TinaEcrPush --policy-document "file://$HOME/tina-workshop/builder-ecr.json"
aws iam create-instance-profile --instance-profile-name tina-workshop-builder-profile
aws iam add-role-to-instance-profile --instance-profile-name tina-workshop-builder-profile --role-name tina-workshop-builder-role
```

Nếu role/profile cùng tên đã tồn tại, dừng lại và kiểm tra quyền sở hữu trước khi dùng; đừng ghi đè role của hệ thống khác. Sau khi tạo, đợi IAM đồng bộ trước khi chọn profile ở EC2.

## 4. Tạo máy build ARM64 trên EC2 Console

1. Vào **EC2 → Instances → Launch instances**. Đặt tên `tina-workshop-builder`.
2. Chọn **Amazon Linux 2023**, kiến trúc **64-bit (Arm)**; ví dụ `m7g.2xlarge` nếu Region và quota cho phép. Build bot/model nặng; chọn máy ít RAM có thể hết bộ nhớ. Máy này có phí theo thời gian chạy.
3. **Key pair:** chọn *Proceed without a key pair*. Ở **Network settings**, chọn VPC của stack `tina-staging`, một public subnet trong `PublicSubnetIds`, bật **Auto-assign public IP**. Tạo security group không có inbound rule, giữ outbound cho kết nối Internet.
4. **Configure storage:** ví dụ 200 GiB gp3, bật mã hóa. Trong **Advanced details → IAM instance profile**, chọn `tina-workshop-builder-profile`; bật **IMDSv2 required** nếu tùy chọn xuất hiện. Chọn **Launch instance**.
5. Chờ instance Running và Systems Manager nhận diện máy. Chọn instance → **Connect → Session Manager → Connect**. Nếu tab không kết nối, kiểm tra IAM profile, SSM Agent, public IP, route tới Internet Gateway và outbound HTTPS.

## 5. Build và push image từ EC2

Lệnh trong mục này chạy **trên phiên Session Manager của EC2**, không chạy trong CloudShell. Cài Docker và Git, sau đó dùng shell root cho phiên build tạm:

```bash
sudo dnf install -y docker git
sudo systemctl enable --now docker
sudo -i
cd /root
git clone --filter=blob:none https://github.com/poor-frog/TINA.git tina-source
cd tina-source
git fetch origin feat/s3-ephemeral-workspaces
git checkout --detach 7d6bba8109f6eac51c0d8241a7083e3e364cf59d
git rev-parse HEAD
docker buildx version
```

Tải script build của workshop: {{< workshop-file path="scripts/tina-ecr-build.sh" label="tải tina-ecr-build.sh" >}}. Trong website đã xuất bản, nhấp phải liên kết đó → **Copy link address**. Thay URL vào lệnh sau trên EC2; nếu bạn đang xem tài liệu chưa xuất bản, chuyển đúng file `static/scripts/tina-ecr-build.sh` từ bản workshop của bạn sang EC2 trước.

```bash
curl -fL 'DAN_URL_TEP_SCRIPT_VUA_SAO_CHEP' -o /root/tina-ecr-build.sh
export AWS_REGION=us-east-1
export TINA_IMAGE_TAG=ws-v1
bash /root/tina-ecr-build.sh --source /root/tina-source --region "$AWS_REGION" --plan
```

Kiểm tra bản source, Region, tên repository và nhãn. Lệnh `--plan` không build hay push. Để thử phiên âm bằng VieGem trong phạm vi giấy phép phi thương mại, build thêm image model bằng `--with-viegem`. Model VieGem có giấy phép **CC-BY-NC-SA-4.0** và điều khoản Gemma; đọc [model card](https://huggingface.co/5CD-AI/VieGem-ASR) và [ghi chú giấy phép](https://github.com/poor-frog/TINA/blob/7d6bba8109f6eac51c0d8241a7083e3e364cf59d/deploy/transcription/viegem/README.md) trước khi dùng. Nếu không phù hợp, bỏ `--with-viegem`, bỏ stack VieGem và để trường transcription trống ở core.

```bash
bash /root/tina-ecr-build.sh --source /root/tina-source --region "$AWS_REGION" --with-viegem
```

Build tải dependency và model từ Internet, có thể mất nhiều thời gian và dung lượng. Script build 6 image ứng dụng và một image VieGem khi chọn tùy chọn trên, push vào ECR của **tài khoản gắn với instance role** và in digest. Source được lấy từ commit cố định; script không sao chép các tệp `.env` trong máy. Nếu lệnh lỗi, đọc lỗi đầu tiên; khi chạy lại sau một phần push, dùng `export TINA_IMAGE_TAG=ws-v2` vì tag immutable và đổi `TINA_TAG` tương ứng trong CloudShell.

Trên **ECR → Private repositories**, mở `tina-staging/terminal` hoặc `tina-staging/bot`; kiểm tra tag và digest:

{{< workshop-screenshot file="08-ecr-image.png" description="ECR repository của bạn có image tag và digest sau khi build." >}}

Sau khi kiểm tra mọi image cần thiết đã có, **terminate EC2 builder** nếu không dùng nữa; ECR vẫn giữ image. Không xóa volume hay resource của máy khác.
