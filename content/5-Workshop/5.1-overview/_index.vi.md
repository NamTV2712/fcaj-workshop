---
aliases: ["/vi/5-workshop/5.1-workshop-overview/"]
title: "Tổng quan và tiêu chí đánh giá"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

## Mục tiêu

Sau workshop, người thực hành có thể nhận diện đường đi của request, xác minh trạng thái từng lớp bằng AWS Console, tạo một mạng lab riêng, kiểm tra image/log và trình bày kết quả có bằng chứng. Hoàn thành các bước này **không đồng nghĩa** đã triển khai lại toàn bộ TINA.

## Môi trường staging đã quan sát

Ngày 25/11/2026, tại `us-east-1`, AWS CLI trả về các thành phần sau:

| Lớp | Tài nguyên staging | Cách đánh giá |
| --- | --- | --- |
| Nền tảng | Stack `tina-foundation`: VPC, subnet, route table, S3 gateway endpoint, ECS cluster và một số ECR repository | CloudFormation → stack → Resources; VPC → Your VPCs |
| Kết nối ra ngoài | `tina-staging-egress`: NAT gateway, Elastic IP và route | VPC → NAT gateways và Route tables |
| Biên | `tina-staging-edge`: CloudFront, VPC origin, ALB nội bộ và listener | CloudFront → Distributions; EC2 → Load balancers |
| Dữ liệu | `tina-staging-datastores`: RDS PostgreSQL, ElastiCache Valkey | RDS → Databases; ElastiCache → Valkey/Redis OSS caches |
| Ứng dụng | Các stack `tina-staging-core`, `-terminal`, `-runtime`, `-agent-api`, `-agent-reach`, `-mcp`, `-flows`, `-voice`, `-viegem` | ECS → cluster `tina-foundation-ecs` → Services |
| Bot | `tina-staging-bot` tạo task definition và role; runtime điều phối bot theo nhu cầu | CloudFormation → Resources; ECS → Task definitions/Tasks |

Tại thời điểm kiểm tra, 11 service staging có `runningCount = desiredCount = 1`; database staging hiển thị `available`. Số task chạy chỉ chứng minh ECS đã khởi chạy chúng; cần xem target health, log và chạy thử tính năng để đánh giá sâu hơn. Trạng thái có thể thay đổi sau thời điểm này.

Luồng tổng quát: **trình duyệt → CloudFront → VPC origin → ALB nội bộ → Terminal/gateway → các service nội bộ → PostgreSQL/Valkey/S3**. Thành phần giọng nói và phiên âm là các service riêng; không coi một thành phần chạy là bằng chứng cả chuỗi đã hoạt động.

## Bắt đầu quan sát trên Console

1. Mở AWS Console, kiểm tra tên tài khoản và chọn **N. Virginia (us-east-1)** ở góc trên.
2. Vào **CloudFormation → Stacks**, lọc `tina-staging` và mở từng stack. Xem **Overview**, **Resources** và **Events**.

{{< workshop-screenshot file="01-cloudformation-staging.png" description="Danh sách các stack TINA staging và trạng thái trên CloudFormation." >}}

3. Ghi tên stack, trạng thái, thời điểm và logical resource ID cần tìm. Không sao chép giá trị secret hoặc mọi output vào báo cáo.
4. Vào **Amazon ECS → Clusters → tina-foundation-ecs → Services**. So sánh **Desired tasks** với **Running tasks** của từng service.

{{< workshop-screenshot file="02-ecs-services.png" description="Danh sách service staging trong ECS, gồm số task mong muốn và đang chạy." >}}

5. Mở **tina-staging-bot → Resources** và xác nhận bot có task definition; không yêu cầu phải tồn tại một bot service chạy thường trực.

**Đạt:** xác định được từng lớp và service liên quan, ghi được thời điểm kiểm tra; không có nghĩa là đã kiểm thử ứng dụng.

## Phân biệt đề xuất và thực tế

![Sơ đồ kiến trúc AWS trong proposal TINA](/images/2-Proposal/tina_aws_architecture.png)

*Sơ đồ trong proposal; một số thành phần hoặc kết nối có thể khác với staging thực tế.*

Sơ đồ trong proposal mô tả kiến trúc mục tiêu. Cognito, Bedrock, SES, WAF hay một chức năng nào trên sơ đồ chỉ được ghi là đã tích hợp sau khi bạn kiểm tra được cấu hình và hành vi thực tế. Ví dụ: danh sách Cognito user pool tại thời điểm khảo sát không trả về pool nào ở `us-east-1`; không suy ra mọi vùng hay mọi tài khoản đều không có.
