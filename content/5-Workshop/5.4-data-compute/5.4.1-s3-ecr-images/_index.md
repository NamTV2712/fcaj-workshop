---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.1-prepare/"]
title: "S3, ECR and ARM64 image build"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

## 1. Verify your S3 bucket

In **S3 → General purpose buckets**, find the `StagingRecordingsBucket` name from the `tina-staging` stack outputs. This bucket was created privately in your account; keep **Block all public access** enabled. Under **Management → Lifecycle rules**, verify the expiration rule for the `runtime-invocations/` prefix. Do not upload private data for screenshots.

{{< workshop-screenshot file="07-s3-lab.jpg" description="Recordings bucket in your lab account, showing Block Public Access enabled and the lifecycle rule." >}}

## 2. Create the remaining ECR repositories

The foundation stack already created `tina-staging/bot`, `tina-staging/runtime`, and `tina-staging/meeting-api`. In CloudShell, create the four additional required repositories:

```bash
for name in terminal gateway admin-api viegem; do
  aws ecr create-repository --region "$AWS_REGION" \
    --repository-name "tina-staging/$name" \
    --image-tag-mutability IMMUTABLE --encryption-configuration encryptionType=AES256
done
```

If a repository already exists in your account, verify its name and permissions, remove it from the loop, and run the command for the remaining ones. Do not change the `tina-staging` prefix: several execution roles in this pinned template version grant read access specifically to this prefix.

> **Fast option (recommended — skip Sections 3, 4, and 5, avoid EC2 OOM / SSM Offline):**
> Instead of launching an EC2 builder to compile Docker images (which requires heavy RAM), run the block below **directly in CloudShell** to copy the prebuilt `linux/arm64` images from GHCR into your ECR under tag `$TINA_TAG` (`ws-v1`), then jump straight to **[5.4.2](../5.4.2-data-secrets/)**:
>
> ```bash
> export AWS_REGION="${AWS_REGION:-us-east-1}"
> export TINA_ACCOUNT="${TINA_ACCOUNT:-$(aws sts get-caller-identity --query Account --output text)}"
> export TINA_TAG="${TINA_TAG:-ws-v1}"
> if [ ! -x /tmp/crane ]; then
>   curl -sSL "https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz" | tar -xz -C /tmp crane
> fi
> ECR_REG="${TINA_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
> aws ecr get-login-password --region "$AWS_REGION" | /tmp/crane auth login "$ECR_REG" -u AWS --password-stdin
> for name in terminal gateway meeting-api admin-api runtime bot viegem; do
>   /tmp/crane copy "ghcr.io/poor-frog/tina-${name}:workshop-arm64" "${ECR_REG}/tina-staging/${name}:${TINA_TAG}"
> done
> ```

## 3. Create an IAM instance profile for the builder (only if building on EC2)

The following commands create a temporary EC2 role with the Systems Manager policy and ECR push permissions scoped to `tina-staging/*` repositories. Run this once in CloudShell using an identity with IAM management permissions:

```bash
cat > "$HOME/tina-workshop/builder-trust.json" <<'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}
EOF
cat > "$HOME/tina-workshop/builder-ecr.json" <<EOF
{"Version":"2012-10-17","Statement":[
  {"Effect":"Allow","Action":"ecr:GetAuthorizationToken","Resource":"*"},
  {"Effect":"Allow","Action":["ecr:DescribeRepositories","ecr:DescribeImages","ecr:BatchCheckLayerAvailability","ecr:InitiateLayerUpload","ecr:UploadLayerPart","ecr:CompleteLayerUpload","ecr:PutImage","ecr:BatchGetImage","ecr:GetDownloadUrlForLayer"],"Resource":"arn:aws:ecr:${AWS_REGION}:${TINA_ACCOUNT}:repository/tina-staging/*"}
]}
EOF
aws iam create-role --role-name tina-workshop-builder-role --assume-role-policy-document "file://$HOME/tina-workshop/builder-trust.json"
aws iam attach-role-policy --role-name tina-workshop-builder-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
aws iam put-role-policy --role-name tina-workshop-builder-role --policy-name TinaEcrPush --policy-document "file://$HOME/tina-workshop/builder-ecr.json"
aws iam create-instance-profile --instance-profile-name tina-workshop-builder-profile
aws iam add-role-to-instance-profile --instance-profile-name tina-workshop-builder-profile --role-name tina-workshop-builder-role
```

