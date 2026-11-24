---
title: "Build VPC and Networking"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

Tạo nền tảng mạng theo proposal: VPC trải 2 AZ với subnet public, private-app và private-data; egress có kiểm soát qua NAT; VPC endpoint để lưu lượng S3/ECR không đi Internet công cộng.

#### 1. VPC và subnet

- VPC: `tina-vpc`, CIDR `10.0.0.0/16`, bật DNS hostnames và DNS resolution.
- `us-east-1a`: `tina-public-1a` `10.0.1.0/24`, `tina-app-1a` `10.0.11.0/24`, `tina-data-1a` `10.0.21.0/24`
- `us-east-1b`: `tina-public-1b` `10.0.2.0/24`, `tina-app-1b` `10.0.12.0/24`, `tina-data-1b` `10.0.22.0/24`

```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region us-east-1
aws ec2 create-subnet --vpc-id <vpc> --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
# lặp cho 5 subnet còn lại
```

#### 2. Ra Internet

Tạo `tina-igw`, gắn vào VPC; cấp Elastic IP và tạo `tina-nat` ở subnet **public**.

#### 3. Route table và security group

- `tina-public-rt`: `0.0.0.0/0 → tina-igw`, gắn 2 subnet public.
- `tina-app-rt`: `0.0.0.0/0 → tina-nat`, gắn 2 subnet app.
- `tina-data-rt`: **không** có route `0.0.0.0/0`, gắn 2 subnet data.
- Security group: `tina-alb-sg` (443 từ Internet), `tina-web-sg` (443/8080 chỉ từ ALB), `tina-data-sg` (cổng DB/cache chỉ từ app SG).

#### 4. VPC endpoint (tối ưu chi phí trong proposal)

- **Gateway endpoint** `tina-s3-gwe` cho `com.amazonaws.us-east-1.s3`, thêm route vào app/data route table.
- **Interface endpoint** `tina-ecr-api` / `tina-ecr-dkr` cho ECR ở subnet app, dùng SG interface.

```bash
aws ec2 create-vpc-endpoint --vpc-id <vpc> --service-name com.amazonaws.us-east-1.s3 \
  --vpc-endpoint-type Gateway --route-table-ids <app-rt> <data-rt>
```

#### Kiểm tra

```bash
aws ec2 describe-vpcs --vpc-ids <vpc>
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc>"
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc>"
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=<vpc>"
```

- **Ảnh cần chụp:** `screenshot-02-vpc-subnets.png`, `screenshot-03-route-tables.png`, `screenshot-04-vpc-endpoints.png`.

#### Nội dung

- [Tạo VPC và subnet](5.3.1-create-gwe/)
- [Route table và endpoint](5.3.2-test-gwe/)
