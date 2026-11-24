---
title: "Create VPC and Subnets"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

#### Console steps

1. **VPC → Create VPC** → `tina-vpc`, `10.0.0.0/16`, enable DNS hostnames.
2. **Subnets → Create subnet** ×6 using the CIDRs in the parent page, selecting the matching AZ.
3. **Internet Gateways → Create internet gateway** `tina-igw` → Attach to `tina-vpc`.
4. **Elastic IPs → Allocate** → note the address.
5. **NAT Gateways → Create** `tina-nat`, subnet `tina-public-1a`, associate the EIP.

#### CLI equivalent

```bash
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
aws ec2 modify-vpc-attribute --vpc-id $VPC --enable-dns-hostnames
aws ec2 create-subnet --vpc-id $VPC --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-internet-gateway
aws ec2 create-nat-gateway --subnet-id <public-subnet> --allocation-id <eipalloc>
```

Record the VPC ID and six subnet IDs in your notes.

- **Screenshot:** `screenshot-02-vpc-subnets.png`.
