---
aliases: ["/vi/5-workshop/5.1-workshop-overview/"]
title: "Tổng quan và tiêu chí đánh giá"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

## Bạn sẽ tạo gì?

Trên tài khoản AWS mới, CloudFormation tạo VPC hai Availability Zone, ECS cluster, bucket riêng, mạng ra, RDS PostgreSQL, Valkey, CloudFront, ALB và các ECS service. Image được **bạn tự build từ source** rồi đẩy vào ECR của bạn. Dùng tên có `staging` vì một số template và quyền ECR của phiên bản nguồn này yêu cầu tên đó; các tài nguyên vẫn thuộc tài khoản của bạn.

```text
Trình duyệt → CloudFront/WAF → ALB nội bộ → Terminal (ECS)
                                              ↓
                                  Gateway + meeting/admin API
                                    ↓           ↓        ↓
                             Runtime/ECS bot   RDS    Valkey
                                    ↓           ↓
                                  S3          VieGem (tùy chọn)
```

Để đánh giá bài thực hành, cần xem stack của chính người học tạo thành công, service đạt trạng thái mong muốn và thử luồng đăng nhập/meeting. Stack `CREATE_COMPLETE` chỉ xác nhận AWS đã tạo tài nguyên, chưa chứng minh toàn bộ chức năng TINA hoạt động.

Sau khi hoàn thành các phần bên dưới, ảnh này thể hiện danh sách stack của **tài khoản thực hành**:

{{< workshop-screenshot file="01-cloudformation-staging.png" description="Các stack TINA do bạn tạo và trạng thái trong CloudFormation." >}}

Ảnh kế tiếp thể hiện trạng thái service trong cluster của bạn:

{{< workshop-screenshot file="02-ecs-services.png" description="ECS service của tài khoản thực hành, gồm desired và running tasks." >}}

## Tiêu chí cuối bài

- URL CloudFront của bạn mở được trang TINA và đăng nhập bằng tài khoản Google thử nghiệm.
- ECS core, runtime và terminal chạy ổn định; target group terminal healthy.
- Tạo cuộc họp thử được phép, quan sát bot; nếu bật ASR, kiểm tra transcript và ghi rõ lỗi nếu có.
- Biết nguồn chi phí và xóa đúng tài nguyên khi kết thúc.

Không dùng CloudFormation `static/cloudformation/tina-infrastructure.yaml` cũ trong kho workshop: nó không phải bộ template được dùng trong lộ trình này.
