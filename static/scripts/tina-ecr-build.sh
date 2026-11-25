#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Build TINA's AWS-pilot source into the learner's own private ECR repositories.
set -Eeuo pipefail

readonly EXPECTED_REVISION=7d6bba8109f6eac51c0d8241a7083e3e364cf59d
SOURCE_DIR="$PWD"
REGION="${AWS_REGION:-us-east-1}"
readonly PREFIX=tina-staging
TAG="${TINA_IMAGE_TAG:-ws-$(date -u +%Y%m%d%H%M%S)}"
PLAN_ONLY=0
WITH_VIEGEM=0
WITH_ADDONS=0
WITH_FULL=0

usage() {
  cat <<'EOF'
Usage: tina-ecr-build.sh --source /path/to/TINA [--region us-east-1]
                         [--with-viegem] [--with-addons] [--full] [--plan]

Run on a Linux ARM64 builder with Docker, BuildKit, AWS CLI, Git and an IAM role
allowed to push to the private ECR repositories. Create the repositories first.
--plan only prints the build plan; it does not call AWS or Docker.
--with-viegem downloads the model assets and builds the non-commercial ASR image.
--with-addons also builds the optional agent, MCP and flows images.
--full builds workspace-pilot, agent, MCP, flows and VieGem images for tina-full.yml.
Place tina-cognito.patch next to this script when using --full.
The prefix tina-staging is required by the pinned CloudFormation templates.
TINA_IMAGE_TAG can override the image tag.
EOF
}

while (($#)); do
  case "$1" in
    --source) (($# >= 2)) || { usage >&2; exit 2; }; SOURCE_DIR="$2"; shift 2 ;;
    --region) (($# >= 2)) || { usage >&2; exit 2; }; REGION="$2"; shift 2 ;;
    --with-viegem) WITH_VIEGEM=1; shift ;;
    --with-addons) WITH_ADDONS=1; shift ;;
    --full) WITH_FULL=1; WITH_ADDONS=1; WITH_VIEGEM=1; shift ;;
    --plan) PLAN_ONLY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ "$PREFIX" =~ ^[a-z0-9]+([._/-][a-z0-9]+)*$ ]] || { echo 'Invalid ECR prefix.' >&2; exit 2; }
[[ "$TAG" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$ ]] || { echo 'Invalid image tag.' >&2; exit 2; }
command -v git >/dev/null || { echo 'Git is required.' >&2; exit 1; }
SOURCE_DIR="$(cd -- "$SOURCE_DIR" && pwd -P)"
REVISION="$(git -C "$SOURCE_DIR" rev-parse HEAD)"
[[ "$REVISION" == "$EXPECTED_REVISION" ]] || {
  echo "Wrong source revision: expected $EXPECTED_REVISION, found $REVISION." >&2
  exit 1
}

images=(terminal gateway meeting-api admin-api runtime bot)
if ((WITH_ADDONS)); then images+=(agent-api agent-reach agent-worker mcp flows); fi
if ((WITH_VIEGEM)); then images+=(viegem); fi
printf 'Revision: %s\nRegion: %s\nECR prefix: %s\nTag: %s\n' "$REVISION" "$REGION" "$PREFIX" "$TAG"
printf 'Repositories to create: '; printf '%s ' "${images[@]/#/$PREFIX/}"; printf '\n'
if ((PLAN_ONLY)); then
  echo 'Plan only: no image was built, pushed, or authenticated.'
  exit 0
fi

[[ "$(uname -m)" == 'aarch64' || "$(uname -m)" == 'arm64' ]] || {
  echo 'Use a Linux ARM64 builder for these ARM64 Fargate task definitions.' >&2; exit 1;
}
for cmd in aws docker tar mktemp; do
  command -v "$cmd" >/dev/null || { echo "Missing command: $cmd" >&2; exit 1; }
done
docker info >/dev/null
docker buildx version >/dev/null
ACCOUNT="$(aws sts get-caller-identity --region "$REGION" --query Account --output text --no-cli-pager)"
[[ "$ACCOUNT" =~ ^[0-9]{12}$ ]] || { echo 'Could not determine the AWS account.' >&2; exit 1; }
REGISTRY="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"
for name in "${images[@]}"; do
  aws ecr describe-repositories --region "$REGION" --repository-names "$PREFIX/$name" --no-cli-pager >/dev/null || {
    echo "Create the private ECR repository $PREFIX/$name first." >&2; exit 1;
  }
done

umask 077
TEMP_BASE="$(cd -- "${TMPDIR:-/tmp}" && pwd -P)"
WORK_DIR="$(mktemp -d "$TEMP_BASE/tina-workshop-build.XXXXXXXX")"
cleanup() {
  case "$WORK_DIR" in "$TEMP_BASE"/tina-workshop-build.*) rm -rf -- "$WORK_DIR" ;; esac
}
trap cleanup EXIT
mkdir -p "$WORK_DIR/source" "$WORK_DIR/docker-config"
# Archive only the pinned tracked commit and exclude all env/key files.
git -C "$SOURCE_DIR" archive --format=tar "$REVISION" |
  tar --exclude='.env' --exclude='.env.*' --exclude='.env.keys' -xf - -C "$WORK_DIR/source"
