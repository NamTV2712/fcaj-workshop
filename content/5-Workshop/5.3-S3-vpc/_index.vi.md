---
title: "Build từ source"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

#### 1. Pull code

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
```

Repo cung cấp Dockerfile, Compose file và build script — đây là source đầu vào, không phải bản deploy hoàn chỉnh.

#### 2. Khôi phục cấu hình

Copy `.env.keys` tương ứng vào gốc repo rồi bảo vệ:

```bash
chmod 600 .env.keys
```

Key tự tạo không giải mã được config đã mã hóa. Không commit hay dán key.

#### 3. Xem kế hoạch build

```bash
make plan
```

Output chỉ đọc gồm `project`, `services`, `images`, `volumes`, `viegem_device` và các dòng capability. Ghi lại danh sách `images` sắp build.

- **Ảnh cần chụp:** `screenshot-02-make-plan.png`.

#### 4. Build từng service từ Dockerfile

```bash
make build       # mọi image Compose service
make bot         # riêng image bot Playwright (BROWSER_IMAGE)
```

Bước này biên dịch từng service locally — **không** kéo image `ghcr.io/poor-frog/tina-*:prod` cho các service ứng dụng. Tag local tạo ra gồm `tina/v012-<service>:dev` và `tina/tina-bot:dev`. Các job cài model (`viegem-models`, `gipformer-models`, `tts-models`, `meeting-voice-models`) chạy trong bản deploy đầy đủ.

- **Ảnh cần chụp:** `screenshot-03-docker-build.png`, `screenshot-04-images-built.png` (`docker images | grep tina`).

#### 5. Chạy và kiểm tra trong một lệnh (tùy chọn)

```bash
make all
```

Build nếu cần, tạo `.env` với secret được mint, chạy stack với `up -d --wait`, kiểm tra health, cài/restore controller ASR ở `18007`, cấp API key scoped (`SCOPES=bot,tx`) và in URL Terminal/API.

- **Ảnh cần chụp:** `screenshot-05-make-all-success.png` (che key).

#### Biến thể hữu ích

- `TINA_VIEGEM_DEVICE=cpu make all` — build/chạy CPU rõ ràng (không có fallback tự động khi lỗi GPU).
- `DOCKER_CONTEXT=orbstack make all` — chọn context OrbStack.
- `make doctor` — kiểm tra readiness read-only.

#### Nội dung

- [Chuẩn bị](../5.2-Prerequiste/)
- [Kiểm tra dịch vụ](../5.4-s3-onprem/)
