---
aliases: ["/vi/5-workshop/5.6-cleanup/"]
title: "Dọn dẹp và bộ bằng chứng"
date: 2026-11-25
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

## Trước khi xóa

Chỉ dọn tài nguyên **lab do bạn tự tạo** sau khi xác nhận tài khoản, Region, tên, tag, quyền sở hữu và dữ liệu có thể xóa. Không xóa stack, bucket, database, image hay VPC `tina-staging-*`, `tina-prod-*` hoặc bất kỳ tài nguyên của người khác. Xóa bucket/object, image và database là mất dữ liệu nếu không có bản sao; kiểm tra yêu cầu lưu trữ/snapshot trước.

## Thứ tự dọn lab trên Console

1. **ECS → Clusters**: xóa service/task **lab** sau khi đã xác định đúng cluster và không còn người dùng; đợi tài nguyên liên quan tách khỏi target group. Xóa cluster lab nếu đã rỗng và không cần giữ.
2. **EC2 → Load Balancers/Target Groups** và **CloudFront**: nếu bạn đã tạo các tài nguyên lab, xóa theo phụ thuộc; CloudFront có thể cần disable và chờ hoàn tất trước khi xóa.
3. **RDS → Databases** và **ElastiCache**: quyết định snapshot/lưu dữ liệu theo yêu cầu của chủ lab, rồi xóa đúng tài nguyên lab. Chờ xóa hoàn tất; kiểm tra snapshot và storage còn lưu vì chúng có thể tiếp tục tính phí.
4. **S3 → Buckets**: kiểm tra chỉ còn tệp thử của lab. Chỉ xóa object/version hoặc bucket khi chủ dữ liệu cho phép mất dữ liệu; bucket có versioning phải xử lý cả version/delete marker theo nhu cầu.
5. **ECR → Repositories**: chỉ xóa repository và image lab sau khi xác nhận không service nào cần dùng.
6. **VPC → Endpoints**: xóa endpoint lab; **NAT gateways**: xóa NAT lab và đợi xóa xong; **Elastic IPs**: release đúng Elastic IP của lab. Không release địa chỉ đang gắn cho hệ thống khác.
7. Gỡ subnet association/route lab khi cần, xóa subnet, route table và security group lab; detach rồi xóa Internet Gateway lab; cuối cùng xóa VPC lab. Nếu AWS báo dependency, xem chính xác tài nguyên phụ thuộc trước khi xóa tiếp.
8. Xem lại **VPC**, **ECS**, **RDS**, **ElastiCache**, **S3**, **ECR**, **CloudFront** và Billing/Cost Explorer để chắc chắn lab không còn thành phần tính phí ngoài ý muốn. Cost Explorer cập nhật không tức thời.

{{< workshop-screenshot file="22-cleanup-lab.png" description="Bằng chứng tài nguyên lab đã được dọn theo phạm vi thực hành." >}}

Nếu bạn tạo stack CloudFormation trong lab, mở **CloudFormation → Stacks → stack lab → Delete**, theo dõi **Events**. Stack có thể giữ lại tài nguyên do deletion policy, snapshot hoặc bucket còn dữ liệu; kiểm tra và xử lý đúng quyền sau khi stack xóa. Không dùng lệnh xóa hàng loạt theo tên gần giống.

## Hồ sơ gửi người đánh giá

- Link source/release và commit hoặc digest mà người đánh giá được phép truy cập.
- Bảng thành phần, trạng thái, thời điểm, Expected/Actual/Verdict; mô tả rõ mục đã chạy và mục còn Blocked.
- Ảnh thật theo các tên gợi ý ở từng trang, đã che bí mật và thông tin riêng tư.
- Biên bản kiểm thử với dữ liệu giả, giới hạn đã biết, ước tính chi phí và bằng chứng dọn các tài nguyên lab.
- Nếu chưa chạy lại được từ đầu, ghi rõ thiếu artifact/cấu hình nào; không đánh dấu hoàn thành toàn bộ deployment.

## Tự chụp và lưu ảnh trên Windows

1. Mở đúng trang AWS Console được ghi ở bước thực hành. Kiểm tra tên service, Region, trạng thái và thời gian có thể đọc được; thu gọn các vùng chứa thông tin không cần thiết.
2. Nhấn `Windows + Shift + S`, chọn vùng màn hình cần chụp; mở thông báo của Snipping Tool để xem ảnh. Bạn cũng có thể mở Snipping Tool trước và chọn **New**.
3. Trước khi chia sẻ, cắt hoặc che bằng mảng màu đặc account ID, email, hostname nội bộ, token, secret, thông tin cá nhân và nội dung cuộc họp. Kiểm tra lại ảnh sau khi che.
4. Chọn **Save as**, lưu định dạng PNG vào `D:/Project/fcj-workshop-template/static/images/5-Workshop/tina/`. Tạo thư mục `tina` nếu chưa có; đặt tên theo gợi ý ở từng trang, ví dụ `03-vpc-subnets.png`.
5. Mở lại ảnh đã lưu để kiểm tra nội dung. Các vị trí ảnh đã được đánh dấu trong từng trang: chỉ cần lưu đúng tên rồi dựng lại website; không cần tự sửa Markdown. Nếu đang dùng `hugo server` mà vị trí ảnh chưa cập nhật, hãy khởi động lại server. Không dùng ảnh chụp của môi trường khác để thể hiện kết quả của bài lab này.
