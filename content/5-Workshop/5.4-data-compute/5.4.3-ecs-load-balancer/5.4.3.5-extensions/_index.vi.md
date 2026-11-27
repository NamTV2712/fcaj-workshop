---
title: "Phạm vi và tính năng mở rộng"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5.4.3.5 </b> "
---

## Những gì đã cấu hình

Lộ trình này triển khai bản thử nghiệm meetings hoàn chỉnh: Terminal, Google sign-in, core, Runtime khởi chạy bot ECS, lưu trữ và tùy chọn VieGem. Luồng này đã được kiểm chứng thực tế trên tài khoản AWS độc lập cho cả đăng nhập Google, bot tham gia cuộc họp và phiên âm VieGem.

## Những gì có sẵn dưới dạng mở rộng tùy chọn

- **Amazon Bedrock (`amazon.nova-lite-v1:0`)**: Template gộp [5.4A](../../../5.4-full-cloudformation/) đã cấu hình sẵn quyền `bedrock:InvokeModel` cho `amazon.nova-lite-v1:0` (`bedrock-converse`) phục vụ ghi chú, tóm tắt và Agent. Nếu dùng tài khoản mới, vào **Amazon Bedrock → Model catalog** tại `us-east-1` để xác nhận quyền gọi model `Amazon Nova Lite` đã hoạt động.
- **Amazon SES (Email follow-up sau cuộc họp)**: Yêu cầu **tên miền riêng trên Route 53** (để cấu hình bản ghi DKIM, SPF, DMARC) nên không tự bật trong bản lab mặc định. Khi có tên miền riêng, bạn có thể triển khai trực tiếp template `deploy/aws/staging-ses.yml` từ nhánh `main` của dự án (tạo sẵn SES ConfigurationSet, EmailIdentity, bản ghi DNS Route 53, Secrets Manager lưu thông tin SMTP và 3 CloudWatch Alarm cảnh báo bounce/complaint):

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-ses \
  --template-file deploy/aws/staging-ses.yml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    DomainName=your-domain.example \
    HostedZoneId=Z1234567890ABC \
    AlertEmail=ops@your-domain.example
```

- **CloudWatch Dashboard & Cảnh báo vận hành (Alarms)**: Bên cạnh 13 Log Group có sẵn, nhánh `main` cung cấp template `deploy/aws/staging-workspace-s3-monitoring.yml` tạo 10 Metric Filter, 20 CloudWatch Alarm (ALB 5xx, ECS memory ≥85%, RDS CPU/storage/connections, S3 sync) và 1 CloudWatch Dashboard tổng hợp; cùng script `deploy/aws/apply-ecr-lifecycle.sh` để tự dọn image cũ trên ECR.
- **Workspace/agent workbench & Voice (LiveKit/VieNeu)**: Lộ trình nhiều stack dựng bản `meetings` gọn nhẹ; nếu muốn bật đầy đủ Workspace, Agent, MCP, Flows và Voice hãy dùng template gộp [5.4A](../../../5.4-full-cloudformation/) kèm bộ 15 image `workshop-arm64`.
- **Vận hành production**: SSO doanh nghiệp, tên miền tùy chỉnh (`staging-domain-acm.yml`), Multi-AZ/backup và CI/CD tự động (`staging-github-ecr.yml`) đều có sẵn template tham khảo trong [thư mục deploy/aws trên nhánh main](https://github.com/poor-frog/TINA/tree/main/deploy/aws). Trước khi đưa vào production, cần rà soát quyền IAM, hạn mức dịch vụ và kiểm thử riêng từng tính năng.
