---
title: "Route Tables and VPC Endpoints"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

#### Route tables

1. `tina-public-rt`: add `0.0.0.0/0 → tina-igw`, associate `tina-public-1a` and `tina-public-1b`.
2. `tina-app-rt`: add `0.0.0.0/0 → tina-nat`, associate the two app subnets.
3. `tina-data-rt`: leave only the local route, associate the two data subnets.

#### VPC endpoints

1. **Endpoints → Create endpoint** → AWS services → `com.amazonaws.us-east-1.s3`, type **Gateway**, VPC `tina-vpc`, route tables `tina-app-rt` and `tina-data-rt`.
2. Create interface endpoints `com.amazonaws.us-east-1.ecr.api` and `com.amazonaws.us-east-1.ecr.dkr`, type **Interface**, in both app subnets, with the interface security group and DNS names enabled.

#### Security groups

- `tina-alb-sg`: inbound 443 from `0.0.0.0/0`.
- `tina-web-sg`: inbound 443/8080 from `tina-alb-sg`.
- `tina-data-sg`: inbound 5432 (RDS) and 6379 (Redis) from `tina-web-sg` / task security groups.

#### Verification

```bash
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc>"
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=<vpc>"
aws ec2 describe-security-groups --filters "Name=vpc-id,Values=<vpc>"
```

- **Screenshots:** `screenshot-03-route-tables.png`, `screenshot-04-vpc-endpoints.png`.
