---
title: "Worklog Tuần 9"
date: 2026-11-14
weight: 9
chapter: false
pre: " <b> 1.9. </b> "
---
### Mục tiêu tuần 9:

* Làm quen và đóng góp vào dự án TINA — hệ thống meeting bot & transcription thời gian thực self-hosted.
* Triển khai, cải thiện trợ lý giọng nói cuộc họp (meeting voice assistant), Knowledge graph và hạ tầng CI/test.
* Làm việc theo nhánh/PR, tuân thủ quy trình review và tiêu chuẩn CI của dự án.

### Các công việc cần triển khai trong tuần này:

| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Làm quen repository TINA: đọc README, AGENTS.md, CONTRIBUTING.md và tìm hiểu kiến trúc (meeting bot, ASR, translation, Knowledge graph, voice assistant). <br> - Chuẩn bị môi trường development: cài Dotenvx, cấu hình private key, chạy `make plan` / `make all`. <br> - Tìm hiểu luồng retrieval & playback của meeting voice assistant, bắt đầu cải thiện độ chính xác và trải nghiệm phát lại. | 09/11/2026 | 09/11/2026 |  |
| 3 | - Gia cố runtime voice assistant self-hosted; cải thiện grounded answers và stage diagnostics. <br> - Hiển thị LiveKit voice defaults khi chưa chọn meeting. <br> - Sửa lỗi giữ audio ASR qua cửa sổ 30 giây. <br> - Thêm Knowledge sidebar & graph riêng biệt; chia sẻ root Dotenvx key với TTS. | 10/11/2026 | 10/11/2026 |  |
| 4 | - Khôi phục CI gates cho PR #9, ổn định fixture voice preview, sửa lỗi CI Python và cài dependency test TTS. <br> - Merge PR #9: thêm self-hosted meeting voice assistant và Knowledge graph. <br> - Ổn định test: renamed speaker transcript event, subscribe acknowledgement, meeting knowledge proposal edit. <br> - Merge PR #10: sửa speaker mapping trong CI. | 11/11/2026 | 11/11/2026 |  |
| 5 | - Mở rộng governed meeting voice assistant: clarification/progress handling, draft task & decision có owner review, approved-action scoped, retrieval đa meeting, tính toán deterministic, spoken source navigation; giữ meeting-source checks & playback receipts làm nguồn chuẩn. <br> - Cập nhật test coverage cho gateway voice navigation route. <br> - Sửa voice session identifiers thành kiểu string. <br> - Tích hợp trained TINA wakeword models vào repository. | 12/11/2026 | 13/11/2026 |  |
| 6 | - Tối ưu UI: compact Knowledge YAML metadata. <br> - Rà soát toàn bộ thay đổi, cập nhật tài liệu dự án (README, extension guide, contract docs). <br> - Tổng kết tuần và cập nhật worklog. | 13/11/2026 | 13/11/2026 |  |

### Kết quả đạt được tuần 9:

* Hiểu kiến trúc và quy trình phát triển của TINA, thiết lập được môi trường self-hosted (Docker/WSL2, Dotenvx, Terminal cổng 23000 và API gateway cổng 28056).
* Xây dựng và merge thành công self-hosted meeting voice assistant cùng Knowledge graph (PR #9), bao gồm Knowledge sidebar/graph riêng biệt.
* Cải thiện grounded voice answers, stage diagnostics, LiveKit voice defaults và khả năng retrieval/playback của trợ lý giọng nói.
* Tích hợp trained TINA wakeword models; khắc phục lỗi mất audio ASR qua cửa sổ 30 giây và chuyển voice session identifiers sang kiểu string.
* Khôi phục và ổn định CI: PR #9/#10, Python/TTS test dependencies, speaker mapping, subscribe/speaker/transcript event tests.
* Mở rộng governed voice assistant với clarification, owner-reviewed drafts, scoped actions, deterministic calculations và spoken source navigation.
* Nắm được quy trình PR/review của dự án và cách bảo vệ khóa bí mật (Dotenvx, không commit private key).
