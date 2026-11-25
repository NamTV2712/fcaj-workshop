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

## 3. Cost Estimation and Optimization

Check **Billing → Budgets** and **Cost Explorer**; billing data can lag behind actual usage. Budgets send alerts only—they do not automatically delete resources.

### Reference Cost Estimate (`us-east-1`, pilot workload)

The table below estimates on-demand pricing in `us-east-1` for a pilot workload (~10 users, ~5 meetings/week, ~20 meeting-hours/month):

| Service Category | Key Sizing | Est. Monthly Cost |
| --- | --- | --- |
| **ECS Fargate (ARM64)** | Terminal, Core, Runtime, Agent (24/7) + Bot/VieGem (on-demand ~20 h/month) | ~$38–42 |
| **Networking** | 1 ALB (~$18) + 1 NAT Gateway (~$33) + 3 Public IPv4 (~$11) + CloudFront (~$1) | ~$63 |
| **Data Stores** | RDS PostgreSQL `db.t4g.micro` (~$14) + ElastiCache Valkey `cache.t4g.micro` (~$11.7) + S3 (~$0.3) | ~$26 |
| **Security & Observability** | AWS WAF (~$8) + Secrets Manager (~$2) + KMS (~$1) + CloudWatch (~$3.5) + ECR (~$1) | ~$15.5 |
| **Total (24/7 full stack)** | Full pilot architecture | **~$145/month** |

### Cost Optimization Strategies

1. **ARM64 (Graviton) on Fargate & RDS `t4g`**: reduces compute costs by ~20% compared to equivalent x86_64 sizing.
2. **VPC Endpoints (free S3 Gateway + ECR/Logs/Secrets Manager)**: keeps private image pulls, logs, and secret reads off the NAT Gateway, avoiding `$0.045/GB` NAT data processing fees.
3. **Off-hours scale-down**: scaling non-essential ECS services to `desiredCount=0` and stopping RDS outside working hours (~10 h/day, weekdays) lowers pilot costs to **~$70–80/month**.
4. **On-demand Bot & meeting tasks**: Bot tasks are spawned only when a meeting starts and stop automatically when it ends, avoiding 24/7 idle compute.
5. **S3 Lifecycle & AWS Budgets**: auto-expire temporary `runtime-invocations/` objects after 1 day, transition older recordings to cheaper storage classes, and set **AWS Budgets** alerts at **50%, 80%, and 100%**.

{{< workshop-screenshot file="21-budget.png" description="Lab account budget and alert status; redact email addresses and account ID." >}}

When you finish the lab, proceed to [cleanup](../5.6-cleanup-evidence/) to avoid ongoing charges.
