---
aliases: ["/vi/5-workshop/5.3-s3-vpc/5.3.1-create-gwe/"]
title: "Tạo VPC và subnet trên Console"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

## 1. Tạo VPC

1. Chọn Region `us-east-1`; vào **VPC → Your VPCs → Create VPC**.
2. Chọn **VPC only**. Đặt **Name tag** `tina-ws-vpc`, **IPv4 CIDR** `10.80.0.0/16`, IPv6 để mặc định không cấp, tenancy **Default**; chọn **Create VPC**.

{{< workshop-screenshot file="03a-create-vpc.png" description="Form tạo VPC lab với tên và CIDR trước khi xác nhận." >}}

3. Chọn VPC mới → **Actions → Edit VPC settings**. Bật **DNS resolution** và **DNS hostnames**, lưu lại.
4. Ghi VPC ID vào ghi chú riêng. Từ đây luôn kiểm tra cột VPC ID trước khi chọn tài nguyên.

## 2. Tạo sáu subnet

1. Vào **VPC → Subnets → Create subnet**, chọn VPC lab.
2. Thêm các subnet theo bảng. Chọn một AZ cho nhóm A và AZ khác cho nhóm B; trong `us-east-1` có thể là `us-east-1a` và `us-east-1b` nếu tài khoản của bạn cung cấp.

| Name | AZ | CIDR |
| --- | --- | --- |
| `tina-ws-public-a` | A | `10.80.1.0/24` |
| `tina-ws-public-b` | B | `10.80.2.0/24` |
| `tina-ws-app-a` | A | `10.80.11.0/24` |
| `tina-ws-app-b` | B | `10.80.12.0/24` |
| `tina-ws-data-a` | A | `10.80.21.0/24` |
| `tina-ws-data-b` | B | `10.80.22.0/24` |

{{< workshop-screenshot file="03b-create-subnets.png" description="Form tạo subnet lab với VPC, tên, AZ và CIDR." >}}

3. Chọn **Create subnet**, chờ tất cả ở trạng thái **Available**. Bảng có thể yêu cầu thêm từng subnet hoặc thêm nhiều hàng trong cùng một form tùy giao diện AWS.
4. Lọc theo VPC lab, kiểm tra mỗi AZ có ba subnet và mỗi dải không trùng nhau. Ghi sáu subnet ID.

{{< workshop-screenshot file="03-vpc-subnets.png" description="Sáu subnet của VPC lab, kèm CIDR và Availability Zone." >}}

Subnet chỉ thực sự có đường ra Internet khi được gắn route table phù hợp và tài nguyên có cấu hình IP cần thiết; tên `public` không tự tạo kết nối. NAT sẽ đặt trong public subnet ở bước kế tiếp.

