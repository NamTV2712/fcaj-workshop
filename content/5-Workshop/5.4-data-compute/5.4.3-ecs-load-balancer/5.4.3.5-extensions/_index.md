---
title: "Scope and extensions"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.4.3.5 </b> "
---

## What is configured

This path deploys a complete meetings test environment: Terminal, Google sign-in, core services, Runtime launching ECS bot tasks, storage, and optional VieGem. This flow has been verified end-to-end on an independent AWS account across Google sign-in, meeting bot participation, and VieGem transcription.

## Optional Extensions Ready to Deploy

- **Amazon Bedrock (`amazon.nova-lite-v1:0`)**: The single-stack template in [5.4A](../../../5.4-full-cloudformation/) already grants `bedrock:InvokeModel` permissions for `amazon.nova-lite-v1:0` (`bedrock-converse`) to power notes, summaries, and the Agent. On a fresh account, open **Amazon Bedrock → Model catalog** in `us-east-1` to confirm access to `Amazon Nova Lite`.
- **Amazon SES (Post-meeting follow-up emails)**: Requires a **custom domain hosted in Route 53** (for DKIM, SPF, and DMARC DNS records), so it is not enabled by default in the base lab. Once you have a domain, deploy `deploy/aws/staging-ses.yml` from the project's `main` branch (provisions SES ConfigurationSet, EmailIdentity, Route 53 DNS records, SMTP credentials in Secrets Manager, and 3 CloudWatch reputation alarms for bounces/complaints):

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-ses \
  --template-file deploy/aws/staging-ses.yml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    DomainName=your-domain.example \
    HostedZoneId=Z1234567890ABC \
    AlertEmail=ops@your-domain.example
```

- **CloudWatch Dashboard & Operational Alarms**: In addition to the 13 built-in Log Groups, `main` includes `deploy/aws/staging-workspace-s3-monitoring.yml` (10 Metric Filters, 20 CloudWatch Alarms covering ALB 5xx, ECS memory ≥85%, RDS CPU/storage/connections, and S3 sync, plus a unified CloudWatch Dashboard) and `deploy/aws/apply-ecr-lifecycle.sh` to expire old ECR images automatically.
- **Workspace/agent workbench & Voice (LiveKit/VieNeu)**: The multi-stack walkthrough deploys the lightweight `meetings` tier; to enable the full Workspace, Agent, MCP, Flows, and Voice stack, use the combined template in [5.4A](../../../5.4-full-cloudformation/) with all 15 `workshop-arm64` images.
- **Production operations**: Additional SSO providers, custom domains (`staging-domain-acm.yml`), Multi-AZ/backup, and automated CI/CD (`staging-github-ecr.yml`) are available as reference templates in [deploy/aws on main](https://github.com/poor-frog/TINA/tree/main/deploy/aws). Before going to production, review IAM permissions, service quotas, and validate each feature independently.
