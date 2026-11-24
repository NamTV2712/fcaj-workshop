---
title: "Build from Source"
date: 2026-11-24
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

#### 1. Pull the code

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
```

The repository supplies Dockerfiles, Compose files and build scripts — it is the source input, not a finished deployment.

#### 2. Restore configuration

Copy the matching `.env.keys` to the repository root and protect it:

```bash
chmod 600 .env.keys
```

A newly generated key cannot decrypt the repository's encrypted config. Never commit or paste the key.

#### 3. Preview the build plan

```bash
make plan
```

Read-only output: `project`, `services`, `images`, `volumes`, `viegem_device`, capability lines. Note the full list of `images` you are about to build.

- **Screenshot:** `screenshot-02-make-plan.png`.

#### 4. Build every service from its Dockerfile

```bash
make build       # all Compose service images
make bot         # Playwright bot image explicitly (BROWSER_IMAGE)
```

This compiles each service locally — no `ghcr.io/poor-frog/tina-*:prod` image is pulled for the application services. Resulting local tags include `tina/v012-<service>:dev` and `tina/tina-bot:dev`. Model-install jobs (`viegem-models`, `gipformer-models`, `tts-models`, `meeting-voice-models`) run as part of the full deployment.

- **Screenshots:** `screenshot-03-docker-build.png`, `screenshot-04-images-built.png` (`docker images | grep tina`).

#### 5. Start and verify in one command (optional)

```bash
make all
```

Builds (if needed), seeds ignored `.env` with minted secrets, starts the stack with `up -d --wait`, checks health, installs/restores the ASR controller on `18007`, provisions a scoped API key (`SCOPES=bot,tx`) and prints the Terminal/API URLs.

- **Screenshot:** `screenshot-05-make-all-success.png` (redact the key).

#### Useful variants

- `TINA_VIEGEM_DEVICE=cpu make all` — explicit CPU build/run (no automatic fallback after a failed GPU check).
- `DOCKER_CONTEXT=orbstack make all` — select the OrbStack context.
- `make doctor` — read-only readiness check.

#### Content

- [Prerequisites](../5.2-Prerequiste/)
- [Verify the services](../5.4-s3-onprem/)
