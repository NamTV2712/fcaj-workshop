---
aliases: ["/vi/5-workshop/5.3-s3-vpc/"]
title: "Dựng VPC và mạng trên Console"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

## Mục tiêu

Tạo một mạng **lab riêng** với hai Availability Zone, sáu subnet, Internet Gateway, một NAT Gateway và route table. Sau đó tạo security group và S3 gateway endpoint. Các bước này dạy thao tác mạng; chúng chưa tự tạo hệ thống TINA.

> Các giá trị dưới đây là **ví dụ cho lab mới**, không phải cấu hình của staging. Staging quan sát được dùng VPC `10.42.0.0/16`; production dùng VPC khác. Không sửa hai VPC đó để làm bài thực hành. Nếu CIDR ví dụ trùng mạng đang kết nối hoặc chính sách tài khoản, chọn CIDR riêng không chồng lấn.

| Tên ví dụ | IPv4 CIDR | Vai trò |
| --- | --- | --- |
| `tina-ws-vpc` | `10.80.0.0/16` | Toàn bộ mạng lab |
| `tina-ws-public-a`, `tina-ws-public-b` | `10.80.1.0/24`, `10.80.2.0/24` | Public, hai AZ |
| `tina-ws-app-a`, `tina-ws-app-b` | `10.80.11.0/24`, `10.80.12.0/24` | Private cho ứng dụng, hai AZ |
| `tina-ws-data-a`, `tina-ws-data-b` | `10.80.21.0/24`, `10.80.22.0/24` | Private cho dữ liệu, hai AZ |

NAT Gateway, Elastic IP và các interface endpoint có thể phát sinh phí kể cả khi bạn chưa đưa ứng dụng vào lab. Một NAT ở AZ A giúp lab đơn giản hơn nhưng không dự phòng khi AZ A gặp sự cố.

1. [Tạo VPC và sáu subnet](5.3.1-vpc-subnets/).
2. [Tạo gateway, route, security group và endpoint](5.3.2-gateways-routing/).

**Kết quả:** VPC và subnet tồn tại, route/association khớp bảng; bước này chưa kiểm tra được lưu lượng ứng dụng.
