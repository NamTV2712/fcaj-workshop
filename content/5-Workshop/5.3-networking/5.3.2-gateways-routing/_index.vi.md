---
aliases: ["/vi/5-workshop/5.3-s3-vpc/5.3.2-test-gwe/"]
title: "Gateway, route, security group và endpoint"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

## 1. Internet Gateway và NAT Gateway

1. **VPC → Internet gateways → Create internet gateway**; đặt `tina-ws-igw`, tạo xong chọn gateway → **Actions → Attach to VPC** → VPC lab.

{{< workshop-screenshot file="04a-igw-attached.png" description="Internet Gateway lab đã gắn vào VPC." >}}

2. **VPC → Elastic IPs → Allocate Elastic IP address**; tạo một địa chỉ cho lab và ghi allocation ID.
3. **VPC → NAT gateways → Create NAT gateway**: tên `tina-ws-nat`, subnet `tina-ws-public-a`, connectivity type **Public**, chọn Elastic IP vừa cấp. Tạo và chờ trạng thái **Available**.

{{< workshop-screenshot file="04b-nat-available.png" description="NAT Gateway lab ở trạng thái Available, gắn public subnet." >}}

4. Kiểm tra lại `tina-ws-public-a` sẽ được gắn public route table trong bước 2. NAT sẽ không hoạt động như dự kiến nếu subnet chứa nó không có route tới Internet Gateway.

## 2. Route table và subnet association

1. **VPC → Route tables → Create route table**; tạo ba bảng `tina-ws-public-rt`, `tina-ws-app-rt`, `tina-ws-data-rt` trong VPC lab.
2. Chọn từng bảng → **Routes → Edit routes → Add route**, giữ route `local` tự có và thêm:

| Bảng | Route cần thêm | Subnet cần gắn |
| --- | --- | --- |
| `tina-ws-public-rt` | `0.0.0.0/0` → `tina-ws-igw` | Hai subnet public |
| `tina-ws-app-rt` | `0.0.0.0/0` → `tina-ws-nat` | Hai subnet app |
| `tina-ws-data-rt` | Không thêm default route ra Internet | Hai subnet data |

3. Với từng bảng, mở **Subnet associations → Edit subnet associations**, chọn đúng các subnet và lưu.
4. Kiểm tra tab **Routes** và **Subnet associations** của từng bảng. Hai subnet data không có route `0.0.0.0/0`.

{{< workshop-screenshot file="04-route-tables.png" description="Route table và subnet association của VPC lab." >}}

## 3. Security group cho bài lab

Vào **VPC → Security groups → Create security group**, tạo trong VPC lab:

- `tina-ws-alb-sg`: mở 443 từ CIDR người đánh giá được phép truy cập khi cần một ALB truy cập trực tiếp; không thêm quy tắc này nếu dùng ALB nội bộ và CloudFront VPC origin như staging.
- `tina-ws-app-sg`: chỉ cho phép cổng ứng dụng từ security group của ALB hoặc service cần gọi. Cổng cụ thể phải khớp container/target group bạn cấu hình.
- `tina-ws-db-sg`: cho phép TCP 5432 từ `tina-ws-app-sg`; cho phép cổng cache thực tế chỉ từ security group của client được phép.
- `tina-ws-endpoint-sg`: khi tạo **interface endpoint**, cho phép TCP 443 từ security group của task cần truy cập endpoint.

Đây là ví dụ tối thiểu; TINA thực tế có nhiều service và cổng riêng. Chỉ tạo rule sau khi xác định nguồn/đích. Không mở database hoặc cổng nội bộ cho Internet.

{{< workshop-screenshot file="06-security-groups.png" description="Security group lab và các rule chỉ cho phép nguồn cần thiết." >}}

## 4. S3 gateway endpoint

1. Vào **VPC → Endpoints → Create endpoint**.
2. Name `tina-ws-s3`, tìm dịch vụ `com.amazonaws.us-east-1.s3` có type **Gateway**, chọn VPC lab.
3. Chọn route table app và data cần truy cập S3; để policy mặc định trong lab hoặc cấu hình policy theo yêu cầu bảo mật được duyệt. Tạo endpoint và chờ **Available**.
4. Quay lại route table, xác nhận route prefix list S3 đã xuất hiện. Route đó không thay thế IAM/bucket policy.

{{< workshop-screenshot file="05-s3-endpoint.png" description="S3 gateway endpoint và route table liên kết của lab." >}}

Nếu cần interface endpoint cho ECR/CloudWatch Logs/Secrets Manager, mỗi endpoint có chi phí và yêu cầu DNS, subnet, security group TCP 443 phù hợp. NAT và endpoint không phải bằng chứng container đã pull image thành công.

