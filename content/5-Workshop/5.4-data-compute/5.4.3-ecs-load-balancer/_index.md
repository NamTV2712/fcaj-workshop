---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.3-test-endpoint/"]
title: "Deploy ECS and the website"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

## Deployment order

The steps below deploy the website into **your** VPC and ECS cluster. Run the commands in CloudShell using the `stackout` and `repoarn` helpers along with the `TINA_SRC` and `TINA_TAG` variables prepared earlier. Each page requires the previous stack to succeed.

1. [Create WAF and CloudFront/ALB](5.4.3.1-edge/).
2. [Deploy the bot task and Runtime](5.4.3.2-runtime/).
3. [Deploy optional ASR and core](5.4.3.3-core/).
4. [Configure Google sign-in and deploy Terminal](5.4.3.4-terminal/).
5. [Review scope and optional extensions](5.4.3.5-extensions/).

Before continuing, confirm that the image tag in CloudShell matches the tag built on EC2:

```bash
export TINA_TAG=ws-v1
image() {
  local name="$1" digest
  digest="$(aws ecr describe-images --region "$AWS_REGION" --repository-name "tina-staging/$name" --image-ids "imageTag=$TINA_TAG" --query 'imageDetails[0].imageDigest' --output text)" || return 1
  [[ "$digest" =~ ^sha256:[a-f0-9]{64}$ ]] || { echo "Digest not found for $name:$TINA_TAG" >&2; return 1; }
  printf '%s.dkr.ecr.%s.amazonaws.com/tina-staging/%s@%s' "$TINA_ACCOUNT" "$AWS_REGION" "$name" "$digest"
}
image terminal
```

If you built with a different tag, update `TINA_TAG` to match. Every Fargate task in the templates uses **ARM64**; do not accidentally use AMD64 images. Image digests and ARNs belong to your account and do not need to be exposed publicly in screenshots.
