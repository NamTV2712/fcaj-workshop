---
aliases: ["/vi/5-workshop/5.6-cleanup/"]
title: "Dọn dẹp tài nguyên và bằng chứng"
date: 2026-11-25
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

## 1. Xác nhận tài nguyên thuộc bài thực hành

Các thao tác xóa dưới đây xóa môi trường và dữ liệu thử của bạn. Chỉ thực hiện khi bạn đã lưu những gì cần giữ và đã xác định đúng tài khoản, Region, tên stack. Không xóa tài nguyên của môi trường khác. Trước khi xóa, kết thúc meeting và chờ bot task ngừng; terminate EC2 builder đã tạo ở bài.

## 2. Xóa theo thứ tự phụ thuộc

Trong CloudShell, xóa từng stack và đợi hoàn tất trước stack tiếp theo. Bỏ `tina-ws-viegem` nếu bạn không tạo:

```bash
for s in tina-ws-terminal tina-ws-core tina-ws-viegem tina-ws-runtime tina-ws-bot tina-ws-edge tina-ws-data tina-ws-egress; do
  aws cloudformation delete-stack --region "$AWS_REGION" --stack-name "$s"
  aws cloudformation wait stack-delete-complete --region "$AWS_REGION" --stack-name "$s"
done
```

Nếu có lỗi, dừng lại đọc **CloudFormation → Events** và xử lý dependency; không tiếp tục xóa mù. CloudFront có thể mất thời gian để xóa. Không xóa foundation ngay nếu các repository do foundation quản lý còn image: ECR có thể từ chối xóa repository không rỗng.

## 3. Kiểm tra ECR, bucket, snapshot và role

1. **ECR:** với ba repository `tina-staging/bot`, `tina-staging/runtime`, `tina-staging/meeting-api`, chọn toàn bộ image của bài và **Delete**. Sau đó xóa stack foundation:

   ```bash
   aws cloudformation delete-stack --region "$AWS_REGION" --stack-name tina-staging
   aws cloudformation wait stack-delete-complete --region "$AWS_REGION" --stack-name tina-staging
   ```

2. Bốn ECR repository còn lại đã tạo thủ công bằng CLI nên không tự bị xóa; dùng Console chọn từng repository `tina-staging/terminal`, `gateway`, `admin-api`, `viegem` và xóa khi chắc chắn không cần image.
3. **S3:** foundation có `DeletionPolicy: Retain`; bucket recordings và object vẫn tồn tại. Trong S3, xác định đúng bucket từ output đã lưu, tải dữ liệu cần giữ, rồi **Empty → Delete** nếu bạn muốn xóa toàn bộ dữ liệu thử. Không xóa bucket chỉ vì tên giống.
4. **RDS → Snapshots:** stack data giữ lại snapshot khi xóa database. Giữ snapshot nếu cần khôi phục, hoặc xóa snapshot thử sau khi kiểm tra. Snapshot và bucket còn tồn tại có thể tiếp tục tính phí.
5. **WAF:** xóa Web ACL `tina-workshop-acl` sau khi edge đã xóa. **Secrets Manager:** secret Google tạo thủ công vẫn còn; xóa theo quy trình của bạn nếu không dùng. Tùy chọn xóa log group còn lại khi chắc chắn không cần bằng chứng.
6. Sau khi builder đã terminate, gỡ role khỏi instance profile và xóa đúng IAM resources được tạo trong bài. Ví dụ:

   ```bash
   aws iam remove-role-from-instance-profile --instance-profile-name tina-workshop-builder-profile --role-name tina-workshop-builder-role
   aws iam delete-instance-profile --instance-profile-name tina-workshop-builder-profile
   aws iam delete-role-policy --role-name tina-workshop-builder-role --policy-name TinaEcrPush
   aws iam detach-role-policy --role-name tina-workshop-builder-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
   aws iam delete-role --role-name tina-workshop-builder-role
   ```

7. Kiểm tra lại **EC2/EBS, NAT/EIP, ECS, RDS, ElastiCache, CloudFront, WAF, S3, ECR và Billing** để xác nhận không còn tài nguyên thử ngoài ý muốn.

{{< workshop-screenshot file="22-cleanup-lab.png" description="Trạng thái xóa tài nguyên của môi trường thực hành sau khi đã kiểm tra; che account ID." >}}

## 4. Bằng chứng để đánh giá

Ghi ngày, commit `7d6bba8109f6eac51c0d8241a7083e3e364cf59d`, trạng thái từng bước, lỗi và cách khắc phục. Ảnh phải là ảnh thật, đặt tại từng bước của trang; không đưa secret, transcript thật hoặc thông tin cá nhân vào tài liệu công khai.
