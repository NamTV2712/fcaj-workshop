---
title: "Prerequisites"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

#### Local tools

```bash
git --version
aws --version
docker version --format '{{.Server.Version}}'   # >= 26
docker compose version                           # must support up --wait
python3 --version                               # >= 3.10
make --version
dotenvx --version                               # npm i -g @dotenvx/dotenvx
```

Source builds need roughly **8 vCPUs / 16 GB RAM**. Use WSL2 on Windows; macOS should start OrbStack/Docker Desktop first.

#### AWS account and CLI

1. Sign in to the AWS console as an administrator (or an IAM user with permissions for VPC, EC2, ECS, ECR, RDS, ElastiCache, S3, IAM, Cognito, Bedrock, SES, CloudFront, WAF, CloudWatch, Budgets).
2. Configure the CLI with region `us-east-1`:
   ```bash
   aws configure
   aws sts get-caller-identity
   ```
3. Never put access keys, `.env.keys` values or API keys into screenshots or documentation.

#### Source code

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
cp <secure-location>/.env.keys .   # matching private key
chmod 600 .env.keys
```

#### Failure checklist

| Symptom | Fix |
| --- | --- |
| `aws` command not found | Install AWS CLI v2 |
| `Unable to locate credentials` | `aws configure` again, correct profile |
| Docker < 26 | Start Docker/OrbStack/WSL integration |
| Dotenvx cannot decrypt | Restore the matching `.env.keys`, `chmod 600` |

- **Screenshots:** `screenshot-00-prereqs.png` (versions + `aws sts get-caller-identity`, account id masked), `screenshot-01-clone.png`.
