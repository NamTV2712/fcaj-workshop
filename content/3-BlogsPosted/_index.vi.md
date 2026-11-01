---
title: "Các bài blogs đã đăng"
date: 2026-10-22
weight: 3
chapter: false
pre: " <b> 3. </b> "
---

Trong quá trình thực tập tại AWS First Cloud AI Journey, mình đã dành thời gian nghiên cứu các bài viết từ AWS Blog, kết hợp với trải nghiệm thực tế từ các hands-on lab và quá trình học tập hàng ngày để viết các bài chia sẻ kỹ thuật. Mỗi bài blog đều tập trung vào một chủ đề cụ thể, giúp mình tổng hợp kiến thức, chia sẻ kinh nghiệm cũng như giới thiệu các giải pháp và thực hành tốt nhất (Best Practices) trên AWS. Mục tiêu của mình là đóng góp cho cộng đồng AWS Study Group bằng những nội dung thực tế, dễ tiếp cận và có thể áp dụng trực tiếp vào công việc hàng ngày.

Các bài viết đã đăng trên AWS Study Group:

### [Blog 1 - Amazon Transcribe vs OpenAI Whisper: Giải pháp Nhận dạng Giọng nói-Văn bản nào phù hợp tiếng Việt?](3.1-Blog1/)

Amazon Transcribe và OpenAI Whisper cùng giải quyết bài toán chuyển giọng nói thành văn bản nhưng theo hai hướng khác nhau: một dịch vụ được AWS quản lý hoàn toàn và một mô hình mã nguồn mở có thể tự triển khai. Bài viết so sánh chất lượng nhận dạng tiếng Việt, mô hình triển khai, chi phí vận hành và sự đánh đổi giữa tính tiện lợi và khả năng kiểm soát. Nội dung cũng trình bày các kiến trúc AWS thực tế, từ phiên âm hàng loạt đến gần thời gian thực, đồng thời hướng dẫn cách đánh giá khách quan bằng Word Error Rate (WER) và Character Error Rate (CER). Thay vì mặc định một giải pháp là tốt hơn, bài viết chỉ ra cách benchmark cả hai trên cùng một tập dữ liệu tiếng Việt để lựa chọn dựa trên độ chính xác, ngân sách và yêu cầu vận hành.

### [Blog 2 - Từ Bản transcript Cuộc họp sang Nhiệm vụ Notion với DynamoDB Streams, Lambda và Bedrock](3.2-Blog2/)

Bài viết mô tả một pipeline hướng sự kiện tự động khởi chạy khi bản transcript cuộc họp được đánh dấu hoàn thành trong DynamoDB. DynamoDB Streams kích hoạt AWS Lambda, hàm này đọc transcript từ Amazon S3, gọi Amazon Bedrock để trích xuất các mục hành động và lưu các nhiệm vụ đề xuất để con người xem xét trước khi tạo trong Notion. Nội dung giải thích chi tiết từng bước, bao gồm Lambda handler, thiết kế prompt, kiểm tra idempotency, bước xác nhận của con người và các cân nhắc về chi phí. Bài viết cũng thảo luận cách mở rộng mô hình này cho email, ticket hỗ trợ, transcript tổng đài và các công cụ quản lý nhiệm vụ khác, biến nó thành một blueprint tái sử dụng cho tự động hóa serverless.

### [Blog 3 - Amazon Nova 2.5 Sonic: Từ Trợ lý Giọng nói đến Trợ lý Giọng nói Thực hiện Nhiệm vụ](3.3-Blog3/)

Bài viết tìm hiểu Amazon Nova 2.5 Sonic, mô hình speech-to-speech trên Amazon Bedrock hướng tới việc thay thế pipeline STT → LLM → TTS truyền thống bằng một mô hình thời gian thực duy nhất. Nội dung đề cập đến tương tác giọng nói độ trễ thấp, barge-in, gọi công cụ, gọi công cụ bất đồng bộ và phiên đa phương thức, sau đó trình bày cách kết hợp Nova Sonic với AgentCore Runtime, Gateway, Lambda và DynamoDB để xây dựng một trợ lý giọng nói hoàn chỉnh. Bài viết cũng phân tích các trường hợp sử dụng thực tế, giới hạn ngôn ngữ hiện tại, chi phí, yêu cầu vận hành và khi nào một dịch vụ phiên âm đơn giản như Amazon Transcribe vẫn là lựa chọn phù hợp hơn.
