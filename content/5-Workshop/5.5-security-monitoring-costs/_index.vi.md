---
aliases: ["/vi/5-workshop/5.5-policy/"]
title: "Bảo mật, giám sát và chi phí"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

## 1. Kiểm tra quyền và secret

Vào **IAM → Roles**, xem execution role và task role do stack tạo. Kiểm tra ECR repository, S3 bucket, Secrets Manager và ECS task được cấp quyền phù hợp với môi trường của bạn. Không chụp policy chứa account ID nếu chưa che. EC2 builder chỉ nên tồn tại trong thời gian build.

{{< workshop-screenshot file="19-role-policy.png" description="Role và phạm vi policy của môi trường thực hành; che định danh tài khoản." >}}

RDS, Valkey và service chạy trong subnet riêng; secret được tham chiếu bằng ARN. CloudFront sử dụng WAF và VPC origin tới ALB nội bộ. Cấu hình hiện tại dành cho lab: xem lại mã hóa kết nối nội bộ, backup, IAM và rule WAF trước khi phục vụ người dùng thật.

## 2. Xem log và health

Trong **ECS → Clusters → service → Tasks → task → Logs**, hoặc **CloudWatch → Log groups**, xem log khi task khởi động và lúc thử meeting. Trong CloudFormation, tab **Events** cho biết lỗi khởi tạo stack. Không đưa access token, URL meeting, nội dung transcript hoặc thông tin cá nhân vào ảnh.

{{< workshop-screenshot file="20-logs.png" description="CloudWatch log của task đã che token, thông tin người dùng và nội dung meeting." >}}

Nếu ECS `CannotPullContainerError`, kiểm tra đúng digest ARM64, execution role ECR và đường ra NAT. Nếu hết quota, kiểm tra Service Quotas. Nếu target unhealthy, kiểm tra log Terminal, port 3000 và health path `/api/auth/providers`.

## 3. Ước tính chi phí và tối ưu chi phí

Xem **Billing → Budgets** và **Cost Explorer**; chi phí có thể cập nhật chậm. Budget chỉ gửi cảnh báo, không tự xóa tài nguyên.

### Ước tính chi phí tham khảo (`us-east-1`, môi trường thí điểm)

Bảng dưới ước tính theo giá on-demand tại `us-east-1` với tải thí điểm (~10 người dùng, ~5 cuộc họp/tuần, ~20 giờ họp/tháng):

| Nhóm dịch vụ | Cấu hình chính | Chi phí ước tính/tháng |
| --- | --- | --- |
| **ECS Fargate (ARM64)** | Terminal, Core, Runtime, Agent (chạy 24/7) + Bot/VieGem (chạy theo cuộc họp ~20 giờ/tháng) | ~38–42 USD |
| **Mạng** | 1 ALB (~18 USD) + 1 NAT Gateway (~33 USD) + 3 Public IPv4 (~11 USD) + CloudFront (~1 USD) | ~63 USD |
| **Dữ liệu** | RDS PostgreSQL `db.t4g.micro` (~14 USD) + ElastiCache Valkey `cache.t4g.micro` (~11.7 USD) + S3 (~0.3 USD) | ~26 USD |
| **Bảo mật & Giám sát** | AWS WAF (~8 USD) + Secrets Manager (~2 USD) + KMS (~1 USD) + CloudWatch (~3.5 USD) + ECR (~1 USD) | ~15.5 USD |
| **Tổng cộng (chạy 24/7)** | Toàn bộ kiến trúc thí điểm | **~145 USD/tháng** |

### Các biện pháp tối ưu chi phí

1. **Dùng kiến trúc ARM64 (Graviton) trên Fargate & RDS `t4g`**: giảm ~20% chi phí compute so với x86_64 cùng cấu hình.
2. **Dùng VPC Endpoints (S3 Gateway miễn phí, ECR/Logs/Secrets Manager)**: giảm lưu lượng đi qua NAT Gateway (tránh phí $0.045/GB xử lý qua NAT).
3. **Tắt/scale về 0 ngoài giờ làm việc**: đưa các ECS service không cần trực về `desiredCount=0` và tạm dừng RDS ngoài giờ (~10 giờ/ngày, 5 ngày/tuần) giúp giảm chi phí thực tế xuống còn **~70–80 USD/tháng**.
4. **Chạy Bot & VieGem theo nhu cầu (on-demand)**: task Bot chỉ spawn khi có cuộc họp và tự dừng khi kết thúc, không tốn tiền chạy nhàn rỗi 24/7.
5. **S3 Lifecycle & Budget Alerts**: cấu hình rule tự xóa file tạm `runtime-invocations/` sau 1 ngày, chuyển bản ghi âm cũ sang lớp lưu trữ rẻ hơn và đặt **AWS Budgets** cảnh báo ở các mốc **50%, 80%, 100%**.

{{< workshop-screenshot file="21-budget.png" description="Budget tài khoản thực hành và trạng thái cảnh báo; che email và account ID." >}}

Khi ngừng thực hành, chuyển sang [dọn dẹp](../5.6-cleanup-evidence/) để tránh tiếp tục tính phí.
