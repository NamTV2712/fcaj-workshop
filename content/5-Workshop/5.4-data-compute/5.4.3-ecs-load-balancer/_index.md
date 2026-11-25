---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.3-test-endpoint/"]
title: "ECS, Task Definitions and Load Balancer"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

## A. Inspect ECS staging

1. Open **Amazon ECS → Clusters → tina-foundation-ecs → Services**.
2. For each `tina-staging-*` service, record status, **Desired tasks**, **Running tasks** and **Pending tasks**. Select a service → **Deployments and events** to read initialisation or task replacement errors.

{{< workshop-screenshot file="12-ecs-services.png" description="ECS service list with desired, running and pending tasks." >}}

3. Open **Tasks**, select a running task → view the task definition, containers, status and the **View logs in CloudWatch** link. Do not capture environment values, tokens, secrets or internal URLs.

{{< workshop-screenshot file="13-ecs-task.png" description="ECS task details and container status; environment and secrets masked." >}}

4. Open **Task definitions** → select the revision in use and compare image, CPU/memory, ports, task role, execution role, log configuration and **secret names**. Do not edit a staging revision.
5. Find stack `tina-staging-bot` in CloudFormation and check the bot task definition. Bots are started on demand; the absence of a permanently running bot service is not an error.

For example, observed on 25 November 2026: Terminal used container port 3000; core had several containers including gateway on port 8000. This is a configuration snapshot, not a substitute for the task definition of the release you will deploy.

## B. Inspect ALB and CloudFront

1. **CloudFormation → tina-staging-edge → Resources**: identify the distribution, VPC origin, load balancer and listener.
2. **EC2 → Load Balancers**: open the staging ALB, check **Scheme = internal**, VPC and listeners. Do not copy or change rules of a system serving users.
3. **EC2 → Target Groups**: compare the two staging target groups. Open **Targets** and view **Health status** and the reason if unhealthy. At check time, terminal and gateway were both `healthy`; terminal used health path `/api/auth/providers`, gateway used `/health`.

{{< workshop-screenshot file="14-target-health.png" description="Health status of the terminal or gateway target group." >}}

4. **CloudFront → Distributions** → open the distribution from the edge stack: check deployment status, origin and **VPC origin**. Staging CloudFront connects to an internal ALB; pointing a CloudFront origin directly at a public ALB DNS is a different architecture.

{{< workshop-screenshot file="15-cloudfront-origin.png" description="CloudFront distribution and VPC origin; domain and internal identifiers masked." >}}

5. If unhealthy, check the container/target group port, health path, security group, task state and logs first. Do not fix staging if your task is only evaluation.

## C. Create a lab ECS when a full release kit exists

1. **ECS → Clusters → Create cluster** → name `tina-ws-cluster`, choose networking/compute per the release guide. Creating a cluster does not create services.
2. **ECS → Task definitions → Create new task definition** → choose Fargate if compatible; fill family, valid CPU/memory, task/execution roles, ECR image + digest, ports, non-sensitive environment variables, secret references and log group according to the manifest of **each service**.
3. With the lab cluster, choose **Create → Service**; select the correct task definition/revision, task count, app subnets, security groups, service discovery and load balancer/target group per the manifest. Check **Events** and task health after creation.
4. Repeat in the release dependency order, including migration/init jobs, PostgreSQL/Valkey/S3 connections, internal endpoints and the runtime that starts bots. Verify each service before creating dependent services.

**Stopping point:** the workshop does not yet contain a tested portable manifest/task definition set and dependency order. You cannot fill every field correctly from this page or claim a new cluster runs full TINA. The instructor must prepare and test the release kit as described in [Validate the application](../5.4.4-application-validation/).

Fargate does not support declaring GPUs for a task; observed staging VieGem ran Fargate tasks, which does not mean it used a GPU. If a release requires GPU, choose compatible GPU infrastructure and recheck cost/quota. [AWS: Fargate task definition differences](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html).
