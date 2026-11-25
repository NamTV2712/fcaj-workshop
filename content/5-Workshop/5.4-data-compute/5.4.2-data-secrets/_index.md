---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.2-create-interface-enpoint/"]
title: "RDS, Valkey and secrets"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

## 1. Deploy RDS and Valkey

In **CloudShell**, run the following after the foundation and egress stacks are complete:

```bash
VPC_ID="$(stackout tina-staging VpcId)"
DATA_SUBNETS="$(stackout tina-staging DataSubnetIds)"
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-data --template-file "$TINA_SRC/deploy/aws/staging-data.yml" \
  --parameter-overrides "VpcId=$VPC_ID" "DataSubnetIds=$DATA_SUBNETS" DeployValkey=true
```

Wait for `CREATE_COMPLETE`. The template provisions PostgreSQL 17, Valkey 8, subnet groups, and dedicated security groups. RDS is configured with **Publicly accessible = No**, and the master password is managed by RDS/Secrets Manager. The stack also generates the Valkey secret; you do not need to enter any passwords in the CLI.

Go to **RDS → Databases**, select the database created by the stack, and verify that its status is **Available** and **Public access = No**:

{{< workshop-screenshot file="09-rds.png" description="Your RDS PostgreSQL instance is Available and not publicly accessible." >}}

Go to **ElastiCache → Valkey caches** (or the equivalent list in the current console UI), select the stack's replication group, and verify its status:

{{< workshop-screenshot file="10-valkey.png" description="Your Valkey cluster is Available in the lab VPC." >}}

Go to **Secrets Manager → Secrets** and view only the names and ARNs of the RDS/Valkey secrets. **Do not click Retrieve secret value when taking screenshots**:

{{< workshop-screenshot file="11-secret-metadata.png" description="Secret metadata created by the stack, without exposing secret values." >}}

Go to **VPC → Security groups** and inspect the rules allowing the application security group to access PostgreSQL and Valkey:

{{< workshop-screenshot file="06-security-groups.png" description="After creating the data stack, capture the application and database security groups without exposing sensitive details." >}}

## 2. Retrieve outputs for the next steps

```bash
stackout tina-ws-data AppSecurityGroupId
stackout tina-ws-data PostgresHost
stackout tina-ws-data PostgresSecretArn
stackout tina-ws-data ValkeyHost
stackout tina-ws-data ValkeySecretArn
```

These values are internal endpoints or ARNs, not passwords. You do not need to paste secret values into the terminal. The template uses Single-AZ RDS and a single-node Valkey cluster for testing rather than a high-availability design. Deleting the data stack creates an RDS snapshot as defined by the template; that snapshot may still incur storage charges.
