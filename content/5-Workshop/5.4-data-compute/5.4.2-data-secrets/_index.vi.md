---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.2-create-interface-enpoint/"]
title: "RDS, Valkey và Secrets Manager"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

## 1. Tạo RDS và Valkey

Trong **CloudShell**, chạy sau khi foundation và egress hoàn tất:

```bash
VPC_ID="$(stackout tina-staging VpcId)"
DATA_SUBNETS="$(stackout tina-staging DataSubnetIds)"
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-data --template-file "$TINA_SRC/deploy/aws/staging-data.yml" \
  --parameter-overrides "VpcId=$VPC_ID" "DataSubnetIds=$DATA_SUBNETS" DeployValkey=true
```

Đợi `CREATE_COMPLETE`. Template tạo PostgreSQL 17, Valkey 8, subnet group và security group riêng. RDS được đặt **Publicly accessible = No**; password master do RDS/Secrets Manager quản lý. Hệ thống tạo secret Valkey; không cần nhập mật khẩu vào CLI.

Vào **RDS → Databases**, chọn database của stack, kiểm tra trạng thái **Available** và **Public access = No**:

{{< workshop-screenshot file="09-rds.png" description="RDS PostgreSQL của bạn đã Available và không public." >}}

Vào **ElastiCache → Valkey caches** (hoặc danh sách tương đương trên giao diện hiện tại), chọn replication group của stack và kiểm tra trạng thái:

{{< workshop-screenshot file="10-valkey.png" description="Valkey của bạn đã Available trong VPC thực hành." >}}

Vào **Secrets Manager → Secrets**, chỉ xem tên và ARN của secret RDS/Valkey. **Không chọn Retrieve secret value để chụp ảnh**:

{{< workshop-screenshot file="11-secret-metadata.png" description="Metadata secret do stack tạo, không hiển thị giá trị secret." >}}

Vào **VPC → Security groups**, xem rule cho phép application security group truy cập PostgreSQL và Valkey:

{{< workshop-screenshot file="06-security-groups.png" description="Sau khi tạo stack data, chụp security group của ứng dụng và database; không hiển thị thông tin nhạy cảm." >}}

## 2. Lấy thông số cho các bước tiếp

```bash
stackout tina-ws-data AppSecurityGroupId
stackout tina-ws-data PostgresHost
stackout tina-ws-data PostgresSecretArn
stackout tina-ws-data ValkeyHost
stackout tina-ws-data ValkeySecretArn
```

Các giá trị là endpoint nội bộ hoặc ARN, không phải mật khẩu. Bạn không cần dán giá trị secret vào terminal. Template dùng RDS Single-AZ và Valkey một node để thử nghiệm, không phải thiết kế sẵn sàng cao. Xóa stack data tạo RDS snapshot theo template; snapshot vẫn có thể tính phí.
