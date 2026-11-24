---
title: "Create VPC and Subnets in the Console"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

All steps below are done in the **AWS Management Console** (region `us-east-1`). Do not use the CLI here.

#### 1. Create the VPC

1. Open **VPC → Your VPCs → Create VPC**.
2. Set:
   - **Name tag:** `tina-vpc`
   - **IPv4 CIDR block:** `10.0.0.0/16`
   - **Tenancy:** Default
3. Choose **Create VPC**, then select the VPC → **Actions → Edit VPC settings** → tick **Enable DNS hostnames** → Save.

#### 2. Create the 6 subnets (this is where the 2 AZs are chosen)

Open **VPC → Subnets → Create subnet**, choose `tina-vpc`, then add each subnet one by one. The **Availability Zone** dropdown in this form is where `us-east-1a` / `us-east-1b` are selected:

| Name tag | Availability Zone | IPv4 CIDR |
| --- | --- | --- |
| `tina-public-1a` | `us-east-1a` | `10.0.1.0/24` |
| `tina-public-1b` | `us-east-1b` | `10.0.2.0/24` |
| `tina-app-1a` | `us-east-1a` | `10.0.11.0/24` |
| `tina-app-1b` | `us-east-1b` | `10.0.12.0/24` |
| `tina-data-1a` | `us-east-1a` | `10.0.21.0/24` |
| `tina-data-1b` | `us-east-1b` | `10.0.22.0/24` |

After creating, use the **Availability Zone** column in the subnet list to confirm 3 subnets in each AZ.

> If the practice account already has a VPC named `tina-vpc`, use a unique name such as `tina-ws-vpc` and pass that VPC ID to the CloudFormation template — the CIDRs above still work.

#### 3. Internet Gateway

1. **VPC → Internet Gateways → Create internet gateway** → name `tina-igw` → Create.
2. With it selected: **Actions → Attach to VPC** → choose `tina-vpc`.

#### 4. NAT Gateway

1. **VPC → Elastic IPs → Allocate Elastic IP address** → note the allocation.
2. **VPC → NAT Gateways → Create NAT gateway**:
   - **Name:** `tina-nat`
   - **Subnet:** `tina-public-1a`
   - **Elastic IP allocation ID:** the one just created
3. Choose **Create NAT gateway** and wait until State = `Available`.

#### Screenshots

- `screenshot-02-vpc-subnets.png` — VPC with `10.0.0.0/16` and the 6 subnets, AZ column visible.
- `screenshot-02b-igw-nat.png` — `tina-igw` attached, `tina-nat` available.
