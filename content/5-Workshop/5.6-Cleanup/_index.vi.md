---
title: "Dọn dẹp"
date: 2026-11-24
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

#### Dừng môi trường

```bash
make down
make ps
```

`make down` giữ database, bản ghi âm và workspace — chỉ dừng service thuộc quyền quản lý của deployment này và xóa LaunchAgent MPS native trên macOS nhưng vẫn giữ file model. `make ps` sau đó không nên còn container thuộc quyền quản lý.

- **Ảnh cần chụp:** `screenshot-11-make-down.png`.

#### Xóa hoàn toàn (chỉ khi thật sự muốn mất dữ liệu)

```bash
make -C deploy/compose destroy DESTROY=yes
```

Lệnh này xóa volume Compose — thao tác phá hủy. **Không** chạy trong buổi thực hành trừ khi được yêu cầu rõ ràng.

#### Tóm tắt xử lý sự cố

| Triệu chứng | Cách sửa |
| --- | --- |
| Docker < 26 | Khởi động Docker/OrbStack/WSL; `docker context show`; `DOCKER_CONTEXT=orbstack make all` |
| Dotenvx không giải mã | Copy đúng `.env.keys`, `chmod 600` |
| Bot kẹt ở `requested` | `make bot`; kiểm tra `docker image inspect "$BROWSER_IMAGE"` và log `runtime` |
| `POST /bots` → 503 thiếu backend phiên âm | Cấu hình trong Settings → Models / `.env`, hoặc gửi `{"transcribe_enabled":false}` |
| Cổng 18002 xung đột | Dừng LaunchAgent host trước khi chạy Compose |
| VieGem `auto` lỗi trên Windows | Chạy WSL2 với driver NVIDIA + Docker GPU integration, hoặc `TINA_VIEGEM_DEVICE=cpu make all` |
| Thiếu model KWS | Cung cấp `hey_tina.onnx`, `tina_oi.onnx` trong `TINA_KWS_MODELS_DIR` |
| Agent "No model credentials" | Cấu hình provider trong Settings → Models |

#### Checklist ảnh cuối cùng cho báo cáo

1. `screenshot-00-prereqs.png`
2. `screenshot-01-clone.png`
3. `screenshot-02-make-plan.png`
4. `screenshot-03-docker-build.png`
5. `screenshot-04-images-built.png`
6. `screenshot-05-make-all-success.png` (che API key)
7. `screenshot-06-containers-healthy.png`
8. `screenshot-07-service-logs.png`
9. `screenshot-08-terminal.png`
10. `screenshot-09-asr-status.png`
11. `screenshot-10-make-probe.png`
12. `screenshot-11-make-down.png`
13. `screenshot-12-waf-iam-budgets.png` / `screenshot-13-aws-services.png` (nếu có)
