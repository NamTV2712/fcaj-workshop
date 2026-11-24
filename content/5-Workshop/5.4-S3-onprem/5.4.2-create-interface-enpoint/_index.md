---
title: "Data, Identity and AI"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

#### RDS PostgreSQL

```bash
aws rds create-db-instance \
  --db-instance-identifier tina-db --db-instance-class db.t4g.micro \
  --engine postgres --allocated-storage 20 --storage-type gp3 \
  --db-name tina --master-username tinauser --master-user-password '<secret>' \
  --vpc-security-group-ids <tina-data-sg> --db-subnet-group-name <data-subnets> \
  --storage-encrypted --kms-key-id <tina-key-arn>
```

#### ElastiCache Redis

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id tina-cache --cache-node-type cache.t4g.micro \
  --engine redis --num-cache-nodes 1 --cache-subnet-group-name <data-subnets> \
  --security-group-ids <tina-data-sg>
```

#### Cognito with Google OAuth

Create user pool `tina-users`, add a Google identity provider with client ID/secret from Google Auth Platform, create an app client with callback `https://<cloudfront-domain>/api/auth/callback/google`, and note the user pool ID.

#### Bedrock and SES

- In **Bedrock → Model access**, enable the models used for notes/summaries/agent (e.g. Claude/Nova) in `us-east-1`.
- In **SES**, verify the sending domain and create the SMTP/API credentials stored in Secrets Manager.

```bash
aws rds describe-db-instances --db-instance-identifier tina-db
aws elasticache describe-cache-clusters --cache-cluster-id tina-cache
aws cognito-idp list-user-pools --max-results 10
aws bedrock list-foundation-models --region us-east-1
aws sesv2 get-account
```

- **Screenshots:** `screenshot-08-rds-redis.png`, `screenshot-09-cognito.png`, `screenshot-10-bedrock-ses.png`.
