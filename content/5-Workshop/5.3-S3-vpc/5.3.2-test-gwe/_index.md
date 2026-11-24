---
title: "Preview and Deploy"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

#### Read-only preview

```bash
make plan
```

Note `project`, `docker_context`, `services`, `viegem_device` and the capability lines. Nothing is created.

#### Deploy

```bash
make all
```

Wait for the ready block:

```text
Terminal UI: http://127.0.0.1:<TERMINAL_PORT>
API gateway: http://127.0.0.1:<API_GATEWAY_HOST_PORT>
TINA Compose ready: <project>
```

On a fresh clone the ports are `13000` / `18056`; on the pre-configured `tina-production` instance they may be `23000` / `28056`. Always use the printed URLs.

- **Screenshots:** `screenshot-04-make-plan.png`, `screenshot-05-make-all-success.png` (redact API key).
