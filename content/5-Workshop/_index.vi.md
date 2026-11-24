---
title: "Workshop"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Dựng lại toàn bộ service TINA từ source

#### Tổng quan

Workshop này **dựng lại toàn bộ stack service TINA từ mã nguồn**. Code trên GitHub chỉ được pull về để cung cấp source — mỗi service sau đó được build locally từ Dockerfile của chính nó và khởi chạy dưới dạng container. Mục tiêu là chứng minh kiến trúc trong Proposal có thể tái tạo được: bạn không dùng image đóng gói sẵn, mà tự dựng và kiểm chứng từng thành phần.

Proposal định nghĩa 5 service ứng dụng trên ECS/Fargate — **Web serving, Bot (Playwright), STT (VieGem), TTS (VieNeu) và Agent** — cùng các service hỗ trợ và kho dữ liệu. Trong workshop local này bạn build tất cả từ source vừa clone:

| Service kiến trúc | Build từ source trong workshop |
| --- | --- |
| Web serving | `terminal`, `gateway`, `meeting-api`, `admin-api`, `dashboard` |
| Bot (Playwright) | `tina-bot` từ Dockerfile của bot (`BROWSER_IMAGE`) |
| STT | `viegem` và/hoặc `gipformer` từ thư mục service tương ứng |
| TTS | `tts` (VieNeu) và `tts-models` |
| Agent | `agent-api`, `agent-worker`, `agent-reach`, `runtime`, `mcp` |
| Follow-up/flows | `flows-api`, `flows-worker`, `flows-mailbox` |
| Kho dữ liệu | `postgres` (PostgreSQL), `redis`, `storage` (versitygw tương đương S3) |
| Định danh/email/biên | Google OAuth trong Terminal, Flows/Resend/SMTP, Caddy/gateway — cùng bản AWS tương ứng trong proposal |

#### "Dựng từ đầu" nghĩa là gì ở đây

1. **Pull code** — clone `https://github.com/poor-frog/TINA.git`; repo chỉ cung cấp Dockerfile, Compose file và build script, không phải hệ thống hoàn chỉnh.
2. **Khôi phục cấu hình** — đặt `.env.keys` tương ứng ở gốc repo để đọc config đã mã hóa.
3. **Build mọi image locally** — `make build` (hoặc `make all` build trước khi chạy) biên dịch từng service từ Dockerfile. Tag local dạng `tina/v012-<service>:dev`; `BROWSER_IMAGE` mặc định `tina/tina-bot:dev`.
4. **Khởi chạy & kiểm tra** — chạy toàn bộ stack rồi soi từng container, health endpoint và log để xác nhận mọi service chạy được.
5. **Dừng/dọn** — `make down` dừng service nhưng giữ dữ liệu.

Repo có sẵn image registry (`ghcr.io/poor-frog/tina-*:prod`), nhưng workshop này **cố tình không dùng** — bước build chính là nội dung cần thực hành.

#### Cổng — lưu ý quan trọng

| Dịch vụ | Fresh clone | `tina-production` cấu hình sẵn |
| --- | --- | --- |
| Terminal UI | `13000` | `23000` |
| API gateway | `18056` | `28056` |
| ASR control | `18007` | `18007` |
| VieGem | `18005` | `18005` |
| Gipformer | `18002` | `18002` |

Luôn tin vào dòng `Terminal UI:` / `API gateway:` do `make all` in ra.

#### Hướng dẫn thực hành ngày 25/11/2026

**Bước 0 — Pull code & chuẩn bị**

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
cp <duong-dan-bao-mat>/.env.keys .   # key riêng tương ứng
chmod 600 .env.keys
```
Kiểm tra Docker ≥ 26, Compose hỗ trợ `up --wait`, Python 3.10+, `make`, Dotenvx và (Linux/WSL2) driver NVIDIA.

- **Ảnh cần chụp:** `screenshot-00-prereqs.png`, `screenshot-01-clone.png`.

**Bước 1 — Xem kế hoạch build**

```bash
make plan
```
Ghi lại `project`, `services`, `images`, `volumes`, `viegem_device` và các dòng capability. Lệnh chỉ đọc.

- **Ảnh cần chụp:** `screenshot-02-make-plan.png`.

**Bước 2 — Build từng service từ source**

```bash
make build      # build mọi image Compose từ Dockerfile
make bot        # build riêng image bot Playwright
```
Nếu muốn một lệnh build + chạy + kiểm tra: `make all`. Ở bản cài mới, lệnh này cũng mint secret cần thiết, chạy job cài model, chờ health và cấp API key scoped.

- **Ảnh cần chụp:** `screenshot-03-docker-build.png`, `screenshot-04-images-built.png` (`docker images | grep tina`).

**Bước 3 — Khởi chạy toàn bộ stack**

```bash
make all
```
Chụp các dòng `Terminal UI:` / `API gateway:` / `TINA Compose ready:`. Giữ API key bí mật.

- **Ảnh cần chụp:** `screenshot-05-make-all-success.png` (che key).

**Bước 4 — Kiểm tra từng service**

```bash
make ps
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker logs --tail 100 <ten-container>
```
Kiểm tra mọi service trong bảng trên: Web serving, Bot, STT, TTS, Agent, flows, kho dữ liệu cùng các health endpoint ở trang [Kiểm tra dịch vụ](5.4-s3-onprem/).

- **Ảnh cần chụp:** `screenshot-06-containers-healthy.png`, `screenshot-07-service-logs.png`.

**Bước 5 — Kiểm tra luồng AI/dữ liệu**

Đăng nhập Terminal, kiểm tra Settings → Models, transcript trực tiếp, ghi chú/tóm tắt, dropdown ngôn ngữ (**Tiếng Việt / English / Song ngữ**), wake word và câu trả lời bằng giọng nói; rồi chạy `make probe` cho hành trình S0–S8.

- **Ảnh cần chụp:** `screenshot-08-terminal.png`, `screenshot-09-asr-status.png`, `screenshot-10-make-probe.png`.

**Bước 6 — Dừng và dọn**

```bash
make down
```
Xác nhận service đã dừng và volume dữ liệu vẫn giữ lại.

- **Ảnh cần chụp:** `screenshot-11-make-down.png`.

#### Mẹo

* Windows native Python/PowerShell không được hỗ trợ — dùng WSL2; Apple Silicon dùng MPS; Linux/WSL2 có NVIDIA dùng Docker CUDA. Không có fallback CPU tự động — dùng rõ `TINA_VIEGEM_DEVICE=cpu make all`.
* Build từ source cần khoảng **8 vCPU / 16 GB RAM**; job cài model tải weight nên cần thời gian.
* Không commit hay chụp `.env.keys`, API key hay secret OAuth.

#### Nội dung

1. [Tổng quan workshop](5.1-workshop-overview/)
2. [Chuẩn bị](5.2-prerequiste/)
3. [Build từ source](5.3-s3-vpc/)
4. [Kiểm tra dịch vụ](5.4-s3-onprem/)
5. [Kiểm tra chi phí & bảo mật](5.5-policy/)
6. [Dọn dẹp](5.6-cleanup/)
