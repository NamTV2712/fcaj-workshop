---
aliases: ["/vi/5-workshop/5.2-prerequiste/"]
title: "Chuẩn bị"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

## 1. Tài khoản và Region

1. Dùng tài khoản AWS riêng để thực hành, có quyền tạo CloudFormation, IAM role, VPC, EC2, ECS, ECR, RDS, ElastiCache, S3, CloudFront, WAF, Secrets Manager và CloudWatch. Không dùng tài khoản sản xuất.
2. Đăng nhập AWS Console, chọn **US East (N. Virginia), `us-east-1`** ở góc trên. CloudFront và WAF cho CloudFront dùng cấu hình toàn cục; WAF API cho CloudFront yêu cầu `us-east-1`.

{{< workshop-screenshot file="00-region.png" description="AWS Console đang chọn Region us-east-1." >}}

3. Trong **Billing and Cost Management → Budgets → Create budget**, tạo budget chi phí với ngưỡng và email của bạn. Xác nhận email cảnh báo theo hướng dẫn AWS. Budget chỉ cảnh báo, không tự dừng tài nguyên.

{{< workshop-screenshot file="00-budget.png" description="Budget và ngưỡng cảnh báo của tài khoản thực hành; che email và account ID." >}}

4. Trong **Service Quotas**, kiểm tra quota Fargate On-Demand, EC2 Graviton, Elastic IP và RDS. Mỗi bot cần 4 vCPU/8 GiB; core 2 vCPU, VieGem 2 vCPU, cùng runtime và terminal. Chừa đủ quota cho cả task thay thế khi ECS triển khai lại. Lưu ý tài khoản **AWS Free Plan** có giới hạn số lượng RDS instance tối đa — nếu tài khoản đã chạy sẵn RDS khác, bước tạo PostgreSQL có thể báo `ServiceLimitExceeded`.

NAT Gateway, IPv4 công cộng, Fargate, RDS, Valkey, ALB, WAF, S3, ECR, builder và CloudFront có thể tính phí. Xem [AWS Pricing Calculator](https://calculator.aws/) theo Region và thời gian bạn định chạy. Đây không phải bài đảm bảo thuộc Free Tier.

> **Lộ trình nhanh (khuyên dùng):** Nếu bạn chọn triển khai nhanh bằng một file CloudFormation và bộ image ARM64 dựng sẵn trên GHCR, sau khi hoàn tất **Mục 1** ở trên, bạn chỉ cần mở **AWS CloudShell (`us-east-1`)** rồi chuyển thẳng sang **[5.4A Triển khai bằng một CloudFormation](../5.4-full-cloudformation/)** (bỏ qua Mục 2 và Mục 3 bên dưới).

## 2. Mã nguồn và template (dành cho lộ trình nhiều stack 5.3 → 5.4)

Bài dùng commit `0c206d46940f95c3469d1a65d18722e4f4fe96e5` trên nhánh `main` của [repository TINA](https://github.com/poor-frog/TINA), đã tích hợp đầy đủ ECS backend, VieGem ASR, Voice, Bedrock (`amazon.nova-lite-v1:0`), Amazon SES (`staging-ses.yml`) và CloudWatch Dashboard/Alarms (`staging-workspace-s3-monitoring.yml`).

Trên máy của bạn, tải [ZIP mã nguồn ở commit này](https://github.com/poor-frog/TINA/archive/0c206d46940f95c3469d1a65d18722e4f4fe96e5.zip), giải nén. Ghi nhớ thư mục `deploy/aws/` vì bước Console sẽ yêu cầu chọn `foundation.yml` (còn nếu chọn lộ trình nhanh 5 lệnh [5.4A](../5.4-full-cloudformation/) thì không cần tải ZIP hay tự build Docker). Không cần sao chép secret từ máy tác giả.

## 3. Mở AWS CloudShell

Trên Console, chọn biểu tượng **CloudShell** và xác nhận Region `us-east-1`. Các lệnh bash từ đây chạy trong CloudShell, trừ khi trang ghi rõ chạy trong Session Manager của EC2.

Trong CloudShell, tải cùng phiên bản template và khai báo các hàm đọc output:

```bash
mkdir -p "$HOME/tina-workshop"
cat > "$HOME/tina-workshop/env.sh" <<'EOF'
export AWS_REGION=us-east-1
export AWS_PAGER=''
export TINA_REV=0c206d46940f95c3469d1a65d18722e4f4fe96e5
export TINA_SRC="$HOME/tina-workshop/TINA-${TINA_REV}"
export TINA_ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
export TINA_TAG=ws-v1
stackout() {
  aws cloudformation describe-stacks --region "$AWS_REGION" --stack-name "$1" \
    --query "Stacks[0].Outputs[?OutputKey=='$2'].OutputValue | [0]" --output text
}
repoarn() {
  aws ecr describe-repositories --region "$AWS_REGION" --repository-names "tina-staging/$1" \
    --query 'repositories[0].repositoryArn' --output text
}
image() {
  local d
  d="$(aws ecr describe-images --region "$AWS_REGION" --repository-name "tina-staging/$1" \
    --image-ids "imageTag=$TINA_TAG" --query 'imageDetails[0].imageDigest' --output text)" || return 1
  printf '%s.dkr.ecr.%s.amazonaws.com/tina-staging/%s@%s' "$TINA_ACCOUNT" "$AWS_REGION" "$1" "$d"
}
EOF
grep -q 'tina-workshop/env.sh' ~/.bashrc || echo 'source "$HOME/tina-workshop/env.sh"' >> ~/.bashrc
source "$HOME/tina-workshop/env.sh"
curl -fL "https://github.com/poor-frog/TINA/archive/${TINA_REV}.zip" -o "$HOME/tina-workshop/source.zip"
unzip -q -o "$HOME/tina-workshop/source.zip" -d "$HOME/tina-workshop"
```

Các lệnh trên tự lưu biến và hàm vào `~/tina-workshop/env.sh` (và nạp sẵn trong `~/.bashrc`), nên dù CloudShell bị đóng/mở lại ở các bước `5.3` → `5.4` vẫn không bị mất `$TINA_SRC`, `$TINA_ACCOUNT`, `$TINA_TAG` hay `stackout`. Các bước sau dùng nhãn image `ws-v1`; nếu build lại sau khi đã push một phần, chọn nhãn mới và dùng nhất quán ở cả EC2 lẫn CloudShell vì ECR đặt immutable.
