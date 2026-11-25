---
aliases: ["/vi/5-workshop/5.3-s3-vpc/5.3.1-create-gwe/"]
title: "Tạo foundation và VPC"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

## 1. Tạo stack nền tảng trên AWS Console

Nếu đây là lần đầu dùng ECS trong tài khoản thực hành, mở AWS CloudShell và kiểm tra role ECS dùng để quản lý cluster:

```bash
aws iam get-role --role-name AWSServiceRoleForECS --query 'Role.Arn' --output text
```

Nếu lệnh báo `NoSuchEntity`, chạy lệnh dưới đây để tạo role. Nếu báo `AccessDenied`, nhờ quản trị viên AWS kiểm tra và tạo role bằng danh tính có quyền `iam:CreateServiceLinkedRole` cho `ecs.amazonaws.com`.

```bash
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
```

Sau khi tạo, chờ IAM đồng bộ rồi tiếp tục. Nếu đã gặp lỗi `Unable to assume the service linked role` và stack `tina-staging` ở `ROLLBACK_COMPLETE`, xác nhận đó là stack thực hành vừa tạo, xóa stack lỗi, chờ `DELETE_COMPLETE` rồi tạo lại. Stack ở `CREATE_FAILED` có thể dùng **Retry** nếu Console hiện nút đó. Xem [role dành cho ECS trong tài liệu AWS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles-for-clusters.html).

Nếu muốn CloudFormation tạo role trong tài khoản **chưa có** `AWSServiceRoleForECS`, thêm đoạn dưới vào mục `Resources:` sẵn có của `foundation.yml`. Đặt `ECSServiceLinkedRole` ngang cấp với `Cluster`, rồi thêm `DependsOn` vào resource `Cluster`. Giữ nguyên toàn bộ `Properties` hiện có của `Cluster`. Khi tạo stack, xác nhận quyền tạo tài nguyên IAM nếu Console yêu cầu.

```yaml
  ECSServiceLinkedRole:
    Type: AWS::IAM::ServiceLinkedRole
    DeletionPolicy: Retain
    Properties:
      AWSServiceName: ecs.amazonaws.com

  Cluster:
    Type: AWS::ECS::Cluster
    DependsOn: ECSServiceLinkedRole
    # Giữ nguyên Properties của Cluster ngay bên dưới.
```

Role này dùng chung trong tài khoản. Nếu role đã tồn tại hoặc bạn tạo lại stack sau khi xóa, dùng template gốc với bước kiểm tra CloudShell ở trên. `Retain` giữ role lại khi xóa stack, nên khai báo tạo lại có thể báo trùng tên. [Tài liệu CloudFormation về ServiceLinkedRole](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-iam-servicelinkedrole.html)

1. Vào **CloudFormation → Stacks → Create stack → With new resources (standard)**.
2. Mở [foundation.yml trên GitHub](https://github.com/poor-frog/TINA/blob/7d6bba8109f6eac51c0d8241a7083e3e364cf59d/deploy/aws/foundation.yml), chọn **Download raw file** và lưu thành `foundation.yml`. Trong CloudFormation, chọn **Template is ready → Upload a template file → Choose file**, chọn file vừa tải rồi bấm **Next**.

   Trong repo **poor-frog/TINA**, chọn nhánh `feat/s3-ephemeral-workspaces` rồi mở `deploy/aws/foundation.yml`. Link trên mở đúng commit `7d6bba8…` để bạn tải riêng file cho bước Console.

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
