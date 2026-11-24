---
title: "Kiểm tra các dịch vụ"
date: 2026-11-24
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

#### 1. Container

```bash
make ps
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker logs --tail 100 <ten-container>
```

Service chạy liên tục: `agent-reach`, `admin-api`, `runtime`, `agent-api`, `meeting-api`, `gateway`, `flows-api`, `mcp`, `terminal`, `postgres`, `redis`, `storage` + `storage-init`. Job cài model một lần phải `Exited (0)`. Bot họp xuất hiện dưới tên `tina-mtg-*`.

- **Ảnh cần chụp:** `screenshot-06-containers-healthy.png`.

#### 2. Web serving và API gateway

Mở URL `Terminal UI:` từ `make all`, đăng nhập Google (user đầu tiên thành admin), rồi kiểm tra API:

```bash
export API_KEY=tina_...       # từ make all hoặc make -C deploy/compose provision-token
export API=http://127.0.0.1:18056
curl -sS -o /dev/null -w '%{http_code}\n' "$API/health"                  # 200
curl -sS -H "X-API-Key: $API_KEY" "$API/meetings"                       # 2xx
curl -sS http://127.0.0.1:18057/health   # admin-api
curl -sS http://127.0.0.1:18080/health   # meeting-api
curl -sS http://127.0.0.1:18090/health   # runtime
curl -sS http://127.0.0.1:18100/health   # agent-api
curl -sS http://127.0.0.1:18200/health   # flows-api
curl -sS http://127.0.0.1:18900/health   # versitygw storage
```

- **Ảnh cần chụp:** `screenshot-07-terminal-signed-in.png`, `screenshot-08-gateway-health.png`.

#### 3. STT (VieGem / Gipformer)

```bash
curl -sS http://127.0.0.1:18002/health   # Gipformer (profile asr)
curl -sS http://127.0.0.1:18002/status
curl -sS http://127.0.0.1:18005/health   # VieGem (profile viegem / native)
curl -sS http://127.0.0.1:18005/status
```

Trong Terminal: **Settings → Models → Transcription** — chọn model managed, xác nhận công tắc tài khoản bật và quan sát UI hiển thị trạng thái vật lý của worker tách biệt với trạng thái bật. Controller ASR ở `18007` có xác thực; kiểm tra qua UI hoặc `tina asr verify`, không dùng curl không key.

- **Ảnh cần chụp:** `screenshot-09-asr-status.png`.

#### 4. TTS và Agent

```bash
docker compose exec -T tts python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').status)"
curl -sS http://127.0.0.1:18100/health
tina asr verify
```

Cấu hình provider trong **Settings → Models** (vd `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN` hoặc endpoint tương thích). Sau đó kiểm tra transcript trực tiếp, ghi chú, tóm tắt và dropdown **Tiếng Việt / English / Song ngữ** trong giao diện cuộc họp.

- **Ảnh cần chụp:** `screenshot-10-tts-agent-ready.png`.

#### 5. Chạy toàn bộ hành trình

```bash
make probe
```

Các bước S0 ready → S1 spawn → S2 schedule → S3 boot → S4 join → S5 transcribe/WS → S6 SSE live view → S7 stop → S8 log sweep, mỗi bước có Expected / Actual / Verdict. Với `BROWSER_IMAGE=mock-bot:dev` kết quả GREEN ổn định; với bot thật tại URL giả, `join_failure` có tên là kết quả GREEN trung thực.

- **Ảnh cần chụp:** `screenshot-11-make-probe.png`.

#### CLI hỗ trợ

```bash
make cli-install && export PATH="$HOME/.local/bin:$PATH"
tina status
tina doctor --full
tina logs runtime --tail 50
tina open terminal
```
