---
title: "Tổng quan workshop"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

#### Kiến trúc TINA trong một trang

TINA là trợ lý cuộc họp self-hosted. Bot tham gia Google Meet/Zoom/Teams, stream âm thanh tới worker STT tiếng Việt, ghi transcript vào lưu trữ bền vững, dùng agent LLM tạo ghi chú/tóm tắt/dịch và trả lời "Ask TINA", phát câu trả lời qua TTS rồi gửi email follow-up sau cuộc họp.

Proposal đặt các thành phần này trên AWS:

- **Biên/truy cập:** CloudFront + AWS WAF → Application Load Balancer.
- **Định danh:** Amazon Cognito liên kết Google OAuth.
- **Tính toán:** Amazon ECS trên AWS Fargate — Web serving, Bot (Playwright), STT (VieGem), TTS (VieNeu), Agent.
- **Dữ liệu:** Amazon RDS (PostgreSQL), ElastiCache (Redis), Amazon S3.
- **AI/email:** Amazon Bedrock cho agent, Amazon SES gửi follow-up.
- **Vận hành:** ECR, GitHub Actions, CloudWatch, IAM, Secrets Manager, KMS, Budgets/Cost Explorer.

![Kiến trúc AWS của TINA](/images/2-Proposal/tina_aws_architecture.png)

#### Những gì đã được đóng gói sẵn

Repo cung cấp đầy đủ stack Compose local cùng image do CI build:

- **Image GHCR:** `ghcr.io/poor-frog/tina-<service>` cho `terminal`, `gateway`, `meeting-api`, `agent-api`, `admin-api`, `runtime`, `agent-worker`, `mcp`, `flows`, `dashboard`, `agent-reach`, `tts`, `bot`, `livekit-agent`, `viegem`, và tùy chọn `gipformer`. Tag bất biến theo commit SHA, sau đó job promote đẩy `:prod` và `:latest`.
- **Build local:** `tina/v012-<service>:dev`, với `BROWSER_IMAGE` mặc định `tina/tina-bot:dev`.
- **Entrypoint:** `make plan` (read-only), `make all` (seed env, build, start, verify), rồi `make doctor`, `make ps`, `make logs`, `make probe`, `make down`.

#### Ngày mai bạn sẽ kiểm tra gì

Bạn không tự tạo tài nguyên AWS — môi trường thực hành chạy bản tương đương local:

| Node kiến trúc | Tương đương local |
| --- | --- |
| Task ECS Fargate | Compose services: `terminal`, `gateway`, `meeting-api`, `agent-api`, `admin-api`, `runtime`, `mcp`, `flows-*`, `dashboard` |
| RDS / ElastiCache | Container `postgres` (17-alpine), `redis` (valkey:8-alpine) |
| S3 | Container `storage` (versitygw) + `storage-init` |
| Bot (Playwright) | Image `tina-bot:*`, container `tina-mtg-*` theo từng cuộc họp |
| STT | `viegem` (18005) và/hoặc `gipformer` (18002) |
| TTS / Agent | Container `tts` nội bộ, `agent-api` / `agent-worker` |
| CloudFront/WAF/ALB/Cognito/SES/Bedrock | Output `make plan`, sơ đồ docs và (nếu có) AWS CLI |

#### Cổng — lưu ý quan trọng

| Dịch vụ | Fresh clone | `tina-production` cấu hình sẵn |
| --- | --- | --- |
| Terminal UI | `13000` | `23000` |
| API gateway | `18056` | `28056` |
| ASR control | `18007` | `18007` |
| VieGem | `18005` | `18005` |
| Gipformer | `18002` | `18002` |

Luôn tin vào dòng `Terminal UI:` / `API gateway:` do `make all` in ra.

- **Ảnh cần chụp:** `screenshot-00-architecture-and-plan.png`.
