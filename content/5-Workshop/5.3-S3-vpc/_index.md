---
title: "Pull và deploy code"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

#### 1. Clone repository

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD    # ghi lại commit này
```

Đặt `.env.keys` tương ứng ở gốc repo rồi `chmod 600 .env.keys`.

- **Ảnh cần chụp:** `screenshot-03-clone.png`.

#### 2. Xem trước bằng `make plan`

```bash
make plan
```

Lệnh in JSON gồm `project`, `docker_context`, `env_file`, `compose_files`, `services`, `viegem_device`, `meeting_voice`, `tts_credentials_ready`, `kws_models_source`, `native_viegem`, `container_viegem`, `images`, `volumes`, `order` và các dòng capability. Lệnh **chỉ đọc** — không tạo file hay secret. Ghi lại `project` và `viegem_device`.

- **Ảnh cần chụp:** `screenshot-04-make-plan.png`.

#### 3. Deploy bằng `make all`

```bash
make all
```

Diễn biến:

1. `mint-dev-env.sh` tạo `deploy/compose/.env` từ `.env.example` nếu thiếu và mint `ADMIN_TOKEN`, `INTERNAL_API_SECRET`, `TINA_FLOWS_API_KEY`, `TINA_FLOWS_TIMELINE_KEY`, `NEXTAUTH_SECRET`.
2. Preflight kiểm tra Docker ≥ 26 và tính nhất quán binding.
3. Build `tina/meet-join-env:dev`, bot Playwright (`BROWSER_IMAGE`, mặc định `tina/tina-bot:dev`), mọi image Compose và `agent-worker`; pull image registry; chạy job cài model.
4. `up -d --no-build --pull never --wait --wait-timeout 180`.
5. Kiểm tra readiness: service đang chạy và `healthy`, job một lần phải `Exited (0)`.
6. Cài/restore host controller ASR tại `127.0.0.1:18007`.
7. Cấp API key scoped (`SCOPES=bot,tx`) và in:

```text
Terminal UI: http://127.0.0.1:<TERMINAL_PORT>
API gateway: http://127.0.0.1:<API_GATEWAY_HOST_PORT>
API access provisioned. ...
TINA Compose ready: <project>
```

`make all` chỉ xác nhận **control-plane sẵn sàng**, không đo độ chính xác ASR hay cuộc họp thật — dùng `make probe` cho luồng đầy đủ.

- **Ảnh cần chụp:** `screenshot-05-make-all-success.png` (che API key).

#### Biến thể hữu ích

- `TINA_VIEGEM_DEVICE=cpu make all` — deploy CPU rõ ràng (không có fallback tự động khi lỗi GPU).
- `DOCKER_CONTEXT=orbstack make all` — khi Docker trỏ context khác.
- `make build` / `make bot` — chỉ build lại image hoặc bot.
- `make doctor` — kiểm tra readiness read-only.

#### Nội dung

- [Chuẩn bị](../5.2-Prerequiste/)
- [Kiểm tra dịch vụ](../5.4-s3-onprem/)
