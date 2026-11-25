---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.2-create-interface-enpoint/"]
title: "Dữ liệu, secret và dịch vụ bổ sung"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

## A. Kiểm tra dữ liệu staging

1. **RDS → Databases** → lọc `tina-staging`; mở database staging → **Connectivity & security**. Kiểm tra trạng thái **Available**, engine PostgreSQL, VPC, subnet group, security group và **Public access = No**.

{{< workshop-screenshot file="09-rds.png" description="RDS PostgreSQL staging hoặc lab: trạng thái và public access." >}}

2. **ElastiCache → Valkey/Redis OSS caches** → chọn cache staging bằng cách đối chiếu trong **CloudFormation → tina-staging-datastores → Resources**. Xem trạng thái, subnet group, security group và cấu hình mã hóa thực tế.

{{< workshop-screenshot file="10-valkey.png" description="ElastiCache Valkey: trạng thái và cấu hình mạng của môi trường được kiểm tra." >}}

3. **Secrets Manager → Secrets**: đối chiếu tên/metadata secret mà stack hoặc task definition tham chiếu. Không chọn **Retrieve secret value**, không chụp hoặc sao chép giá trị.

{{< workshop-screenshot file="11-secret-metadata.png" description="Metadata của secret; không hiển thị giá trị secret." >}}

4. Nếu cần xác nhận kết nối, làm qua tác vụ thử được người quản trị cho phép trong VPC. Chỉ thấy database `Available` chưa chứng minh ứng dụng đăng nhập và ghi dữ liệu được.

## B. Tạo database lab khi cần

Việc này phát sinh chi phí. Nếu chỉ đánh giá môi trường có sẵn, bỏ qua phần B.

1. **RDS → Subnet groups → Create DB subnet group**: tên `tina-ws-db-subnets`, chọn VPC lab, thêm hai AZ và hai subnet data; tạo group.
2. **RDS → Databases → Create database**: chọn **Standard create**, engine PostgreSQL và phiên bản/class được tài khoản hỗ trợ. Chọn mức cấu hình và dung lượng phù hợp budget; không giả định một class luôn có ở mọi Region.
3. Đặt identifier `tina-ws-db`; chọn cách quản lý mật khẩu phù hợp chính sách, ưu tiên Secrets Manager khi tùy chọn khả dụng. Không ghi mật khẩu vào tài liệu, terminal history hay ảnh.
4. Trong **Connectivity**, chọn VPC lab và DB subnet group, **Public access = No**, chọn `tina-ws-db-sg`. Bật mã hóa; xem lại backup và deletion protection theo chính sách của lab.
5. Chọn **Create database**, chờ **Available**. Kiểm tra lại subnet và SG; ghi endpoint vào nơi làm việc riêng, không đưa vào tài liệu công khai.

Để thực hành Valkey, vào **ElastiCache → Create**, chọn Valkey, chế độ và subnet/SG phù hợp, bật mã hóa và xác thực theo lựa chọn được hỗ trợ. Ghi rõ cache lab và thời gian tạo vì cache cũng phát sinh chi phí. Các bước này tạo dịch vụ độc lập; cần cấu hình từng service TINA và migration được kiểm chứng để thực sự sử dụng chúng.

## C. Cognito, Bedrock và SES

Đây là các mục **kiểm tra nếu kiến trúc triển khai của bạn có tích hợp**; không coi việc tạo tài nguyên là đã kết nối ứng dụng.

- **Cognito:** kiểm tra ứng dụng thật dùng cơ chế đăng nhập nào trước. Trong lần khảo sát, danh sách user pool tại `us-east-1` không trả về pool nào; Terminal trong source có Google/NextAuth. Tạo user pool không tự chuyển đăng nhập sang Cognito.
- **Bedrock:** trong **Amazon Bedrock → Model catalog**, chọn model, kiểm tra quyền truy cập, Region và chi phí. Quy trình cấp quyền có thể khác theo nhà cung cấp/model. Chỉ kiểm thử qua cấu hình provider mà phiên bản TINA hỗ trợ.
- **SES:** **Amazon SES → Verified identities → Create identity** để xác minh email/domain của bạn. Ở thời điểm khảo sát, tài khoản đang có `ProductionAccessEnabled = false`; khi SES sandbox, cần xác minh người nhận hoặc dùng mailbox simulator. Việc bật SES không tự cấu hình luồng gửi mail của TINA.

