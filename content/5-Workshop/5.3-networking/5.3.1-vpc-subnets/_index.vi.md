---
aliases: ["/vi/5-workshop/5.3-s3-vpc/5.3.1-create-gwe/"]
title: "Tạo foundation và VPC"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

## 1. Tạo stack nền tảng trên AWS Console

1. Vào **CloudFormation → Stacks → Create stack → With new resources (standard)**.
2. Chọn **Template is ready → Upload a template file → Choose file**; chọn `deploy/aws/foundation.yml` trong ZIP đã giải nén trên máy bạn. Chọn **Next**.

{{< workshop-screenshot file="03a-create-vpc.png" description="Màn hình CloudFormation chọn tệp foundation.yml để tạo VPC và nền tảng." >}}

3. Nhập **Stack name = `tina-staging`**, chọn **Next**. Tên này bắt buộc cho bài vì nó quyết định tiền tố của ba repository ECR và một số policy của template ứng dụng.
4. Để tùy chọn khác ở mặc định, chọn **Next → Submit**. Chờ `CREATE_COMPLETE`; nếu lỗi chọn tab **Events**, tìm dòng `CREATE_FAILED` đầu tiên và đọc lý do.
5. Vào tab **Outputs**, ghi nhận `VpcId`, `PublicSubnetIds`, `AppSubnetIds`, `DataSubnetIds`, `AppRouteTableIds`, `ClusterName` và `StagingRecordingsBucket`. Bài dùng bucket này cho recording và file invocation tạm.

{{< workshop-screenshot file="03b-create-subnets.png" description="CloudFormation Outputs của stack nền tảng: VPC, subnet, cluster và bucket; che account ID nếu xuất hiện." >}}

## 2. Kiểm tra tài nguyên được tạo

1. Vào **VPC → Your VPCs**, tìm VPC theo `VpcId` trong Outputs.
2. Vào **Subnets**, lọc theo VPC đó. Bạn thấy hai public subnet, hai app subnet và hai data subnet trên hai Availability Zone.

{{< workshop-screenshot file="03-vpc-subnets.png" description="Sáu subnet do foundation tạo, với VPC và Availability Zone." >}}

3. Tại **ECS → Clusters**, xác nhận cluster trong output đã tồn tại. Bucket của stack bật chặn truy cập công khai, mã hóa và quy tắc tự hết hạn file dưới `runtime-invocations/` sau một ngày. Không sửa trực tiếp tài nguyên do stack quản lý.
