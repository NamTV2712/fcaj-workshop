---
title: "Containers and Ports"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

#### List the running stack

```bash
make ps
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Expect `terminal`, `gateway`, `meeting-api`, `agent-api`, `admin-api`, `runtime`, `mcp`, `flows-api`, `postgres`, `redis`, `storage`, `storage-init` to be up. One-shot model jobs should have exited 0.

#### Ports to record

| Service | Fresh clone | tina-production |
| --- | --- | --- |
| Terminal | 13000 | 23000 |
| API gateway | 18056 | 28056 |
| ASR control | 18007 | 18007 |
| VieGem | 18005 | 18005 |
| Gipformer | 18002 | 18002 |

- **Screenshot:** `screenshot-06-containers-healthy.png`.