SRC="$WORK_DIR/source"
if ((WITH_FULL)); then
  SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
  git -C "$SRC" apply --no-index "$SCRIPT_DIR/tina-cognito.patch"
fi
export DOCKER_CONFIG="$WORK_DIR/docker-config" DOCKER_BUILDKIT=1 AWS_PAGER=''
aws ecr get-login-password --region "$REGION" |
  docker login --username AWS --password-stdin "$REGISTRY" >/dev/null

push_image() {
  local name="$1" dockerfile="$2" context="$3"
  shift 3
  local image="$REGISTRY/$PREFIX/$name:$TAG"
  printf '\nBuilding %s\n' "$PREFIX/$name"
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
  docker build --platform linux/arm64 --file "$SRC/core/runtime/Dockerfile" \
    --tag tina-workshop/runtime-base "$SRC/core/runtime"
  push_image runtime deploy/aws/workspace-pilot.Dockerfile . --target runtime \
    --build-arg RUNTIME_BASE=tina-workshop/runtime-base \
    --build-arg AGENT_BASE=tina-workshop/runtime-base --build-arg WORKER_BASE=tina-workshop/runtime-base
else
  push_image runtime core/runtime/Dockerfile core/runtime
fi
docker build --platform linux/arm64 --file "$SRC/core/meetings/modules/join/Dockerfile.env" \
  --tag tina/meet-join-env:dev "$SRC/core/meetings/modules/join"
push_image bot core/meetings/services/bot/Dockerfile . --build-arg "TINA_IMAGE_VERSION=$REVISION"
if ((WITH_ADDONS)); then
  if ((WITH_FULL)); then
    docker build --platform linux/arm64 --file "$SRC/core/agent/services/agent-api/Dockerfile" \
      --tag tina/v012-agent-api:staging-voice "$SRC"
    docker build --platform linux/arm64 --file "$SRC/deploy/aws/voice-worker.Dockerfile" \
      --tag tina-workshop/agent-voice "$SRC"
    push_image agent-api deploy/aws/workspace-pilot.Dockerfile . --target agent \
      --build-arg AGENT_BASE=tina-workshop/agent-voice \
      --build-arg RUNTIME_BASE=tina-workshop/agent-voice --build-arg WORKER_BASE=tina-workshop/agent-voice
  else
    push_image agent-api core/agent/services/agent-api/Dockerfile .
  fi
  push_image agent-reach deploy/agent-reach/Dockerfile deploy/agent-reach
  if ((WITH_FULL)); then
    docker build --platform linux/arm64 --file "$SRC/core/agent/worker/Dockerfile" \
      --tag tina-workshop/worker-base "$SRC"
    push_image agent-worker deploy/aws/workspace-pilot.Dockerfile . --target worker \
      --build-arg WORKER_BASE=tina-workshop/worker-base \
      --build-arg RUNTIME_BASE=tina-workshop/worker-base --build-arg AGENT_BASE=tina-workshop/worker-base
  else
    push_image agent-worker core/agent/worker/Dockerfile .
  fi
  push_image mcp core/meetings/services/mcp/Dockerfile core/meetings/services/mcp
  push_image flows core/flows/Dockerfile .
fi

if ((WITH_VIEGEM)); then
  ASSETS="${TINA_VIEGEM_CACHE:-$HOME/.cache/tina-workshop/viegem-fsmn}"
  mkdir -p "$ASSETS"
  docker build --platform linux/arm64 --build-arg TORCH_VARIANT=cpu \
    --file "$SRC/deploy/transcription/viegem/Dockerfile" \
    --tag tina/v012-viegem:staging-cpu-base "$SRC"
  docker run --rm --platform linux/arm64 --mount "type=bind,src=$ASSETS,dst=/assets" \
    tina/v012-viegem:staging-cpu-base python install-models.py --directory /assets
  push_image viegem deploy/aws/viegem.Dockerfile deploy/aws --build-context "viegem_assets=$ASSETS"
fi

printf '\nImage digests for CloudFormation (keep the account-specific values private):\n'
for name in "${images[@]}"; do
  digest="$(aws ecr describe-images --region "$REGION" --repository-name "$PREFIX/$name" \
    --image-ids "imageTag=$TAG" --query 'imageDetails[0].imageDigest' --output text --no-cli-pager)"
  [[ "$digest" =~ ^sha256:[a-f0-9]{64}$ ]] || { echo "Digest missing for $name" >&2; exit 1; }
  printf '%-14s %s/%s/%s@%s\n' "$name" "$REGISTRY" "$PREFIX" "$name" "$digest"
done
