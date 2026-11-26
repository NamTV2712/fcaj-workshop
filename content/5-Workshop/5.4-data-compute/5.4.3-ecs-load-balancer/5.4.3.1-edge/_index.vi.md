---
title: "WAF, CloudFront và ALB"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.4.3.1 </b> "
---

## 1. Tạo Web ACL trên AWS Console

1. Vào **AWS WAF & Shield → Web ACLs → Create web ACL**.
2. Đặt tên `tina-workshop-acl`. Ở **Resource type**, chọn **CloudFront distributions**; web ACL loại này được quản lý tại `us-east-1`. Để danh sách associated resources trống vì CloudFormation sẽ gắn distribution sau.
3. Trong phần rules, có thể thêm AWS Managed Rules **Core rule set** để thực hành và giữ default action **Allow**. Quy tắc WAF và request có thể phát sinh phí; tùy chỉnh và thử rule trước khi dùng thật. Giữ các tùy chọn metrics mặc định, chọn **Create web ACL**.
4. Mở Web ACL vừa tạo, sao chép **ARN** của nó. Không dùng ARN của một Regional Web ACL.

{{< workshop-screenshot file="23-waf-acl.png" description="Web ACL phạm vi CloudFront đã tạo, che account ID trong ARN." >}}

{{< workshop-screenshot file="23-waf-acl(2).png" description="Chi tiết Web ACL phạm vi CloudFront đã tạo, che account ID trong ARN." >}}

## 2. Triển khai CloudFront và ALB nội bộ

Trong CloudShell, thay giá trị placeholder bằng ARN Web ACL **của bạn**:

```bash
WAF_ARN='DAN_ARN_WEB_ACL_CLOUDFRONT_CUA_BAN'
VPC_ID="$(stackout tina-staging VpcId)"
APP_SUBNETS="$(stackout tina-staging AppSubnetIds)"
PREFIX_ID="$(aws ec2 describe-managed-prefix-lists --region "$AWS_REGION" \
  --filters Name=prefix-list-name,Values=com.amazonaws.global.cloudfront.origin-facing \
  --query 'PrefixLists[0].PrefixListId' --output text)"
printf 'Prefix list: %s\n' "$PREFIX_ID"
```

Nếu prefix list là `None` hoặc rỗng, kiểm tra Region trước khi tiếp tục. Tạo stack:

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-edge --template-file "$TINA_SRC/deploy/aws/staging-edge.yml" \
  --parameter-overrides "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "CloudFrontOriginPrefixListId=$PREFIX_ID" "WebAclArn=$WAF_ARN"
```

Đợi `CREATE_COMPLETE`, có thể mất thời gian do CloudFront VPC origin. Truy cập `StageUrl` lấy từ output kèm `/edge-health`: phải thấy `TINA_EDGE_READY`. Truy cập gốc lúc này có thể trả 503 vì Terminal chưa tạo.

```bash
stackout tina-ws-edge StageUrl
```

Tại **CloudFront → Distributions**, mở distribution trong output `DistributionId`, kiểm tra origin kiểu VPC và trạng thái triển khai:

{{< workshop-screenshot file="15-cloudfront-origin.png" description="CloudFront distribution và VPC origin của bạn; che domain và account ID nếu chia sẻ." >}}

ALB có scheme **internal**, không có IP public. HTTPS chấm dứt ở CloudFront, template kết nối HTTP từ CloudFront tới ALB nội bộ; mô hình này dành cho bài thử nghiệm. Xem [yêu cầu CloudFront VPC origin](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html).
