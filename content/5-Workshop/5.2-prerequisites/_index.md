---
aliases: ["/5-workshop/5.2-prerequiste/"]
title: "Prerequisites"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

## 1. Account and Region

1. Use an isolated AWS account for the lab with permissions to create CloudFormation stacks, IAM roles, VPC, EC2, ECS, ECR, RDS, ElastiCache, S3, CloudFront, WAF, Secrets Manager, and CloudWatch resources. Do not use a production account.
2. Sign in to the AWS Console and select **US East (N. Virginia), `us-east-1`** in the top-right corner. CloudFront and WAF for CloudFront use global configuration, and the WAF API for CloudFront requires `us-east-1`.

{{< workshop-screenshot file="00-region.png" description="AWS Console with Region us-east-1 selected." >}}

3. In **Billing and Cost Management → Budgets → Create budget**, create a cost budget with your chosen threshold and email address. Confirm the alert email following the AWS instructions. A budget only sends alerts; it does not automatically stop resources.

{{< workshop-screenshot file="00-budget.png" description="Budget and alert threshold for your lab account; mask your email and account ID." >}}

4. In **Service Quotas**, check your quotas for Fargate On-Demand, EC2 Graviton, and Elastic IPs. Each bot requires 4 vCPU / 8 GiB; core uses 2 vCPU, VieGem uses 2 vCPU, plus runtime and terminal. Leave enough headroom for replacement tasks during ECS redeployments. If any quota is too low, request an increase before proceeding.

NAT Gateway, public IPv4 addresses, Fargate, RDS, Valkey, ALB, WAF, S3, ECR, the builder instance, and CloudFront may incur charges. Check the [AWS Pricing Calculator](https://calculator.aws/) for your Region and expected runtime. This workshop is not guaranteed to stay within the AWS Free Tier.

## 2. Source Code and Templates

This workshop uses the pinned commit `7d6bba8109f6eac51c0d8241a7083e3e364cf59d` in the [TINA repository](https://github.com/poor-frog/TINA), which includes the ECS backend. Do not substitute `main`: the checked `main` branch does not contain the corresponding ECS backend.

On your local machine, download the [source ZIP at this commit](https://github.com/poor-frog/TINA/archive/7d6bba8109f6eac51c0d8241a7083e3e364cf59d.zip) and extract it. Note the `deploy/aws/` directory because a Console step will ask you to upload `foundation.yml`. You will build the container images on a dedicated ARM64 EC2 instance in a later section; you do not need to copy any secrets from the author's machine.

## 3. Open AWS CloudShell

In the Console, click the **CloudShell** icon and confirm that the Region is `us-east-1`. All bash commands from here on run in CloudShell unless a page explicitly states to run them in EC2 Session Manager.

In CloudShell, download the same template revision and define helper functions for reading stack outputs:

```bash
export AWS_REGION=us-east-1
export AWS_PAGER=''
export TINA_REV=7d6bba8109f6eac51c0d8241a7083e3e364cf59d
mkdir -p "$HOME/tina-workshop"
curl -fL "https://github.com/poor-frog/TINA/archive/${TINA_REV}.zip" -o "$HOME/tina-workshop/source.zip"
unzip -q -o "$HOME/tina-workshop/source.zip" -d "$HOME/tina-workshop"
export TINA_SRC="$HOME/tina-workshop/TINA-${TINA_REV}"
stackout() { aws cloudformation describe-stacks --region "$AWS_REGION" --stack-name "$1" --query "Stacks[0].Outputs[?OutputKey=='$2'].OutputValue | [0]" --output text; }
repoarn() { aws ecr describe-repositories --region "$AWS_REGION" --repository-names "tina-staging/$1" --query 'repositories[0].repositoryArn' --output text; }
export TINA_ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
export TINA_TAG=ws-v1
```

These commands write files into your CloudShell home directory. If CloudShell reconnects and loses your variables or helper functions, simply re-run the block above—you do not need to recreate any stacks. Subsequent steps use the image tag `ws-v1`; if you need to rebuild after a partial push, choose a new tag and use it consistently in both EC2 and CloudShell because ECR repositories are configured with immutable tags.
