---
aliases: ["/5-workshop/5.5-policy/"]
title: "Security, Monitoring and Cost"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

## 1. Check roles and secrets

1. Go to **CloudFormation → the staging stack to check → Resources**, find IAM roles and Secrets Manager secrets, and open each resource's metadata.
2. **IAM → Roles**: check the trust relationship and policy of the **task execution role** (pull image, write logs, read secrets at ECS startup) and the **task role** (permissions the application uses). Compare with real need; do not widen permissions just to get past an error.

{{< workshop-screenshot file="19-role-policy.png" description="IAM roles and policies to check; mask identifiers that need not be shared." >}}

3. **Secrets Manager**: check names, descriptions, encryption keys and rotation if applicable. Do not choose to display values. In the task definition, only confirm a secret reference and the variable name; do not capture environment values.
4. **S3/RDS**: check encryption and private access per the earlier pages. A role or secret existing is not proof that IAM reached least privilege.

## 2. Check logs and alarms

1. **ECS → cluster → service → Tasks → task → Logs**, select the matching log group; or go to **CloudWatch → Log groups** and find the name from the task definition.
2. Filter to the test window. Note task startup, health checks and related errors; do not put access tokens, meeting content or user data in screenshots.

{{< workshop-screenshot file="20-logs.png" description="CloudWatch logs with tokens, meeting content and user data masked." >}}

3. **CloudWatch → Alarms → All alarms**: find alarms that actually exist and record their state. Do not assume an alarm `tina-ecs-high-cpu` exists just because that name appeared in older documents.

## 3. CloudFront, WAF and cost

1. **CloudFront → Distributions** → select the staging distribution → check HTTPS, origin and WAF if attached. In **AWS WAF → Web ACLs**, select the CloudFront scope and the Region the Console requires to compare the ACL. Record **not verified** if you lack view permission.
2. **Billing and Cost Management → Cost Explorer** → choose a time range and group by Service; note that data can be delayed and do not infer exact cost for one stack without proper allocation.
3. **Budgets → Budgets** → check the lab account's budgets and notifications. A budget only alerts as configured; you must still monitor and delete lab resources yourself.

{{< workshop-screenshot file="21-budget.png" description="Lab AWS Budget and alert state; email and account ID masked." >}}
