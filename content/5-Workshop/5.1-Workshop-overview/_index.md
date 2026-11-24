---
title: "Workshop Overview"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

#### Target architecture

You are rebuilding the full architecture from the proposal on AWS in `us-east-1`, starting from an empty account:

1. **Network:** VPC `10.0.0.0/16` across `us-east-1a` and `us-east-1b` — public, private-app and private-data subnets; Internet Gateway; NAT Gateway; route tables; security groups; VPC endpoints for S3 and ECR.
2. **Edge:** CloudFront + AWS WAF in front of an Application Load Balancer.
3. **Identity:** Cognito user pool with Google OAuth.
4. **Compute:** ECS cluster on Fargate with five services — Web serving, Bot (Playwright), STT (VieGem), TTS (VieNeu), Agent.
5. **Data:** RDS PostgreSQL (transcripts), ElastiCache Redis (live state), S3 (recordings/exports).
6. **AI/email:** Amazon Bedrock (agent, notes, summaries, translation), Amazon SES (follow-up emails).
7. **Operations:** ECR, IAM task roles, Secrets Manager, KMS, CloudWatch, Budgets/Cost Explorer.

![TINA AWS Architecture](/images/2-Proposal/tina_aws_architecture.png)

#### Source code is only an input

Pull `https://github.com/poor-frog/TINA.git` to obtain Dockerfiles, Compose files and build scripts. You will:

- build each image from its Dockerfile (`make build`, `make bot`),
- push the images to the ECR repositories you create,
- write the ECS task definitions that reference those images,
- let the application use the AWS resources you create (RDS, ElastiCache, S3, Bedrock, SES, Cognito).

No pre-built `ghcr.io/poor-frog/tina-*:prod` image is used in this workshop.

#### Verification mindset

For every resource, capture evidence: the console page or `aws … describe-*` output, the resulting health check, and the application behaviour. The final checklist in [Clean up](../5.6-cleanup/) lists exact screenshot names.

- **Screenshot:** `screenshot-00-prereqs.png`.
