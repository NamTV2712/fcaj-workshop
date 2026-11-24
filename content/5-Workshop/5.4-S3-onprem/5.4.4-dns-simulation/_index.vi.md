---
title: "Chạy toàn bộ hành trình"
date: 2026-11-24
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

#### Chạy probe

```bash
make probe
```

Các bước: **S0** ready → **S1** spawn → **S2** schedule → **S3** boot → **S4** join → **S5** transcribe/WS → **S6** SSE live view → **S7** stop → **S8** log sweep. Mỗi bước in Expected / Actual / Verdict.

- Với `BROWSER_IMAGE=mock-bot:dev` kết quả GREEN ổn định.
- Với bot thật tại URL cuộc họp giả, `join_failure` có tên là kết quả GREEN trung thực.

#### CLI bổ sung

```bash
make cli-install && export PATH="$HOME/.local/bin:$PATH"
tina status
tina doctor --full
tina logs runtime --tail 50
```

- **Ảnh cần chụp:** `screenshot-11-make-probe.png`.
