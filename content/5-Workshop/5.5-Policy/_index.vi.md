---
title: "Kiểm tra chi phí & bảo mật"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

#### Đối chiếu với proposal

Proposal nêu rõ các kiểm soát bảo mật và chi phí. Hãy kiểm chứng thay vì chỉ tin vào sơ đồ.

**Bảo mật**

- **Biên:** CloudFront trước ALB, web ACL WAF gắn vào, chỉ HTTPS mở ra Internet.
- **Định danh:** Cognito user pool liên kết Google OAuth, JWT cấp cho web app.
- **Tối thiểu quyền:** IAM task role riêng cho từng service, secret trong Secrets Manager, mã hóa KMS, TLS khi truyền, security group chỉ cho ALB → Web và luồng nội bộ.

**Chi phí**

- AWS Budgets alert ở **50%, 80%, 100%** hạn mức tháng.
- Tắt Web/Agent, RDS, ElastiCache ngoài giờ; Fargate Spot cho task cuộc họp; VPC endpoint cho S3/ECR; lifecycle rule trên S3.

#### Bằng chứng local (không cần tài khoản AWS)

```bash
make plan
make doctor
make -C deploy/compose provision-token   # API key scoped mới (scopes bot,tx)
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Xem `.env` / `deploy/compose/.env` để thấy `SCOPES=bot,tx`, internal secrets và `TOKEN` phiên âm — mọi giá trị bí mật phải được che trong ảnh.

#### Bằng chứng AWS (chỉ khi có credentials của tài khoản thực hành)

Không dán credentials hay giá trị bí mật.

```bash
aws wafv2 list-web-acls --scope CLOUDFRONT
aws elbv2 describe-load-balancers
aws cloudfront list-distributions
aws cognito-idp list-user-pools --max-results 10
aws rds describe-db-instances
aws elasticache describe-cache-clusters
aws s3 ls
aws bedrock list-foundation-models --region us-east-1
aws sesv2 get-account
aws ecr describe-repositories --region us-east-1
```

#### Ảnh cần chụp

- `screenshot-12-waf-iam-budgets.png`
- `screenshot-13-aws-services.png` (nếu có credentials)
