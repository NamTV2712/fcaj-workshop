---
title: "Xem trước & deploy"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

#### Xem trước (read-only)

```bash
make plan
```

Ghi lại `project`, `docker_context`, `services`, `viegem_device` và các dòng capability. Lệnh không tạo file hay secret.

#### Deploy

```bash
make all
```

Đợi khối ready:

```text
Terminal UI: http://127.0.0.1:<TERMINAL_PORT>
API gateway: http://127.0.0.1:<API_GATEWAY_HOST_PORT>
TINA Compose ready: <project>
```

Fresh clone dùng `13000`/`18056`; bản `tina-production` có thể dùng `23000`/`28056`. Luôn dùng URL do `make all` in ra.

- **Ảnh cần chụp:** `screenshot-04-make-plan.png`, `screenshot-05-make-all-success.png` (che API key).
