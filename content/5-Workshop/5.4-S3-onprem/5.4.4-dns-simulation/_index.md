---
title: "Full Journey Probe"
date: 2026-11-24
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

#### Run the journey probe

```bash
make probe
```

Stages: **S0** ready → **S1** spawn → **S2** schedule → **S3** boot → **S4** join → **S5** transcribe/WS → **S6** SSE live view → **S7** stop → **S8** log sweep. Each stage prints Expected / Actual / Verdict.

- With `BROWSER_IMAGE=mock-bot:dev` the run is deterministically GREEN.
- With the real bot at a dead synthetic meeting URL, a named `join_failure` is the truthful GREEN outcome.

#### CLI extras

```bash
make cli-install && export PATH="$HOME/.local/bin:$PATH"
tina status
tina doctor --full
tina logs runtime --tail 50
```

- **Screenshot:** `screenshot-11-make-probe.png`.
