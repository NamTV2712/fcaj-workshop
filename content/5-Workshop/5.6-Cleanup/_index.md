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
3. `screenshot-02-vpc-subnets.png`
4. `screenshot-03-route-tables.png`
5. `screenshot-04-ecr-repos.png`
6. `screenshot-05-images-built.png`
7. `screenshot-06-stack-complete.png`
8. `screenshot-07-bedrock-ses.png`
9. `screenshot-08-cost-explorer.png`
10. `screenshot-13-ecs-alb-healthy.png`
11. `screenshot-14-cloudfront-waf.png`
12. `screenshot-15-cloudwatch-budgets-cost-explorer.png`
13. `screenshot-16-iam-secrets-kms.png`
14. `screenshot-17-app-running.png`
15. `screenshot-18-transcript.png`
