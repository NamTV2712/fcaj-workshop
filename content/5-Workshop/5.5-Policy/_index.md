---
title: "Cost and Security Checks"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

#### What to check against the proposal

The proposal lists explicit security and cost controls. Verify them rather than assuming from the diagram.

**Security**

- **Edge:** CloudFront in front of the ALB, AWS WAF web ACL attached, only HTTPS exposed publicly.
- **Identity:** Cognito user pool federated with Google OAuth, JWT issued to the web app.
- **Least privilege:** one IAM task role per service; secrets in Secrets Manager, encryption with KMS; TLS in transit; security groups allowing ALB → Web and internal service-to-service traffic only.

**Cost**

- AWS Budgets alerts at **50%, 80% and 100%** of the monthly limit.
- Off-hours scale-down of Web/Agent, RDS and ElastiCache; Fargate Spot for meeting tasks; VPC endpoints for S3/ECR; S3 lifecycle rules.

#### Local evidence (no AWS account required)

```bash
make plan
make doctor
make -C deploy/compose provision-token   # fresh scoped API key (scopes bot,tx)
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Review `.env` / `deploy/compose/.env` for `SCOPES=bot,tx`, internal secrets and the transcription `TOKEN` — all secret values should be redacted in screenshots.

#### AWS evidence (only if the practice account has credentials)

Never paste credentials or secret values.

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

#### Screenshots

- `screenshot-12-waf-iam-budgets.png`
- `screenshot-13-aws-services.png` (if credentials exist)
