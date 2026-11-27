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

## 2. Inspect CloudWatch Logs, Metrics, and Alarms

In **ECS → Clusters → service → Tasks → task → Logs**, or **CloudWatch → Log groups**, review logs during task startup and while running a test meeting (`tina-full.yml` automatically provisions 13 Log Groups for all ECS services and enables `CloudWatchMetricsEnabled` on AWS WAF). In CloudFormation, the **Events** tab shows stack provisioning errors. Do not include access tokens, meeting URLs, transcript content, or personal data in screenshots.

{{< workshop-screenshot file="20-logs.png" description="CloudWatch task logs with tokens, user details, and meeting content redacted." >}}

To monitor system health, open **CloudWatch → Metrics → All metrics** and check `AWS/ECS` (`CPUUtilization`, `MemoryUtilization`), `AWS/ApplicationELB` (`HTTPCode_Target_5XX_Count`, `HealthyHostCount`), and `AWS/RDS` (`CPUUtilization`, `FreeStorageSpace`, `DatabaseConnections`). When you need full operational alerting (10 Metric Filters, 20 Alarms, and a unified Dashboard), deploy `deploy/aws/staging-workspace-s3-monitoring.yml` from `main` (see [Section 5.4.3.5](../5.4-data-compute/5.4.3-ecs-load-balancer/5.4.3.5-extensions/)).

If ECS reports `CannotPullContainerError`, check that the digest is ARM64, the execution role has ECR permissions, and outbound NAT routing works. If you hit quota limits, check Service Quotas. If targets are unhealthy, inspect Terminal logs, port 3000, and the `/api/auth/providers` health check path.

## 3. Cost Estimation and Optimization

Check **Billing → Budgets** and **Cost Explorer**; billing data can lag behind actual usage. Budgets send alerts only—they do not automatically delete resources.

### Reference Cost Estimate (`us-east-1`, single pilot environment)

The table below uses official AWS `us-east-1` on-demand pricing (730 h/month) for **a single pilot environment** (≈10 users, ≈5 meetings/week, ≈20 meeting-hours/month):

| Service Category | Key Sizing | Est. Monthly Cost |
| --- | --- | --- |
| **ECS Fargate (ARM64)** | Web/Agent 24/7 (≈$28.80) + Bot/VieGem/VieNeu on-demand ≈20 h/month (≈$3.20) | ≈$32.00 |
| **Networking** | 1 Internal ALB (≈$18.00) + 1 NAT Gateway (≈$33.30) + 1 Public IPv4 for NAT (≈$3.65) + CloudFront (≈$1.00) | ≈$55.95 |
| **Data Stores** | RDS PostgreSQL `db.t4g.micro` + 20 GB gp3 (≈$14.00) + ElastiCache Valkey `cache.t4g.micro` (≈$9.34) + S3 (≈$0.33) | ≈$23.67 |
| **AI & Messaging** | Amazon Bedrock `amazon.nova-lite-v1:0` (≈$0.54; budgeted with fallback ≈$3.00) + optional Amazon SES (≈$0.01) | ≈$3.01 |
| **Security & Observability** | AWS WAF (≈$8.00) + Secrets Manager (≈$2.00) + KMS (≈$1.00) + CloudWatch (≈$3.50) + ECR (≈$1.00) | ≈$15.50 |
| **Total (24/7 full stack)** | Full single pilot environment | **≈$130.13/month** |
| **Hands-on lab session (2–3 h)** | Deploy, validate, and delete per Section 5.6 | **≈$1–2 / lab session** |

> **Note:** If you deploy the combined `tina-full.yml` template (5.4A) and leave all optional services (Voice, Agent, MCP, Flows, and 4 VPC Interface Endpoints) running 24/7 without deleting them, monthly costs will be higher than the lean table above. Always run cleanup in [Section 5.6](../5.6-cleanup-evidence/) right after finishing the lab.

### Cost Optimization Strategies

1. **ARM64 (Graviton) on Fargate & RDS `t4g`**: reduces compute costs by ≈20% compared to equivalent x86_64 sizing.
2. **VPC Endpoints (free S3 Gateway + ECR/Logs/Secrets Manager)**: keeps private image pulls, logs, and secret reads off the NAT Gateway, avoiding `$0.045/GB` NAT data processing fees.
3. **Off-hours scale-down**: scaling non-essential ECS services to `desiredCount=0` and stopping RDS outside working hours (≈10 h/day, weekdays) lowers pilot costs to **≈$70–80/month**.
4. **On-demand Bot & meeting tasks**: Bot tasks are spawned only when a meeting starts and stop automatically when it ends, avoiding 24/7 idle compute.
5. **S3 Lifecycle & AWS Budgets**: auto-expire temporary `runtime-invocations/` objects after 1 day, transition older recordings to cheaper storage classes, and set **AWS Budgets** alerts at **50%, 80%, and 100%**.

{{< workshop-screenshot file="21-budget.png" description="Lab account budget and alert status; redact email addresses and account ID." >}}

When you finish the lab, proceed to [cleanup](../5.6-cleanup-evidence/) to avoid ongoing charges.
