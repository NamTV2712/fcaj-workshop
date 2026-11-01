---
title: "Worklog Tuần 7"
date: 2026-10-31
weight: 7
chapter: false
pre: " <b> 1.7. </b> "
---

### Mục tiêu tuần 7

- Hiểu về tin nhắn và xử lý sự kiện trong microservices, bao gồm giao tiếp bất đồng bộ và hàng đợi tin nhắn.
- Thiết kế kiến trúc AWS của dự án, xác định các dịch vụ cần thiết và định nghĩa các luồng dữ liệu chính.
- Chuẩn bị không gian làm việc riêng biệt U4 – Trải nghiệm Cuộc họp Đã Giữ và xem lại cơ sở dự án hiện tại.
- Phân tích các yêu cầu chức năng và phi chức năng của U4 và chuẩn bị tài liệu thiết kế kỹ thuật và kế hoạch triển khai.

### Các công việc cần triển khai trong tuần này:

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Nghiên cứu tin nhắn đồng bộ và bất đồng bộ trong microservices và vai trò của kiến trúc hướng sự kiện. <br> - Khám phá Amazon SQS, Amazon SNS, và Amazon EventBridge để giao tiếp giữa các dịch vụ. <br> - Xem xét lại các lần thử lại, hàng đợi thư mục thư từ (DLQs), và xử lý sự kiện kháng lỗi. | 26/10/2026 | 26/10/2026 | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 3 | - Thiết kế kiến trúc AWS của dự án bằng cách sử dụng VPC, mạng con công khai/riêng, Trình cân bằng tải ứng dụng, và các khối lượng công việc EC2 riêng biệt cho Backend và xử lý ASR. <br> - Xác định các dịch vụ hỗ trợ, bao gồm Amazon S3, Amazon DynamoDB, Amazon Bedrock, AWS Lambda, và Amazon CloudWatch, dựa trên yêu cầu hệ thống. <br> - Hoàn thành sơ đồ kiến trúc và tài liệu luồng API REST, truyền âm thanh WebSocket, nhận dạng giọng nói, lưu trữ và xử lý AI. | 27/10/2026 | 27/10/2026 |  |
| 4 | - Kiểm tra thay đổi Git cục bộ, chuẩn bị không gian làm việc riêng biệt U4, đồng bộ với main và ghi lại commit cơ sở. <br> - Xem xét không gian và ý định AI-DLC liên quan, kiểm tra trạng thái đơn vị, và tuân theo quy trình nhắc/chỉnh U4. <br> - Cài đặt các dependencies từ lockfiles và chạy các kiểm tra backend và tiện ích mở rộng hiện có để ghi lại các vấn đề cơ sở. | 28/10/2026 | 28/10/2026 |  |
| 5 | - Xem xét các tiêu chí chấp nhận của ba câu chuyện chính và bảy câu chuyện chung của U4; xác định các sự phụ thuộc trên U1, U2, U3 và U5. <br> - Thiết kế các luồng lịch sử cuộc họp, chi tiết, xuất, xóa, nhận và điều hướng, bao gồm các thực thể dữ liệu và trạng thái tải/lỗi. <br> - Chuẩn bị tài liệu thiết kế chức năng và truy mãn; chỉ định các NFR về kiểm soát truy cập, phân trang, lưu trữ, độ tin cậy, khả năng tiếp cận và hiệu suất. | 29/10/2026 | 29/10/2026 |  |
| 6 | - Thiết kế hành vi phi chức năng của U4, bao gồm phân quyền, xóa cache, khôi phục thời gian chờ, xử lý nội dung an toàn và chẩn đoán. <br> - Định nghĩa tích hợp backend, quyền IAM, mẫu truy cập lịch sử cuộc họp và sự tương thích dữ liệu với các bản ghi U1 hiện có. <br> - Chuẩn bị Kế hoạch Sinh Mã, sở hữu mô-đun, thứ tự triển khai TDD, hướng dẫn kiểm tra và các mục phối hợp giữa các đơn vị để xem xét. | 30/10/2026 | 30/10/2026 |  |

### Kết quả đạt được tuần 7

- Nâng cao hiểu biết về giao tiếp hướng sự kiện trong microservices và vai trò của Amazon SQS, SNS và EventBridge.
- Tạo ra sơ đồ kiến trúc AWS và làm rõ các luồng công việc chính của ứng dụng và các kết nối giữa các dịch vụ.
- Thiết lập cơ sở phát triển U4 rõ ràng hơn, quy trình sở hữu và cách tiếp cận để xác định các vấn đề tồn tại trước đó.
- Tổ chức các tiêu chí chấp nhận, chức năng, sự phụ thuộc tích hợp và yêu cầu phi chức năng của U4.
- Chuẩn bị tài liệu thiết kế kỹ thuật và kế hoạch triển khai làm cơ sở để xem xét và phát triển tiếp theo.
