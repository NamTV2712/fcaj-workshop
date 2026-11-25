---
aliases: ["/5-workshop/5.3-s3-vpc/5.3.2-test-gwe/"]
title: "Gateways, Routes, Security Groups and Endpoint"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

## 1. Internet Gateway and NAT Gateway

1. **VPC → Internet gateways → Create internet gateway**; name it `tina-ws-igw`, then select it → **Actions → Attach to VPC** → the lab VPC.

{{< workshop-screenshot file="04a-igw-attached.png" description="Lab Internet Gateway attached to the VPC." >}}

2. **VPC → Elastic IPs → Allocate Elastic IP address**; create one address for the lab and record the allocation ID.
3. **VPC → NAT gateways → Create NAT gateway**: name `tina-ws-nat`, subnet `tina-ws-public-a`, connectivity type **Public**, and select the Elastic IP just allocated. Create it and wait for **Available**.

{{< workshop-screenshot file="04b-nat-available.png" description="Lab NAT Gateway in Available state, attached to a public subnet." >}}

4. Note that `tina-ws-public-a` will be attached to the public route table in step 2. NAT will not work as expected if its subnet has no route to the Internet Gateway.

## 2. Route tables and subnet associations

1. **VPC → Route tables → Create route table**; create `tina-ws-public-rt`, `tina-ws-app-rt` and `tina-ws-data-rt` in the lab VPC.
2. Select each table → **Routes → Edit routes → Add route**, keep the automatic `local` route and add:

| Table | Route to add | Subnets to associate |
| --- | --- | --- |
| `tina-ws-public-rt` | `0.0.0.0/0` → `tina-ws-igw` | Two public subnets |
| `tina-ws-app-rt` | `0.0.0.0/0` → `tina-ws-nat` | Two app subnets |
| `tina-ws-data-rt` | No default route to the Internet | Two data subnets |

3. For each table, open **Subnet associations → Edit subnet associations**, select the correct subnets and save.
4. Check the **Routes** and **Subnet associations** tabs of each table. The two data subnets must have no `0.0.0.0/0` route.

{{< workshop-screenshot file="04-route-tables.png" description="Route tables and subnet associations of the lab VPC." >}}

## 3. Security groups for the lab

Go to **VPC → Security groups → Create security group** in the lab VPC:

- `tina-ws-alb-sg`: open 443 from the CIDR the evaluator is allowed to use when a directly reachable ALB is needed; omit this if using an internal ALB and CloudFront VPC origin as in staging.
- `tina-ws-app-sg`: allow the application port only from the ALB's security group or the calling service. The port must match the container/target group you configure.
- `tina-ws-db-sg`: allow TCP 5432 from `tina-ws-app-sg`; allow the real cache port only from the permitted client security group.
- `tina-ws-endpoint-sg`: for an **interface endpoint**, allow TCP 443 from the task security group that needs the endpoint.

These are minimal examples; real TINA has many services and ports. Create a rule only after identifying source and destination. Never open a database or internal port to the Internet.

{{< workshop-screenshot file="06-security-groups.png" description="Lab security groups and rules allowing only the required sources." >}}

## 4. S3 gateway endpoint

1. Go to **VPC → Endpoints → Create endpoint**.
2. Name it `tina-ws-s3`, find `com.amazonaws.us-east-1.s3` with type **Gateway**, and select the lab VPC.
3. Select the app and data route tables that need S3; keep the default policy in the lab or configure an approved policy. Create the endpoint and wait for **Available**.
4. Return to the route tables and confirm the S3 prefix-list route appeared. That route does not replace IAM or bucket policies.

{{< workshop-screenshot file="05-s3-endpoint.png" description="Lab S3 gateway endpoint and its associated route tables." >}}

If you need interface endpoints for ECR/CloudWatch Logs/Secrets Manager, each has a cost and requires DNS, subnets and a security group allowing TCP 443. NAT and endpoints are not proof that a container pulled its image successfully.
