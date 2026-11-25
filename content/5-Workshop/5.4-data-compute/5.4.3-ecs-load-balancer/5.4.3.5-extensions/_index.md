---
title: "Scope and extensions"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.4.3.5 </b> "
---

## What is configured

This path targets a meetings test deployment: Terminal, Google sign-in, core services, Runtime launching ECS bot tasks, storage, and optional VieGem. These steps still need to be executed end-to-end on a clean account to verify sign-in, the bot, and transcription.

## What is not fully reproduced

- **Workspace/agent workbench:** the current Terminal image is built with `NEXT_PUBLIC_TERMINAL_MODE=meetings`; `WorkspacePilotUserIds`, the agent API, worker, IAM, storage, and model provider are not configured. Do not expect the same agent UI or capabilities as the full upstream system.
- **Voice/TTS/wake word:** requires different models, licenses, and images; you must deploy LiveKit/voice separately and configure its endpoints, secrets, models, and networking. TINA does not include a hosted transcription or voice service.
- **Production integrations and operations:** additional SSO providers, custom domains, backup/restore, high availability, CI/CD, and full observability are outside this guide.

The pinned commit includes the [upstream AWS deployment guide](https://github.com/poor-frog/TINA/blob/7d6bba8109f6eac51c0d8241a7083e3e364cf59d/deploy/aws/README.md) and additional templates. Treat them as a starting point for extensions rather than evidence that those features have been validated in this workshop. Before enabling them, prepare valid secrets and permissions, verify model licenses, validate parameters, and test each feature independently.