If a role or profile with the same name already exists, stop and verify ownership before using it; do not overwrite a role belonging to another system. After creating them, wait for IAM propagation before selecting the profile in EC2.

## 4. Launch an ARM64 build instance in the EC2 Console

1. Go to **EC2 → Instances → Launch instances**. Name it `tina-workshop-builder`.
2. Choose **Amazon Linux 2023**, architecture **64-bit (Arm)**; for example, **`t4g.small`** (Free Plan compatible; larger instances such as `m7g.2xlarge` require a Paid Plan or higher quota). Smaller RAM instances require the 8 GiB swap file in Section 5—or use the **Fast option (`crane copy` in CloudShell)** in Section 2 to avoid running out of memory while building `bot`/`viegem`. This instance incurs charges while running.
3. **Key pair:** choose *Proceed without a key pair*. Under **Network settings**, select the `tina-staging` stack VPC, one public subnet from `PublicSubnetIds`, and enable **Auto-assign public IP**. Create a security group with no inbound rules, keeping outbound rules for Internet access.
4. **Configure storage:** for example, 200 GiB gp3; click the **Advanced** button in the top-right corner of the **Configure storage** panel to enable encryption (**Encrypted → Yes**). Under **Advanced details → IAM instance profile**, select `tina-workshop-builder-profile`; enable **IMDSv2 required** if shown. Click **Launch instance**.
5. Wait until the instance state is Running and Systems Manager detects it. Select the instance → **Connect → Session Manager → Connect**. If the tab cannot connect, verify the IAM profile, SSM Agent, public IP, route to the Internet Gateway, and outbound HTTPS access.

## 5. Build and push images from EC2

Run the commands in this section **inside the EC2 Session Manager session**, not in CloudShell. Add an 8 GiB swap file first to prevent out-of-memory hangs (which cause SSM Agent to go `Offline` while building `bot`/`viegem`), install Docker and Git, then switch to a root shell for this temporary build session:

```bash
sudo fallocate -l 8G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
sudo dnf install -y docker git
sudo systemctl enable --now docker
sudo -i
cd /root
git clone --filter=blob:none https://github.com/poor-frog/TINA.git tina-source
cd tina-source
git fetch origin feat/s3-ephemeral-workspaces
git checkout --detach 7d6bba8109f6eac51c0d8241a7083e3e364cf59d
git rev-parse HEAD
docker buildx version
```

Download the workshop build script: {{< workshop-file path="scripts/tina-ecr-build.sh" label="download tina-ecr-build.sh" >}}, **or** click the **▶ Click to expand...** line below to reveal and paste the block directly into EC2 to create `/root/tina-ecr-build.sh` without downloading an external file:

> **Fast deployment tip:** If you prefer not to build Docker images on EC2, see [5.4A Quick Deploy with 1 CloudFormation Stack](../../5.4-full-cloudformation/) to copy the prebuilt set of 15 `linux/arm64` images (including VieGem and Voice) directly from GHCR into ECR right from CloudShell.

<details>
<summary style="cursor:pointer;font-weight:600;color:#0073bb;text-decoration:underline;">▶ Click to expand &amp; copy the complete <code>/root/tina-ecr-build.sh</code> script</summary>

