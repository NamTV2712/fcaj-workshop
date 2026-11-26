---
title: "Workshop"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# TINA – Self-Hosted Meeting & AI Agent System on AWS

This workshop guides you through using **your own AWS account** to build a test deployment of TINA: CloudFront → internal ALB → ECS Fargate, backed by PostgreSQL on RDS, Valkey on ElastiCache, S3, and ECR. You create fresh resources and sign in at the URL provisioned by your account.

This walkthrough combines the **AWS Console for CloudFormation, EC2, and WAF** with the AWS CLI and CloudFormation for the remaining steps. You do not need access to the author's account or machine.

> **Scope and status:** the code and templates have been cross-checked against the project's AWS branch, but the full path has not yet been re-run from scratch on a blank account. Results should be verified during your hands-on run—especially building ARM64 images, signing in, having the bot join a meeting, and transcription. This is a single-AZ data test environment, not a production configuration.

The initial deployment runs **Terminal in meetings mode**, Google sign-in, the meeting bot, and optionally VieGem for non-commercial transcription testing. Full workspace/agent capabilities, voice assistant, additional models, and extra integrations are not enabled by default in this build; see the [extensions section](5.4-data-compute/5.4.3-ecs-load-balancer/5.4.3.5-extensions/).

## Quick Single-File Deployment (Recommended)

See [single CloudFormation deployment](5.4-full-cloudformation/) to use the combined `tina-full.yml` template together with the pre-built set of 15 ARM64 images on GHCR (including **VieGem** and 3 Voice images): simply paste 5 short commands into **AWS CloudShell** (~15–20 minutes), then attach your own Google OAuth credentials to run the full web app. The multi-stack walkthrough below is for cases where you want to build and inspect each infrastructure layer individually.

## Walkthrough Order

1. [Overview and acceptance criteria](5.1-overview/).
2. [Account, quotas, and source code preparation](5.2-prerequisites/).
3. [VPC and network foundation](5.3-networking/).
4. [Build images, create data stores, deploy the website, and test](5.4-data-compute/).
5. [Monitoring and costs](5.5-security-monitoring-costs/).
6. [Cleanup and evidence](5.6-cleanup-evidence/).

You will need time to build images and wait for RDS, ElastiCache, and CloudFront to provision; there is no measured total duration yet for a complete end-to-end run. AWS resources, models, and data transfer may incur charges as soon as resources are created.

## Guide Screenshots

After each step that shows a **Screenshot needed** box, take a real screenshot and save the PNG to `static/images/5-Workshop/tina/` using the exact filename shown in the box. When the site is rebuilt, the image will appear **directly beneath the corresponding step**. The [screenshot checklist](/images/5-Workshop/tina/README.md) is for tracking; images are not grouped at the bottom of the page.

Do not include passwords, client secrets, tokens, personal information, or real meeting content in screenshots. Mask your account ID, email address, and private domains before sharing.
