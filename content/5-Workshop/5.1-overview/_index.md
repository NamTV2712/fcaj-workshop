---
aliases: ["/5-workshop/5.1-workshop-overview/"]
title: "Overview and acceptance"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

## What Will You Build?

In a fresh AWS account, CloudFormation creates a two-Availability-Zone VPC, an ECS cluster, a private S3 bucket, outbound networking, RDS PostgreSQL, Valkey, CloudFront, an ALB, and the ECS services. You **build the images yourself from source** and push them to your own ECR repositories. Names include `staging` because some templates and ECR permissions in this source revision require that prefix; all resources still belong to your own account.

```text
Browser → CloudFront/WAF → Internal ALB → Terminal (ECS)
                                              ↓
                                  Gateway + meeting/admin API
                                    ↓           ↓        ↓
                             Runtime/ECS bot   RDS    Valkey
                                    ↓           ↓
                                  S3          VieGem (optional)
```

To evaluate the lab, verify that the stacks created in your own account succeed, the services reach their desired state, and the sign-in/meeting flow works. A stack in `CREATE_COMPLETE` only confirms that AWS provisioned the resources—it does not prove that all TINA functionality works.

After completing the sections below, this screenshot shows the stack list in your **lab account**:

{{< workshop-screenshot file="01-cloudformation-staging.png" description="TINA stacks you created and their statuses in CloudFormation." >}}

The next screenshot shows the service status inside your cluster:

{{< workshop-screenshot file="02-ecs-services.png" description="ECS services in your lab account, including desired and running tasks." >}}

## Acceptance Criteria

- Your CloudFront URL loads the TINA site and allows signing in with a test Google account.
- The ECS core, runtime, and terminal services run stably, and the terminal target group is healthy.
- Create an authorized test meeting and observe the bot; if ASR is enabled, verify the transcript and note any errors encountered.
- Understand the cost drivers and cleanly delete all resources when finished.

Do not use the legacy `static/cloudformation/tina-infrastructure.yaml` template in the workshop repository: it is not part of the template set used in this walkthrough.
