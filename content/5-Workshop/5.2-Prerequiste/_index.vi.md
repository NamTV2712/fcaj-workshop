---
title: "Chuẩn bị"
date: 2026-11-24
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

#### Công cụ local

```bash
git --version
aws --version
docker version --format '{{.Server.Version}}'   # >= 26
docker compose version                           # hỗ trợ up --wait
python3 --version                               # >= 3.10
make --version
dotenvx --version                               # npm i -g @dotenvx/dotenvx
```

Build từ source cần khoảng **8 vCPU / 16 GB RAM**. Windows dùng WSL2; macOS khởi động OrbStack/Docker Desktop trước.

#### Tài khoản và CLI AWS

1. Đăng nhập console AWS bằng user admin (hoặc IAM user có quyền VPC, EC2, ECS, ECR, RDS, ElastiCache, S3, IAM, Cognito, Bedrock, SES, CloudFront, WAF, CloudWatch, Budgets).
2. Cấu hình CLI vùng `us-east-1`:
   ```bash
   aws configure
   aws sts get-caller-identity
   ```
3. Không đưa access key, giá trị `.env.keys` hay API key vào ảnh/tài liệu.

#### Source code

```bash
git clone https://github.com/poor-frog/TINA.git
cd TINA
git rev-parse --short HEAD
cp <duong-dan-bao-mat>/.env.keys .   # key riêng tương ứng
chmod 600 .env.keys
```

#### Checklist lỗi

| Triệu chứng | Cách sửa |
| --- | --- |
| Không có lệnh `aws` | Cài AWS CLI v2 |
| `Unable to locate credentials` | Chạy lại `aws configure`, đúng profile |
| Docker < 26 | Khởi động Docker/OrbStack/WSL |
| Dotenvx không giải mã | Copy đúng `.env.keys`, `chmod 600` |

- **Ảnh cần chụp:** `screenshot-00-prereqs.png` (version + `aws sts get-caller-identity`, che account id), `screenshot-01-clone.png`.
