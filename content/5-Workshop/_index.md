---
title: "Workshop"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Build the Whole TINA Architecture from Scratch

#### Overview

This workshop rebuilds **everything** in the TINA proposal: the AWS infrastructure (VPC, networking, data stores, identity, AI, email, edge) **and** the application services compiled from source. The GitHub repository is pulled only as source input — you create the AWS resources yourself, build each service from its Dockerfile, push the images to ECR, deploy them on ECS Fargate, then verify and capture screenshots.

Nothing is assumed to exist beforehand. You start from an empty AWS account in `us-east-1`.

![TINA AWS Architecture](/images/2-Proposal/tina_aws_architecture.png)

#### Manual vs CloudFormation

**Done by hand (first):**

1. `tina-vpc` (`10.0.0.0/16`) and 6 subnets across `us-east-1a` / `us-east-1b` — 2 public, 2 private-app, 2 private-data.
2. Internet Gateway `tina-igw`, EIP and NAT Gateway `tina-nat`; 3 route tables.
3. Six ECR repositories (`tina-terminal`, `tina-gateway`, `tina-bot`, `tina-stt`, `tina-tts`, `tina-agent`). Create these **before** the stack so you can push images first — ECS services created by CloudFormation reference `:prod` images and will not wait for them.

**Created by CloudFormation:** VPC endpoints (S3/ECR), S3, KMS, IAM, Secrets Manager, RDS, ElastiCache, Cognito, ALB, ECS cluster + 5 Fargate services, CloudWatch, CloudFront + WAF, Budgets.

Template: `static/cloudformation/tina-infrastructure.yaml`.

```bash
aws cloudformation deploy \
  --template-file tina-infrastructure.yaml \
  --stack-name tina-infra \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1 \
  --parameter-overrides \
      VpcId=<vpc-id> PublicSubnet1=<public-1a> PublicSubnet2=<public-1b> \
      PrivateSubnet1=<app-1a> PrivateSubnet2=<app-1b> \
      AppRouteTableId=<app-rt> DataRouteTableId=<data-rt> \
      DBPassword='<strong-password>' CertificateArn=<acm-cert-arn>
```

Bedrock model access, SES domain verification and Cost Explorer review are done in the console.

#### Service coverage check

| Service in the request | Created by | Method |
| --- | --- | --- |
| VPC | Step 1 | Manual |
| 2 Availability Zones | Step 1 (`us-east-1a`, `us-east-1b`) | Manual |
| Public subnet + 2 private subnets | Step 1 (plus 2 data subnets) | Manual |
| Internet Gateway | Step 1 (`tina-igw`) | Manual |
| NAT Gateway | Step 1 (`tina-nat`) | Manual |
| ECR | Step 2 (6 repositories) | Manual |
| VPC endpoints for S3/ECR | Stack | CloudFormation |
| S3 | Stack (recordings/exports) | CloudFormation |
| KMS | Stack (`tina-key`) | CloudFormation |
| IAM | Stack (task roles) | CloudFormation |
| Secrets Manager | Stack (`tina/core`) | CloudFormation |
| RDS | Stack (`tina-db`) | CloudFormation |
| ElastiCache | Stack (`tina-cache`) | CloudFormation |
| Cognito | Stack (`tina-users`) | CloudFormation |
| ALB | Stack (`tina-alb`) | CloudFormation |
| ECS + 5 Fargate services | Stack (`tina-cluster`) | CloudFormation |
| CloudWatch | Stack (`/ecs/tina` + alarm) | CloudFormation |
| CloudFront | Stack (`tina-cdn`) | CloudFormation |
| WAF | Stack (`tina-waf-acl`, attached to CloudFront) | CloudFormation |
| AWS Budgets | Stack (`tina-monthly`, 50/80/100%) | CloudFormation |
| Bedrock | Console (model access) | Console |
| SES | Console (verified domain) | Console |
| Cost Explorer | Console (7-day cost review) | Console |

#### Naming convention

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
| ECR | `tina-<service>` (6 repos) |
| ECS cluster / services | `tina-cluster`; `tina-web`, `tina-bot`, `tina-stt`, `tina-tts`, `tina-agent` |
| ALB / target group | `tina-alb`, `tina-web-tg` |
| RDS / ElastiCache | `tina-db` (db.t4g.micro), `tina-cache` (cache.t4g.micro) |
| Cognito / Bedrock | `tina-users`, Claude/Nova model access |
| SES / CloudFront / WAF | verified domain, `tina-cdn`, `tina-waf-acl` |
| Secrets / KMS / Budget | `tina/core`, `tina-key`, `tina-monthly` |

#### Step-by-step guide

**Step 0 — Prepare account, tools and source**
```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
chmod 600 .env.keys
aws configure            # region us-east-1, never paste secrets into screenshots
```
- **Screenshots:** `screenshot-00-prereqs.png`, `screenshot-01-clone.png`.

**Step 1 — Build VPC and networking by hand**
Create the VPC, 6 subnets, IGW, NAT and 3 route tables. Public `0.0.0.0/0 → IGW`; app `0.0.0.0/0 → NAT`; data has no `0.0.0.0/0`.
- **Screenshots:** `screenshot-02-vpc-subnets.png`, `screenshot-03-route-tables.png`.

**Step 2 — Create ECR repos, build from source, push images**
```bash
for s in terminal gateway bot stt tts agent; do
  aws ecr create-repository --repository-name tina-$s --region us-east-1
done
make build && make bot
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
# tag and push each tina/v012-<service>:dev image as <account>.dkr.ecr.us-east-1.amazonaws.com/tina-<service>:prod
```
- **Screenshots:** `screenshot-04-ecr-repos.png`, `screenshot-05-images-built.png`.

**Step 3 — Deploy the rest with CloudFormation**
Run the `aws cloudformation deploy` command above, then verify stack status `CREATE_COMPLETE`.
- **Screenshot:** `screenshot-06-stack-complete.png`.

**Step 4 — Console-only services**
Enable Bedrock model access, verify the SES domain, open Cost Explorer.
- **Screenshots:** `screenshot-07-bedrock-ses.png`, `screenshot-08-cost-explorer.png`.

**Step 5 — Verify services**
Use the child pages: [data & compute](5.4-s3-onprem/), [ALB/ECS](5.4-s3-onprem/5.4.3-test-endpoint/), [running system](5.4-s3-onprem/5.4.4-dns-simulation/), [security & cost](5.5-policy/).
- **Screenshots:** `screenshot-13-ecs-alb-healthy.png`, `screenshot-17-app-running.png`, `screenshot-18-transcript.png`.

**Step 6 — Clean up**
Delete the CloudFormation stack, then the manually created VPC resources; locally run `make down`.

#### Tips

* Native Windows Python/PowerShell is unsupported — use WSL2; Apple Silicon uses MPS; Linux/WSL2 with NVIDIA uses Docker CUDA. No automatic CPU fallback — use `TINA_VIEGEM_DEVICE=cpu make all` explicitly.
* Source builds need roughly **8 vCPUs / 16 GB RAM** and time for model downloads.
* Never commit or screenshot `.env.keys`, API keys, OAuth secrets or the DB password.

#### Contents

1. [Workshop overview](5.1-workshop-overview/)
2. [Prerequisites](5.2-prerequiste/)
3. [Build VPC and networking](5.3-s3-vpc/)
4. [Build data, identity and compute](5.4-s3-onprem/)
5. [Security, monitoring and cost](5.5-policy/)
6. [Clean up](5.6-cleanup/)
