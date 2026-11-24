---
title: "Worklog Tuần 11"
date: 2026-11-27
weight: 11
chapter: false
pre: " <b> 1.11. </b> "
---
### Mục tiêu tuần 11:

* Đánh giá kết quả kiểm thử, tìm điểm nghẽn và tối ưu chi phí cho kiến trúc AWS của TINA.
* Tăng tốc dịch trực tiếp tiếng Việt sang tiếng Anh và hoàn thiện pipeline CI/CD triển khai lên AWS.
* Kiểm tra bảo mật cơ bản (WAF, IAM), thử nghiệm phương án tắt dịch vụ ngoài giờ, Fargate Spot và VPC endpoint.

### Các công việc cần triển khai trong tuần này:

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Tăng tốc dịch trực tiếp từng cụm Việt → Anh, thêm cơ chế batch drain và giảm độ trễ. <br> - Bổ sung ngữ cảnh người nói/lượt thoại, ưu tiên đoạn cuối, lưu lựa chọn ngôn ngữ và làm sạch badge EN. <br> - Cập nhật tài liệu contract `meeting-translation.v2` cho chế độ hàng loạt và ngữ cảnh. <br> - Merge PR #26 (`enhance/streamming_translate_Vi2En`). | 23/11/2026 | 23/11/2026 |  |
| 3 | - Chuyển sang dịch qua HTTP trực tiếp, dọn worker tạm và thêm "thought bubble" STT mềm. <br> - Sửa cú pháp concurrency trong GitHub Actions, publish image `tina-tts`, cho phép bật gipformer theo lựa chọn và thêm `workflow_dispatch`. <br> - Khai báo `TINA_DIRECT_TRANSLATE` trong `config.v1` và dọn dung lượng đĩa cho bản build bot. <br> - Đánh giá kết quả kiểm thử, xác định các điểm nghẽn của luồng dịch và deploy. | 24/11/2026 | 24/11/2026 |  |
| 4 | - Publish `livekit-agent`, làm sạch manifest ECR và promote tag `demo`/`latest`. <br> - Đổi tên bộ kit và workflow `aws-demo` thành `aws`. <br> - Promote tag `:prod` thay vì `:demo` trên các workflow và bản deploy AWS. <br> - Rà soát phương án tối ưu chi phí: tắt Web/Agent/RDS/ElastiCache ngoài giờ, dùng Fargate Spot cho Bot/STT/TTS và VPC endpoint cho S3/ECR. | 25/11/2026 | 25/11/2026 |  |
| 5 | - Kiểm tra bảo mật cơ bản: web ACL của WAF, IAM task role tối thiểu quyền, Secrets Manager và KMS. <br> - Đối chiếu cấu hình production trên AWS (ECS/Fargate, ALB, CloudFront, Cognito, SES) với bản thiết kế trong proposal. <br> - Theo dõi chi phí bằng AWS Budgets và Cost Explorer, cập nhật lại ước tính trong proposal. | 26/11/2026 | 26/11/2026 |  |
| 6 | - Tổng hợp kết quả đánh giá, cập nhật proposal và tài liệu kiến trúc. <br> - Tổng kết tuần, cập nhật worklog và chuẩn bị cho các bước demo/tổng kết dự án. | 27/11/2026 | 27/11/2026 |  |

### Kết quả đạt được tuần 11:

* Tăng tốc và ổn định luồng dịch trực tiếp Việt → Anh thông qua PR #26: batch drain, ngữ cảnh speaker/turn, ưu tiên đoạn cuối và lưu lựa chọn ngôn ngữ.
* Chuyển sang dịch qua HTTP trực tiếp, dọn worker tạm và cập nhật tài liệu contract `meeting-translation.v2`.
* Hoàn thiện pipeline CI/CD trên GitHub Actions/GHCR: publish `tina-tts` và `livekit-agent`, làm sạch manifest ECR, promote tag `:prod`, đổi tên kit/workflow AWS và thêm `workflow_dispatch`.
* Rà soát các phương án tối ưu chi phí theo proposal: tắt dịch vụ ngoài giờ, Fargate Spot cho task cuộc họp, VPC endpoint cho S3/ECR và cảnh báo AWS Budgets.
* Kiểm tra bảo mật cơ bản với WAF và IAM task role tối thiểu quyền; đối chiếu cấu hình production với kiến trúc đã thiết kế.
* Nắm rõ hơn quy trình đánh giá điểm nghẽn, kiểm thử hồi quy và cập nhật tài liệu kiến trúc cho dự án.
