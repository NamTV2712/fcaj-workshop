---
title: "ALB and ECS Services"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

The CloudFormation template creates the ALB, target group, ECS cluster and the five Fargate services. Verify them with:

```bash
aws elbv2 describe-load-balancers --names tina-alb
aws elbv2 describe-target-groups --names tina-web-tg
aws elbv2 describe-target-health --target-group-arn <tg-arn>
aws ecs describe-services --cluster tina-cluster \
  --services tina-web tina-bot tina-stt tina-tts tina-agent
aws ecs list-tasks --cluster tina-cluster
```

Expected: all five services have `RUNNING` count equal to desired count, the target group shows `healthy`, and tasks use private subnets with `tina-web-sg` / `tina-data-sg`.

If a service cannot pull its image, confirm the matching ECR repository exists and the image with tag `:prod` was pushed before the stack was deployed — ECS does not wait for images.

```bash
aws logs tail /ecs/tina --follow
```

- **Screenshot:** `screenshot-13-ecs-alb-healthy.png`.
