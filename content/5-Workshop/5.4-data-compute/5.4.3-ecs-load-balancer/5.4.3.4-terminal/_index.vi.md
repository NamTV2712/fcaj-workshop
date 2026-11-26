---
title: "Đăng nhập Google và Terminal"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4.3.4 </b> "
---

## 1. Tạo OAuth client của bạn

1. Chạy `stackout tina-ws-edge StageUrl` trong CloudShell, lấy URL HTTPS CloudFront **của bạn**, không có dấu `/` ở cuối.
2. Vào [Google Cloud Console](https://console.cloud.google.com/), tạo hoặc chọn Google Cloud project do bạn quản lý. Vào **Google Auth Platform → Branding/Audience**, cấu hình thông tin ứng dụng và chọn **Testing** nếu chỉ thử; thêm tài khoản Google của bạn vào **Test users**. Giao diện Google có thể đổi tên mục.
3. Vào **Clients → Create client → Web application**. Thêm **Authorized redirect URI** đúng mẫu `https://<cloudfront-domain-cua-ban>/api/auth/callback/google`. Lưu và nhận client ID, client secret. Đọc [Google OAuth web server](https://developers.google.com/identity/protocols/oauth2/web-server) nếu gặp lỗi URI. Dùng công khai/production có thể cần tên miền thuộc quyền quản lý và xác minh ứng dụng với Google.

{{< workshop-screenshot file="5.4.3.4-1.2-ggcloudconsole.png" description="Cấu hình Google OAuth Web application client và Authorized redirect URI trên Google Cloud Console." >}}

4. Trong CloudShell, tạo một file tạm chỉ chủ sở hữu đọc được, mở trình soạn thảo:

```bash
umask 077
GOOGLE_JSON="$(mktemp)"
nano "$GOOGLE_JSON"
```

Nhập JSON bên dưới, thay bằng **client ID và client secret thật của bạn**; không gửi, lưu vào Git hay chụp ảnh nội dung này. Trong nano chọn `Ctrl+O`, Enter để lưu và `Ctrl+X` để thoát:

```json
{"client_id":"DAN_GOOGLE_CLIENT_ID","client_secret":"DAN_GOOGLE_CLIENT_SECRET"}
```

Tạo secret từ file, chỉ lấy ARN và xóa file tạm. Nếu secret cùng tên đã có, dừng để kiểm tra thay vì ghi đè:

```bash
if GOOGLE_SECRET_ARN="$(aws secretsmanager create-secret --region "$AWS_REGION" \
  --name tina-workshop-google --secret-string "file://$GOOGLE_JSON" \
  --query ARN --output text)"; then
  rm -f -- "$GOOGLE_JSON"
  unset GOOGLE_JSON
else
  echo "Tạo secret thất bại; kiểm tra và xóa file tạm an toàn: $GOOGLE_JSON"
fi
```

Để kiểm tra trên Console, vào **Secrets Manager → Secrets → tina-workshop-google** và chỉ xem metadata, không chọn **Retrieve secret value**:

{{< workshop-screenshot file="25-google-secret.png" description="Metadata của Google OAuth secret; che ARN, không hiển thị giá trị secret." >}}

## 2. Triển khai website

Trong CloudShell, dùng ARN secret vừa tạo. Nếu CloudShell đã mở lại, chạy lại khối khởi tạo ở [Chuẩn bị](../../../5.2-prerequisites/) và hàm `image` ở [trang triển khai](../), sau đó lấy lại các biến `CLUSTER`, `VPC_ID`, `APP_SUBNETS`, `INTERNAL_SECRET_ARN` như các trang trước và lấy ARN bằng `aws secretsmanager describe-secret --secret-id tina-workshop-google --query ARN --output text`.

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-terminal --template-file "$TINA_SRC/deploy/aws/staging-terminal.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "CoreClientSecurityGroupId=$(stackout tina-ws-core ClientSecurityGroupId)" \
    "AlbSecurityGroupId=$(stackout tina-ws-edge OriginSecurityGroupId)" \
    "ListenerArn=$(stackout tina-ws-edge ListenerArn)" "StageUrl=$(stackout tina-ws-edge StageUrl)" \
    "TerminalImage=$(image terminal)" "TerminalRepositoryArn=$(repoarn terminal)" \
    "AdminTokenArn=$(stackout tina-ws-core AdminTokenArn)" \
    "InternalSecretArn=$INTERNAL_SECRET_ARN" "GoogleSecretArn=$GOOGLE_SECRET_ARN"
```

Terminal image đã build với chế độ `meetings`; để `WorkspacePilotUserIds` mặc định rỗng. Chờ stack thành công và task Running. Tại **EC2 → Target groups**, mở target group được trả trong output `TargetGroupArn` của stack Terminal, chọn **Targets** và đợi **healthy**:

{{< workshop-screenshot file="14-target-health.png" description="Target group Terminal của bạn có target healthy." >}}

Mở `StageUrl` của bạn. Trong một instance mới, người đăng nhập đầu tiên có thể nhận quyền quản trị; vì vậy trước khi chia sẻ URL, tự đăng nhập bằng Google test user của bạn. Sau đó tiếp tục [kiểm thử](../../5.4.4-application-validation/).
