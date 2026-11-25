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

## 3. Chi phí

Xem **Billing → Budgets** và **Cost Explorer**; chi phí có thể cập nhật chậm. Kiểm tra NAT, public IPv4, EC2 builder/EBS, RDS, Valkey, Fargate, ALB, CloudFront, WAF, ECR và snapshot. Budget gửi cảnh báo, không tự xóa tài nguyên.

{{< workshop-screenshot file="21-budget.png" description="Budget tài khoản thực hành và trạng thái cảnh báo; che email và account ID." >}}

Khi ngừng thực hành, chuyển sang [dọn dẹp](../5.6-cleanup-evidence/) để tránh tiếp tục tính phí.
