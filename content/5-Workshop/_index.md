---
title: "Workshop"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Deploy and Verify TINA on AWS

#### Overview

This workshop turns the TINA proposal into a hands-on session. The proposal describes a containerized system on **Amazon ECS with AWS Fargate** in `us-east-1`, where five services — **Web serving, Bot, STT (VieGem), TTS (VieNeu) and Agent** — work together to join meetings, transcribe audio in real time, answer questions and send follow-up emails. Amazon S3 stores recordings, RDS stores transcripts, ElastiCache carries live state, Amazon Bedrock powers the agent, and Cognito/SES/CloudFront/WAF/ALB handle identity, email and edge routing.

The repository already ships a **packaged build**: CI publishes container images (with `:prod`, `:demo` and `:latest` tags) and the deploy kit provides `make plan` / `make all`. Your task tomorrow is therefore not to build everything from scratch, but to **pull the code, start the packaged deployment, verify every service against the architecture, and capture screenshots as evidence**.

| Workshop component | Corresponding role in the TINA architecture |
| --- | --- |
| `make plan` | Read-only check of project, profiles and `viegem_device` before starting workers |
| `make all` | Installs models, builds/starts services and verifies ASR |
| Terminal UI (default port `13000`) | Web serving task — Next.js terminal, API and WebSocket gateway |
| API gateway (default port `18056`) | Backend routes used by Terminal and the Chrome extension |
| Ports `23000` / `28056` | Only for the pre-configured `tina-production` OrbStack instance — confirm with `make plan` and `make all` |
| ASR control (port `18007`) | Host controller that starts/stops managed Gipformer and VieGem workers |
| VieGem `18005` / Gipformer `18002` | STT workers — Vietnamese speech to text |
| ECR / GHCR images | Container images for Web, Bot, STT, TTS and Agent services |
| CloudWatch / Budgets | Logs, metrics, alarms and cost alerts from the proposal |

#### Preparation checklist (do this before tomorrow)

1. **Windows:** use **WSL2** with Docker Desktop's Linux/WSL integration and the NVIDIA Windows driver. Native Windows Python/PowerShell deployment is **not supported**.
2. **macOS:** start OrbStack or Docker Desktop first; Apple Silicon uses native PyTorch MPS for VieGem.
3. Install **Docker Engine 26+**, Compose with `up --wait`, **Python 3.10+** and **make**.
4. Install **Dotenvx** (`npm install --global @dotenvx/dotenvx` or the Homebrew tap on macOS).
5. Obtain the matching private **`.env.keys`** file from the owner through a secure channel. A newly generated key will not decrypt this repository's config. Never commit or paste the key.
6. Have the GitHub repository URL ready: `https://github.com/poor-frog/TINA.git`.

#### Step-by-step guide for the practice day (25/11/2026)

**Step 0 — Pull the code**

1. Clone and enter the repo:
   ```
   git clone https://github.com/poor-frog/TINA.git
   cd TINA
   ```
2. Place `.env.keys` at the repository root, then run `chmod 600 .env.keys`.
3. **Screenshots:** `w0-clone.png` (repo cloned), `w0-env-key.png` (key file present, with the value hidden).

**Step 1 — Preview the deployment (read-only)**

1. Run `make plan`. It shows the project, enabled profiles and the proposed `viegem_device` **without starting any worker**.
2. Confirm the profiles are `automation,asr,dashboard,viegem` and note the selected device (native MPS on Apple Silicon, Docker CUDA on WSL2/NVIDIA, or explicit CPU with `TINA_VIEGEM_DEVICE=cpu`).
3. **Screenshots:** `w1-plan.png` (full `make plan` output).

**Step 2 — Start everything**

1. Run `make all`. It installs models, builds services, starts them and verifies ASR with an authenticated audio probe.
2. Wait for the ready message containing the two URLs. On a fresh clone these are:
   - Terminal UI: `http://127.0.0.1:13000`
   - API gateway: `http://127.0.0.1:18056`
   If you are on the pre-configured `tina-production` instance they may be `23000` / `28056` — always trust the URLs printed by `make all`.
3. Keep the API key printed by `make all` private; do not screenshot its value.
4. **Screenshots:** `w2-make-all-start.png`, `w2-make-all-ready.png` (URLs visible, key masked).

**Step 3 — Verify the services in the architecture**

1. List running containers: `docker ps` (or `docker compose ps`). Identify Web, Bot, STT (VieGem/Gipformer), TTS and Agent containers and their ports.
2. Check logs for errors: `docker logs <container-name>` for each service.
3. Open the **Terminal UI** URL printed by `make all` in a browser, sign in with Google, and confirm the Terminal UI loads (first user becomes admin).
4. Confirm the API gateway responds:
   ```
   export API=http://127.0.0.1:18056   # 28056 on tina-production
   export API_KEY=tina_...             # from make all / provision-token
   curl -sS -o /dev/null -w '%{http_code}\n' "$API/health"
   curl -sS -H "X-API-Key: $API_KEY" "$API/meetings"
   ```
5. **Screenshots:** `w3-docker-ps.png`, `w3-logs.png`, `w3-terminal-ui.png`, `w3-gateway.png`.

**Step 4 — Verify the AI and data path**

1. In Settings → Models, confirm the transcription model (VieGem or Gipformer) is selected and the account switch is on.
2. Confirm a managed worker starts and the UI shows its physical state separately from the account's enabled state.
3. Open the meeting UI and check the live transcript, notes, summary and the **Tiếng Việt / English / Song ngữ** language dropdown.
4. Check that S3/RDS/ElastiCache/Bedrock/SES are reflected in the running stack (task definitions, environment configuration, CloudWatch logs) rather than assuming from the diagram.
5. **Screenshots:** `w4-models.png`, `w4-worker-state.png`, `w4-transcript.png`, `w4-language.png`, `w4-cloudwatch.png`.

**Step 5 — Check cost and security items from the proposal**

1. Confirm WAF is in front of CloudFront and only HTTPS is exposed publicly.
2. Confirm IAM task roles follow least privilege and secrets stay in Secrets Manager/KMS.
3. Confirm AWS Budgets alerts exist at 50%, 80% and 100% of the monthly limit.
4. **Screenshots:** `w5-waf.png`, `w5-iam.png`, `w5-budgets.png`.

**Step 6 — Stop the environment**

1. Run `make down`. It also stops/removes the owned native MPS LaunchAgent while retaining model files.
2. Confirm no owned containers/workers remain and no unexpected cost-generating resources are left running.
3. **Screenshots:** `w6-make-down.png`, `w6-after-down.png`.

#### Tips for a first-time run

* If `make all` fails on GPU/driver/kernel checks, there is **no automatic CPU fallback** — either fix the NVIDIA/WSL2 setup or explicitly use `TINA_VIEGEM_DEVICE=cpu make all`.
* A fresh transcription registry defaults to VieGem; existing personal/global preferences are unchanged.
* `make down` retains database, recordings and workspaces — it only stops the owned services.
* Keep `.env.keys`, the printed API key and any OAuth secrets out of screenshots and documentation.

#### Content

1. [Workshop overview](5.1-workshop-overview/)
2. [Prerequiste](5.2-prerequiste/)
3. [Pull and deploy the code](5.3-s3-vpc/)
4. [Verify the services](5.4-s3-onprem/)
5. [Cost and security checks](5.5-policy/)
6. [Clean up](5.6-cleanup/)
