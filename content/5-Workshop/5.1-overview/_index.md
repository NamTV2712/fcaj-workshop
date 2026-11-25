---
aliases: ["/5-workshop/5.1-workshop-overview/"]
title: "Overview and assessment"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

Inspect CloudFormation stacks `tina-foundation` and `tina-staging-*` in `us-east-1`, then ECS cluster `tina-foundation-ecs`. The observed staging design uses CloudFront with a VPC origin, an internal ALB, multiple ECS services, RDS PostgreSQL, ElastiCache Valkey and S3. The bot has an on-demand task definition rather than a permanently running bot service.

On 25 November 2026, 11 staging services had one running task each. This is a point-in-time count, not proof that meetings and transcription work. Verify target health and run an authorized test with synthetic data.
