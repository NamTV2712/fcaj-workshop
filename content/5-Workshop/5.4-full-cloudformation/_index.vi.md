---
title: "Triển khai bằng một CloudFormation"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4A </b> "
---

## Tổng quan lộ trình triển khai nhanh (5 lệnh trên CloudShell)

{{< workshop-file path="cloudformation/tina-full.yml" label="Tải tina-full.yml" >}}

![Sơ đồ kiến trúc TINA trên AWS](/images/5-Workshop/tina/tina-aws-architecture.png)

Template `tina-full.yml` dựng toàn bộ hạ tầng TINA trong **một stack duy nhất**: VPC 2 AZ, NAT Gateway, S3, CloudFront + WAF, ALB nội bộ, RDS PostgreSQL, ElastiCache Valkey, ECS Fargate (ARM64), Terminal, Bot, Runtime, **VieGem ASR**, Agent API, Agent Reach, MCP, Flows và kho workspace.

Toàn bộ quá trình triển khai được chia thành **5 lệnh ngắn chạy tuần tự trên AWS CloudShell (`us-east-1`)** — chạy xong lệnh nào mới chạy tiếp lệnh sau, không cần tạo EC2 builder hay tự build Docker:

1. **Lệnh 1**: Chuẩn bị biến môi trường, role ECS và công cụ `crane`.
2. **Lệnh 2**: Copy 12 image `linux/arm64` dựng sẵn (gồm **VieGem**) từ GHCR vào ECR của bạn.
3. **Lệnh 3**: Lấy Prefix List (`CloudFront`, `S3`) và upload `tina-full.yml` lên S3 tạm.
4. **Lệnh 4**: Tạo stack `tina-workshop-full`, chờ hoàn tất và lấy `WebsiteUrl`.
5. **Lệnh 5**: Gắn Google OAuth của riêng bạn để đăng nhập vào web.

