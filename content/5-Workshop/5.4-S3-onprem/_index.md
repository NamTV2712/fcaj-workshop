---
title: "Verify the Services"
date: 2026-11-24
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

After building every image from source, confirm that each service in the architecture is actually running.

#### 1. Containers built from source

```bash
make ps
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker images | grep tina
docker logs --tail 100 <container-name>
```

Expected long-running services: `terminal`, `gateway`, `meeting-api`, `admin-api`, `dashboard`, `agent-api`, `agent-reach`, `runtime`, `mcp`, `flows-api`, `flows-worker`, `postgres`, `redis`, `storage`, `storage-init`, `tts`, plus `viegem` and/or `gipformer` depending on profiles. One-shot model jobs should show `Exited (0)`. Meeting bots appear as `tina-mtg-*` containers.

- **Screenshots:** `screenshot-06-containers-healthy.png`, `screenshot-07-service-logs.png`.

#### 2. Web serving and API gateway

Open the Terminal URL printed by `make all`, sign in with Google (first user becomes admin), then check the API:

```bash
export API_KEY=tina_...       # from make all or make -C deploy/compose provision-token
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

- **Screenshots:** `screenshot-08-terminal.png`.

#### 3. STT backends (VieGem / Gipformer)

```bash
curl -sS http://127.0.0.1:18002/health   # Gipformer (asr profile)
curl -sS http://127.0.0.1:18002/status
curl -sS http://127.0.0.1:18005/health   # VieGem (viegem profile / native)
curl -sS http://127.0.0.1:18005/status
```

Then in Terminal: **Settings → Models → Transcription** — select a managed model, confirm the account switch is on, and observe that the UI shows physical worker state separately from the account's enabled state. The controller on `18007` is authenticated; verify through the UI or `tina asr verify`.

- **Screenshot:** `screenshot-09-asr-status.png`.

#### 4. TTS and Agent

```bash
docker compose exec -T tts python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').status)"
curl -sS http://127.0.0.1:18100/health
tina asr verify
```

Configure a model provider in **Settings → Models** before testing Ask TINA. Then check the live transcript, notes, summary and the **Tiếng Việt / English / Song ngữ** dropdown.

#### 5. Full journey probe

```bash
make probe
```

Stages S0 ready → S1 spawn → S2 schedule → S3 boot → S4 join → S5 transcribe/WS → S6 SSE live view → S7 stop → S8 log sweep, each with Expected / Actual / Verdict. With `BROWSER_IMAGE=mock-bot:dev` the run is deterministically GREEN; with the real bot at a dead synthetic URL, a named `join_failure` is the truthful GREEN outcome.

- **Screenshot:** `screenshot-10-make-probe.png`.

#### CLI helper

```bash
make cli-install && export PATH="$HOME/.local/bin:$PATH"
tina status
tina doctor --full
tina logs runtime --tail 50
```
