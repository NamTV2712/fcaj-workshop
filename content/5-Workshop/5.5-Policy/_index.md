---
title: "Security, Monitoring and Cost"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

All resources in this section are created by the CloudFormation template (`tina-infrastructure.yaml`). Your job is to verify them.

#### IAM

```bash
aws iam get-role --role-name tina-task-execution-role
aws iam get-role --role-name tina-task-role
```
Check the task execution role can read Secrets Manager and decrypt with KMS; the task role allows S3, Bedrock and SES only.

#### Secrets Manager and KMS

```bash
aws secretsmanager describe-secret --secret-id tina/core
aws kms describe-key --key-id <tina-key-id>
```
Verify secrets are not written into task definitions or code and that S3/RDS use `tina-key`.

#### CloudFront and WAF

```bash
aws cloudfront list-distributions
aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1
```
Confirm the CloudFront distribution points to the ALB, `ViewerProtocolPolicy` redirects to HTTPS, and the WAF ACL `tina-waf-acl` is associated in CLOUDFRONT scope.

#### CloudWatch

```bash
aws logs describe-log-groups --log-group-name-prefix /ecs/tina
aws cloudwatch describe-alarms --alarm-names tina-ecs-high-cpu
aws logs tail /ecs/tina --follow
```
Verify logs from all five ECS services arrive under `/ecs/tina` and the CPU alarm exists.

#### AWS Budgets and Cost Explorer

```bash
aws budgets describe-budgets --account-id <account-id>
```
The budget `tina-monthly` alerts at 80%. In the **Cost Explorer** console, filter by the last 7 days and by service to confirm costs for ECS, RDS, NAT Gateway, S3 and Bedrock are visible; compare with the proposal's ~$148/month estimate and note the off-hours saving.

#### HTTPS/edge check

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://<cloudfront-domain>/health
```

#### Screenshots

- `screenshot-14-cloudfront-waf.png`
- `screenshot-15-cloudwatch-budgets-cost-explorer.png`
- `screenshot-16-iam-secrets-kms.png`
