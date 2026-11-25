---
title: "Bot and Fargate Runtime"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.4.3.2 </b> "
---

## 1. Create the bot task definition

In CloudShell:

```bash
CLUSTER="$(stackout tina-staging ClusterName)"
BUCKET="$(stackout tina-staging StagingRecordingsBucket)"
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-bot --template-file "$TINA_SRC/deploy/aws/ecs-bot.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "BotImage=$(image bot)" \
    "BotRepositoryArn=$(repoarn bot)" "InvocationBucket=$BUCKET" ProbeInvocation=false
```

This template creates the bot task definition and IAM roles. Bot tasks are launched on demand by Runtime when a meeting is requested; having no always-on bot service is expected.

## 2. Deploy Runtime

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

Wait for the stack to succeed. This template also creates the `tina-staging.local` Cloud Map private namespace in your VPC; do not create a duplicate namespace in the same VPC. Retrieve the **namespace ID** for the subsequent stacks:

```bash
NAMESPACE_ID="$(aws cloudformation describe-stack-resource --region "$AWS_REGION" \
  --stack-name tina-ws-runtime --logical-resource-id DiscoveryNamespace \
  --query 'StackResourceDetail.PhysicalResourceId' --output text)"
printf 'Namespace ID: %s\n' "$NAMESPACE_ID"
```

Go to **ECS → Clusters**, select the cluster from `ClusterName`, and verify that the Runtime service has a Running task. After deploying core and terminal, return here to capture the full service list:

{{< workshop-screenshot file="12-ecs-services.png" description="ECS services after deploying Runtime, core, and terminal, showing desired and running tasks." >}}

Open the Runtime task → **Containers** and inspect its status; capture only sections that do not expose tokens or sensitive environment variables:

{{< workshop-screenshot file="13-ecs-task.png" description="Runtime task and container status; redact environment variables and sensitive details." >}}

If the task does not reach Running, check **Deployments and events**, CloudWatch logs, Fargate quotas, NAT egress routing, ECR permissions, and image architecture.
