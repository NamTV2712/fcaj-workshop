---
aliases: ["/vi/5-workshop/5.4-s3-onprem/"]
title: "Dữ liệu, image, ECS và ứng dụng"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

## Dựng hệ thống theo thứ tự phụ thuộc

1. [Tạo ECR và build image ARM64 trên EC2](5.4.1-s3-ecr-images/).
2. [Tạo RDS PostgreSQL, Valkey và secret](5.4.2-data-secrets/).
3. [Tạo edge, runtime, core, Terminal và tùy chọn ASR](5.4.3-ecs-load-balancer/).
4. [Đăng nhập và kiểm thử meeting](5.4.4-application-validation/).

Mỗi phần dựa vào output của phần trước. Tên `tina-staging` trong template là tên kỹ thuật trong tài khoản của bạn, không yêu cầu dùng môi trường của tác giả.
