---
aliases: ["/5-workshop/5.4-s3-onprem/"]
title: "Data, Images, ECS and Application"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

This part combines two kinds of activity:

- **Observe staging:** view configuration, tasks, target health, logs and results from an environment you are allowed to read. Do not change existing services.
- **Practise in the lab:** create a bucket, an ECR repository and, if needed, other services in the lab account. Creating a resource does not integrate it into TINA.

## Order of work

1. [S3, ECR and images](5.4.1-s3-ecr-images/).
2. [RDS, Valkey, secrets and additional services](5.4.2-data-secrets/).
3. [ECS, task definitions and load balancer](5.4.3-ecs-load-balancer/).
4. [Validate the application flow](5.4.4-application-validation/).

Real staging uses several stacks. At the time of the check, `tina-staging-core` had containers `schema-init`, `meeting`, `admin`, `asr-control` and `gateway`; `tina-staging-terminal` was a separate task. Configuration may change between deployments. Verify against the stacks and task definitions currently running; do not assume a five-container list is enough to rebuild the whole system.

Do not run `make ps` on a laptop to prove ECS is running — that is local Docker Compose state. Do not assume a resource created in the Console is used by the application: the corresponding service must still be configured and deployed.
