---
aliases: ["/5-workshop/5.4-s3-onprem/"]
title: "Images, data and application"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

## Build the system in dependency order

1. [Create ECR repositories and build ARM64 images on EC2](5.4.1-s3-ecr-images/).
2. [Create RDS PostgreSQL, Valkey, and secrets](5.4.2-data-secrets/).
3. [Deploy edge, runtime, core, Terminal, and optional ASR](5.4.3-ecs-load-balancer/).
4. [Sign in and validate a meeting](5.4.4-application-validation/).

Each section depends on the outputs of the previous section. The name `tina-staging` in the templates is a technical name in your own AWS account and does not require using the author's environment.
