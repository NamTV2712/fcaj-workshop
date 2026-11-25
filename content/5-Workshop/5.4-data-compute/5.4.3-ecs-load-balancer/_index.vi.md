---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.3-test-endpoint/"]
title: "Triển khai ECS và website"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

## Thứ tự triển khai

Các bước dưới đây tạo website trên VPC và cluster **của bạn**. Chạy các lệnh trong CloudShell với hàm `stackout`, `repoarn` và biến `TINA_SRC`, `TINA_TAG` đã chuẩn bị. Mỗi trang yêu cầu stack trước đó thành công.

1. [Tạo WAF và CloudFront/ALB](5.4.3.1-edge/).
2. [Tạo bot task và Runtime](5.4.3.2-runtime/).
3. [Tạo ASR tùy chọn và core](5.4.3.3-core/).
4. [Cấu hình Google và triển khai Terminal](5.4.3.4-terminal/).
5. [Xem phạm vi và các tính năng mở rộng](5.4.3.5-extensions/).

Trước khi tiếp tục, xác nhận nhãn image trong CloudShell khớp nhãn đã build trên EC2:

```bash
export TINA_TAG=ws-v1
image() {
  local name="$1" digest
  digest="$(aws ecr describe-images --region "$AWS_REGION" --repository-name "tina-staging/$name" --image-ids "imageTag=$TINA_TAG" --query 'imageDetails[0].imageDigest' --output text)" || return 1
  [[ "$digest" =~ ^sha256:[a-f0-9]{64}$ ]] || { echo "Không tìm thấy digest của $name:$TINA_TAG" >&2; return 1; }
  printf '%s.dkr.ecr.%s.amazonaws.com/tina-staging/%s@%s' "$TINA_ACCOUNT" "$AWS_REGION" "$name" "$digest"
}
image terminal
```

Nếu build bằng tag khác, đổi `TINA_TAG` cho khớp. Mỗi task Fargate trong template dùng **ARM64**; không dùng nhầm image AMD64. Giá trị digest và ARN thuộc tài khoản của bạn, không cần công khai khi chụp ảnh.
