---
title: "S3, ECR and Images"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

#### Create S3 buckets

```bash
aws s3api create-bucket --bucket tina-<name>-recordings --region us-east-1
aws s3api put-bucket-encryption --bucket tina-<name>-recordings \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"<tina-key-arn>"}}]}'
aws s3api put-bucket-lifecycle-configuration --bucket tina-<name>-recordings \
  --lifecycle-configuration '{"Rules":[{"ID":"archive","Status":"Enabled","Filter":{"Prefix":"recordings/"},"Transitions":[{"Days":30,"StorageClass":"STANDARD_IA"}]}]}'
```
Repeat for `tina-<name>-exports`.

#### Create ECR repositories

```bash
for s in terminal gateway bot stt tts agent; do
  aws ecr create-repository --repository-name tina-$s --region us-east-1
done
```

#### Build from source and push

```bash
make build && make bot
docker images | grep tina
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag tina/v012-terminal:dev $ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/tina-terminal:prod
docker push $ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/tina-terminal:prod
# repeat for every service
```

- **Screenshots:** `screenshot-05-s3-buckets.png`, `screenshot-06-ecr-repos.png`, `screenshot-07-images-built.png`.
