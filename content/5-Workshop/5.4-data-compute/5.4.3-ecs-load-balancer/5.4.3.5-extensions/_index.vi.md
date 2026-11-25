---
title: "Phạm vi và tính năng mở rộng"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.4.3.5 </b> "
---

## Những gì đã cấu hình

Lộ trình này nhắm tới bản thử nghiệm meetings: Terminal, Google sign-in, core, Runtime khởi chạy bot ECS, lưu trữ, và tùy chọn VieGem. Các bước này vẫn cần được chạy trọn vẹn từ tài khoản trắng để xác nhận đăng nhập, bot và transcript.

## Những gì chưa được tái tạo đầy đủ

- **Workspace/agent workbench:** image Terminal hiện build `NEXT_PUBLIC_TERMINAL_MODE=meetings`; chưa cấu hình `WorkspacePilotUserIds`, agent API, worker, IAM, storage và model provider. Không hứa có giao diện hoặc chức năng agent giống hệ thống gốc.
- **Voice/TTS/wake word:** cần model, bản quyền và image khác; phải triển khai LiveKit/voice và cấu hình endpoint, secret, model, networking riêng. TINA không tự có dịch vụ phiên âm hay giọng nói được host sẵn.
- **Tích hợp và vận hành production:** chưa hướng dẫn SSO khác, tên miền riêng, sao lưu/khôi phục, HA, CI/CD và giám sát đầy đủ.

Source ở commit cố định có [hướng dẫn triển khai AWS gốc](https://github.com/poor-frog/TINA/blob/7d6bba8109f6eac51c0d8241a7083e3e364cf59d/deploy/aws/README.md) và các template bổ sung. Đó là điểm bắt đầu để mở rộng, không phải bằng chứng rằng các tính năng trên đã được kiểm thử trong workshop này. Trước khi bật, cần tự chuẩn bị secret và quyền hợp lệ, đối chiếu model license, xác thực tham số và test riêng từng tính năng.
