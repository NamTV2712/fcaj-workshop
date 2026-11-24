---
title: "Dữ liệu, định danh và AI"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

#### RDS PostgreSQL

```bash
aws rds create-db-instance \
  --db-instance-identifier tina-db --db-instance-class db.t4g.micro \
  --engine postgres --allocated-storage 20 --storage-type gp3 \
  --db-name tina --master-username tinauser --master-user-password '<secret>' \
  --vpc-security-group-ids <tina-data-sg> --db-subnet-group-name <data-subnets> \
  --storage-encrypted --kms-key-id <tina-key-arn>
```

#### ElastiCache Redis

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id tina-cache --cache-node-type cache.t4g.micro \
  --engine redis --num-cache-nodes 1 --cache-subnet-group-name <data-subnets> \
  --security-group-ids <tina-data-sg>
```

#### Cognito với Google OAuth

Tạo user pool `tina-users`, thêm Google identity provider với client ID/secret từ Google Auth Platform, tạo app client với callback `https://<cloudfront-domain>/api/auth/callback/google`, ghi lại user pool ID.

#### Bedrock và SES

- Trong **Bedrock → Model access**, cấp quyền các model dùng cho ghi chú/tóm tắt/agent (vd Claude/Nova) tại `us-east-1`.
- Trong **SES**, xác minh domain gửi và tạo credential SMTP/API lưu trong Secrets Manager.

```bash
aws rds describe-db-instances --db-instance-identifier tina-db
aws elasticache describe-cache-clusters --cache-cluster-id tina-cache
aws cognito-idp list-user-pools --max-results 10
aws bedrock list-foundation-models --region us-east-1
aws sesv2 get-account
```

- **Ảnh cần chụp:** `screenshot-08-rds-redis.png`, `screenshot-09-cognito.png`, `screenshot-10-bedrock-ses.png`.
