---
title: "ASR, TTS and Agent"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

#### STT backends

```bash
curl -sS http://127.0.0.1:18002/health
curl -sS http://127.0.0.1:18002/status
curl -sS http://127.0.0.1:18005/health
curl -sS http://127.0.0.1:18005/status
```

In Terminal: **Settings → Models → Transcription**. Selecting a managed model starts it and verifies authenticated audio; the account switch only affects the signed-in account. The UI shows physical worker state separately from the account's enabled state. A worker with no demand retires after ten idle seconds.

#### TTS and Agent

```bash
docker compose exec -T tts python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').status)"
curl -sS http://127.0.0.1:18100/health
tina asr verify
```

Configure a provider in **Settings → Models** before testing Ask TINA. Then check the live transcript, notes, summary and the **Tiếng Việt / English / Song ngữ** dropdown.

- **Screenshots:** `screenshot-09-asr-status.png`, `screenshot-10-tts-agent-ready.png`.