```bash
cat > /root/tina-ecr-build.sh <<'EOF'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
readonly EXPECTED_REVISION=7d6bba8109f6eac51c0d8241a7083e3e364cf59d
SOURCE_DIR="$PWD"
REGION="${AWS_REGION:-us-east-1}"
readonly PREFIX=tina-staging
TAG="${TINA_IMAGE_TAG:-ws-$(date -u +%Y%m%d%H%M%S)}"
PLAN_ONLY=0; WITH_VIEGEM=0; WITH_ADDONS=0; WITH_FULL=0
while (($#)); do
  case "$1" in
    --source) SOURCE_DIR="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --with-viegem) WITH_VIEGEM=1; shift ;;
    --with-addons) WITH_ADDONS=1; shift ;;
    --full) WITH_FULL=1; WITH_ADDONS=1; WITH_VIEGEM=1; shift ;;
    --plan) PLAN_ONLY=1; shift ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
SOURCE_DIR="$(cd -- "$SOURCE_DIR" && pwd -P)"
REVISION="$(git -C "$SOURCE_DIR" rev-parse HEAD)"
[[ "$REVISION" == "$EXPECTED_REVISION" ]] || { echo "Wrong source revision: expected $EXPECTED_REVISION, found $REVISION." >&2; exit 1; }
images=(terminal gateway meeting-api admin-api runtime bot)
((WITH_ADDONS)) && images+=(agent-api agent-reach agent-worker mcp flows)
((WITH_VIEGEM)) && images+=(viegem)
printf 'Revision: %s\nRegion: %s\nECR prefix: %s\nTag: %s\n' "$REVISION" "$REGION" "$PREFIX" "$TAG"
((PLAN_ONLY)) && { echo 'Plan only: no image was built or pushed.'; exit 0; }
ACCOUNT="$(aws sts get-caller-identity --region "$REGION" --query Account --output text --no-cli-pager)"
REGISTRY="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf -- "$WORK_DIR"' EXIT
mkdir -p "$WORK_DIR/source"
git -C "$SOURCE_DIR" archive --format=tar "$REVISION" | tar --exclude='.env' --exclude='.env.*' --exclude='.env.keys' -xf - -C "$WORK_DIR/source"
SRC="$WORK_DIR/source"
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$REGISTRY" >/dev/null
push_image() {
  local name="$1" dockerfile="$2" context="$3"; shift 3
  local image="$REGISTRY/$PREFIX/$name:$TAG"
  docker build --platform linux/arm64 --file "$SRC/$dockerfile" --tag "$image" "$@" "$SRC/$context"
  docker push "$image"
}
if ((WITH_FULL)); then
  push_image terminal clients/terminal/Dockerfile . --build-arg NEXT_PUBLIC_TERMINAL_MODE=workspace-pilot
else
  push_image terminal clients/terminal/Dockerfile . --build-arg NEXT_PUBLIC_TERMINAL_MODE=meetings
fi
push_image gateway core/gateway/services/gateway/Dockerfile .
push_image meeting-api core/meetings/services/meeting-api/Dockerfile .
push_image admin-api core/identity/services/admin-api/Dockerfile core/identity/services/admin-api
if ((WITH_FULL)); then
  docker build --platform linux/arm64 --file "$SRC/core/runtime/Dockerfile" --tag tina-workshop/runtime-base "$SRC/core/runtime"
  push_image runtime deploy/aws/workspace-pilot.Dockerfile . --target runtime --build-arg RUNTIME_BASE=tina-workshop/runtime-base --build-arg AGENT_BASE=tina-workshop/runtime-base --build-arg WORKER_BASE=tina-workshop/runtime-base
else
  push_image runtime core/runtime/Dockerfile core/runtime
fi
docker build --platform linux/arm64 --file "$SRC/core/meetings/modules/join/Dockerfile.env" --tag tina/meet-join-env:dev "$SRC/core/meetings/modules/join"
push_image bot core/meetings/services/bot/Dockerfile . --build-arg "TINA_IMAGE_VERSION=$REVISION"
if ((WITH_ADDONS)); then
  if ((WITH_FULL)); then
    docker build --platform linux/arm64 --file "$SRC/core/agent/services/agent-api/Dockerfile" --tag tina/v012-agent-api:staging-voice "$SRC"
    docker build --platform linux/arm64 --file "$SRC/deploy/aws/voice-worker.Dockerfile" --tag tina-workshop/agent-voice "$SRC"
    push_image agent-api deploy/aws/workspace-pilot.Dockerfile . --target agent --build-arg AGENT_BASE=tina-workshop/agent-voice --build-arg RUNTIME_BASE=tina-workshop/agent-voice --build-arg WORKER_BASE=tina-workshop/agent-voice
  else
    push_image agent-api core/agent/services/agent-api/Dockerfile .
  fi
  push_image agent-reach deploy/agent-reach/Dockerfile deploy/agent-reach
  if ((WITH_FULL)); then
    docker build --platform linux/arm64 --file "$SRC/core/agent/worker/Dockerfile" --tag tina-workshop/worker-base "$SRC"
    push_image agent-worker deploy/aws/workspace-pilot.Dockerfile . --target worker --build-arg WORKER_BASE=tina-workshop/worker-base --build-arg RUNTIME_BASE=tina-workshop/worker-base --build-arg AGENT_BASE=tina-workshop/worker-base
  else
    push_image agent-worker core/agent/worker/Dockerfile .
  fi
  push_image mcp core/meetings/services/mcp/Dockerfile core/meetings/services/mcp
  push_image flows core/flows/Dockerfile .
fi
if ((WITH_VIEGEM)); then
  ASSETS="${TINA_VIEGEM_CACHE:-$HOME/.cache/tina-workshop/viegem-fsmn}"
  mkdir -p "$ASSETS"
  docker build --platform linux/arm64 --build-arg TORCH_VARIANT=cpu --file "$SRC/deploy/transcription/viegem/Dockerfile" --tag tina/v012-viegem:staging-cpu-base "$SRC"
  docker run --rm --platform linux/arm64 --mount "type=bind,src=$ASSETS,dst=/assets" tina/v012-viegem:staging-cpu-base python install-models.py --directory /assets
  push_image viegem deploy/aws/viegem.Dockerfile deploy/aws --build-context "viegem_assets=$ASSETS"
fi
for name in "${images[@]}"; do
  digest="$(aws ecr describe-images --region "$REGION" --repository-name "$PREFIX/$name" --image-ids "imageTag=$TAG" --query 'imageDetails[0].imageDigest' --output text --no-cli-pager)"
  printf '%-14s %s/%s/%s@%s\n' "$name" "$REGISTRY" "$PREFIX" "$name" "$digest"
done
EOF
chmod +x /root/tina-ecr-build.sh
```

