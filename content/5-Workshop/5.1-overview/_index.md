---
aliases: ["/5-workshop/5.1-workshop-overview/"]
title: "Overview and Evaluation Criteria"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

## Objectives

After this workshop, the practitioner can trace the request path, verify each layer's state in the AWS Console, create a separate lab network, inspect images/logs and present evidence-backed results. Completing these steps **does not mean** TINA was redeployed end to end.

## Staging environment observed

On 25 November 2026 in `us-east-1`, AWS CLI returned the following components:

| Layer | Staging resource | How to evaluate |
| --- | --- | --- |
| Foundation | Stack `tina-foundation`: VPC, subnets, route tables, S3 gateway endpoint, ECS cluster and some ECR repositories | CloudFormation → stack → Resources; VPC → Your VPCs |
| Egress | `tina-staging-egress`: NAT gateway, Elastic IP and routes | VPC → NAT gateways and Route tables |
| Edge | `tina-staging-edge`: CloudFront, VPC origin, internal ALB and listener | CloudFront → Distributions; EC2 → Load balancers |
| Data | `tina-staging-datastores`: RDS PostgreSQL, ElastiCache Valkey | RDS → Databases; ElastiCache → Valkey/Redis OSS caches |
| Application | Stacks `tina-staging-core`, `-terminal`, `-runtime`, `-agent-api`, `-agent-reach`, `-mcp`, `-flows`, `-voice`, `-viegem` | ECS → cluster `tina-foundation-ecs` → Services |
| Bot | `tina-staging-bot` creates a task definition and role; runtime starts bots on demand | CloudFormation → Resources; ECS → Task definitions/Tasks |

At the time of the check, 11 staging services had `runningCount = desiredCount = 1`; the staging database showed `available`. Running tasks only prove ECS started them — check target health, logs and a functional test for deeper evaluation. State may change after that time.

General flow: **browser → CloudFront → VPC origin → internal ALB → Terminal/gateway → internal services → PostgreSQL/Valkey/S3**. Voice and transcription are separate services; one running component is not evidence that the whole chain works.

## Start observing in the Console

1. Open the AWS Console, check the account name and select **N. Virginia (us-east-1)** in the top-right corner.
2. Go to **CloudFormation → Stacks**, filter `tina-staging` and open each stack. View **Overview**, **Resources** and **Events**.

{{< workshop-screenshot file="01-cloudformation-staging.png" description="List of TINA staging stacks and their status in CloudFormation." >}}

3. Record stack names, status, timestamps and the logical resource IDs you need. Do not copy secret values or every output into the report.
4. Go to **Amazon ECS → Clusters → tina-foundation-ecs → Services**. Compare **Desired tasks** with **Running tasks** for each service.

{{< workshop-screenshot file="02-ecs-services.png" description="Staging services in ECS, including desired and running task counts." >}}

5. Open **tina-staging-bot → Resources** and confirm the bot has a task definition; a permanently running bot service is not required.

**Pass condition:** you can identify each layer and its related services and record the check time; this does not mean the application was tested.

## Proposal versus reality

![AWS architecture diagram in the TINA proposal](/images/2-Proposal/tina_aws_architecture.png)

*Diagram from the proposal; some components or connections may differ from real staging.*

The proposal diagram describes the target architecture. Record Cognito, Bedrock, SES, WAF or any feature on the diagram as integrated only after you verify configuration and real behaviour. For example, listing Cognito user pools returned no pool in `us-east-1` at survey time; do not infer that no region or account has one.
