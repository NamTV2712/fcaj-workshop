---
title: "VieGem tùy chọn và core"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.4.3.3 </b> "
---

## 1. Tùy chọn: tạo VieGem ASR

Chỉ chạy phần này nếu đã build `viegem` bằng `--with-viegem`, việc sử dụng phù hợp điều khoản model và bạn chấp nhận chi phí. VieGem dùng Fargate **CPU**, mỗi task 2 vCPU/8 GiB; template mặc định `DesiredCount=0`, vì vậy để chạy thử cần đặt `1`.

Trong CloudShell, với biến từ trang Runtime vẫn còn:

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-viegem --template-file "$TINA_SRC/deploy/aws/staging-viegem.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "AppSecurityGroupId=$APP_SG" "ServiceNamespaceId=$NAMESPACE_ID" \
    "VieGemImage=$(image viegem)" "VieGemRepositoryArn=$(repoarn viegem)" DesiredCount=1
```

Chờ task chạy ổn định rồi lấy URL và secret ARN, không lấy giá trị token:

```bash
TRANSCRIPTION_URL="$(stackout tina-ws-viegem WorkerUrl)"
TRANSCRIPTION_TOKEN_ARN="$(stackout tina-ws-viegem WorkerTokenArn)"
```

Nếu không triển khai VieGem, dùng hai giá trị rỗng dưới đây. Website có thể được triển khai nhưng **chưa có dịch vụ phiên âm**; không đánh dấu bước transcript đã đạt.

```bash
TRANSCRIPTION_URL=''
TRANSCRIPTION_TOKEN_ARN=''
```

{{< workshop-screenshot file="24-viegem-service.png" description="Nếu dùng VieGem, chụp ECS service và số task running; không hiển thị token." >}}

## 2. Tạo core: admin API, meeting API và gateway

Trong cùng CloudShell:

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

Template có init/migration cho database và dùng secret trong Secrets Manager. Chờ stack và ECS service ổn định; nếu lỗi migration, kiểm tra CloudWatch logs của task core, kết nối RDS/Valkey, secret ARN và security group trước. Không đăng nội dung log có dữ liệu nhạy cảm.

Để dùng cho Terminal, lấy **ARN** của secret nội bộ được stack tạo:

```bash
INTERNAL_SECRET_ARN="$(aws cloudformation describe-stack-resource --region "$AWS_REGION" \
  --stack-name tina-ws-core --logical-resource-id InternalSecret \
  --query 'StackResourceDetail.PhysicalResourceId' --output text)"
```

Template này chưa cấu hình agent, voice hay TTS; các tham số đó giữ mặc định rỗng.
