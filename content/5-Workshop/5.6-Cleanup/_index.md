---
title: "Clean Up"
date: 2026-11-24
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

#### Stop the environment

```bash
make down
make ps
```

`make down` preserves database, recordings and workspaces — it only stops the services owned by this deployment and removes the owned native MPS LaunchAgent on macOS while keeping model files. `make ps` afterwards should show no owned containers running.

- **Screenshots:** `screenshot-11-make-down.png`.

#### Full teardown (only if you really want to delete data)

```bash
make -C deploy/compose destroy DESTROY=yes
```

This deletes the Compose volumes — a destructive operation. Do **not** run it during the practice session unless explicitly instructed.

#### Troubleshooting quick reference

| Symptom | Fix |
| --- | --- |
| Docker engine < 26 | Start Docker/OrbStack/WSL integration; `docker context show`; `DOCKER_CONTEXT=orbstack make all` |
| Dotenvx cannot decrypt | Restore the matching root `.env.keys`, `chmod 600` |
| Bot stuck at `requested` | `make bot`; check `docker image inspect "$BROWSER_IMAGE"` and `runtime` logs |
| `POST /bots` → 503 no transcription backend | Configure transcription in Settings → Models / `.env`, or send `{"transcribe_enabled":false}` |
| Port 18002 conflict | Stop the host LaunchAgent before Compose |
| VieGem `auto` fails on Windows | Run in WSL2 with NVIDIA driver + Docker GPU integration, or `TINA_VIEGEM_DEVICE=cpu make all` |
| KWS models missing | Provide `hey_tina.onnx` and `tina_oi.onnx` under `TINA_KWS_MODELS_DIR` |
| Agent: "No model credentials" | Configure a provider in Settings → Models |

#### Final screenshot checklist for the report

1. `screenshot-00-prereqs.png`
2. `screenshot-01-clone.png`
3. `screenshot-02-make-plan.png`
4. `screenshot-03-docker-build.png`
5. `screenshot-04-images-built.png`
6. `screenshot-05-make-all-success.png` (redact API key)
7. `screenshot-06-containers-healthy.png`
8. `screenshot-07-service-logs.png`
9. `screenshot-08-terminal.png`
10. `screenshot-09-asr-status.png`
11. `screenshot-10-make-probe.png`
12. `screenshot-11-make-down.png`
13. `screenshot-12-waf-iam-budgets.png` / `screenshot-13-aws-services.png` (if applicable)
