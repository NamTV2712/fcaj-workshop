---
title: "Kiểm tra hệ thống đang chạy"
date: 2026-11-24
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

#### Kiểm tra ứng dụng

Lấy domain CloudFront từ output của stack rồi mở trên trình duyệt:

```bash
aws cloudformation describe-stacks --stack-name tina-infra \
  --query 'Stacks[0].Outputs'
curl -sS -o /dev/null -w '%{http_code}\n' https://<cloudfront-domain>/health
```

1. Đăng nhập qua Cognito/Google (user đầu tiên thành admin).
2. Trong **Settings → Models**, chọn provider để agent trả lời được.
3. Xác nhận transcript trực tiếp, ghi chú, tóm tắt và dropdown **Tiếng Việt / English / Song ngữ**.
4. Kiểm tra wake word và câu trả lời bằng giọng nói qua bot.

#### Kiểm tra luồng dữ liệu

```bash
aws s3 ls s3://tina-<ten>-recordings
aws rds describe-db-instances --db-instance-identifier tina-db
aws elasticache describe-cache-clusters --cache-cluster-id tina-cache
```
Bản ghi âm lên S3 qua gateway endpoint (không tốn phí NAT); transcript vào RDS và trạng thái trực tiếp vào ElastiCache ở private data subnet.

#### Ảnh cần chụp

- `screenshot-17-app-running.png`
- `screenshot-18-transcript.png`
