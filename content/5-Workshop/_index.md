---
title: "Workshop"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Build and Run Every TINA Service from Source

#### Overview

This workshop rebuilds the **entire TINA service stack from source code**. The GitHub repository is pulled only to provide the code — every service is then built locally from its Dockerfile and started as a container. The goal is to prove that the architecture in the proposal is reproducible: you do not rely on pre-built images, you construct and verify each component yourself.

The proposal defines five application services on Amazon ECS/Fargate — **Web serving, Bot (Playwright), STT (VieGem), TTS (VieNeu) and Agent** — plus supporting services and data stores. In this local workshop you build all of them from the cloned source:

| Architecture service | Built from source in this workshop |
| --- | --- |
| Web serving | `terminal`, `gateway`, `meeting-api`, `admin-api`, `dashboard` |
| Bot (Playwright) | `tina-bot` from the bot Dockerfile (`BROWSER_IMAGE`) |
| STT | `viegem` and/or `gipformer` from their service directories |
| TTS | `tts` (VieNeu) and `tts-models` |
| Agent | `agent-api`, `agent-worker`, `agent-reach`, `runtime`, `mcp` |
| Follow-up/flows | `flows-api`, `flows-worker`, `flows-mailbox` |
| Data stores | `postgres` (PostgreSQL), `redis` (Redis-compatible), `storage` (S3-compatible versitygw) |
| Identity/email/edge | Google OAuth in Terminal, Flows/Resend/SMTP mail, Caddy/gateway — plus the AWS equivalents documented in the proposal |

#### What "build from scratch" means here

1. **Pull the code** — clone `https://github.com/poor-frog/TINA.git`; the repo supplies Dockerfiles, Compose files and build scripts, not a finished system.
2. **Restore configuration** — place the matching `.env.keys` at the repo root so encrypted config can be read.
3. **Build every image locally** — `make build` (or `make all`, which builds before starting) compiles each service from its Dockerfile. Local tags follow `tina/v012-<service>:dev`; `BROWSER_IMAGE` defaults to `tina/tina-bot:dev`.
4. **Start and verify** — bring up the full stack, then inspect each container, health endpoint and log to confirm every service runs.
5. **Tear down** — `make down` stops the services while keeping data.

Pre-built registry images (`ghcr.io/poor-frog/tina-*:prod`) exist in the project, but this workshop deliberately **does not rely on them** — the build step is the point of the exercise.

#### Ports — important

| Service | Fresh clone | Pre-configured `tina-production` |
| --- | --- | --- |
| Terminal UI | `13000` | `23000` |
| API gateway | `18056` | `28056` |
| ASR control | `18007` | `18007` |
| VieGem | `18005` | `18005` |
| Gipformer | `18002` | `18002` |

Always trust the `Terminal UI:` / `API gateway:` lines printed by `make all`.

#### Step-by-step guide for the practice day (25/11/2026)

**Step 0 — Pull the code and prepare**

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
cp <your-secure-location>/.env.keys .   # matching private key
chmod 600 .env.keys
```
Verify Docker ≥ 26, `docker compose` with `up --wait`, Python 3.10+, `make`, Dotenvx and (on Linux/WSL2) NVIDIA driver visibility.

- **Screenshots:** `screenshot-00-prereqs.png`, `screenshot-01-clone.png`.

**Step 1 — Preview the build plan**

```bash
make plan
```
Note `project`, `services`, `images`, `volumes`, `viegem_device` and the capability lines. This is read-only.

- **Screenshot:** `screenshot-02-make-plan.png`.

**Step 2 — Build every service from source**

```bash
make build      # builds all Compose service images from Dockerfiles
make bot        # builds the Playwright bot image explicitly
```
If you prefer a single command that builds, starts and verifies: `make all`. On a fresh install it also mints the required secrets, runs model-install jobs, waits for health and provisions a scoped API key.

- **Screenshots:** `screenshot-03-docker-build.png`, `screenshot-04-images-built.png` (`docker images | grep tina`).

**Step 3 — Start the full stack**

```bash
make all
```
Capture the final `Terminal UI:` / `API gateway:` / `TINA Compose ready:` lines. Keep the printed API key private.

- **Screenshot:** `screenshot-05-make-all-success.png` (redact the key).

**Step 4 — Verify every service**

```bash
make ps
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker logs --tail 100 <container-name>
```
Check every service in the table above: Web serving, Bot, STT, TTS, Agent, flows, data stores, plus the health endpoints in the [Verify the services](5.4-s3-onprem/) page.

- **Screenshots:** `screenshot-06-containers-healthy.png`, `screenshot-07-service-logs.png`.

**Step 5 — Verify the AI/data flow**

Sign in to Terminal, check Settings → Models, live transcript, notes/summary, language dropdown (`Tiếng Việt / English / Song ngữ`), wake word and spoken replies; then run `make probe` for the S0–S8 journey.

- **Screenshots:** `screenshot-08-terminal.png`, `screenshot-09-asr-status.png`, `screenshot-10-make-probe.png`.

**Step 6 — Stop and clean up**

```bash
make down
```
Confirm services are stopped and data volumes preserved.

- **Screenshot:** `screenshot-11-make-down.png`.

#### Tips

* Native Windows Python/PowerShell is unsupported — use WSL2; Apple Silicon uses MPS; Linux/WSL2 with NVIDIA uses Docker CUDA. No automatic CPU fallback — use `TINA_VIEGEM_DEVICE=cpu make all` explicitly.
* A source build needs roughly **8 vCPUs / 16 GB RAM**; model install jobs download weights, so allow time.
* Never commit or screenshot `.env.keys`, API keys or OAuth secrets.

#### Content

1. [Workshop overview](5.1-workshop-overview/)
2. [Prerequiste](5.2-prerequiste/)
3. [Build from source](5.3-s3-vpc/)
4. [Verify the services](5.4-s3-onprem/)
5. [Cost and security checks](5.5-policy/)
6. [Clean up](5.6-cleanup/)
