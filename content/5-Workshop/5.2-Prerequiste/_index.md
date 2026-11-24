---
title: "Prerequisites"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

#### Environment checklist

Run these commands and capture the output before building:

```bash
docker version --format '{{.Server.Version}}'   # must be >= 26
docker context show
python3 --version                               # >= 3.10 (3.12 for Python gates)
make --version
dotenvx --version
```

A source build is heavier than pulling images: allow roughly **8 vCPUs / 16 GB RAM**. On Linux/WSL2 also record GPU visibility:

```bash
nvidia-smi -L
docker run --rm --gpus all --entrypoint nvidia-smi python:3.11-slim -L
```

**OS rules**

- **Windows:** run everything inside **WSL2** with Docker Desktop's Linux/WSL integration and the NVIDIA Windows driver. Native Windows Python/PowerShell is **not supported**.
- **macOS Apple Silicon:** start OrbStack or Docker Desktop; VieGem builds/runs as native PyTorch MPS via a LaunchAgent on port `18005`.
- **Linux/WSL2 with NVIDIA:** VieGem builds/runs as a Docker CUDA container (pinned `cu130` wheels); Gipformer stays CPU-only on `18002`.

#### Install Dotenvx and restore the key

```bash
npm install --global @dotenvx/dotenvx
# macOS alternative:
# brew tap dotenvx/brew && brew trust dotenvx/brew && brew install dotenvx
```

Copy the matching private `.env.keys` from your secure backup to the **repository root**, then:

```bash
chmod 600 .env.keys
```

A newly generated key will **not** decrypt this repository's Dotenvx-encrypted `deploy/compose/.env`. Never commit or paste the key.

#### Google OAuth

Create a Web application OAuth client and register the callback URI matching your Terminal origin:

- fresh clone: `http://127.0.0.1:13000/api/auth/callback/google`
- `tina-production`: `http://127.0.0.1:23000/api/auth/callback/google`

If the env file is plain, fill `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` and `NEXTAUTH_URL`. Optionally encrypt with `dotenvx encrypt -f deploy/compose/.env`.

#### Common environment failures

| Symptom | Fix |
| --- | --- |
| Docker engine < 26 | Start Docker/OrbStack/WSL integration; `docker context show`; `DOCKER_CONTEXT=orbstack make all` |
| Dotenvx cannot decrypt | Install Dotenvx, restore the **matching** `.env.keys`, `chmod 600` |
| TTS requires shared release key | Same matching `.env.keys` |
| `ADMIN_TOKEN` missing or placeholder | Fresh install mints it; an existing placeholder must be deliberately rotated |
| Port 18007 already owned | `make down` first, or override `TINA_ASR_CONTROL_PORT` |

- **Screenshots:** `screenshot-00-prereqs.png`, `screenshot-01-clone.png`.
