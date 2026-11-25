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

4. Trong **Service Quotas**, kiểm tra quota Fargate On-Demand, EC2 Graviton và Elastic IP. Mỗi bot cần 4 vCPU/8 GiB; core 2 vCPU, VieGem 2 vCPU, cùng runtime và terminal. Chừa đủ quota cho cả task thay thế khi ECS triển khai lại. Nếu quota thiếu, yêu cầu tăng trước khi tiếp tục.

NAT Gateway, IPv4 công cộng, Fargate, RDS, Valkey, ALB, WAF, S3, ECR, builder và CloudFront có thể tính phí. Xem [AWS Pricing Calculator](https://calculator.aws/) theo Region và thời gian bạn định chạy. Đây không phải bài đảm bảo thuộc Free Tier.

## 2. Mã nguồn và template

Bài dùng commit cố định `7d6bba8109f6eac51c0d8241a7083e3e364cf59d` trong [repository TINA](https://github.com/poor-frog/TINA), có ECS backend. Đừng thay bằng `main`: phiên bản `main` đã kiểm tra không có backend ECS tương ứng.

Trên máy của bạn, tải [ZIP mã nguồn ở commit này](https://github.com/poor-frog/TINA/archive/7d6bba8109f6eac51c0d8241a7083e3e364cf59d.zip), giải nén. Ghi nhớ thư mục `deploy/aws/` vì bước Console sẽ yêu cầu chọn `foundation.yml`. Thực hiện build bằng một EC2 ARM64 riêng ở phần sau; không cần sao chép secret từ máy tác giả.

## 3. Mở AWS CloudShell

Trên Console, chọn biểu tượng **CloudShell** và xác nhận Region `us-east-1`. Các lệnh bash từ đây chạy trong CloudShell, trừ khi trang ghi rõ chạy trong Session Manager của EC2.

Trong CloudShell, tải cùng phiên bản template và khai báo các hàm đọc output:

```bash
export AWS_REGION=us-east-1
export AWS_PAGER=''
export TINA_REV=7d6bba8109f6eac51c0d8241a7083e3e364cf59d
mkdir -p "$HOME/tina-workshop"
curl -fL "https://github.com/poor-frog/TINA/archive/${TINA_REV}.zip" -o "$HOME/tina-workshop/source.zip"
unzip -q -o "$HOME/tina-workshop/source.zip" -d "$HOME/tina-workshop"
export TINA_SRC="$HOME/tina-workshop/TINA-${TINA_REV}"
stackout() { aws cloudformation describe-stacks --region "$AWS_REGION" --stack-name "$1" --query "Stacks[0].Outputs[?OutputKey=='$2'].OutputValue | [0]" --output text; }
repoarn() { aws ecr describe-repositories --region "$AWS_REGION" --repository-names "tina-staging/$1" --query 'repositories[0].repositoryArn' --output text; }
export TINA_ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
export TINA_TAG=ws-v1
```

Các lệnh ghi file trong thư mục CloudShell của bạn. Nếu CloudShell mở lại và mất biến/hàm, chạy lại khối trên; không phải tạo lại stack. Các bước sau dùng nhãn image `ws-v1`; nếu build lại sau khi đã push một phần, chọn nhãn mới và dùng nhất quán ở cả EC2 lẫn CloudShell vì ECR đặt immutable.
