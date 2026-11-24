---
title: "Container & cổng"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

#### Liệt kê stack đang chạy

```bash
make ps
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Kỳ vọng `terminal`, `gateway`, `meeting-api`, `agent-api`, `admin-api`, `runtime`, `mcp`, `flows-api`, `postgres`, `redis`, `storage`, `storage-init` đều up. Job cài model một lần đã `Exited (0)`.

#### Cổng cần ghi

| Dịch vụ | Fresh clone | tina-production |
| --- | --- | --- |
| Terminal | 13000 | 23000 |
| API gateway | 18056 | 28056 |
| ASR control | 18007 | 18007 |
| VieGem | 18005 | 18005 |
| Gipformer | 18002 | 18002 |

- **Ảnh cần chụp:** `screenshot-06-containers-healthy.png`.
