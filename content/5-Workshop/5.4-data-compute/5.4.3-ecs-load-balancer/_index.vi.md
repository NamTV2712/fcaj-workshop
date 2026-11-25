---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.3-test-endpoint/"]
title: "ECS, task definition và load balancer"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

## A. Kiểm tra ECS staging

1. Mở **Amazon ECS → Clusters → tina-foundation-ecs → Services**.
2. Với mỗi service `tina-staging-*`, ghi trạng thái, **Desired tasks**, **Running tasks** và **Pending tasks**. Chọn service → tab **Deployments and events** để đọc lỗi khởi tạo hoặc thay thế task.

{{< workshop-screenshot file="12-ecs-services.png" description="Danh sách ECS service với desired, running và pending tasks." >}}

3. Mở **Tasks**, chọn một task đang chạy → xem task definition, các container, trạng thái và link **View logs in CloudWatch**. Không chụp environment values, token, secret hoặc URL nội bộ.

{{< workshop-screenshot file="13-ecs-task.png" description="Chi tiết một ECS task và trạng thái container; che environment và secret." >}}

4. Mở **Task definitions** → chọn phiên bản đang dùng, đối chiếu image, CPU/memory, port, task role, execution role, cấu hình log và **tên** secret. Không chỉnh sửa revision staging.
5. Tìm stack `tina-staging-bot` trong CloudFormation và kiểm tra bot task definition. Bot được tạo theo nhu cầu; không xem việc không có service bot chạy thường trực là lỗi.

Ví dụ quan sát ngày 25/11/2026: Terminal dùng cổng container 3000; core gồm nhiều container, bao gồm gateway cổng 8000. Đây là ảnh chụp cấu hình tại một thời điểm, không thay cho task definition của bản release bạn sẽ triển khai.

## B. Kiểm tra ALB và CloudFront

1. **CloudFormation → tina-staging-edge → Resources**: xác định distribution, VPC origin, load balancer và listener.
2. **EC2 → Load Balancers**: mở ALB staging, kiểm tra **Scheme = internal**, VPC và listener. Không sao chép hoặc thay đổi rule của hệ thống đang phục vụ người dùng.
3. **EC2 → Target Groups**: đối chiếu hai target group của staging. Mở **Targets** và xem **Health status** và lý do nếu unhealthy. Tại thời điểm kiểm tra, terminal và gateway đều `healthy`; terminal dùng health path `/api/auth/providers`, gateway dùng `/health`.

{{< workshop-screenshot file="14-target-health.png" description="Trạng thái health của target group terminal hoặc gateway." >}}

4. **CloudFront → Distributions** → mở distribution từ stack edge: kiểm tra trạng thái triển khai, origin và **VPC origin**. CloudFront của staging kết nối ALB nội bộ; cấu hình một CloudFront origin trỏ thẳng DNS ALB công khai là kiến trúc khác.

{{< workshop-screenshot file="15-cloudfront-origin.png" description="CloudFront distribution và VPC origin; che domain và định danh nội bộ." >}}

5. Nếu unhealthy, kiểm tra trước cổng container/target group, health path, security group, tình trạng task và log. Không sửa staging nếu bạn chỉ có nhiệm vụ đánh giá.

## C. Tạo ECS lab khi có bộ release đầy đủ

1. **ECS → Clusters → Create cluster** → tên `tina-ws-cluster`, chọn networking/compute theo hướng dẫn release. Tạo cluster không tự tạo service.
2. **ECS → Task definitions → Create new task definition** → chọn Fargate nếu workload tương thích; điền family, CPU/memory hợp lệ, task/execution role, image ECR + digest, cổng, biến môi trường không nhạy cảm, secret references và log group theo manifest của **từng service**.
3. Với cluster lab, chọn **Create → Service**; chọn đúng task definition/revision, số task, app subnets, security groups, service discovery và load balancer/target group theo manifest. Kiểm tra **Events** và task health sau khi tạo.
4. Lặp theo thứ tự phụ thuộc của bộ release, bao gồm migration/init job, kết nối PostgreSQL/Valkey/S3, internal endpoints và runtime điều phối bot. Kiểm tra từng service trước khi tạo service phụ thuộc.

**Điểm dừng:** hiện workshop chưa có manifest/task definition và thứ tự phụ thuộc portable đã được kiểm thử đầy đủ. Vì thế không thể điền chính xác mọi trường từ trang này hoặc tuyên bố một cluster mới đã chạy đầy đủ TINA. Người hướng dẫn cần chuẩn bị và chạy thử bộ release như mô tả ở [Kiểm tra hệ thống](../5.4.4-application-validation/).

Fargate không hỗ trợ khai báo GPU cho task; VieGem trong staging quan sát được chạy task Fargate, không có nghĩa là dùng GPU. Nếu release đòi hỏi GPU, chọn hạ tầng GPU tương thích và kiểm tra lại chi phí/quota. [AWS: Fargate task definition differences](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html).

