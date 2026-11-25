---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.4-dns-simulation/"]
title: "Kiểm tra hệ thống và chuẩn bị tái triển khai"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

## A. Kiểm tra ứng dụng đang chạy

1. Trong **CloudFormation → Stacks → tina-staging-edge → Outputs**, tìm `StageUrl`. Chỉ người được cấp quyền mới mở URL này; không dán URL nội bộ vào báo cáo công khai.
2. Mở URL staging bằng trình duyệt. Đối chiếu mã HTTP/trang đăng nhập với mục tiêu bài kiểm tra. Ngày 25/11/2026, một yêu cầu HEAD tới URL này trả `200`; đây chỉ là kiểm tra truy cập, không chứng minh đăng nhập hoặc luồng họp.

{{< workshop-screenshot file="16-app-login.png" description="Trang đăng nhập hoặc phản hồi web của môi trường thử." >}}

3. Nếu được phép và có tài khoản thử, đăng nhập bằng phương thức được cấu hình thực tế. Dùng cuộc họp thử và dữ liệu giả, được tất cả người tham gia đồng ý; không quay/chụp người hoặc nội dung riêng tư.
4. Kiểm tra theo thứ tự: tạo hoặc tham gia cuộc họp thử → bot vào → âm thanh được gửi đến endpoint STT tự host → transcript xuất hiện → dừng cuộc họp → kiểm tra kết quả/lưu trữ theo quyền được cấp.

{{< workshop-screenshot file="17-test-meeting.png" description="Cuộc họp thử và bot tham gia, dùng dữ liệu giả đã được cho phép." >}}

{{< workshop-screenshot file="18-test-transcript.png" description="Transcript của cuộc họp thử; không dùng nội dung riêng tư." >}}

5. Ghi **Expected**, **Actual**, thời điểm và **Pass/Fail/Blocked** cho từng bước. Nếu chưa có quyền, model, URL họp hoặc dữ liệu thử, ghi **Blocked** cùng lý do; không thay bằng ảnh hoặc kết quả giả.

| Kiểm tra | Đạt khi | Bằng chứng |
| --- | --- | --- |
| Truy cập web | Mở được URL staging và nhận phản hồi phù hợp | Ảnh trang thử sau khi che thông tin riêng |
| ECS/ALB | Service ổn định và target phù hợp `healthy` | Ảnh service + target health |
| Họp thử | Bot vào đúng phòng thử được cho phép | Ảnh hoặc log đã che thông tin |
| Phiên âm | Nội dung thử xuất hiện đúng theo tiêu chí đã đặt | Ảnh transcript giả + thời điểm |
| Ghi dữ liệu | Tệp thử có thể tìm thấy tại nơi hệ thống thực sự dùng | Object metadata, không chụp dữ liệu riêng |

## B. Làm cho workshop có thể tái triển khai từ đầu

Người hướng dẫn cần chuẩn bị các mục sau trước khi yêu cầu reviewer dựng lại toàn hệ thống:

1. Một commit/tag source có thể truy cập và tập image/digest tương ứng, kèm kiến trúc CPU, quyền pull và hướng dẫn build.
2. Bộ template hoặc manifest cho **toàn bộ** stack được sử dụng, thứ tự triển khai và danh sách parameter/đầu ra; không chứa account ID, mật khẩu, token hay secret thật. Các template đang nằm trong AWS có thể được xem qua **CloudFormation → stack → Template** và được rà soát trước khi đưa vào bộ release.
3. Tài liệu thiết lập role/SG/service discovery, DB migration, DNS/certificate, secret, STT, model và chi phí/quota. Xác định rõ phần nào bắt buộc, phần nào tùy chọn.
4. Chạy lại bằng tài khoản lab sạch; ghi thời gian, lệnh, ảnh và lỗi đã khắc phục. Lặp lại việc kiểm tra ứng dụng và dọn lab từ đầu đến cuối.
5. Chỉ sau đó công bố hướng dẫn với phiên bản cố định. Không đẩy source/image/template lên nơi công khai nếu chưa được chủ dự án cho phép và chưa rà soát nội dung.