</details>

Once `/root/tina-ecr-build.sh` is in place, run a dry-run build plan (`--plan`):

```bash
export AWS_REGION=us-east-1
export TINA_IMAGE_TAG=ws-v1
bash /root/tina-ecr-build.sh --source /root/tina-source --region "$AWS_REGION" --plan
```

Verify the source revision, Region, repository prefix, and tag. The `--plan` flag does not build or push anything. To test transcription with VieGem under non-commercial license terms, also build the model image with `--with-viegem`. The VieGem model is licensed under **CC-BY-NC-SA-4.0** and the Gemma terms; review the [model card](https://huggingface.co/5CD-AI/VieGem-ASR) and [license notes](https://github.com/poor-frog/TINA/blob/7d6bba8109f6eac51c0d8241a7083e3e364cf59d/deploy/transcription/viegem/README.md) before using it. If those terms do not fit your use case, omit `--with-viegem`, skip the VieGem stack, and leave the transcription parameters empty in the core stack.

```bash
bash /root/tina-ecr-build.sh --source /root/tina-source --region "$AWS_REGION" --with-viegem
```

The build downloads dependencies and model files from the Internet, which can take significant time and disk space. With the option above, the script builds 6 application images plus 1 VieGem image, pushes them to ECR in the **account attached to the instance role**, and prints their digests. The source is archived from the pinned commit; the script never copies local `.env` files. If the command fails, check the first error; when retrying after a partial push, set `export TINA_IMAGE_TAG=ws-v2` because tags are immutable, and update `TINA_TAG` accordingly in CloudShell.

In **ECR → Private repositories**, open `tina-staging/terminal` or `tina-staging/bot` and verify the tag and digest:

{{< workshop-screenshot file="08-ecr-image.png" description="Your ECR repository showing the image tag and digest after the build." >}}

After confirming that all required images are present, **terminate the EC2 builder** if you no longer need it; ECR retains the pushed images. Do not delete volumes or resources belonging to other instances.
