---
title: "ASR, TTS & Agent"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

#### Backend STT

```bash
curl -sS http://127.0.0.1:18002/health
curl -sS http://127.0.0.1:18002/status
curl -sS http://127.0.0.1:18005/health
curl -sS http://127.0.0.1:18005/status
```

Trong Terminal: **Settings → Models → Transcription**. Chọn model managed sẽ khởi động worker và xác thực audio; công tắc tài khoản chỉ ảnh hưởng tài khoản đang đăng nhập. UI hiển thị trạng thái vật lý tách biệt với trạng thái bật của tài khoản. Worker không có nhu cầu dùng sẽ dừng sau mười giây.

#### TTS và Agent

```bash
docker compose exec -T tts python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').status)"
curl -sS http://127.0.0.1:18100/health
tina asr verify
```

Cấu hình provider trong **Settings → Models** trước khi thử Ask TINA. Sau đó kiểm tra transcript trực tiếp, ghi chú, tóm tắt và dropdown **Tiếng Việt / English / Song ngữ**.

- **Ảnh cần chụp:** `screenshot-09-asr-status.png`, `screenshot-10-tts-agent-ready.png`.
