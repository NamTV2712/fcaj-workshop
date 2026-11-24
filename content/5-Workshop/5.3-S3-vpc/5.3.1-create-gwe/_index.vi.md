---
title: "Tạo VPC và subnet"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

#### Các bước trên Console

1. **VPC → Create VPC** → `tina-vpc`, `10.0.0.0/16`, bật DNS hostnames.
2. **Subnets → Create subnet** ×6 theo CIDR ở trang cha, chọn đúng AZ.
3. **Internet Gateways → Create internet gateway** `tina-igw` → Attach vào `tina-vpc`.
4. **Elastic IPs → Allocate** → ghi lại địa chỉ.
5. **NAT Gateways → Create** `tina-nat`, subnet `tina-public-1a`, gắn EIP đó.

#### Lệnh CLI tương đương

```bash
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
aws ec2 modify-vpc-attribute --vpc-id $VPC --enable-dns-hostnames
aws ec2 create-subnet --vpc-id $VPC --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-internet-gateway
aws ec2 create-nat-gateway --subnet-id <public-subnet> --allocation-id <eipalloc>
```

Ghi VPC ID và 6 subnet ID vào notes.

- **Ảnh cần chụp:** `screenshot-02-vpc-subnets.png`.
