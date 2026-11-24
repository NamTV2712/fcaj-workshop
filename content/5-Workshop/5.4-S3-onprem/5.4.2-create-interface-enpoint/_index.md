---
title: "Terminal UI and API Gateway"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

#### Sign in

Open the Terminal URL printed by `make all` and sign in with Google. The first successful sign-in becomes administrator. Google callback URI must be:

- `http://127.0.0.1:13000/api/auth/callback/google` (fresh clone), or
- `http://127.0.0.1:23000/api/auth/callback/google` (tina-production).

#### Check the API

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

- **Screenshots:** `screenshot-07-terminal-signed-in.png`, `screenshot-08-gateway-health.png`.
