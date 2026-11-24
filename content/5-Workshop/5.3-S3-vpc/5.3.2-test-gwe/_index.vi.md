---
title: "Route table và VPC endpoint"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

#### Route table

1. `tina-public-rt`: thêm `0.0.0.0/0 → tina-igw`, gắn `tina-public-1a` và `tina-public-1b`.
2. `tina-app-rt`: thêm `0.0.0.0/0 → tina-nat`, gắn 2 subnet app.
3. `tina-data-rt`: chỉ giữ route local, gắn 2 subnet data.

#### VPC endpoint

1. **Endpoints → Create endpoint** → AWS services → `com.amazonaws.us-east-1.s3`, loại **Gateway**, VPC `tina-vpc`, route table `tina-app-rt` và `tina-data-rt`.
2. Tạo interface endpoint `com.amazonaws.us-east-1.ecr.api` và `com.amazonaws.us-east-1.ecr.dkr`, loại **Interface**, ở 2 subnet app, dùng SG interface và bật DNS name.

#### Security group

- `tina-alb-sg`: inbound 443 từ `0.0.0.0/0`.
- `tina-web-sg`: inbound 443/8080 từ `tina-alb-sg`.
- `tina-data-sg`: inbound 5432 (RDS) và 6379 (Redis) từ `tina-web-sg` / task SG.

#### Kiểm tra

```bash
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc>"
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=<vpc>"
aws ec2 describe-security-groups --filters "Name=vpc-id,Values=<vpc>"
```

- **Ảnh cần chụp:** `screenshot-03-route-tables.png`, `screenshot-04-vpc-endpoints.png`.
