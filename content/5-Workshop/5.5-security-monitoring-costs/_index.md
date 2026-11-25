---
aliases: ["/5-workshop/5.5-policy/"]
title: "Security, monitoring and cost"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

## 1. Review permissions and secrets

Go to **IAM → Roles** and inspect the execution roles and task roles created by the stacks. Verify that ECR repositories, S3 buckets, Secrets Manager, and ECS tasks are granted permissions appropriate for your environment. Do not capture policies containing your account ID without redacting it. The EC2 builder should only exist while building images.

{{< workshop-screenshot file="19-role-policy.png" description="Roles and policy scope for the lab environment; redact account identifiers." >}}

RDS, Valkey, and the services run in private subnets; secrets are referenced by ARN. CloudFront uses WAF and a VPC origin pointing to an internal ALB. The current configuration is intended for lab use—review internal transport encryption, backups, IAM policies, and WAF rules before serving real users.

## 2. Inspect logs and health

In **ECS → Clusters → service → Tasks → task → Logs**, or **CloudWatch → Log groups**, review logs during task startup and while running a test meeting. In CloudFormation, the **Events** tab shows stack provisioning errors. Do not include access tokens, meeting URLs, transcript content, or personal data in screenshots.

{{< workshop-screenshot file="20-logs.png" description="CloudWatch task logs with tokens, user details, and meeting content redacted." >}}

If ECS reports `CannotPullContainerError`, check that the digest is ARM64, the execution role has ECR permissions, and outbound NAT routing works. If you hit quota limits, check Service Quotas. If targets are unhealthy, inspect Terminal logs, port 3000, and the `/api/auth/providers` health check path.

## 3. Cost

Check **Billing → Budgets** and **Cost Explorer**; billing data can lag behind actual usage. Review NAT Gateway, public IPv4 addresses, EC2 builder/EBS, RDS, Valkey, Fargate, ALB, CloudFront, WAF, ECR, and snapshots. Budgets send alerts only—they do not automatically delete resources.

{{< workshop-screenshot file="21-budget.png" description="Lab account budget and alert status; redact email addresses and account ID." >}}

When you finish the lab, proceed to [cleanup](../5.6-cleanup-evidence/) to avoid ongoing charges.
