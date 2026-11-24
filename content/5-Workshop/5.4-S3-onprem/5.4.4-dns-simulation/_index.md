---
title: "Verify the Running System"
date: 2026-11-24
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

#### Application checks

Get the CloudFront domain from the stack output, then open it in a browser:

```bash
aws cloudformation describe-stacks --stack-name tina-infra \
  --query 'Stacks[0].Outputs'
curl -sS -o /dev/null -w '%{http_code}\n' https://<cloudfront-domain>/health
```

1. Sign in through Cognito/Google (first user becomes admin).
2. In **Settings → Models**, select a model provider so the agent can answer.
3. Confirm the live transcript, notes, summary and the **Tiếng Việt / English / Song ngữ** dropdown.
4. Check the wake word and spoken reply through the bot.

#### Data-path checks

```bash
aws s3 ls s3://tina-<name>-recordings
aws rds describe-db-instances --db-instance-identifier tina-db
aws elasticache describe-cache-clusters --cache-cluster-id tina-cache
```
Recording uploads should land in S3 through the gateway endpoint (no NAT data charges); transcripts go to RDS and live state to ElastiCache in the private data subnets.

#### Screenshots

- `screenshot-17-app-running.png`
- `screenshot-18-transcript.png`
