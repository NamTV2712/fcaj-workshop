---
title: "Workshop Overview"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

#### TINA architecture in one page

TINA is a self-hosted meeting assistant. A bot joins Google Meet / Zoom / Teams, streams audio to a Vietnamese STT worker, writes transcript segments to durable storage, uses an LLM agent for notes, summaries, translation and "Ask TINA", speaks replies through TTS, and emails a follow-up after the meeting.

The proposal places these components on AWS:

- **Edge/entry:** CloudFront + AWS WAF → Application Load Balancer.
- **Identity:** Amazon Cognito with Google OAuth.
- **Compute:** Amazon ECS on AWS Fargate — Web serving, Bot (Playwright), STT (VieGem), TTS (VieNeu), Agent.
- **Data:** Amazon RDS (PostgreSQL) for transcripts, ElastiCache (Redis) for live state, Amazon S3 for recordings.
- **AI/email:** Amazon Bedrock for the agent, Amazon SES for follow-up emails.
- **Operations:** ECR, GitHub Actions, CloudWatch, IAM, Secrets Manager, KMS, Budgets/Cost Explorer.

![TINA AWS Architecture](/images/2-Proposal/tina_aws_architecture.png)

#### What is already packaged

The repository ships a complete local Compose stack plus CI-built container images:

- **GHCR images:** `ghcr.io/poor-frog/tina-<service>` for `terminal`, `gateway`, `meeting-api`, `agent-api`, `admin-api`, `runtime`, `agent-worker`, `mcp`, `flows`, `dashboard`, `agent-reach`, `tts`, `bot`, `livekit-agent`, `viegem`, and optionally `gipformer`. Immutable tags use the commit SHA, then the promote job publishes `:prod` and `:latest`.
- **Local source builds:** `tina/v012-<service>:dev`, with `BROWSER_IMAGE` defaulting to `tina/tina-bot:dev`.
- **Entrypoints:** `make plan` (read-only) and `make all` (seed env, build, start, verify), then `make doctor`, `make ps`, `make logs`, `make probe`, `make down`.

#### What you will actually verify tomorrow

You will not create the AWS resources yourself — the practice environment runs the local Compose equivalent:

| Architecture node | Local equivalent you will see |
| --- | --- |
| ECS Fargate tasks | Compose services: `terminal`, `gateway`, `meeting-api`, `agent-api`, `admin-api`, `runtime`, `mcp`, `flows-*`, `dashboard` |
| RDS / ElastiCache | `postgres` (17-alpine) and `redis` (valkey:8-alpine) containers |
| S3 | `storage` (versitygw) + `storage-init` container |
| Bot (Playwright) | `tina-bot:*` image, containers named `tina-mtg-*` spawned per meeting |
| STT | `viegem` (18005) and/or `gipformer` (18002) |
| TTS / Agent | internal `tts` container and `agent-api` / `agent-worker` |
| CloudFront/WAF/ALB/Cognito/SES/Bedrock | represented by `make plan` output, docs diagram and (if available) AWS CLI checks |

#### Ports — important

| Service | Fresh clone | Pre-configured `tina-production` |
| --- | --- | --- |
| Terminal UI | `13000` | `23000` |
| API gateway | `18056` | `28056` |
| ASR control | `18007` | `18007` |
| VieGem | `18005` | `18005` |
| Gipformer | `18002` | `18002` |

Always trust the `Terminal UI:` / `API gateway:` lines printed by `make all`.

- **Screenshot:** `screenshot-00-architecture-and-plan.png` (this architecture overview plus `make plan` output).
