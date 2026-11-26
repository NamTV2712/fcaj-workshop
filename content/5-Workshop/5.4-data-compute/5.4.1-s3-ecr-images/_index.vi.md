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

> **Cách nhanh (khuyên dùng — bỏ qua Mục 3, 4, 5, tránh lỗi EC2 hết RAM / SSM Offline):**
> Thay vì tạo máy EC2 để build Docker (rất nặng RAM), bạn có thể chạy khối lệnh dưới đây **ngay trong CloudShell** để copy sẵn các image `linux/arm64` (đã build sẵn từ GHCR) vào ECR với đúng nhãn `$TINA_TAG` (`ws-v1`), rồi chuyển thẳng sang **[5.4.2](../5.4.2-data-secrets/)**:
>
> ```bash
> export AWS_REGION="${AWS_REGION:-us-east-1}"
> export TINA_ACCOUNT="${TINA_ACCOUNT:-$(aws sts get-caller-identity --query Account --output text)}"
> export TINA_TAG="${TINA_TAG:-ws-v1}"
> if [ ! -x /tmp/crane ]; then
>   curl -sSL "https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz" | tar -xz -C /tmp crane
> fi
> ECR_REG="${TINA_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
> aws ecr get-login-password --region "$AWS_REGION" | /tmp/crane auth login "$ECR_REG" -u AWS --password-stdin
> for name in terminal gateway meeting-api admin-api runtime bot viegem; do
>   /tmp/crane copy "ghcr.io/poor-frog/tina-${name}:workshop-arm64" "${ECR_REG}/tina-staging/${name}:${TINA_TAG}"
> done
> ```

## 3. Tạo IAM instance profile cho builder (chỉ làm nếu tự build trên EC2)

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

Lệnh trong mục này chạy **trên phiên Session Manager của EC2**, không chạy trong CloudShell. Tạo thêm 8 GiB swap để tránh bị hết RAM (OOM làm SSM chuyển sang `Offline` khi build `bot`/`viegem`), cài Docker và Git, sau đó dùng shell root cho phiên build tạm:

```bash
sudo fallocate -l 8G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
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

Tải script build của workshop: {{< workshop-file path="scripts/tina-ecr-build.sh" label="tải tina-ecr-build.sh" >}}, **hoặc** dán trực tiếp khối lệnh dưới đây vào EC2 để tạo `/root/tina-ecr-build.sh` mà không cần tải file ngoài:

> **Mẹo triển khai nhanh:** Nếu bạn không muốn tự build Docker trên EC2, xem [5.4A Triển khai nhanh bằng 1 CloudFormation](../../5.4-full-cloudformation/) để copy thẳng bộ 12 image `linux/arm64` dựng sẵn (gồm cả VieGem) từ GHCR vào ECR ngay trong CloudShell.

<details>
<summary>Bấm để mở & copy trực tiếp toàn bộ script <code>/root/tina-ecr-build.sh</code></summary>

```bash
cat > /root/tina-ecr-build.sh <<'EOF'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
readonly EXPECTED_REVISION=7d6bba8109f6eac51c0d8241a7083e3e364cf59d
SOURCE_DIR="$PWD"
REGION="${AWS_REGION:-us-east-1}"
readonly PREFIX=tina-staging
TAG="${TINA_IMAGE_TAG:-ws-$(date -u +%Y%m%d%H%M%S)}"
PLAN_ONLY=0; WITH_VIEGEM=0; WITH_ADDONS=0; WITH_FULL=0
while (($#)); do
  case "$1" in
    --source) SOURCE_DIR="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --with-viegem) WITH_VIEGEM=1; shift ;;
    --with-addons) WITH_ADDONS=1; shift ;;
    --full) WITH_FULL=1; WITH_ADDONS=1; WITH_VIEGEM=1; shift ;;
    --plan) PLAN_ONLY=1; shift ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
SOURCE_DIR="$(cd -- "$SOURCE_DIR" && pwd -P)"
REVISION="$(git -C "$SOURCE_DIR" rev-parse HEAD)"
[[ "$REVISION" == "$EXPECTED_REVISION" ]] || { echo "Wrong source revision: expected $EXPECTED_REVISION, found $REVISION." >&2; exit 1; }
images=(terminal gateway meeting-api admin-api runtime bot)
((WITH_ADDONS)) && images+=(agent-api agent-reach agent-worker mcp flows)
((WITH_VIEGEM)) && images+=(viegem)
printf 'Revision: %s\nRegion: %s\nECR prefix: %s\nTag: %s\n' "$REVISION" "$REGION" "$PREFIX" "$TAG"
((PLAN_ONLY)) && { echo 'Plan only: no image was built or pushed.'; exit 0; }
ACCOUNT="$(aws sts get-caller-identity --region "$REGION" --query Account --output text --no-cli-pager)"
REGISTRY="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf -- "$WORK_DIR"' EXIT
mkdir -p "$WORK_DIR/source"
git -C "$SOURCE_DIR" archive --format=tar "$REVISION" | tar --exclude='.env' --exclude='.env.*' --exclude='.env.keys' -xf - -C "$WORK_DIR/source"
SRC="$WORK_DIR/source"
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$REGISTRY" >/dev/null
push_image() {
  local name="$1" dockerfile="$2" context="$3"; shift 3
  local image="$REGISTRY/$PREFIX/$name:$TAG"
  docker build --platform linux/arm64 --file "$SRC/$dockerfile" --tag "$image" "$@" "$SRC/$context"
  docker push "$image"
}
if ((WITH_FULL)); then
  push_image terminal clients/terminal/Dockerfile . --build-arg NEXT_PUBLIC_TERMINAL_MODE=workspace-pilot
