---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.4-dns-simulation/"]
title: "Kiểm thử website và meeting"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

## 1. Kiểm tra website và đăng nhập

Nếu dùng [template gộp](../../5.4-full-cloudformation/), lấy `WebsiteUrl` trong Outputs và đăng nhập bằng tài khoản Cognito được mời. Phần Google bên dưới áp dụng cho lộ trình nhiều stack.

Lấy URL CloudFront do tài khoản của bạn tạo:

```bash
stackout tina-ws-edge StageUrl
```

Mở URL trên trình duyệt. Kiểm tra trang TINA hiển thị, sau đó đăng nhập bằng Google test user đã khai báo. Ảnh dưới đây cần chụp trang đăng nhập của môi trường do bạn dựng:

{{< workshop-screenshot file="16-app-login.png" description="Trang đăng nhập TINA trên URL CloudFront của bạn; che email và domain nếu chia sẻ." >}}

Nếu đăng nhập thất bại: kiểm tra Google OAuth client thuộc đúng project, URI callback khớp chính xác `StageUrl`, user có trong danh sách thử nghiệm, secret JSON có đúng hai key và Terminal đang Running. Kiểm tra log Terminal mà không công khai giá trị secret.

## 2. Thử một cuộc họp

Tạo cuộc họp thử có sự đồng ý của tất cả người tham gia. Trên TINA, tạo meeting theo giao diện, nhập URL cuộc họp thử và bắt đầu. Quan sát bot join, task bot xuất hiện trong ECS và trạng thái cuộc họp thay đổi. Meeting provider, admission hoặc quyền người tham gia có thể ảnh hưởng khả năng bot vào phòng; nếu bot không vào, ghi lỗi và kiểm tra log bot, runtime, quota Fargate, NAT và policy của phòng.

{{< workshop-screenshot file="17-test-meeting.png" description="Cuộc họp thử được phép và trạng thái bot; dùng dữ liệu giả, che thông tin người tham gia." >}}

Nếu đã bật VieGem hợp lệ và luồng audio thành công, nói một câu thử không nhạy cảm, chờ transcript xuất hiện và đối chiếu nội dung. Nếu không bật ASR hoặc chưa có transcript, ghi **chưa đạt/chưa kiểm thử**, không dùng ảnh minh họa giả.

{{< workshop-screenshot file="18-test-transcript.png" description="Transcript của câu thử không nhạy cảm sau khi ASR hoạt động." >}}

Kết thúc meeting và kiểm tra task bot dừng. Nếu ghi âm được bật, kiểm tra metadata object của meeting thử trong bucket riêng; không đưa audio hoặc transcript riêng tư vào báo cáo.

## 3. Ghi kết quả thật

| Kiểm tra | Kết quả mong đợi | Ghi nhận |
| --- | --- | --- |
| Web | URL CloudFront hiển thị Terminal | Pass/Fail và thời điểm |
| Đăng nhập | Tài khoản thử Cognito hoặc Google vào được TINA | Pass/Fail, không ghi secret |
| ECS | Runtime, core và Terminal ổn định, target healthy | desired/running, event |
| Meeting | Bot vào được phòng thử và dừng sau cuộc họp | Kết quả thật |
| Phiên âm | Transcript xuất hiện khi có ASR | Pass/Fail hoặc chưa cấu hình |

Stack `CREATE_COMPLETE` không thay thế kiểm thử này. Phiên bản workshop hiện chưa có bằng chứng chạy hoàn chỉnh trên tài khoản trắng; ghi lại mọi lỗi thực tế để sửa hướng dẫn trước khi giao người khác.
