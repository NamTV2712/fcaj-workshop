---
title: "Workshop"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Dựng toàn bộ kiến trúc TINA từ đầu

#### Tổng quan

Workshop này dựng lại **mọi thứ** trong proposal TINA: hạ tầng AWS (VPC, mạng, kho dữ liệu, định danh, AI, email, biên) **và** các service ứng dụng biên dịch từ source. Repo GitHub chỉ được pull về làm source — bạn tự tạo tài nguyên AWS, build từng service từ Dockerfile, đẩy image lên ECR, deploy lên ECS Fargate, rồi kiểm tra và chụp ảnh.

Không có gì được giả định tồn tại sẵn. Bạn bắt đầu từ tài khoản AWS trống tại `us-east-1`.

#### Những gì sẽ tạo (theo thứ tự)

| # | Lớp | Tài nguyên tạo |
| --- | --- | --- |
| 1 | Tài khoản & công cụ | IAM admin user, AWS CLI, Docker, Dotenvx, clone source |
| 2 | Mạng | VPC `tina-vpc` (`10.0.0.0/16`), 6 subnet qua 2 AZ, Internet Gateway, NAT Gateway, 3 route table, security group |
| 3 | Kết nối riêng | Gateway endpoint cho S3, Interface endpoint cho ECR |
| 4 | Lưu trữ | Bucket S3 cho bản ghi âm/exports, mã hóa + lifecycle rule |
| 5 | Image | Build mọi service từ Dockerfile (`make build`) rồi push lên ECR |
| 6 | Tính toán | ECS cluster, task definition/service cho Web, Bot, STT, TTS, Agent; ALB + target group + health check |
| 7 | Dữ liệu | RDS PostgreSQL, ElastiCache Redis |
| 8 | Định danh & AI | Cognito user pool với Google OAuth, cấp quyền model Bedrock |
| 9 | Email & biên | SES verified domain, CloudFront, AWS WAF |
| 10 | Bảo mật & chi phí | IAM task role, Secrets Manager, KMS, CloudWatch, AWS Budgets |
| 11 | Kiểm tra | Health endpoint, transcript trực tiếp, `make probe`, AWS CLI |
| 12 | Dọn dẹp | Xóa service, ALB, database, VPC, bucket |

![Kiến trúc AWS của TINA](/images/2-Proposal/tina_aws_architecture.png)

#### Quy ước đặt tên

| Tài nguyên | Tên / giá trị |
| --- | --- |
| Region | `us-east-1` |
| VPC | `tina-vpc`, `10.0.0.0/16` |
| Subnet public | `tina-public-1a` `10.0.1.0/24`, `tina-public-1b` `10.0.2.0/24` |
| Subnet private app | `tina-app-1a` `10.0.11.0/24`, `tina-app-1b` `10.0.12.0/24` |
| Subnet private data | `tina-data-1a` `10.0.21.0/24`, `tina-data-1b` `10.0.22.0/24` |
| IGW / NAT | `tina-igw`, `tina-nat` (1 EIP) |
| Route table | `tina-public-rt`, `tina-app-rt`, `tina-data-rt` |
| S3 | `tina-<ten>-recordings`, `tina-<ten>-exports` |
| ECR | `tina-<service>` (terminal, gateway, bot, stt, tts, agent, …) |
| ECS cluster/service | `tina-cluster`; `tina-web`, `tina-bot`, `tina-stt`, `tina-tts`, `tina-agent` |
| ALB / target group | `tina-alb`, `tina-web-tg` |
| RDS / ElastiCache | `tina-db` (db.t4g.micro), `tina-cache` (cache.t4g.micro) |
| Cognito / Bedrock | `tina-users`, quyền model Claude/Nova |
| SES / CloudFront / WAF | domain đã xác minh, `tina-cdn`, `tina-waf-acl` |
| Secret / KMS / Budgets | `tina/*`, `tina-key`, `tina-monthly` |

#### Làm tay hay dùng CloudFormation

Chỉ **3 việc làm tay**; mọi thứ còn lại dùng một template CloudFormation:

- **Làm tay:** `tina-vpc` (`10.0.0.0/16`), 6 subnet trải 2 AZ, và NAT Gateway + Internet Gateway (kèm EIP). Tạo trước và ghi lại ID.
- **CloudFormation:** toàn bộ resource còn lại — S3, ECR, IAM, Secrets Manager, KMS, RDS, ElastiCache, Cognito, ALB, ECS + 5 service Fargate, CloudFront, WAF, CloudWatch, Budgets.

Đường dẫn template: `static/cloudformation/tina-infrastructure.yaml` (copy vào repo đã clone hoặc dùng đường dẫn local).

```bash
aws cloudformation deploy \
  --template-file tina-infrastructure.yaml \
  --stack-name tina-infra \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1 \
  --parameter-overrides \
      VpcId=<vpc-id> PublicSubnet1=<public-1a> PublicSubnet2=<public-1b> \
      PrivateSubnet1=<private-1a> PrivateSubnet2=<private-1b> \
      DBPassword='<mat-khau-manh>' CertificateArn=<acm-cert-arn> \
      GitHubOAuthClientId=<client-id> GitHubOAuthClientSecret=<client-secret>
```

Nếu muốn đi tay từng resource, child page có đầy đủ hướng dẫn — template chỉ để tạo nhanh.

#### Bảng kiểm tra đủ dịch vụ

