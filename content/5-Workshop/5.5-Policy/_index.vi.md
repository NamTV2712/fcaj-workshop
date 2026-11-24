---
title: "Bảo mật, giám sát và chi phí"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

Mọi tài nguyên trong phần này do template CloudFormation (`tina-infrastructure.yaml`) tạo. Nhiệm vụ của bạn là kiểm chứng.

#### IAM

```bash
aws iam get-role --role-name tina-task-execution-role
aws iam get-role --role-name tina-task-role
```
Kiểm tra task execution role đọc được Secrets Manager và giải mã bằng KMS; task role chỉ cho phép S3, Bedrock và SES.

#### Secrets Manager và KMS

```bash
aws secretsmanager describe-secret --secret-id tina/core
aws kms describe-key --key-id <tina-key-id>
```
Xác nhận secret không bị ghi vào task definition/code và S3/RDS dùng `tina-key`.

#### CloudFront và WAF

```bash
aws cloudfront list-distributions
aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1
```
Xác nhận distribution trỏ tới ALB, `ViewerProtocolPolicy` redirect HTTPS và ACL `tina-waf-acl` được gắn ở scope CLOUDFRONT.

#### CloudWatch

```bash
aws logs describe-log-groups --log-group-name-prefix /ecs/tina
aws cloudwatch describe-alarms --alarm-names tina-ecs-high-cpu
aws logs tail /ecs/tina --follow
```
Kiểm tra log của cả 5 service ECS về `/ecs/tina` và alarm CPU tồn tại.

#### AWS Budgets và Cost Explorer

```bash
aws budgets describe-budgets --account-id <account-id>
```
Budget `tina-monthly` cảnh báo ở 80%. Trong console **Cost Explorer**, lọc 7 ngày gần nhất theo service để thấy chi phí ECS, RDS, NAT Gateway, S3, Bedrock; đối chiếu ước tính ~$148/tháng trong proposal và ghi nhận mức tiết kiệm khi tắt ngoài giờ.

#### Kiểm tra HTTPS/biên

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://<cloudfront-domain>/health
```

#### Ảnh cần chụp

- `screenshot-14-cloudfront-waf.png`
- `screenshot-15-cloudwatch-budgets-cost-explorer.png`
- `screenshot-16-iam-secrets-kms.png`