### Các đầu vào thực tế cần đối chiếu

Để lập bảng tham số, mở từng stack trong **CloudFormation → Stacks → chọn stack → Parameters**, sau đó đối chiếu **Outputs** và **Resources** của các stack liên quan. Ghi tên tham số và nguồn cấp; không sao chép giá trị secret hoặc định danh tài khoản vào tài liệu công khai. Những tên dưới đây đã được kiểm tra từ template staging ngày 25/11/2026:

| Stack | Một số đầu vào cần chuẩn bị | Kiểm tra tiếp |
| --- | --- | --- |
| `tina-foundation` | Template hiện không khai báo parameter | Rà CIDR và tên cố định trong template trước khi sửa thành bộ dùng được cho tài khoản khác. Không đồng thời tạo thủ công và để template tạo lại cùng tài nguyên. |
| `tina-staging-egress` | `PublicSubnetId`, `AppRouteTableA`, `AppRouteTableB` | Lấy từ nền tảng của chính môi trường lab. |
| `tina-staging-edge` | `VpcId`, `AppSubnetIds`, `WebAclArn`, `CloudFrontOriginPrefixListId` | Xác định nguồn ARN/prefix list phù hợp Region và lab; kiểm tra cách cấu hình VPC origin. |
| `tina-staging-datastores` | `VpcId`, `DataSubnetIds`, `DeployValkey` | Kiểm tra subnet group, database, cache và cách cấp secret. |
| `tina-staging-bot` | `ClusterName`, `BotRepositoryArn`, `BotImage`, `InvocationBucket`, `ProbeInvocation` | Xác định image digest, quyền chạy task và storage phù hợp. |
| `tina-staging-runtime` | `VpcId`, `AppSubnetIds`, `ClusterName`, `RuntimeImage`, `BotTaskDefinitionArn` cùng các tham số Valkey/workspace | Xem toàn bộ Parameters; xác định rõ tham số tùy chọn, role, storage và service discovery. |
| `tina-staging-core` | `VpcId`, `AppSubnetIds`, `ClusterName`, các image, `PostgresHost`, `ValkeyHost`, `RecordingsBucket`, các secret ARN và URL nội bộ | Đối chiếu đầy đủ phần STT, TTS, runtime, agent, MCP và migration. |
| `tina-staging-terminal` | `StageUrl`, `ListenerArn`, `TerminalImage`, `GoogleSecretArn`, `InternalSecretArn` cùng các tham số VPC, subnet và security group | Chuẩn bị callback/OAuth hợp lệ; không công khai secret hoặc URL riêng. |
| `tina-staging-viegem`, `tina-staging-voice`, `tina-staging-agent-api`, `tina-staging-agent-reach`, `tina-staging-mcp`, `tina-staging-flows` | Image, cluster, subnet, service discovery và tham số kết nối riêng theo từng stack | Xem toàn bộ danh sách trên Console; kiểm chứng các tham số và dependency theo release thực tế. |

Đây là bảng **khảo sát**, chưa phải thứ tự triển khai đã kiểm thử; một số stack tham chiếu lẫn nhau và các tính năng tùy chọn có thể thay đổi dependency. Trước khi xuất template hoặc ảnh để chia sẻ, rà lại hardcoded ARN, domain, account ID và mọi giá trị nhạy cảm.

Template cũ trong `static/cloudformation/tina-infrastructure.yaml` chưa đáp ứng danh sách trên; stack `CREATE_COMPLETE` của một template cũng chưa phải bằng chứng các chức năng ứng dụng hoạt động.

Chỉ dùng dữ liệu thử, không đưa tài liệu hoặc ghi âm thật vào workshop.
