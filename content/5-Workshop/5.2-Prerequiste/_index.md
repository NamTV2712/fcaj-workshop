---
title: "Chuẩn bị"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

#### Danh sách kiểm tra môi trường

Chạy các lệnh sau và chụp kết quả trước khi deploy:

```bash
docker version --format '{{.Server.Version}}'   # phải >= 26
docker context show
python3 --version                               # >= 3.10 (3.12 cho Python gate)
make --version
dotenvx --version
```

Trên Linux/WSL2 ghi thêm thông tin GPU:

```bash
nvidia-smi -L
docker run --rm --gpus all --entrypoint nvidia-smi python:3.11-slim -L
```

**Quy tắc hệ điều hành**

- **Windows:** chạy trong **WSL2** với Docker Desktop tích hợp Linux/WSL và driver NVIDIA. Deploy native Windows Python/PowerShell **không được hỗ trợ**.
- **macOS Apple Silicon:** khởi động OrbStack hoặc Docker Desktop; VieGem chạy native PyTorch MPS qua LaunchAgent ở cổng `18005`.
- **Linux/WSL2 có NVIDIA:** VieGem chạy container Docker CUDA (wheels `cu130`), Gipformer vẫn CPU ở `18002`.

#### Cài Dotenvx và khôi phục key

```bash
npm install --global @dotenvx/dotenvx
# macOS:
# brew tap dotenvx/brew && brew trust dotenvx/brew && brew install dotenvx
```

Copy file `.env.keys` **tương ứng** từ nơi lưu trữ bảo mật vào **gốc repo**, rồi:

```bash
chmod 600 .env.keys
```

Key tự tạo sẽ **không** giải mã được `deploy/compose/.env` đã mã hóa. Không commit hay dán key vào bất cứ đâu.

#### Google OAuth

Tạo OAuth client loại Web application và đăng ký callback trùng origin Terminal:

- fresh clone: `http://127.0.0.1:13000/api/auth/callback/google`
- `tina-production`: `http://127.0.0.1:23000/api/auth/callback/google`

Nếu env dạng plain, điền `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `NEXTAUTH_URL`. Có thể mã hóa bằng `dotenvx encrypt -f deploy/compose/.env`.

#### Lỗi môi trường thường gặp

| Triệu chứng | Cách sửa |
| --- | --- |
| Docker < 26 | Khởi động Docker/OrbStack/WSL; `docker context show`; `DOCKER_CONTEXT=orbstack make all` |
| Dotenvx không giải mã | Cài Dotenvx, copy đúng `.env.keys`, `chmod 600` |
| TTS cần release key | Dùng chính `.env.keys` tương ứng |
| `ADMIN_TOKEN` placeholder | Bản mới sẽ tự mint; bản cũ phải rotate có chủ đích |
| Cổng 18007 bị chiếm | `make down` trước, hoặc đổi `TINA_ASR_CONTROL_PORT` |

- **Ảnh cần chụp:** `screenshot-01-prereqs.png`, `screenshot-02-env-keys-oauth.png` (che bí mật).
