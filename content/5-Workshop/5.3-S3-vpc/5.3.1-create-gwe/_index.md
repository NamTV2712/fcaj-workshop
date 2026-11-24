---
title: "Clone Repo and Restore Keys"
date: 2026-11-24
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

#### Clone

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
```

Record the short commit SHA in your notes.

#### Restore the private key

Copy the matching `.env.keys` from your secure backup to the repository root, then:

```bash
chmod 600 .env.keys
```

A newly generated key cannot decrypt this repository's Dotenvx-encrypted `deploy/compose/.env`. Never commit or paste the key value.

- **Screenshot:** `screenshot-03-clone.png` (repo cloned, commit visible; key value redacted if shown).
