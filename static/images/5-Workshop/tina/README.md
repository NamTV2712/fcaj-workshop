# Danh sách ảnh cần chụp cho workshop TINA

Lưu ảnh PNG đã che thông tin nhạy cảm vào chính thư mục này, với **đúng tên tệp** dưới đây. Vị trí hiển thị đã được đánh dấu ngay sau bước tương ứng trong trang tiếng Việt. Khi website được dựng lại, ảnh sẽ xuất hiện tại vị trí đó; nếu chưa có tệp, trang sẽ hiện thông báo cần bổ sung.

Chỉ dùng ảnh chụp thật của môi trường được phép xem. Không hiển thị mật khẩu, token, giá trị secret, nội dung cuộc họp riêng tư hoặc thông tin cá nhân. Che account ID, domain, email và định danh nội bộ trước khi chia sẻ.

| Tên ảnh | Trang | Chụp gì |
| --- | --- | --- |
| `00-region.png` | 5.2 Chuẩn bị | Region `us-east-1` trên Console. |
| `00-budget.png` | 5.2 Chuẩn bị | Budget và ngưỡng cảnh báo của lab. |
| `01-cloudformation-staging.png` | 5.1 Tổng quan | Danh sách stack TINA staging và trạng thái. |
| `02-ecs-services.png` | 5.1 Tổng quan | ECS services, desired và running tasks. |
| `03a-create-vpc.png` | 5.3.1 VPC/subnet | Form tạo VPC lab và CIDR. |
| `03b-create-subnets.png` | 5.3.1 VPC/subnet | Form tạo subnet lab. |
| `03-vpc-subnets.png` | 5.3.1 VPC/subnet | Sáu subnet lab, CIDR và AZ. |
| `04a-igw-attached.png` | 5.3.2 Gateway/route | Internet Gateway lab đã gắn vào VPC. |
| `04b-nat-available.png` | 5.3.2 Gateway/route | NAT Gateway lab ở trạng thái Available. |
| `04-route-tables.png` | 5.3.2 Gateway/route | Routes và subnet associations của lab. |
| `05-s3-endpoint.png` | 5.3.2 Gateway/route | S3 gateway endpoint và route table. |
| `06-security-groups.png` | 5.3.2 Gateway/route | Security group và rule của lab. |
| `07-s3-lab.png` | 5.4.1 S3/ECR | Bucket lab và object thử. |
| `08-ecr-image.png` | 5.4.1 S3/ECR | Image tag và digest trong ECR lab. |
| `09-rds.png` | 5.4.2 Dữ liệu | PostgreSQL, trạng thái và public access. |
| `10-valkey.png` | 5.4.2 Dữ liệu | Valkey và cấu hình mạng. |
| `11-secret-metadata.png` | 5.4.2 Dữ liệu | Metadata secret, không hiện giá trị. |
| `12-ecs-services.png` | 5.4.3 ECS/ALB | ECS services và số task. |
| `13-ecs-task.png` | 5.4.3 ECS/ALB | Chi tiết task/container, che environment và secret. |
| `14-target-health.png` | 5.4.3 ECS/ALB | Trạng thái target group. |
| `15-cloudfront-origin.png` | 5.4.3 ECS/ALB | CloudFront distribution và VPC origin. |
| `16-app-login.png` | 5.4.4 Kiểm thử | Trang đăng nhập hoặc phản hồi web. |
| `17-test-meeting.png` | 5.4.4 Kiểm thử | Bot tham gia cuộc họp thử được phép. |
| `18-test-transcript.png` | 5.4.4 Kiểm thử | Transcript dùng dữ liệu giả. |
| `19-role-policy.png` | 5.5 Bảo mật | Role và policy được kiểm tra. |
| `20-logs.png` | 5.5 Giám sát | Log đã che thông tin nhạy cảm. |
| `21-budget.png` | 5.5 Chi phí | Budget lab và trạng thái cảnh báo. |
| `22-cleanup-lab.png` | 5.6 Dọn dẹp | Bằng chứng tài nguyên lab đã dọn. |

Hai ảnh ECS và hai ảnh budget phục vụ các bước đánh giá khác nhau; có thể dùng cùng một nội dung chụp phù hợp ở hai tên nếu thực sự chứng minh được cả hai bước. Không dùng ảnh của workshop cũ để thay thế kết quả TINA.
