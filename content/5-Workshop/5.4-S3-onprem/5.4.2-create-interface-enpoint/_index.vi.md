---
title: "Terminal UI & API gateway"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

#### Đăng nhập

Mở URL Terminal do `make all` in ra, đăng nhập Google — user đầu tiên trở thành admin. Callback URI phải là:

- `http://127.0.0.1:13000/api/auth/callback/google` (fresh clone), hoặc
- `http://127.0.0.1:23000/api/auth/callback/google` (tina-production).

#### Kiểm tra API

```bash
export API_KEY=tina_...
export API=http://127.0.0.1:18056
curl -sS -o /dev/null -w '%{http_code}\n' "$API/health"
curl -sS -H "X-API-Key: $API_KEY" "$API/meetings"
curl -sS http://127.0.0.1:18057/health
curl -sS http://127.0.0.1:18080/health
curl -sS http://127.0.0.1:18090/health
curl -sS http://127.0.0.1:18100/health
curl -sS http://127.0.0.1:18200/health
```

- **Ảnh cần chụp:** `screenshot-07-terminal-signed-in.png`, `screenshot-08-gateway-health.png`.
