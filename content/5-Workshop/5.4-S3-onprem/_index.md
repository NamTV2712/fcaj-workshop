---
title: "Dựng dữ liệu, định danh và compute"
date: 2026-11-24
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

#### 1. Lưu trữ và registry

Tạo 2 bucket S3 `tina-<ten>-recordings` và `tina-<ten>-exports`, bật mã hóa KMS (`tina-key`) và lifecycle rule chuyển bản ghi cũ sang lớp rẻ hơn. Tạo repository ECR: `tina-terminal`, `tina-gateway`, `tina-bot`, `tina-stt`, `tina-tts`, `tina-agent`, …

#### 2. Build image từ source và push lên ECR

```bash
make build        # build mọi service từ Dockerfile
make bot          # image bot Playwright
docker images | grep tina
# với mỗi service: tag và push
docker tag tina/v012-terminal:dev <account>.dkr.ecr.us-east-1.amazonaws.com/tina-terminal:prod
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/tina-terminal:prod
```

#### 3. Dữ liệu, định danh và AI

- **RDS** `tina-db`: PostgreSQL `db.t4g.micro`, 20 GB gp3, ở data subnet, mã hóa KMS.
- **ElastiCache** `tina-cache`: Redis `cache.t4g.micro`, ở data subnet.
- **Cognito** `tina-users`: user pool với Google IdP, callback `https://<cloudfront>/api/auth/callback/google`.
- **Bedrock**: cấp quyền các model dùng cho ghi chú/tóm tắt/agent.
- **SES**: xác minh domain gửi.

#### 4. Tính toán và cân bằng tải

- **ALB** `tina-alb`: internet-facing ở public subnet, listener HTTPS, target group `tina-web-tg` health check `/health`.
- **ECS cluster** `tina-cluster` trên Fargate.
- 5 service với task definition trỏ image ECR: `tina-web`, `tina-bot`, `tina-stt`, `tina-tts`, `tina-agent`, đặt ở private app subnet dùng `tina-web-sg`/`tina-data-sg`, IAM task role và secret từ Secrets Manager.

```bash
aws ecs list-services --cluster tina-cluster
aws ecs describe-services --cluster tina-cluster --services tina-web
aws elbv2 describe-target-health --target-group-arn <tg-arn>
```

#### Nội dung

- [S3, ECR và image](5.4.1-prepare/)
- [RDS, ElastiCache, Cognito, Bedrock, SES](5.4.2-create-interface-enpoint/)
- [ALB và ECS service](5.4.3-test-endpoint/)
- [Kiểm tra hệ thống](5.4.4-dns-simulation/)
