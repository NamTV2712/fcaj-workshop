---
title: "Tạo VPC và subnet trên Console"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

Tất cả bước dưới đây làm trên **AWS Management Console** (vùng `us-east-1`). Không dùng CLI ở bước này.

#### 1. Tạo VPC

1. Mở **VPC → Your VPCs → Create VPC**.
2. Điền:
   - **Name tag:** `tina-vpc`
   - **IPv4 CIDR block:** `10.0.0.0/16`
   - **Tenancy:** Default
3. Chọn **Create VPC**, sau đó chọn VPC vừa tạo → **Actions → Edit VPC settings** → tick **Enable DNS hostnames** → Save.

#### 2. Tạo 6 subnet (ở đây chọn 2 AZ)

Mở **VPC → Subnets → Create subnet**, chọn `tina-vpc`, rồi thêm từng subnet. Dropdown **Availability Zone** trong form chính là nơi chọn `us-east-1a` / `us-east-1b`:

| Name tag | Availability Zone | IPv4 CIDR |
| --- | --- | --- |
| `tina-public-1a` | `us-east-1a` | `10.0.1.0/24` |
| `tina-public-1b` | `us-east-1b` | `10.0.2.0/24` |
| `tina-app-1a` | `us-east-1a` | `10.0.11.0/24` |
| `tina-app-1b` | `us-east-1b` | `10.0.12.0/24` |
| `tina-data-1a` | `us-east-1a` | `10.0.21.0/24` |
| `tina-data-1b` | `us-east-1b` | `10.0.22.0/24` |

Sau khi tạo, xem cột **Availability Zone** trong danh sách subnet để xác nhận mỗi AZ có 3 subnet.

> Nếu tài khoản thực hành đã có VPC tên `tina-vpc`, hãy dùng tên khác như `tina-ws-vpc` và truyền VPC ID đó vào template CloudFormation — các CIDR ở trên vẫn dùng được.

#### 3. Internet Gateway

1. **VPC → Internet Gateways → Create internet gateway** → tên `tina-igw` → Create.
2. Giữ nó được chọn: **Actions → Attach to VPC** → chọn `tina-vpc`.

#### 4. NAT Gateway

1. **VPC → Elastic IPs → Allocate Elastic IP address** → ghi lại allocation.
2. **VPC → NAT Gateways → Create NAT gateway**:
   - **Name:** `tina-nat`
   - **Subnet:** `tina-public-1a`
   - **Elastic IP allocation ID:** allocation vừa tạo
3. Chọn **Create NAT gateway** và đợi State = `Available`.

#### Ảnh cần chụp

- `screenshot-02-vpc-subnets.png` — VPC `10.0.0.0/16` với 6 subnet, thấy cột AZ.
- `screenshot-02b-igw-nat.png` — `tina-igw` đã attach, `tina-nat` available.
