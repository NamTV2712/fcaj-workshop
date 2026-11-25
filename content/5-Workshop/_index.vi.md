---
title: "Triển khai TINA trên AWS"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Triển khai website TINA trên AWS

Workshop hướng dẫn bạn dùng **tài khoản AWS của chính mình** để dựng một bản TINA thử nghiệm: CloudFront → ALB nội bộ → ECS Fargate, cùng PostgreSQL trên RDS, Valkey trên ElastiCache, S3 và ECR. Bạn tạo tài nguyên mới và đăng nhập vào URL do tài khoản của bạn cấp.

Bài này phối hợp **AWS Console cho CloudFormation, EC2 và WAF** với AWS CLI và CloudFormation cho các bước còn lại. Bạn không cần truy cập tài khoản hay máy tính của tác giả.

> **Phạm vi và trạng thái:** mã và template đã được đối chiếu với nhánh AWS của dự án, nhưng lộ trình chưa được chạy lại từ đầu trên tài khoản trắng. Kết quả cần được xác nhận qua lần thực hành, đặc biệt là build image ARM64, đăng nhập, bot tham gia và phiên âm. Đây là môi trường thử nghiệm một AZ cho dữ liệu, chưa phải cấu hình production.

Bản đầu triển khai **Terminal chế độ meetings**, đăng nhập Google, bot và có thể thêm VieGem để thử phiên âm phi thương mại. Workspace/agent đầy đủ, trợ lý giọng nói, các mô hình và tích hợp bổ sung không tự bật trong bản này; xem [phần tính năng mở rộng](5.4-data-compute/5.4.3-ecs-load-balancer/5.4.3.5-extensions/).

## Triển khai gọn bằng một file

Xem [triển khai một CloudFormation](5.4-full-cloudformation/) để dùng template gộp. Stack tạo Cognito và cấu hình đăng nhập bằng email, nên người học không cần tạo Google OAuth. Các bước Google bên dưới dành cho lộ trình nhiều stack.

## Thứ tự thực hiện

1. [Tổng quan và kết quả cần đạt](5.1-overview/).
2. [Chuẩn bị tài khoản, quota và mã nguồn](5.2-prerequisites/).
3. [Tạo nền tảng VPC và mạng](5.3-networking/).
4. [Build image, tạo dữ liệu, triển khai website và kiểm thử](5.4-data-compute/).
5. [Giám sát và chi phí](5.5-security-monitoring-costs/).
6. [Dọn dẹp và bằng chứng](5.6-cleanup-evidence/).

Bạn cần thời gian build image, chờ RDS, ElastiCache và CloudFront khởi tạo; chưa có số giờ đo được cho một lượt hoàn chỉnh. AWS, mô hình và việc truyền dữ liệu có thể phát sinh chi phí từ khi tạo tài nguyên.

## Ảnh hướng dẫn

Sau mỗi bước có khung **Ảnh cần bổ sung**, chụp màn hình thực tế rồi lưu PNG vào `static/images/5-Workshop/tina/` đúng tên trong khung. Khi dựng lại website, ảnh sẽ hiện **ngay dưới thao tác tương ứng**. [Danh sách ảnh](/images/5-Workshop/tina/README.md) dùng để kiểm đếm; ảnh không bị gom xuống cuối trang.

Không đưa vào ảnh mật khẩu, client secret, token, thông tin cá nhân hoặc nội dung họp thật. Che account ID, email và tên miền riêng trước khi chia sẻ.
