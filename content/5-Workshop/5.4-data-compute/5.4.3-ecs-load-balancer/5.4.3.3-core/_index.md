---
title: "Optional VieGem and core"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.4.3.3 </b> "
---

## 1. Optional: deploy VieGem ASR

Run this section only if you built `viegem` with `--with-viegem`, your usage complies with the model license terms, and you accept the running cost. VieGem runs on Fargate **CPU** (2 vCPU / 8 GiB per task); the template defaults to `DesiredCount=0`, so set it to `1` for testing.

In CloudShell, with the variables from the Runtime page still set:

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-viegem --template-file "$TINA_SRC/deploy/aws/staging-viegem.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "AppSecurityGroupId=$APP_SG" "ServiceNamespaceId=$NAMESPACE_ID" \
    "VieGemImage=$(image viegem)" "VieGemRepositoryArn=$(repoarn viegem)" DesiredCount=1
```

Wait for the task to stabilize, then retrieve the URL and secret ARN (not the token value):

```bash
TRANSCRIPTION_URL="$(stackout tina-ws-viegem WorkerUrl)"
TRANSCRIPTION_TOKEN_ARN="$(stackout tina-ws-viegem WorkerTokenArn)"
```

If you are not deploying VieGem, set both values to empty strings below. The website can still be deployed, but **no transcription service will be configured**; do not mark the transcript validation step as passed.

```bash
TRANSCRIPTION_URL=''
TRANSCRIPTION_TOKEN_ARN=''
```

{{< workshop-screenshot file="24-viegem-service.png" description="If using VieGem, capture the ECS service and running task count; do not expose the token." >}}

## 2. Deploy core: admin API, meeting API, and gateway

In the same CloudShell session:

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-core --template-file "$TINA_SRC/deploy/aws/staging-core.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "AppSecurityGroupId=$APP_SG" \
    "RuntimeClientSecurityGroupId=$(stackout tina-ws-runtime RuntimeClientSecurityGroupId)" \
    "ServiceNamespaceId=$NAMESPACE_ID" "RuntimeUrl=$(stackout tina-ws-runtime RuntimeUrl)" \
    "AdminImage=$(image admin-api)" "MeetingImage=$(image meeting-api)" "GatewayImage=$(image gateway)" \
    "PostgresHost=$(stackout tina-ws-data PostgresHost)" \
    "PostgresSecretArn=$(stackout tina-ws-data PostgresSecretArn)" \
    "ValkeyHost=$(stackout tina-ws-data ValkeyHost)" \
    "ValkeySecretArn=$(stackout tina-ws-data ValkeySecretArn)" \
    "RecordingsBucket=$BUCKET" "TranscriptionUrl=$TRANSCRIPTION_URL" \
    "TranscriptionTokenArn=$TRANSCRIPTION_TOKEN_ARN"
```

The template runs database init/migrations and reads credentials from Secrets Manager. Wait for the stack and ECS services to stabilize; if migrations fail, check the core task's CloudWatch logs, RDS/Valkey connectivity, secret ARNs, and security groups first. Never publish log excerpts containing sensitive data.

For the Terminal stack, retrieve the **ARN** of the internal secret created by this stack:

```bash
INTERNAL_SECRET_ARN="$(aws cloudformation describe-stack-resource --region "$AWS_REGION" \
  --stack-name tina-ws-core --logical-resource-id InternalSecret \
  --query 'StackResourceDetail.PhysicalResourceId' --output text)"
```

This template does not configure agent, voice, or TTS services yet; those parameters remain empty by default.
