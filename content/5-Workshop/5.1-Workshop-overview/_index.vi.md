---
title: "Tổng quan workshop"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

#### Workshop này làm gì

Chúng ta **dựng lại toàn bộ stack service TINA từ mã nguồn**. Repo GitHub chỉ được pull về làm source; mỗi service sau đó được build locally từ Dockerfile và chạy như một container. Điều này chứng minh kiến trúc trong proposal tái tạo được mà không phụ thuộc vào image đóng gói sẵn.

#### Các service sẽ build

| Nhóm | Service build từ Dockerfile |
| --- | --- |
| Web / API | `terminal`, `gateway`, `meeting-api`, `admin-api`, `dashboard` |
| Bot | `tina-bot` (Playwright), tên image lấy từ `BROWSER_IMAGE` |
| STT | `viegem`, `gipformer` cùng job cài model `viegem-models`, `gipformer-models` |
| TTS | `tts` (VieNeu), `tts-models`, `meeting-voice-models` |
| Agent / runtime | `agent-api`, `agent-worker`, `agent-reach`, `runtime`, `mcp` |
| Follow-up / mail | `flows-api`, `flows-worker`, `flows-mailbox` |
| Kho dữ liệu | `postgres`, `redis`, `storage` (versitygw) + `storage-init` |
| Hỗ trợ | `meet-join-env`, host controller ASR ở `18007` |

![Kiến trúc AWS của TINA](/images/2-Proposal/tina_aws_architecture.png)

Sơ đồ là kiến trúc AWS đích. Ở local, Compose service thay cho ECS task; `postgres`/`redis`/`storage` thay cho RDS/ElastiCache/S3; Google OAuth và Flows mail thay cho Cognito/SES. CloudFront/WAF/ALB/Bedrock được mô tả trong proposal và chỉ kiểm tra bằng AWS CLI khi có credentials.

#### Build hay image đóng gói

Repo có đẩy image GHCR với tag `:prod` / `:latest`, nhưng **workshop này không dùng**. `make build` biên dịch từng service từ Dockerfile, tạo tag local như `tina/v012-terminal:dev`, `tina/v012-gateway:dev`, `tina/v012-viegem:dev` và `tina/tina-bot:dev`. `make all` chạy cùng bước build trước khi khởi động và kiểm tra stack.

#### Cổng

| Dịch vụ | Fresh clone | tina-production |
| --- | --- | --- |
| Terminal UI | 13000 | 23000 |
| API gateway | 18056 | 28056 |
| ASR control | 18007 | 18007 |
| VieGem | 18005 | 18005 |
| Gipformer | 18002 | 18002 |

Luôn tin vào URL do `make all` in ra.

- **Ảnh cần chụp:** `screenshot-00-prereqs.png`, `screenshot-02-make-plan.png`.
