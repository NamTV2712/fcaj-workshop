---
title: "Bot và Runtime trên Fargate"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.4.3.2 </b> "
---

## 1. Tạo bot task definition

Trong CloudShell:

```bash
CLUSTER="$(stackout tina-staging ClusterName)"
BUCKET="$(stackout tina-staging StagingRecordingsBucket)"
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-bot --template-file "$TINA_SRC/deploy/aws/ecs-bot.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "BotImage=$(image bot)" \
    "BotRepositoryArn=$(repoarn bot)" "InvocationBucket=$BUCKET" ProbeInvocation=false
```

Template tạo task definition và IAM role. Bot chỉ được Runtime khởi chạy khi có yêu cầu họp; không có một service bot chạy thường trực là bình thường.

## 2. Tạo Runtime

```bash
VPC_ID="$(stackout tina-staging VpcId)"
APP_SUBNETS="$(stackout tina-staging AppSubnetIds)"
APP_SG="$(stackout tina-ws-data AppSecurityGroupId)"
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-runtime --template-file "$TINA_SRC/deploy/aws/staging-runtime.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "AppSecurityGroupId=$APP_SG" "RuntimeImage=$(image runtime)" \
    "RuntimeRepositoryArn=$(repoarn runtime)" \
    "RuntimeTaskRoleArn=$(stackout tina-ws-bot RuntimeTaskRoleArn)" \
    "BotTaskDefinitionArn=$(stackout tina-ws-bot BotTaskDefinitionArn)" \
    "BotImage=$(image bot)" "InvocationBucket=$BUCKET" \
    "ValkeyHost=$(stackout tina-ws-data ValkeyHost)" \
    "ValkeySecretArn=$(stackout tina-ws-data ValkeySecretArn)"
```

Đợi stack thành công. Template còn tạo Cloud Map private namespace `tina-staging.local` trong VPC của bạn; không tạo trùng namespace trong cùng VPC. Lấy **namespace ID** dùng cho các stack sau:

```bash
NAMESPACE_ID="$(aws cloudformation describe-stack-resource --region "$AWS_REGION" \
  --stack-name tina-ws-runtime --logical-resource-id DiscoveryNamespace \
  --query 'StackResourceDetail.PhysicalResourceId' --output text)"
printf 'Namespace ID: %s\n' "$NAMESPACE_ID"
```

Vào **ECS → Clusters**, chọn cluster từ `ClusterName`, xem service Runtime có task Running. Sau khi tạo core và terminal, trở lại đây để chụp ảnh danh sách:

{{< workshop-screenshot file="12-ecs-services.png" description="ECS services sau khi hoàn thành Runtime, core và terminal, kèm desired/running tasks." >}}

Chọn task Runtime → **Containers** và xem trạng thái; chỉ chụp phần không có token hay environment nhạy cảm:

{{< workshop-screenshot file="13-ecs-task.png" description="Task Runtime và trạng thái container; che environment và thông tin nhạy cảm." >}}

Nếu task không Running, kiểm tra **Deployments and events**, log CloudWatch, quota Fargate, đường ra NAT, quyền ECR và kiến trúc image.
