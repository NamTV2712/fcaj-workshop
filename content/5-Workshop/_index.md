---
title: "Workshop"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Build the Whole TINA Architecture from Scratch

#### Overview

This workshop rebuilds **everything** in the TINA proposal: the AWS infrastructure (VPC, networking, data stores, identity, AI, email, edge) **and** the application services compiled from source code. The GitHub repository is pulled only as source input — you create the AWS resources yourself, build each service from its Dockerfile, push the images to ECR, deploy them on ECS Fargate, then verify and capture screenshots.

Nothing is assumed to exist beforehand. You start from an empty AWS account in `us-east-1`.

#### What you will create (in order)

| # | Layer | Resources you create |
| --- | --- | --- |
| 1 | Account & tools | IAM admin user, AWS CLI, Docker, Dotenvx, local source clone |
| 2 | Network | VPC `tina-vpc` (`10.0.0.0/16`), 6 subnets across 2 AZs, Internet Gateway, NAT Gateway, 3 route tables, security groups |
| 3 | Private connectivity | Gateway endpoint for S3, Interface endpoints for ECR (VPC endpoints from the proposal's cost section) |
| 4 | Storage | S3 buckets for recordings/exports with encryption and lifecycle rule |
| 5 | Images | Build every service from Dockerfile (`make build`) and push to ECR repositories |
| 6 | Compute | ECS cluster, task definitions and services: Web, Bot, STT, TTS, Agent; Application Load Balancer + target group + health check |
| 7 | Data | RDS PostgreSQL, ElastiCache Redis |
| 8 | Identity & AI | Cognito user pool with Google OAuth, Bedrock model access |
| 9 | Email & edge | SES verified domain, CloudFront distribution, AWS WAF web ACL |
| 10 | Security & cost | IAM task roles, Secrets Manager, KMS, CloudWatch logs/alarms, AWS Budgets |
| 11 | Verify | Health endpoints, live transcript, `make probe`, AWS CLI checks |
| 12 | Clean up | Delete services, load balancer, databases, VPC and buckets |

![TINA AWS Architecture](/images/2-Proposal/tina_aws_architecture.png)

#### Naming convention (use these consistently)

| Resource | Name / value |
| --- | --- |
| Region | `us-east-1` |
| VPC | `tina-vpc`, `10.0.0.0/16` |
| Public subnets | `tina-public-1a` `10.0.1.0/24`, `tina-public-1b` `10.0.2.0/24` |
| Private app subnets | `tina-app-1a` `10.0.11.0/24`, `tina-app-1b` `10.0.12.0/24` |
| Private data subnets | `tina-data-1a` `10.0.21.0/24`, `tina-data-1b` `10.0.22.0/24` |
| IGW / NAT | `tina-igw`, `tina-nat` (one EIP) |
| Route tables | `tina-public-rt`, `tina-app-rt`, `tina-data-rt` |
| S3 | `tina-<name>-recordings`, `tina-<name>-exports` |
| ECR | `tina-<service>` (terminal, gateway, bot, stt, tts, agent, …) |
| ECS cluster / services | `tina-cluster`; `tina-web`, `tina-bot`, `tina-stt`, `tina-tts`, `tina-agent` |
| ALB / target group | `tina-alb`, `tina-web-tg` |
| RDS / ElastiCache | `tina-db` (db.t4g.micro), `tina-cache` (cache.t4g.micro) |
| Cognito / Bedrock | `tina-users`, Claude/Nova model access |
| SES / CloudFront / WAF | verified domain, `tina-cdn`, `tina-waf-acl` |
| Secrets / KMS / Budgets | `tina/*`, `tina-key`, `tina-monthly` |

#### Manual vs CloudFormation

Only **three things are done by hand**; everything else comes from one CloudFormation template:

- **By hand:** `tina-vpc` (CIDR `10.0.0.0/16`), the 6 subnets across 2 AZs, and the NAT Gateway + Internet Gateway (including its EIP). Create these first and record the IDs.
- **By CloudFormation:** all remaining resources — S3, ECR, IAM, Secrets Manager, KMS, RDS, ElastiCache, Cognito, ALB, ECS + 5 Fargate services, CloudFront, WAF, CloudWatch, Budgets.

Template path: `static/cloudformation/tina-infrastructure.yaml` (copy it into the cloned repo or reference it by local path).

```bash
aws cloudformation deploy \
  --template-file tina-infrastructure.yaml \
  --stack-name tina-infra \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1 \
  --parameter-overrides \
      VpcId=<vpc-id> PublicSubnet1=<public-1a> PublicSubnet2=<public-1b> \
      PrivateSubnet1=<private-1a> PrivateSubnet2=<private-1b> \
      DBPassword='<strong-password>' CertificateArn=<acm-cert-arn> \
      GitHubOAuthClientId=<client-id> GitHubOAuthClientSecret=<client-secret>
```

If you prefer a fully manual walkthrough, every resource is documented in the child pages — the template only speeds up creation.

#### Service coverage check

| Service in the request | Where it is created | Method |
| --- | --- | --- |
| VPC | Step 1 | Manual |
| 2 Availability Zones | Step 1 (`us-east-1a`, `us-east-1b`) | Manual |
| Public subnet + 2 private subnets | Step 1 (`tina-public-*`, `tina-private-*`) | Manual |
| Internet Gateway | Step 1 (`tina-igw`) | Manual |
| NAT Gateway | Step 1 (`tina-nat`) | Manual |
| S3 | Step 2 (recordings/exports) | CloudFormation |
| ECR | Step 2 (6 repositories) | CloudFormation |
| IAM | Step 5 (task roles) | CloudFormation |
| Secrets Manager | Step 5 (`tina/core`) | CloudFormation |
| KMS | Step 5 (`tina-key`) | CloudFormation |
| RDS | Step 3 (`tina-db`) | CloudFormation |
| ElastiCache | Step 3 (`tina-cache`) | CloudFormation |
| Cognito | Step 3 (`tina-users`) | CloudFormation |
| ALB | Step 4 (`tina-alb`) | CloudFormation |
| ECS + 5 Fargate services | Step 4 (`tina-cluster`) | CloudFormation |
| Bedrock | Step 3 (model access) | Console |
| SES | Step 3 (verified domain) | Console |
| CloudFront | Step 5 (`tina-cdn`) | CloudFormation |
| WAF | Step 5 (`tina-waf-acl`) | CloudFormation |
| CloudWatch | Step 5 (log group/alarm) | CloudFormation |
| AWS Budgets | Step 5 (`tina-monthly`) | CloudFormation |
| Cost Explorer | Step 5 (console review) | Console |

#### Step-by-step guide

**Step 0 — Prepare account, tools and source**

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
chmod 600 .env.keys
aws configure            # region us-east-1, never paste secrets in screenshots
docker version --format '{{.Server.Version}}'   # >= 26
```
- **Screenshots:** `screenshot-00-prereqs.png`, `screenshot-01-clone.png`.

**Step 1 — Build the VPC and networking**

Create `tina-vpc`, 6 subnets, IGW, NAT Gateway, route tables and security groups as in the naming table. Attach public route `0.0.0.0/0 → IGW`, app route `0.0.0.0/0 → NAT`, data route with **no** internet route; add S3 gateway endpoint and ECR interface endpoints.
- **Screenshots:** `screenshot-02-vpc-subnets.png`, `screenshot-03-route-tables.png`, `screenshot-04-vpc-endpoints.png`.

**Step 2 — Storage, ECR and images**

Create the S3 buckets (encryption + lifecycle) and ECR repositories. Build all services locally from source (`make build`, `make bot`), then tag and push each image to ECR.
- **Screenshots:** `screenshot-05-s3-buckets.png`, `screenshot-06-ecr-repos.png`, `screenshot-07-images-built.png`.

**Step 3 — Data, identity and AI**

Create RDS PostgreSQL, ElastiCache Redis, Cognito user pool with Google OAuth callback, enable Bedrock models, verify SES domain.
- **Screenshots:** `screenshot-08-rds-redis.png`, `screenshot-09-cognito.png`, `screenshot-10-bedrock-ses.png`.

**Step 4 — Compute and load balancing**

Create the ALB + target group with health check, then ECS cluster and five task definitions/services using the ECR images, placing tasks in private app subnets with IAM task roles and secrets from Secrets Manager/KMS.
- **Screenshots:** `screenshot-11-alb.png`, `screenshot-12-ecs-cluster.png`, `screenshot-13-task-definitions.png`.

**Step 5 — Edge, security and cost**

Create CloudFront + WAF, CloudWatch log groups/alarms and AWS Budgets at 50/80/100%.
- **Screenshots:** `screenshot-14-cloudfront-waf.png`, `screenshot-15-budgets.png`.

**Step 6 — Verify**

Use the [Verify the services](5.4-s3-onprem/) page: ECS service events, ALB health, logs, app URLs, live transcript and `make probe`. Confirm S3/RDS/ElastiCache traffic stays on VPC endpoints (no NAT charges).
- **Screenshots:** `screenshot-16-ecs-healthy.png`, `screenshot-17-app-running.png`.

**Step 7 — Clean up**

Delete in reverse order: ECS services → ALB → RDS/ElastiCache → endpoints → NAT/IGW → subnets → VPC → S3/ECR. Locally run `make down`.

#### Contents

1. [Workshop overview](5.1-workshop-overview/)
2. [Prerequisites](5.2-prerequiste/)
3. [Build VPC & networking](5.3-s3-vpc/)
4. [Build data, identity & compute](5.4-s3-onprem/)
5. [Security & cost](5.5-policy/)
6. [Clean up](5.6-cleanup/)