| Dịch vụ yêu cầu | Tạo ở đâu | Cách |
| --- | --- | --- |
| VPC | Bước 1 | Tay |
| 2 Availability Zone | Bước 1 (`us-east-1a`, `us-east-1b`) | Tay |
| Public subnet + 2 private subnet | Bước 1 (`tina-public-*`, `tina-private-*`) | Tay |
| Internet Gateway | Bước 1 (`tina-igw`) | Tay |
| NAT Gateway | Bước 1 (`tina-nat`) | Tay |
| S3 | Bước 2 (recordings/exports) | CloudFormation |
| ECR | Bước 2 (6 repository) | CloudFormation |
| IAM | Bước 5 (task role) | CloudFormation |
| Secrets Manager | Bước 5 (`tina/core`) | CloudFormation |
| KMS | Bước 5 (`tina-key`) | CloudFormation |
| RDS | Bước 3 (`tina-db`) | CloudFormation |
| ElastiCache | Bước 3 (`tina-cache`) | CloudFormation |
| Cognito | Bước 3 (`tina-users`) | CloudFormation |
| ALB | Bước 4 (`tina-alb`) | CloudFormation |
| ECS + 5 Fargate service | Bước 4 (`tina-cluster`) | CloudFormation |
| Bedrock | Bước 3 (cấp quyền model) | Console |
| SES | Bước 3 (xác minh domain) | Console |
| CloudFront | Bước 5 (`tina-cdn`) | CloudFormation |
| WAF | Bước 5 (`tina-waf-acl`) | CloudFormation |
| CloudWatch | Bước 5 (log group/alarm) | CloudFormation |
| AWS Budgets | Bước 5 (`tina-monthly`) | CloudFormation |
| Cost Explorer | Bước 5 (xem console) | Console |

#### Hướng dẫn từng bước

**Bước 0 — Chuẩn bị tài khoản, công cụ và source**

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
chmod 600 .env.keys
aws configure            # region us-east-1, không dán bí mật vào ảnh
docker version --format '{{.Server.Version}}'   # >= 26
```
- **Ảnh cần chụp:** `screenshot-00-prereqs.png`, `screenshot-01-clone.png`.

**Bước 1 — Dựng VPC và mạng**

Tạo `tina-vpc`, 6 subnet, IGW, NAT Gateway, 3 route table và security group theo bảng tên. Public route `0.0.0.0/0 → IGW`, app route `0.0.0.0/0 → NAT`, data route **không** có đường ra Internet; thêm gateway endpoint cho S3 và interface endpoint cho ECR.
- **Ảnh cần chụp:** `screenshot-02-vpc-subnets.png`, `screenshot-03-route-tables.png`, `screenshot-04-vpc-endpoints.png`.

**Bước 2 — Lưu trữ, ECR và image**

Tạo bucket S3 (mã hóa + lifecycle) và repository ECR. Build mọi service locally từ source (`make build`, `make bot`), rồi tag và push từng image lên ECR.
- **Ảnh cần chụp:** `screenshot-05-s3-buckets.png`, `screenshot-06-ecr-repos.png`, `screenshot-07-images-built.png`.

**Bước 3 — Dữ liệu, định danh và AI**

Tạo RDS PostgreSQL, ElastiCache Redis, Cognito user pool với Google OAuth callback, cấp quyền model Bedrock, xác minh domain SES.
- **Ảnh cần chụp:** `screenshot-08-rds-redis.png`, `screenshot-09-cognito.png`, `screenshot-10-bedrock-ses.png`.

**Bước 4 — Tính toán và cân bằng tải**

Tạo ALB + target group với health check, rồi ECS cluster và 5 task definition/service dùng image từ ECR, đặt task ở private app subnet với IAM task role và secret từ Secrets Manager/KMS.
- **Ảnh cần chụp:** `screenshot-11-alb.png`, `screenshot-12-ecs-cluster.png`, `screenshot-13-task-definitions.png`.

**Bước 5 — Biên, bảo mật và chi phí**

Tạo CloudFront + WAF, CloudWatch log group/alarm và AWS Budgets ở 50/80/100%.
- **Ảnh cần chụp:** `screenshot-14-cloudfront-waf.png`, `screenshot-15-budgets.png`.

**Bước 6 — Kiểm tra**

Dùng trang [Kiểm tra dịch vụ](5.4-s3-onprem/): ECS service events, ALB health, log, URL ứng dụng, transcript trực tiếp và `make probe`. Xác nhận lưu lượng S3/RDS/ElastiCache đi qua VPC endpoint (không tốn phí NAT).
- **Ảnh cần chụp:** `screenshot-16-ecs-healthy.png`, `screenshot-17-app-running.png`.

**Bước 7 — Dọn dẹp**

Xóa theo thứ tự ngược: ECS service → ALB → RDS/ElastiCache → endpoint → NAT/IGW → subnet → VPC → bucket/ECR. Local chạy `make down`.

#### Nội dung

1. [Tổng quan workshop](5.1-workshop-overview/)
2. [Chuẩn bị](5.2-prerequiste/)
3. [Dựng VPC & mạng](5.3-s3-vpc/)
4. [Dựng dữ liệu, định danh & compute](5.4-s3-onprem/)
5. [Bảo mật & chi phí](5.5-policy/)
6. [Dọn dẹp](5.6-cleanup/)
