---
aliases: ["/vi/5-workshop/5.3-s3-vpc/"]
title: "Dựng VPC và mạng trên Console"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

## Tạo nền tảng bằng CloudFormation

Thay vì tạo từng subnet thủ công, bạn tải template lên CloudFormation Console để tạo VPC hai AZ, các route table, S3 gateway endpoint, ECS cluster, bucket và ba ECR repository nền tảng. Sau đó dùng CLI tạo NAT và route cho ứng dụng.

1. [Tạo foundation trên Console](5.3.1-vpc-subnets/).
2. [Tạo NAT và kiểm tra tuyến mạng](5.3.2-gateways-routing/).

Giữ các output để dùng cho những stack tiếp theo; CLI trong bài tự đọc output từ tài khoản của bạn.
