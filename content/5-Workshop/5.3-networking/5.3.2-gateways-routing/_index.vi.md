---
aliases: ["/vi/5-workshop/5.3-s3-vpc/5.3.2-test-gwe/"]
title: "NAT Gateway, route và endpoint"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

## 1. Tạo NAT Gateway bằng CloudFormation CLI

Foundation đã gắn Internet Gateway cho VPC. Trong CloudShell, chạy:

```bash
PUBLIC_SUBNETS="$(stackout tina-staging PublicSubnetIds)"
APP_ROUTES="$(stackout tina-staging AppRouteTableIds)"
IFS=, read -r PUBLIC_A PUBLIC_B <<< "$PUBLIC_SUBNETS"
IFS=, read -r ROUTE_A ROUTE_B <<< "$APP_ROUTES"
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-egress --template-file "$TINA_SRC/deploy/aws/staging-egress.yml" \
  --parameter-overrides "PublicSubnetId=$PUBLIC_A" "AppRouteTableA=$ROUTE_A" "AppRouteTableB=$ROUTE_B"
```

Kiểm tra Internet Gateway gắn với VPC tại **VPC → Internet gateways**:

{{< workshop-screenshot file="04a-igw-attached.png" description="Internet Gateway của VPC đã attached." >}}

Kiểm tra NAT tại **VPC → NAT gateways**; stack phải `CREATE_COMPLETE` và NAT **Available**:

{{< workshop-screenshot file="04b-nat-available.png" description="NAT Gateway do stack egress tạo, trạng thái Available." >}}

## 2. Kiểm tra route và S3 endpoint

Trong **VPC → Route tables**, xem app route table: tuyến `0.0.0.0/0` trỏ NAT. Public route table trỏ Internet Gateway; data subnet không có default route Internet. Cả hai app route table có S3 gateway endpoint.

{{< workshop-screenshot file="04-route-tables.png" description="Route table của app subnet với default route qua NAT." >}}

Tại **VPC → Endpoints**, tìm endpoint ID từ output `S3EndpointId` của foundation:

{{< workshop-screenshot file="05-s3-endpoint.png" description="S3 gateway endpoint và các route table app được liên kết." >}}

Security group cho application và database sẽ được stack data tạo ở phần sau. Bạn không cần tạo sẵn security group cho chúng.


Cấu hình một NAT dùng chung hai AZ giúp giảm số tài nguyên nhưng có điểm phụ thuộc một AZ và có thể phát sinh phí truyền liên AZ. Xem [tài liệu VPC origin của AWS](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html) cho các điều kiện Internet Gateway và địa chỉ IPv4 còn trống.
