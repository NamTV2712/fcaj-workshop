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

> **Scope and status:** The source code, CloudFormation templates, and all 15 prebuilt ARM64 images (`workshop-arm64`) have been deployed and verified end-to-end on an independent AWS account (including infrastructure provisioning, Google sign-in, meeting bot participation, and VieGem transcription). This workshop deploys a single-AZ data layer to keep lab costs low and is intended for lab/pilot evaluation rather than High Availability production.

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

Estimated completion time is **15–20 minutes** using the quick single-stack path in [5.4A](5.4-full-cloudformation/) (copying prebuilt images from GHCR), or **30–45 minutes** for the multi-stack path (depending on RDS, ElastiCache, and CloudFront provisioning times). AWS resources and data transfer may incur charges as soon as resources are created; remember to clean up all resources in [Section 5.6](5.6-cleanup-evidence/) when finished.

## Guide Screenshots

Each step in this workshop includes **real screenshots** from the AWS Console and the deployed TINA web application directly beneath the corresponding instructions so you can easily verify your progress. Sensitive details (Account IDs, email addresses, and secrets) have been redacted in the reference captures.

When capturing your own screenshots for lab evidence, never expose passwords, client secrets, tokens, personal information, or real meeting content; always mask your Account ID, email address, and private domains before sharing.
