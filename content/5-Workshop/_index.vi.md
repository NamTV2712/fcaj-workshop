---
title: "Workshop"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# TINA – Hệ thống họp & trợ lý AI tự triển khai trên AWS

Workshop hướng dẫn bạn dùng **tài khoản AWS của chính mình** để dựng một bản TINA thử nghiệm: CloudFront → ALB nội bộ → ECS Fargate, cùng PostgreSQL trên RDS, Valkey trên ElastiCache, S3 và ECR. Bạn tạo tài nguyên mới và đăng nhập vào URL do tài khoản của bạn cấp.

Bài này phối hợp **AWS Console cho CloudFormation, EC2 và WAF** với AWS CLI và CloudFormation cho các bước còn lại. Bạn không cần truy cập tài khoản hay máy tính của tác giả.

> **Phạm vi và trạng thái:** Toàn bộ mã nguồn, template CloudFormation và bộ 15 image ARM64 dựng sẵn (`workshop-arm64`) đã được triển khai và kiểm chứng thực tế từ đầu đến cuối trên tài khoản AWS độc lập (bao gồm dựng hạ tầng, đăng nhập Google, bot tham gia cuộc họp và phiên âm VieGem). Kiến trúc trong bài là môi trường lab/thử nghiệm dùng dữ liệu trên một AZ để tối ưu chi phí, chưa phải cấu hình High Availability cho production.

Bản đầu triển khai **Terminal chế độ meetings**, đăng nhập Google, bot và có thể thêm VieGem để thử phiên âm phi thương mại. Workspace/agent đầy đủ, trợ lý giọng nói, các mô hình và tích hợp bổ sung không tự bật trong bản này; xem [phần tính năng mở rộng](5.4-data-compute/5.4.3-ecs-load-balancer/5.4.3.5-extensions/).

## Triển khai nhanh bằng một file (khuyên dùng)

Xem [triển khai một CloudFormation](5.4-full-cloudformation/) để dùng template gộp `tina-full.yml` cùng bộ 15 image ARM64 dựng sẵn trên GHCR (gồm **VieGem** và 3 image Voice): chỉ cần dán 5 lệnh ngắn vào **AWS CloudShell** (~15–20 phút), sau đó gắn Google OAuth của riêng bạn là chạy được web đầy đủ. Lộ trình nhiều stack bên dưới dành cho trường hợp muốn dựng và kiểm tra từng lớp hạ tầng riêng lẻ.

## Thứ tự thực hiện

1. [Tổng quan và kết quả cần đạt](5.1-overview/).
2. [Chuẩn bị tài khoản, quota và mã nguồn](5.2-prerequisites/).
3. [Tạo nền tảng VPC và mạng](5.3-networking/).
4. [Build image, tạo dữ liệu, triển khai website và kiểm thử](5.4-data-compute/).
5. [Giám sát và chi phí](5.5-security-monitoring-costs/).
6. [Dọn dẹp và bằng chứng](5.6-cleanup-evidence/).

Thời gian thực hiện khoảng **15–20 phút** nếu chọn lộ trình triển khai nhanh [5.4A](5.4-full-cloudformation/) (copy sẵn image từ GHCR), hoặc **30–45 phút** cho lộ trình nhiều stack (tùy thời gian chờ RDS, ElastiCache và CloudFront khởi tạo). Các tài nguyên AWS và lưu lượng truyền dữ liệu có thể phát sinh chi phí ngay khi được tạo; hãy dọn dẹp đầy đủ theo [Mục 5.6](5.6-cleanup-evidence/) sau khi hoàn tất.

## Ảnh hướng dẫn

Mỗi bước trong workshop đều đính kèm **ảnh chụp màn hình thực tế** trên AWS Console và giao diện ứng dụng TINA ngay dưới thao tác tương ứng để bạn dễ đối chiếu kết quả. Các thông tin nhạy cảm (Account ID, email, secret) trong ảnh minh họa đã được che mờ.

Khi tự thực hành và lưu lại ảnh làm bằng chứng đánh giá, không để lộ mật khẩu, client secret, token, thông tin cá nhân hoặc nội dung cuộc họp thật; luôn che Account ID, email và tên miền riêng trước khi chia sẻ.