else
  push_image terminal clients/terminal/Dockerfile . --build-arg NEXT_PUBLIC_TERMINAL_MODE=meetings
fi
push_image gateway core/gateway/services/gateway/Dockerfile .
push_image meeting-api core/meetings/services/meeting-api/Dockerfile .
push_image admin-api core/identity/services/admin-api/Dockerfile core/identity/services/admin-api
if ((WITH_FULL)); then
  docker build --platform linux/arm64 --file "$SRC/core/runtime/Dockerfile" --tag tina-workshop/runtime-base "$SRC/core/runtime"
  push_image runtime deploy/aws/workspace-pilot.Dockerfile . --target runtime --build-arg RUNTIME_BASE=tina-workshop/runtime-base --build-arg AGENT_BASE=tina-workshop/runtime-base --build-arg WORKER_BASE=tina-workshop/runtime-base
else
  push_image runtime core/runtime/Dockerfile core/runtime
fi
docker build --platform linux/arm64 --file "$SRC/core/meetings/modules/join/Dockerfile.env" --tag tina/meet-join-env:dev "$SRC/core/meetings/modules/join"
push_image bot core/meetings/services/bot/Dockerfile . --build-arg "TINA_IMAGE_VERSION=$REVISION"
if ((WITH_ADDONS)); then
  if ((WITH_FULL)); then
    docker build --platform linux/arm64 --file "$SRC/core/agent/services/agent-api/Dockerfile" --tag tina/v012-agent-api:staging-voice "$SRC"
    docker build --platform linux/arm64 --file "$SRC/deploy/aws/voice-worker.Dockerfile" --tag tina-workshop/agent-voice "$SRC"
    push_image agent-api deploy/aws/workspace-pilot.Dockerfile . --target agent --build-arg AGENT_BASE=tina-workshop/agent-voice --build-arg RUNTIME_BASE=tina-workshop/agent-voice --build-arg WORKER_BASE=tina-workshop/agent-voice
  else
    push_image agent-api core/agent/services/agent-api/Dockerfile .
  fi
  push_image agent-reach deploy/agent-reach/Dockerfile deploy/agent-reach
  if ((WITH_FULL)); then
    docker build --platform linux/arm64 --file "$SRC/core/agent/worker/Dockerfile" --tag tina-workshop/worker-base "$SRC"
    push_image agent-worker deploy/aws/workspace-pilot.Dockerfile . --target worker --build-arg WORKER_BASE=tina-workshop/worker-base --build-arg RUNTIME_BASE=tina-workshop/worker-base --build-arg AGENT_BASE=tina-workshop/worker-base
  else
    push_image agent-worker core/agent/worker/Dockerfile .
  fi
  push_image mcp core/meetings/services/mcp/Dockerfile core/meetings/services/mcp
  push_image flows core/flows/Dockerfile .
fi
if ((WITH_VIEGEM)); then
  ASSETS="${TINA_VIEGEM_CACHE:-$HOME/.cache/tina-workshop/viegem-fsmn}"
  mkdir -p "$ASSETS"
  docker build --platform linux/arm64 --build-arg TORCH_VARIANT=cpu --file "$SRC/deploy/transcription/viegem/Dockerfile" --tag tina/v012-viegem:staging-cpu-base "$SRC"
  docker run --rm --platform linux/arm64 --mount "type=bind,src=$ASSETS,dst=/assets" tina/v012-viegem:staging-cpu-base python install-models.py --directory /assets
  push_image viegem deploy/aws/viegem.Dockerfile deploy/aws --build-context "viegem_assets=$ASSETS"
fi
for name in "${images[@]}"; do
  digest="$(aws ecr describe-images --region "$REGION" --repository-name "$PREFIX/$name" --image-ids "imageTag=$TAG" --query 'imageDetails[0].imageDigest' --output text --no-cli-pager)"
  printf '%-14s %s/%s/%s@%s\n' "$name" "$REGISTRY" "$PREFIX" "$name" "$digest"
done
EOF
chmod +x /root/tina-ecr-build.sh
```

</details>

Sau khi đã có `/root/tina-ecr-build.sh`, chạy kiểm tra kế hoạch build (`--plan`):

```bash
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
