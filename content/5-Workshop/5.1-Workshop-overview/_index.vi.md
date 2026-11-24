---
title: "Tổng quan workshop"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

#### Kiến trúc mục tiêu

Bạn dựng lại toàn bộ kiến trúc trong proposal trên AWS tại `us-east-1`, bắt đầu từ tài khoản trống:

1. **Mạng:** VPC `10.0.0.0/16` trải `us-east-1a`/`us-east-1b` — subnet public, private-app, private-data; Internet Gateway; NAT Gateway; route table; security group; VPC endpoint cho S3 và ECR.
2. **Biên:** CloudFront + AWS WAF trước Application Load Balancer.
3. **Định danh:** Cognito user pool với Google OAuth.
4. **Tính toán:** ECS cluster trên Fargate với 5 service — Web serving, Bot (Playwright), STT (VieGem), TTS (VieNeu), Agent.
5. **Dữ liệu:** RDS PostgreSQL (transcript), ElastiCache Redis (trạng thái trực tiếp), S3 (bản ghi âm/exports).
6. **AI/email:** Amazon Bedrock (agent, ghi chú, tóm tắt, dịch), Amazon SES (email follow-up).
7. **Vận hành:** ECR, IAM task role, Secrets Manager, KMS, CloudWatch, Budgets/Cost Explorer.

![Kiến trúc AWS của TINA](/images/2-Proposal/tina_aws_architecture.png)

#### Source code chỉ là đầu vào

Pull `https://github.com/poor-frog/TINA.git` để lấy Dockerfile, Compose file và build script. Sau đó bạn:

- build từng image từ Dockerfile (`make build`, `make bot`),
- push image lên repository ECR tự tạo,
- viết task definition ECS tham chiếu các image đó,
- để ứng dụng dùng tài nguyên AWS bạn tạo (RDS, ElastiCache, S3, Bedrock, SES, Cognito).

Workshop **không dùng** image có sẵn `ghcr.io/poor-frog/tina-*:prod`.

#### Tư duy kiểm chứng

Với mỗi tài nguyên, hãy chụp bằng chứng: trang console hoặc output `aws … describe-*`, health check tương ứng và hành vi của ứng dụng. Checklist cuối trong [Dọn dẹp](../5.6-cleanup/) liệt kê đúng tên ảnh cần chụp.

- **Ảnh cần chụp:** `screenshot-00-prereqs.png`.
