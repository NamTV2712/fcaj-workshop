---
aliases: ["/5-workshop/5.2-prerequiste/"]
title: "Prerequisites"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

## 1. Account and scope

1. Sign in to the AWS Console with an appropriately granted identity; prefer IAM Identity Center or an IAM role, not the root user for daily work.
2. Identify whether you are using a **separate lab account** or are only allowed to **read staging**. If reviewers are not granted staging access, provide vetted reports/screenshots instead of asking for your account access.
3. Select **US East (N. Virginia), `us-east-1`**. For another account, choose two available Availability Zones; `1a`/`1b` names do not necessarily map to the same physical locations across accounts.

{{< workshop-screenshot file="00-region.png" description="Region us-east-1 selected in the AWS Console." >}}

4. Set a unique lab prefix, for example `tina-ws-an`, and record VPC, subnet, route table and security group IDs in personal notes. Do not replace staging/production resources with lab names.

## 2. Cost

Go to **Billing and Cost Management → Budgets → Create budget**; choose **Cost budget**, set an amount and an email you control, then create alerts. Estimate first with the [AWS Pricing Calculator](https://calculator.aws/), including at least NAT gateway and data processing, public IPs, ECS, RDS, ElastiCache, VPC interface endpoints, CloudFront and storage. A budget is an alert, not a guarantee that spending stops automatically. Shut down the lab as described on the [Cleanup](../5.6-cleanup-evidence/) page.

{{< workshop-screenshot file="00-budget.png" description="Lab account budget and alert thresholds; mask the email address." >}}

## 3. Tools for optional parts

You can do the Console work without the CLI. To inspect source/images locally, prepare Git, Docker, Docker Compose, `make`, AWS CLI and granted read access to the source. On Windows use WSL2 for bash commands; Node/pnpm versions follow the TINA repository you were given. Check:

```bash
git --version
aws --version
docker version
docker compose version
make --version
aws sts get-caller-identity
```

Do not paste output containing sensitive information into the report. Run `git clone` only after the instructor has provided the URL and correct read access; record the commit/release and image digest so others use the same version. Do not ask participants to copy the project owner's `.env.keys`.

## 4. Conditions for a full deployment

You need an accessible, version-pinned source/image set, configuration for every service, a secret management approach, a domain/certificate if using HTTPS, and a compatible self-hosted STT configuration. Creating one Terminal task, one database and one bucket is not enough to run TINA. A verified release kit from a clean account is not yet provided in this workshop.

Record the date, region, your role and the budget limit; never store secrets in Git.
