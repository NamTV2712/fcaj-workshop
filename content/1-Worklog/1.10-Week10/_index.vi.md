---
title: "Worklog Tuần 10"
date: 2026-11-21
weight: 10
chapter: false
pre: " <b> 1.10. </b> "
---
### Mục tiêu tuần 10:

* Tiếp tục đóng góp vào dự án TINA, tập trung vào các nhánh `demo/aws` và `fix/post-meeting-mail-report`.
* Khôi phục và cải thiện luồng báo cáo follow-up sau cuộc họp; chuẩn hóa lựa chọn AWS VieGem và đồng bộ voice capture.
* Rèn luyện quy trình làm việc với nhánh, hợp nhất `main`, xử lý CI và cập nhật tài liệu kiến trúc.

### Các công việc cần triển khai trong tuần này:

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Khôi phục lựa chọn AWS VieGem và căn chỉnh timing voice capture. <br> - Căn chỉnh endpoint STT theo đồng hồ capture và loại bỏ các biến thể chính tả wake-name thu được từ STT. <br> - Hợp nhất `main` vào nhánh `demo/aws`; đưa shared formatter vào bản build Lite và dọn dẹp voice prefix. <br> - Làm mới code graph sau khi tích hợp `main` và merge PR #12 vào `main`. | 16/11/2026 | 16/11/2026 |  |
| 3 | - Theo dõi, đối chiếu các thay đổi về mail từ các nhánh `feat/post-meeting-email`, `feat/mail-delivery-config`, `fix/shared-smtp-config`. <br> - Tìm hiểu cấu hình SMTP/Resend dùng chung, email follow-up có thương hiệu và đính kèm artifact link. <br> - Tái tạo lỗi thiếu báo cáo follow-up sau cuộc họp, chuẩn bị nhánh `fix/post-meeting-mail-report`. | 17/11/2026 | 17/11/2026 |  |
| 4 | - Khôi phục luồng báo cáo follow-up sau cuộc họp (fix(flows): restore post-meeting follow-up reports). <br> - Tạo lại mô hình luồng báo cáo trong tài liệu kiến trúc và làm mới generated follow-up view. <br> - Xử lý trường hợp thiếu behavior capability; hợp nhất `main` vào nhánh fix. <br> - Merge PR #20 (`fix/post-meeting-mail-report`) vào `main`. | 18/11/2026 | 18/11/2026 |  |
| 5 | - Kiểm tra hồi quy sau khi merge PR #12 và PR #20: luồng ASR/voice, wake-word và báo cáo follow-up. <br> - Đối chiếu fixture và test của luồng mail, đảm bảo module reload không làm sai lệch dữ liệu kiểm thử. <br> - Rà soát CI trên các bản build Lite và bản thường. | 19/11/2026 | 19/11/2026 |  |
| 6 | - Dọn dẹp, cập nhật tài liệu kiến trúc và worklog dự án. <br> - Tổng kết các thay đổi trong tuần, ghi chú các điểm cần theo dõi cho tuần sau. | 20/11/2026 | 20/11/2026 |  |

### Kết quả đạt được tuần 10:

* Đưa nhánh `demo/aws` vào `main` thông qua PR #12: khôi phục lựa chọn AWS VieGem, đồng bộ STT với capture clock, loại bỏ wake-name sai chính tả và dọn voice prefix.
* Đưa shared formatter vào bản build Lite, làm mới code graph và giữ CI ổn định sau khi tích hợp `main`.
* Khôi phục thành công báo cáo follow-up sau cuộc họp và merge PR #20 từ nhánh `fix/post-meeting-mail-report`.
* Cập nhật mô hình luồng báo cáo trong tài liệu kiến trúc, làm mới follow-up view và xử lý trường hợp thiếu behavior capability.
* Phối hợp review các PR về mail của team (SMTP/Resend dùng chung, email follow-up có thương hiệu và artifact link).
* Thành thạo hơn quy trình merge nhiều nhánh với `main`, xử lý xung đột và kiểm tra hồi quy trước khi merge.
