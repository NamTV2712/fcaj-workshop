---
aliases: ["/vi/5-workshop/5.4-s3-onprem/"]
title: "Dữ liệu, image, ECS và ứng dụng"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

Phần này kết hợp hai loại thao tác:

- **Quan sát staging:** xem cấu hình, task, target health, log và kết quả từ môi trường được cấp quyền. Không thay đổi service hiện có.
- **Thực hành trên lab:** tự tạo bucket, ECR repository và nếu cần các dịch vụ khác trong tài khoản lab; việc tạo từng tài nguyên không tự tích hợp chúng vào TINA.

## Thứ tự thực hiện

1. [S3, ECR và image](5.4.1-s3-ecr-images/).
2. [RDS, Valkey, secret và các dịch vụ bổ sung](5.4.2-data-secrets/).
3. [ECS, task definition và load balancer](5.4.3-ecs-load-balancer/).
4. [Kiểm tra luồng ứng dụng](5.4.4-application-validation/).

Staging thực tế gồm nhiều stack. Trong đợt kiểm tra, task `tina-staging-core` có các container `schema-init`, `meeting`, `admin`, `asr-control`, `gateway`; `tina-staging-terminal` là task riêng. Phần cấu hình có thể thay đổi theo lần triển khai. Tham khảo các stack và task definition đang hoạt động để kiểm chứng; không suy ra một danh sách năm container đủ để dựng lại cả hệ thống.

Không chạy `make ps` trên laptop để chứng minh ECS đang chạy; đó là trạng thái Docker Compose cục bộ. Không giả định tài nguyên mới tạo trên Console tự được ứng dụng sử dụng: cần cấu hình và triển khai service tương ứng.
