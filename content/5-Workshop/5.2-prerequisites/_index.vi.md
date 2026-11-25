---
aliases: ["/vi/5-workshop/5.2-prerequiste/"]
title: "Chuẩn bị"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

## 1. Tài khoản và phạm vi

1. Đăng nhập AWS Console bằng danh tính được cấp quyền phù hợp; ưu tiên IAM Identity Center hoặc IAM role, không dùng root cho công việc thường ngày.
2. Xác định bạn đang dùng **tài khoản lab riêng** hay chỉ được **đọc staging hiện có**. Nếu người đánh giá không được cấp quyền vào staging, cung cấp báo cáo/ảnh đã kiểm duyệt thay vì yêu cầu truy cập tài khoản của bạn.
3. Chọn Region **US East (N. Virginia), `us-east-1`**. Với tài khoản khác, chọn hai Availability Zone khả dụng trong tài khoản; tên `1a`/`1b` không nhất thiết tương ứng cùng vị trí vật lý giữa các tài khoản.

{{< workshop-screenshot file="00-region.png" description="Region us-east-1 được chọn trong AWS Console." >}}

4. Đặt tiền tố lab riêng, ví dụ `tina-ws-an`, và ghi lại VPC ID, subnet ID, route table ID, security group ID ở tài liệu cá nhân. Không thay thế tài nguyên staging/prod bằng tên của lab.

## 2. Chi phí

Vào **Billing and Cost Management → Budgets → Create budget**; chọn **Cost budget**, đặt mức tiền và email bạn quản lý, rồi tạo cảnh báo. Ước tính trước bằng [AWS Pricing Calculator](https://calculator.aws/), ít nhất gồm NAT gateway và lưu lượng, IP công cộng, ECS, RDS, ElastiCache, VPC interface endpoint, CloudFront và lưu trữ. Một budget là cảnh báo, không bảo đảm tự dừng chi phí. Việc tắt lab phải làm theo trang [Dọn dẹp](../5.6-cleanup-evidence/).

{{< workshop-screenshot file="00-budget.png" description="Budget và ngưỡng cảnh báo của tài khoản lab; che địa chỉ email." >}}

## 3. Công cụ cho phần tùy chọn

Bạn có thể làm phần Console mà không cần CLI. Để kiểm tra source/image trên máy, chuẩn bị Git, Docker, Docker Compose, `make`, AWS CLI và quyền đọc source được cấp. Trên Windows dùng WSL2 cho các lệnh bash; phiên bản Node/pnpm áp dụng theo repository TINA bạn được giao. Kiểm tra:

```bash
git --version
aws --version
docker version
docker compose version
make --version
aws sts get-caller-identity
```

Không dán output chứa thông tin nhạy cảm vào báo cáo. `git clone` chỉ thực hiện khi người hướng dẫn đã cấp URL và quyền đọc đúng; ghi commit/release và image digest để người khác dùng cùng một phiên bản. Không yêu cầu người tham gia sao chép `.env.keys` của chủ dự án.

## 4. Điều kiện để triển khai đầy đủ

Cần bộ source/image có quyền truy cập và phiên bản cố định, cấu hình cho tất cả service, cách quản lý secret, domain/certificate nếu dùng HTTPS và cấu hình STT tự host tương thích OpenAI. Chỉ tạo một task Terminal, một database và một bucket thì chưa đủ chạy TINA. Bộ release đã kiểm chứng từ tài khoản trống hiện chưa được cung cấp trong workshop này.

Ghi lại ngày, region, vai trò của bạn và giới hạn ngân sách; không lưu secret vào Git.
