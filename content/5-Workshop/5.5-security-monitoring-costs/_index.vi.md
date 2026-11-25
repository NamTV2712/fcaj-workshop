---
aliases: ["/vi/5-workshop/5.5-policy/"]
title: "Bảo mật, giám sát và chi phí"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

## 1. Kiểm tra role và secret

1. Vào **CloudFormation → stack staging cần kiểm tra → Resources**, tìm IAM role và Secrets Manager secret; mở metadata của từng tài nguyên.
2. **IAM → Roles**: kiểm tra trust relationship và policy của **task execution role** (kéo image, ghi log, đọc secret khi ECS khởi động) và **task role** (quyền ứng dụng sử dụng). So sánh với nhu cầu thực tế, không tự mở rộng quyền chỉ để chạy qua lỗi.

{{< workshop-screenshot file="19-role-policy.png" description="IAM role và policy cần kiểm tra; che các định danh không cần chia sẻ." >}}

3. **Secrets Manager**: kiểm tra tên, mô tả, key mã hóa, rotation nếu áp dụng. Không chọn hiển thị giá trị. Trong task definition, chỉ xác nhận có secret reference và tên biến; không chụp giá trị environment.
4. **S3/RDS**: kiểm tra mã hóa và private access theo các trang trước. Không coi một role hoặc một secret tồn tại là bằng chứng IAM đã đạt least privilege.

## 2. Kiểm tra log và cảnh báo

1. **ECS → cluster → service → Tasks → task → Logs**, chọn log group tương ứng; hoặc vào **CloudWatch → Log groups** và tìm tên từ task definition.
2. Lọc khoảng thời gian kiểm thử. Ghi nhận task khởi động, health check và lỗi liên quan; không đưa access token, nội dung cuộc họp hoặc dữ liệu người dùng vào ảnh.

{{< workshop-screenshot file="20-logs.png" description="CloudWatch log đã che token, nội dung cuộc họp và dữ liệu người dùng." >}}

3. **CloudWatch → Alarms → All alarms**: tìm các alarm thực sự tồn tại và ghi trạng thái. Không giả định có alarm `tina-ecs-high-cpu` chỉ vì tên đó từng xuất hiện trong tài liệu cũ.

## 3. CloudFront, WAF và chi phí

1. **CloudFront → Distributions** → chọn distribution staging → kiểm tra HTTPS, origin và WAF nếu được gắn. Trong **AWS WAF → Web ACLs**, chọn phạm vi CloudFront và region do Console yêu cầu để đối chiếu ACL. Ghi **không kiểm chứng** nếu không có quyền xem.
2. **Billing and Cost Management → Cost Explorer** → chọn khoảng thời gian và group theo Service; ghi chú dữ liệu có thể trễ và không tự suy ra chi phí chính xác cho một stack nếu không có phân bổ phù hợp.
3. **Budgets → Budgets** → kiểm tra budget và thông báo của tài khoản lab. Budget chỉ cảnh báo theo cấu hình; bạn vẫn phải tự theo dõi và xóa tài nguyên lab.

{{< workshop-screenshot file="21-budget.png" description="AWS Budget của lab và trạng thái cảnh báo; che email và account ID." >}}

