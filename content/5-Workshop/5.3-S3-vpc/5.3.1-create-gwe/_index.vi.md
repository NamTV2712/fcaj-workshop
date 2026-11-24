---
title: "Clone repo & khôi phục key"
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

Ghi lại commit ngắn vào notes.

#### Khôi phục key riêng

Copy `.env.keys` tương ứng từ nơi lưu trữ bảo mật vào gốc repo, rồi:

```bash
chmod 600 .env.keys
```

Key tự tạo không giải mã được `deploy/compose/.env` đã mã hóa Dotenvx. Không commit hay dán giá trị key.

- **Ảnh cần chụp:** `screenshot-03-clone.png`.
