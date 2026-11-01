---
title: "Blog 2"
date: 2026-10-28
weight: 2
chapter: false
pre: " <b> 3.2. </b> "
---

# Từ Bản transcript Cuộc họp sang Nhiệm vụ Notion: Khi DynamoDB Streams, Lambda và Bedrock Làm Cùng Nhau

Có một bản transcript hoàn chỉnh sau một cuộc họp không nhất thiết có nghĩa là vấn đề theo dõi đã được giải quyết. Một bản transcript có thể chứa hàng nghìn từ, trong khi thông tin hữu ích nhất thường đơn giản hơn nhiều: Ai phụ trách nhiệm vụ nào? Hạn mức là khi nào? Mục tiêu hành động nào vẫn cần quan tâm?

Một cách tiếp cận thực tế là kết hợp **Amazon DynamoDB Streams, AWS Lambda, và Amazon Bedrock** để trích xuất các mục hành động tự động và đồng bộ hóa chúng với Notion.

![Minh họa kiến trúc: từ transcript sang nhiệm vụ Notion](/images/3-BlogsPosted/Blog2.jpg)

## 1. Kiến trúc hoạt động như thế nào?

Hãy tưởng tượng rằng ai đó nói trong cuộc họp:

> "Lan sẽ hoàn thành API đăng nhập đến ngày 30 tháng 10."

Sau cuộc họp kết thúc, hệ thống có thể theo quy trình sau:

**Amazon DynamoDB và DynamoDB Streams**

Hệ thống backend cập nhật trạng thái cuộc họp thành `COMPLETED` trong DynamoDB. DynamoDB Streams bắt nắm sự thay đổi dữ liệu, và AWS Lambda có thể được cấu hình để xử lý sự kiện stream.

Phân tách hữu ích ở đây là backend không cần trực tiếp gọi toàn bộ quy trình AI. Phân tích sau cuộc họp có thể chạy độc lập.

**AWS Lambda**

Lambda đóng vai trò điều phối. Nó nhận sự kiện, truy xuất transcript tương ứng và chuẩn bị nội dung để xử lý bằng AI.

Thay vì sao chép một bản transcript dài vào Notion, hàm Lambda yêu cầu một mô hình sẵn có qua Amazon Bedrock xác định các mục hành động liên quan.

**Amazon Bedrock**

Mô hình ngôn ngữ biến nội dung cuộc trò chuyện thành dữ liệu có cấu trúc. Ví dụ:

- **Nhiệm vụ:** Hoàn thành API đăng nhập
- **Người phụ trách:** Lan
- **Hạn chót:** 30 tháng 10
- **Nguồn:** Đoạn transcript liên quan

Sau khi nhận phản hồi, Lambda xác thực dữ liệu và gọi Notion API để tạo một mục trong cơ sở dữ liệu nhiệm vụ.

## 2. Tại sao không xử lý tất cả trong backend?

Thời gian xử lý AI có thể thay đổi tùy theo độ dài transcript và mô hình được sử dụng.

Nếu toàn bộ quy trình được bao gồm trong yêu cầu chính, backend cũng phải xử lý các vấn đề về thời gian chờ, thử lại và thất bại từ các dịch vụ bên ngoài.

Kết hợp DynamoDB Streams với Lambda tách biệt việc cập nhật cơ sở dữ liệu khỏi phân tích AI. Backend chỉ cần lưu trữ trạng thái cuộc họp; một nhân viên riêng xử lý công việc tiếp theo.

## 3. Những cân nhắc thiết kế quan trọng

Có một số chi tiết cần xử lý cẩn thận.

Thứ nhất, một LLM có thể giao nhầm nhiệm vụ cho người khác hoặc phát sinh một hạn chót. Các trường không được hỗ trợ rõ ràng bởi transcript nên được để trống thay vì bị suy luận.

Thứ hai, các sự kiện DynamoDB Streams có thể được thử lại. Không có bảo vệ trùng lặp, cùng một nhiệm vụ có thể được tạo trong Notion nhiều hơn một lần. Một khóa idempotency gắn với mỗi sự kiện hoặc mục hành động có thể giúp ngăn chặn điều này.

Cuối cùng, các nhiệm vụ quan trọng có thể cần một bước xác nhận rõ ràng từ người dùng trước khi chúng được tạo hoặc cập nhật trong hệ thống bên ngoài.

## Kết luận

Phần thú vị của kiến trúc này không phải là bất kỳ dịch vụ đơn lẻ nào, mà là cách các dịch vụ bổ sung nhau.

DynamoDB Streams phát hiện sự thay đổi, Lambda điều phối xử lý, Bedrock biến ngôn ngữ tự nhiên thành thông tin có cấu trúc, và Notion làm cho kết quả trở nên có thể hành động.

Đây là một mô hình AI sinh tạo thực tế cho một Trợ lý Cuộc họp AI: di chuyển xa hơn việc lưu trữ bản transcript cuộc họp về phía giúp mọi người theo dõi công việc đã đồng ý trong cuộc họp.

## Tài liệu tham khảo

1. [AWS – DynamoDB Streams và Lambda Triggers](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html)
2. [Amazon Bedrock – Structured Outputs](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html)
3. [Notion – Create a Page API](https://developers.notion.com/reference/post-page)

---
**Bài viết đã đăng trên AWS Study Group:** [https://www.facebook.com/groups/awsstudygroupfcj/permalink/2318521822246110/?rdid=ZaQ8iG8gfsmGlEWb#](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2318521822246110/?rdid=ZaQ8iG8gfsmGlEWb#)
