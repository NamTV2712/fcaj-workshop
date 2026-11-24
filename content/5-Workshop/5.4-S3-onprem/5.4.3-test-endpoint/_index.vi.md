---
title: "ALB và ECS service"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

Template CloudFormation tạo ALB, target group, ECS cluster và 5 service Fargate. Kiểm tra bằng:

```bash
aws elbv2 describe-load-balancers --names tina-alb
aws elbv2 describe-target-groups --names tina-web-tg
aws elbv2 describe-target-health --target-group-arn <tg-arn>
aws ecs describe-services --cluster tina-cluster \
  --services tina-web tina-bot tina-stt tina-tts tina-agent
aws ecs list-tasks --cluster tina-cluster
```

Kỳ vọng: cả 5 service có số `RUNNING` bằng desired count, target group `healthy`, task nằm ở private subnet dùng `tina-web-sg`/`tina-data-sg`.

Nếu service không kéo được image, kiểm tra repository ECR tương ứng và image tag `:prod` đã được push **trước khi** deploy stack — ECS không đợi image.

```bash
aws logs tail /ecs/tina --follow
```

- **Ảnh cần chụp:** `screenshot-13-ecs-alb-healthy.png`.
