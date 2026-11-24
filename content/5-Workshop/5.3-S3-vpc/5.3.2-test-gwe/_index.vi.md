---
title: "Route table trên Console"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

Tạo route table trên **AWS Console**. VPC endpoint (S3/ECR) do template CloudFormation tạo ở bước sau — bạn không tạo ở đây.

#### 1. Tạo 3 route table

**VPC → Route Tables → Create route table**, chọn `tina-vpc`, lặp 3 lần:

- `tina-public-rt`
- `tina-app-rt`
- `tina-data-rt`

#### 2. Thêm route

Mở từng bảng → **Routes → Edit routes → Add route**:

| Route table | Destination | Target |
| --- | --- | --- |
| `tina-public-rt` | `0.0.0.0/0` | `tina-igw` |
| `tina-app-rt` | `0.0.0.0/0` | `tina-nat` |
| `tina-data-rt` | *(giữ chỉ route local)* | — |

#### 3. Gắn subnet

Với mỗi route table: **Subnet associations → Edit subnet associations**:

- `tina-public-rt` → `tina-public-1a`, `tina-public-1b`
- `tina-app-rt` → `tina-app-1a`, `tina-app-1b`
- `tina-data-rt` → `tina-data-1a`, `tina-data-1b`

Kiểm tra `tina-data-rt` **không** có route `0.0.0.0/0` — subnet data không được ra Internet trực tiếp.

#### 4. Security group (cũng trên Console)

**VPC → Security Groups → Create security group**, đều trong `tina-vpc`:

- `tina-alb-sg`: inbound 443 và 80 từ `0.0.0.0/0`.
- `tina-web-sg`: inbound 3000, source `tina-alb-sg`.
- `tina-data-sg`: inbound 5432 và 6379, source `tina-web-sg`.

#### Kiểm tra bằng mắt

Chọn từng route table và đọc tab **Routes** và **Subnet associations** ở khung dưới. Stack CloudFormation sẽ tự thêm route endpoint S3/ECR vào `tina-app-rt` và `tina-data-rt`.

- **Ảnh cần chụp:** `screenshot-03-route-tables.png`.
