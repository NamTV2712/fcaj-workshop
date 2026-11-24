---
title: "Build VPC and Networking in the Console"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

Build the network foundation by hand in the **AWS Management Console** (region `us-east-1`): a VPC across two Availability Zones with public, private-app and private-data subnets, Internet Gateway, NAT Gateway, route tables and security groups. VPC endpoints for S3/ECR are added later by the CloudFormation template.

> Do not use the CLI for these steps — the child pages describe the exact console clicks.

#### What you create

| Resource | Value |
| --- | --- |
| VPC | `tina-vpc`, `10.0.0.0/16`, DNS hostnames enabled |
| Subnets (6) | 2 public (`10.0.1.0/24`, `10.0.2.0/24`), 2 app (`10.0.11.0/24`, `10.0.12.0/24`), 2 data (`10.0.21.0/24`, `10.0.22.0/24`) |
| Availability Zones | `us-east-1a` and `us-east-1b` — chosen in the subnet creation form |
| Internet Gateway | `tina-igw`, attached to `tina-vpc` |
| NAT Gateway | `tina-nat` in `tina-public-1a` with one EIP |
| Route tables | `tina-public-rt` (→ IGW), `tina-app-rt` (→ NAT), `tina-data-rt` (no `0.0.0.0/0`) |
| Security groups | `tina-alb-sg`, `tina-web-sg`, `tina-data-sg` |

#### Content

- [Create VPC and subnets in the console](5.3.1-create-gwe/)
- [Route tables and security groups in the console](5.3.2-test-gwe/)

Record the VPC ID, the 6 subnet IDs, `AppRouteTableId` and `DataRouteTableId` — the CloudFormation deploy command needs them as parameters.

- **Screenshots:** `screenshot-02-vpc-subnets.png`, `screenshot-02b-igw-nat.png`, `screenshot-03-route-tables.png`.
