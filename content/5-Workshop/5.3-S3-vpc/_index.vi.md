---
title: "Dựng VPC và mạng trên Console"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

Dựng nền tảng mạng **bằng tay trên AWS Management Console** (vùng `us-east-1`): VPC trải 2 Availability Zone với subnet public, private-app và private-data; Internet Gateway, NAT Gateway, route table và security group. VPC endpoint cho S3/ECR do template CloudFormation tạo ở bước sau.

> Không dùng CLI ở các bước này — trang con mô tả đúng thao tác click trên console.

#### Những gì cần tạo

| Tài nguyên | Giá trị |
| --- | --- |
| VPC | `tina-vpc`, `10.0.0.0/16`, bật DNS hostnames |
| Subnet (6) | 2 public (`10.0.1.0/24`, `10.0.2.0/24`), 2 app (`10.0.11.0/24`, `10.0.12.0/24`), 2 data (`10.0.21.0/24`, `10.0.22.0/24`) |
| Availability Zone | `us-east-1a` và `us-east-1b` — chọn trong form tạo subnet |
| Internet Gateway | `tina-igw`, gắn vào `tina-vpc` |
| NAT Gateway | `tina-nat` ở `tina-public-1a` với 1 EIP |
| Route table | `tina-public-rt` (→ IGW), `tina-app-rt` (→ NAT), `tina-data-rt` (không có `0.0.0.0/0`) |
| Security group | `tina-alb-sg`, `tina-web-sg`, `tina-data-sg` |

#### Nội dung

- [Tạo VPC và subnet trên console](5.3.1-create-gwe/)
- [Route table và security group trên console](5.3.2-test-gwe/)

Ghi lại VPC ID, 6 subnet ID, `AppRouteTableId` và `DataRouteTableId` — lệnh deploy CloudFormation cần các giá trị này làm parameter.

- **Ảnh cần chụp:** `screenshot-02-vpc-subnets.png`, `screenshot-02b-igw-nat.png`, `screenshot-03-route-tables.png`.
