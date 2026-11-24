---
title: "Route Tables in the Console"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

Create the route tables in the **AWS Console**. VPC endpoints (S3 and ECR) are created later by the CloudFormation template — you do not create them here.

#### 1. Create the three route tables

**VPC → Route Tables → Create route table**, choose `tina-vpc`, repeat three times:

- `tina-public-rt`
- `tina-app-rt`
- `tina-data-rt`

#### 2. Add routes

Open each table → **Routes → Edit routes → Add route**:

| Route table | Destination | Target |
| --- | --- | --- |
| `tina-public-rt` | `0.0.0.0/0` | `tina-igw` |
| `tina-app-rt` | `0.0.0.0/0` | `tina-nat` |
| `tina-data-rt` | *(keep only the local route)* | — |

#### 3. Associate subnets

For each route table: **Subnet associations → Edit subnet associations**:

- `tina-public-rt` → `tina-public-1a`, `tina-public-1b`
- `tina-app-rt` → `tina-app-1a`, `tina-app-1b`
- `tina-data-rt` → `tina-data-1a`, `tina-data-1b`

Confirm in the route table list that `tina-data-rt` has **no** `0.0.0.0/0` route — data subnets must not reach the public Internet directly.

#### 4. Security groups (also in the Console)

**VPC → Security Groups → Create security group**, all in `tina-vpc`:

- `tina-alb-sg`: inbound 443 and 80 from `0.0.0.0/0`.
- `tina-web-sg`: inbound 3000 with source `tina-alb-sg`.
- `tina-data-sg`: inbound 5432 and 6379 with source `tina-web-sg`.

#### Verify visually

Select each route table and read the **Routes** and **Subnet associations** tabs bottom pane. The CloudFormation stack will add the S3/ECR endpoint routes to `tina-app-rt` and `tina-data-rt` automatically.

- **Screenshot:** `screenshot-03-route-tables.png`.
