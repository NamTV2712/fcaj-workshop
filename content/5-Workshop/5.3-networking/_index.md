---
aliases: ["/5-workshop/5.3-s3-vpc/"]
title: "Network foundation"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

## Create the Foundation with CloudFormation

Instead of creating each subnet manually, you upload a template in the CloudFormation Console to create a two-AZ VPC, route tables, an S3 gateway endpoint, an ECS cluster, an S3 bucket, and three foundational ECR repositories. Afterward, you use the CLI to add NAT egress and routing for the application.

1. [Create the foundation in the Console](5.3.1-vpc-subnets/).
2. [Create NAT and verify network routes](5.3.2-gateways-routing/).

Keep the stack outputs for the subsequent stacks; the CLI commands in this workshop read those outputs directly from your account.
