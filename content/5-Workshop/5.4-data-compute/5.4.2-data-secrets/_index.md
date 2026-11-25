---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.2-create-interface-enpoint/"]
title: "Data, Secrets and Additional Services"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

## A. Inspect staging data

1. **RDS → Databases** → filter `tina-staging`; open the staging database → **Connectivity & security**. Check status **Available**, PostgreSQL engine, VPC, subnet group, security group and **Public access = No**.

{{< workshop-screenshot file="09-rds.png" description="Staging or lab RDS PostgreSQL: status and public access." >}}

2. **ElastiCache → Valkey/Redis OSS caches** → select the staging cache by cross-checking **CloudFormation → tina-staging-datastores → Resources**. View status, subnet group, security group and actual encryption configuration.

{{< workshop-screenshot file="10-valkey.png" description="ElastiCache Valkey: status and network configuration of the inspected environment." >}}

3. **Secrets Manager → Secrets**: compare the names/metadata referenced by the stack or task definition. Do not choose **Retrieve secret value**, and do not capture or copy values.

{{< workshop-screenshot file="11-secret-metadata.png" description="Secret metadata; no secret values shown." >}}

4. If a connection must be confirmed, do it through an authorised test task in the VPC. Seeing a database `Available` does not prove the application can log in and write data.

## B. Create a lab database when needed

This incurs cost. If you only evaluate the existing environment, skip part B.

1. **RDS → Subnet groups → Create DB subnet group**: name `tina-ws-db-subnets`, select the lab VPC and add two AZs plus the two data subnets; create the group.
2. **RDS → Databases → Create database**: choose **Standard create**, PostgreSQL and a version/class supported by the account. Pick a tier and storage within the budget; do not assume one class is available in every Region.
3. Set identifier `tina-ws-db`; choose a password management method per policy, preferring Secrets Manager when available. Do not write the password into documents, terminal history or screenshots.
4. In **Connectivity**, select the lab VPC and DB subnet group, **Public access = No**, and `tina-ws-db-sg`. Enable encryption; review backup and deletion protection per lab policy.
5. Choose **Create database** and wait for **Available**. Recheck subnets and SG; record the endpoint in a private workspace, never in public documents.

To practise Valkey, go to **ElastiCache → Create**, choose Valkey, a suitable mode, subnets and SG, and enable encryption/authentication as supported. Record the lab cache and creation time because caches also cost money. These steps create independent services; real use requires configuring each TINA service and verified migrations.

## C. Cognito, Bedrock and SES

These are **checks if your deployed architecture integrates them**; creating a resource does not connect the application.

- **Cognito:** first check which sign-in mechanism the real application uses. At survey time, listing user pools in `us-east-1` returned none; Terminal in the source uses Google/NextAuth. Creating a user pool does not switch login to Cognito.
- **Bedrock:** in **Amazon Bedrock → Model catalog**, select a model and check access, Region and cost. The enablement process can differ by provider/model. Only test through a provider configuration supported by your TINA version.
- **SES:** **Amazon SES → Verified identities → Create identity** to verify your email/domain. At survey time the account had `ProductionAccessEnabled = false`; in the SES sandbox you must verify recipients or use the mailbox simulator. Enabling SES does not configure TINA's mail flow.
