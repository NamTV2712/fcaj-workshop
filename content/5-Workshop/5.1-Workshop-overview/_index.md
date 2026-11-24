---
title: "Workshop Overview"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

#### What this workshop does

We rebuild the **entire TINA service stack from source code**. The GitHub repository is pulled only as source input; every service is then built locally from its Dockerfile and run as a container. This proves the proposal's architecture is reproducible without relying on any pre-built registry image.

#### Services you will build

| Group | Services built from Dockerfiles |
| --- | --- |
| Web / API | `terminal`, `gateway`, `meeting-api`, `admin-api`, `dashboard` |
| Bot | `tina-bot` (Playwright), image name from `BROWSER_IMAGE` |
| STT | `viegem`, `gipformer` plus model-install jobs `viegem-models`, `gipformer-models` |
| TTS | `tts` (VieNeu), `tts-models`, `meeting-voice-models` |
| Agent / runtime | `agent-api`, `agent-worker`, `agent-reach`, `runtime`, `mcp` |
| Follow-up / mail | `flows-api`, `flows-worker`, `flows-mailbox` |
| Data stores | `postgres`, `redis`, `storage` (versitygw) + `storage-init` |
| Support | `meet-join-env`, ASR host controller on `18007` |

![TINA AWS Architecture](/images/2-Proposal/tina_aws_architecture.png)

The diagram shows the target AWS architecture. Locally, Compose services stand in for the ECS tasks; `postgres`/`redis`/`storage` stand in for RDS/ElastiCache/S3; Google OAuth and Flows mail stand in for Cognito and SES. CloudFront/WAF/ALB/Bedrock are documented in the proposal and verified with AWS CLI only if credentials are available.

#### Build vs packaged image

The repository does publish GHCR images tagged `:prod` / `:latest`, but **this workshop does not use them**. `make build` compiles each service from its Dockerfile, producing local tags such as `tina/v012-terminal:dev`, `tina/v012-gateway:dev`, `tina/v012-viegem:dev` and `tina/tina-bot:dev`. `make all` runs the same build step before starting and verifying the stack.

#### Ports

| Service | Fresh clone | tina-production |
| --- | --- | --- |
| Terminal UI | 13000 | 23000 |
| API gateway | 18056 | 28056 |
| ASR control | 18007 | 18007 |
| VieGem | 18005 | 18005 |
| Gipformer | 18002 | 18002 |

Always trust the URLs printed by `make all`.

- **Screenshot:** `screenshot-00-prereqs.png` and `screenshot-02-make-plan.png`.