> **Lưu ý:** Thực hiện ở Region **`us-east-1`**, tránh chạy đè trên tài khoản đã có sẵn stack `tina-staging-*`. Nếu dùng tài khoản **AWS Free Plan**, kiểm tra trước hạn mức RDS (Free Plan giới hạn số lượng RDS instance — nếu đã có sẵn RDS khác có thể gặp `ServiceLimitExceeded`). Model VieGem dùng giấy phép phi thương mại **CC-BY-NC-SA-4.0** và điều khoản Gemma ([model card](https://huggingface.co/5CD-AI/VieGem-ASR)).

---

## Lệnh 1 — Chuẩn bị CloudShell, role ECS và đăng nhập ECR

Mở **AWS CloudShell** tại Region **`us-east-1`**, dán lệnh sau và nhấn Enter:

```bash
export AWS_REGION=us-east-1
export AWS_PAGER=''
export STACK_NAME=tina-workshop-full
export AWS_ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
export ECR_REG="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# Tạo service-linked role cho ECS (chỉ cần cho tài khoản chưa từng chạy ECS)
aws iam get-role --role-name AWSServiceRoleForECS >/dev/null 2>&1 \
  || aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com

# Tải công cụ crane vào /tmp để copy image trực tiếp trên CloudShell (không cần Docker)
if [ ! -x /tmp/crane ]; then
  curl -sSL "https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz" \
    | tar -xz -C /tmp crane
fi

# Đăng nhập crane vào ECR của tài khoản bạn
aws ecr get-login-password --region "$AWS_REGION" \
  | /tmp/crane auth login "$ECR_REG" -u AWS --password-stdin

echo "OK: Account=$AWS_ACCOUNT | ECR=$ECR_REG"
```

**Giải thích:** Lệnh này tự lấy mã tài khoản AWS (`AWS_ACCOUNT`), đảm bảo có `AWSServiceRoleForECS`, tải binary `crane` (~8 MB) và đăng nhập sẵn vào ECR. Khi thấy dòng `OK: Account=...` là xong Lệnh 1.

---

## Lệnh 2 — Copy 12 image ARM64 (gồm VieGem) từ GHCR vào ECR

Dán lệnh sau để tạo 12 repository `tina-staging/*` trong ECR và copy toàn bộ 12 image `linux/arm64` từ `ghcr.io/poor-frog/tina-*:workshop-arm64` sang ECR của bạn (mất khoảng 1–3 phút):

```bash
GHCR_PREFIX="ghcr.io/poor-frog"
GHCR_TAG="workshop-arm64"
SERVICES=(terminal gateway meeting-api admin-api runtime bot agent-api agent-reach agent-worker mcp flows viegem)
: > /tmp/tina-digests.env

for name in "${SERVICES[@]}"; do
  aws ecr describe-repositories --region "$AWS_REGION" --repository-names "tina-staging/$name" >/dev/null 2>&1 \
    || aws ecr create-repository --region "$AWS_REGION" --repository-name "tina-staging/$name" \
         --image-tag-mutability IMMUTABLE --encryption-configuration encryptionType=AES256 >/dev/null

  echo ">>> Copying $name..."
  /tmp/crane copy "${GHCR_PREFIX}/tina-${name}:${GHCR_TAG}" "${ECR_REG}/tina-staging/${name}:${GHCR_TAG}"

  DIGEST="$(aws ecr describe-images --region "$AWS_REGION" --repository-name "tina-staging/$name" \
    --image-ids "imageTag=${GHCR_TAG}" --query 'imageDetails[0].imageDigest' --output text)"
  VAR_NAME="$(echo "$name" | tr '[:lower:]-' '[:upper:]_')_DIGEST"
  echo "export ${VAR_NAME}=${DIGEST}" >> /tmp/tina-digests.env
done

source /tmp/tina-digests.env
echo "=== Đã lưu đủ 12 digest vào /tmp/tina-digests.env ==="
cat /tmp/tina-digests.env
```

**Giải thích:** Thay vì phải tạo EC2 ARM64 và tự build Docker trong 1–2 tiếng, `crane copy` sao chép thẳng image từ GHCR sang ECR và lưu đủ 12 chuỗi `sha256:...` vào `/tmp/tina-digests.env`. Đợi in ra đủ 12 dòng `export ..._DIGEST=sha256:...` rồi chuyển sang Lệnh 3.

<details>
<summary>Tùy chọn nâng cao: tự build 12 image từ source bằng EC2 ARM64 (nếu không dùng GHCR)</summary>

Nếu muốn tự build từ commit `7d6bba8109f6eac51c0d8241a7083e3e364cf59d`, xem hướng dẫn tạo EC2 ARM64 và script inline `/root/tina-ecr-build.sh` tại [5.4.1 S3, ECR và build image ARM64](../5.4-data-compute/5.4.1-s3-ecr-images/) rồi chạy với cờ `--full`.

</details>

---

## Lệnh 3 — Lấy Prefix List & upload `tina-full.yml` lên S3 tạm

Tải file `tina-full.yml` bằng nút tải ở đầu trang, bấm **Actions → Upload file** trên CloudShell để đẩy lên thư mục gốc `~/` (tức `~/tina-full.yml`), sau đó chạy lệnh sau:

```bash
CF_PL="$(aws ec2 describe-managed-prefix-lists --region "$AWS_REGION" \
  --filters Name=prefix-list-name,Values=com.amazonaws.global.cloudfront.origin-facing \
  --query 'PrefixLists[0].PrefixListId' --output text)"
S3_PL="$(aws ec2 describe-managed-prefix-lists --region "$AWS_REGION" \
  --filters Name=prefix-list-name,Values=com.amazonaws.us-east-1.s3 \
  --query 'PrefixLists[0].PrefixListId' --output text)"

TPL_BUCKET="tina-cfn-tpl-${AWS_ACCOUNT}-${AWS_REGION}"
aws s3 mb "s3://${TPL_BUCKET}" --region "$AWS_REGION" 2>/dev/null || true
aws s3 cp ~/tina-full.yml "s3://${TPL_BUCKET}/tina-full.yml" --region "$AWS_REGION"

echo "OK: CF_PL=$CF_PL | S3_PL=$S3_PL | TPL=https://${TPL_BUCKET}.s3.${AWS_REGION}.amazonaws.com/tina-full.yml"
```

**Giải thích:**
- `CF_PL` và `S3_PL` là 2 Managed Prefix List ID của AWS tại `us-east-1`, dùng để khóa Security Group chỉ cho phép lưu lượng từ CloudFront và S3.
- Do `tina-full.yml` (~151 KB) lớn hơn giới hạn 51 KB inline của CloudFormation, cần upload lên S3 tạm để CloudFormation đọc qua `--template-url`.

---

## Lệnh 4 — Tạo stack `tina-workshop-full` và lấy `WebsiteUrl`

Dán lệnh sau để khởi tạo toàn bộ stack và chờ AWS dựng xong (RDS + Valkey + CloudFront + ECS mất khoảng **12–18 phút**):

```bash
source /tmp/tina-digests.env

aws cloudformation create-stack --region "$AWS_REGION" \
  --stack-name "$STACK_NAME" \
  --template-url "https://${TPL_BUCKET}.s3.${AWS_REGION}.amazonaws.com/tina-full.yml" \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameters \
    ParameterKey=CloudFrontOriginPrefixListId,ParameterValue="$CF_PL" \
    ParameterKey=S3PrefixListId,ParameterValue="$S3_PL" \
    ParameterKey=WorkspaceOwnerIds,ParameterValue="" \
    ParameterKey=GoogleSecretArn,ParameterValue="" \
    ParameterKey=EnableVoice,ParameterValue="false" \
    ParameterKey=VoicePilotRoom,ParameterValue="" \
    ParameterKey=BotDigest,ParameterValue="$BOT_DIGEST" \
    ParameterKey=RuntimeDigest,ParameterValue="$RUNTIME_DIGEST" \
    ParameterKey=AdminDigest,ParameterValue="$ADMIN_API_DIGEST" \
    ParameterKey=MeetingDigest,ParameterValue="$MEETING_API_DIGEST" \
    ParameterKey=GatewayDigest,ParameterValue="$GATEWAY_DIGEST" \
    ParameterKey=TerminalDigest,ParameterValue="$TERMINAL_DIGEST" \
    ParameterKey=AgentApiDigest,ParameterValue="$AGENT_API_DIGEST" \
    ParameterKey=AgentWorkerDigest,ParameterValue="$AGENT_WORKER_DIGEST" \
    ParameterKey=AgentReachDigest,ParameterValue="$AGENT_REACH_DIGEST" \
    ParameterKey=McpDigest,ParameterValue="$MCP_DIGEST" \
    ParameterKey=FlowsDigest,ParameterValue="$FLOWS_DIGEST" \
    ParameterKey=VieGemDigest,ParameterValue="$VIEGEM_DIGEST" \
    ParameterKey=VieNeuDigest,ParameterValue="" \
    ParameterKey=LiveKitDigest,ParameterValue="" \
    ParameterKey=LiveKitAgentDigest,ParameterValue=""

echo "Đang chờ CloudFormation dựng xong (~12-18 phút)..."
aws cloudformation wait stack-create-complete --region "$AWS_REGION" --stack-name "$STACK_NAME"

WEBSITE_URL="$(aws cloudformation describe-stacks --region "$AWS_REGION" \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='WebsiteUrl'].OutputValue" --output text)"
echo "WebsiteUrl: $WEBSITE_URL"
curl -sS "${WEBSITE_URL}/edge-health" && echo ""
```

**Giải thích:**
- Lần tạo đầu để trống `GoogleSecretArn` vì bạn cần `WebsiteUrl` sinh ra từ CloudFront để khai báo Redirect URI bên Google.
- Khi xong, `curl .../edge-health` sẽ in **`TINA_EDGE_READY`** và bạn mở `WebsiteUrl` trên trình duyệt sẽ thấy trang đầu của TINA.

{{< workshop-screenshot file="26-cloudformation-full.png" description="CloudFormation stack một file, danh sách tham số đã che account ID và ARN." >}}

---

## Lệnh 5 — Gắn Google OAuth của riêng bạn để đăng nhập web

1. Vào [Google Cloud Console](https://console.cloud.google.com/) → **Google Auth Platform → Clients → Create client → Web application**.
2. Thêm **Authorized redirect URI** theo đúng `WebsiteUrl` ở Lệnh 4:
   `https://<domain-cloudfront-cua-ban>/api/auth/callback/google`
   Lưu để lấy `Client ID` và `Client secret` (nếu app ở chế độ **Testing**, thêm Gmail của bạn vào **Test users**).
3. Quay lại **CloudShell**, thay `DAN_GOOGLE_CLIENT_ID` và `DAN_GOOGLE_CLIENT_SECRET` rồi chạy lệnh cuối:

```bash
umask 077
GOOGLE_JSON="$(mktemp)"
cat > "$GOOGLE_JSON" <<'EOF'
{"client_id":"DAN_GOOGLE_CLIENT_ID","client_secret":"DAN_GOOGLE_CLIENT_SECRET"}
EOF

GOOGLE_SECRET_ARN="$(aws secretsmanager create-secret --region "$AWS_REGION" \
  --name "${STACK_NAME}-google-oauth" --secret-string "file://$GOOGLE_JSON" \
  --query ARN --output text)"
rm -f -- "$GOOGLE_JSON"

aws cloudformation update-stack --region "$AWS_REGION" \
  --stack-name "$STACK_NAME" \
  --use-previous-template \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameters \
    ParameterKey=CloudFrontOriginPrefixListId,UsePreviousValue=true \
    ParameterKey=S3PrefixListId,UsePreviousValue=true \
    ParameterKey=WorkspaceOwnerIds,UsePreviousValue=true \
    ParameterKey=GoogleSecretArn,ParameterValue="$GOOGLE_SECRET_ARN" \
    ParameterKey=EnableVoice,UsePreviousValue=true \
    ParameterKey=VoicePilotRoom,UsePreviousValue=true \
    ParameterKey=BotDigest,UsePreviousValue=true \
    ParameterKey=RuntimeDigest,UsePreviousValue=true \
    ParameterKey=AdminDigest,UsePreviousValue=true \
    ParameterKey=MeetingDigest,UsePreviousValue=true \
    ParameterKey=GatewayDigest,UsePreviousValue=true \
    ParameterKey=TerminalDigest,UsePreviousValue=true \
    ParameterKey=AgentApiDigest,UsePreviousValue=true \
    ParameterKey=AgentWorkerDigest,UsePreviousValue=true \
    ParameterKey=AgentReachDigest,UsePreviousValue=true \
    ParameterKey=McpDigest,UsePreviousValue=true \
    ParameterKey=FlowsDigest,UsePreviousValue=true \
    ParameterKey=VieGemDigest,UsePreviousValue=true \
    ParameterKey=VieNeuDigest,UsePreviousValue=true \
    ParameterKey=LiveKitDigest,UsePreviousValue=true \
    ParameterKey=LiveKitAgentDigest,UsePreviousValue=true

aws cloudformation wait stack-update-complete --region "$AWS_REGION" --stack-name "$STACK_NAME"
echo "HOÀN TẤT! Mở $WEBSITE_URL để đăng nhập bằng Google."
```

**Giải thích:** Lệnh tạo secret chứa thông tin Google OAuth trong Secrets Manager (và xóa ngay file tạm trên CloudShell), sau đó cập nhật container `Terminal` nhận `GOOGLE_CLIENT_ID` và `GOOGLE_CLIENT_SECRET`. Đợi ~1–2 phút cho Terminal khởi động lại là đăng nhập Google sử dụng đầy đủ web, bot và VieGem.

---

## Voice và dọn dẹp tài nguyên khi kết thúc

- **Voice (tùy chọn)**: 3 image `linux/arm64` của nhánh Voice cũng đã có sẵn trên GHCR (`ghcr.io/poor-frog/tina-livekit:workshop-arm64`, `tina-livekit-agent:workshop-arm64`, `tina-vieneu:workshop-arm64`). Nếu muốn bật Voice, copy thêm 3 image này vào `tina-staging/{livekit,livekit-agent,vieneu}` trong ECR rồi cập nhật stack với `EnableVoice=true`, `VoicePilotRoom` và 3 digest tương ứng (`LiveKitDigest`, `LiveKitAgentDigest`, `VieNeuDigest`).
- **Dọn dẹp**: chạy `aws cloudformation delete-stack --stack-name tina-workshop-full --region us-east-1`, sau đó kiểm tra và xóa các tài nguyên giữ lại (`DeletionPolicy: Retain`: bucket S3, KMS key, snapshot RDS) theo [5.6 Dọn dẹp và bằng chứng](../5.6-cleanup-evidence/).
