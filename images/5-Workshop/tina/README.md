# Ảnh cần chụp cho workshop triển khai TINA

Lưu PNG đã che thông tin nhạy cảm vào thư mục này đúng tên bên dưới. Mỗi ảnh hiển thị ngay sau thao tác tương ứng trong trang tiếng Việt khi dựng lại Hugo. Chỉ dùng ảnh thật; không chụp secret, token, dữ liệu cá nhân hoặc nội dung họp thật.

| Tên tệp | Trang | Nội dung |
| --- | --- | --- |
| `00-budget.png` | Chuẩn bị | Budget và ngưỡng cảnh báo của tài khoản thực hành; che email và account ID. |
| `00-region.png` | Chuẩn bị | AWS Console đang chọn Region us-east-1. |
| `01-cloudformation-staging.png` | Tổng quan và tiêu chí đánh giá | Các stack TINA do bạn tạo và trạng thái trong CloudFormation. |
| `02-ecs-services.png` | Tổng quan và tiêu chí đánh giá | ECS service của tài khoản thực hành, gồm desired và running tasks. |
| `03-vpc-subnets.png` | Tạo foundation và VPC | Sáu subnet do foundation tạo, với VPC và Availability Zone. |
| `03a-create-vpc.png` | Tạo foundation và VPC | Màn hình CloudFormation chọn tệp foundation.yml để tạo VPC và nền tảng. |
| `03b-create-subnets.png` | Tạo foundation và VPC | CloudFormation Outputs của stack nền tảng: VPC, subnet, cluster và bucket; che account ID nếu xuất hiện. |
| `04-route-tables.png` | NAT Gateway, route và endpoint | Route table của app subnet với default route qua NAT. |
| `04a-igw-attached.png` | NAT Gateway, route và endpoint | Internet Gateway của VPC đã attached. |
| `04b-nat-available.png` | NAT Gateway, route và endpoint | NAT Gateway do stack egress tạo, trạng thái Available. |
| `05-s3-endpoint.png` | NAT Gateway, route và endpoint | S3 gateway endpoint và các route table app được liên kết. |
| `06-security-groups.png` | RDS, Valkey và Secrets Manager | Sau khi tạo stack data, chụp security group của ứng dụng và database; không hiển thị thông tin nhạy cảm. |
| `07-s3-lab.png` | S3, ECR và build image ARM64 | Bucket recordings của tài khoản thực hành, chế độ chặn truy cập công khai và lifecycle rule. |
| `08-ecr-image.png` | S3, ECR và build image ARM64 | ECR repository của bạn có image tag và digest sau khi build. |
| `09-rds.png` | RDS, Valkey và Secrets Manager | RDS PostgreSQL của bạn đã Available và không public. |
| `10-valkey.png` | RDS, Valkey và Secrets Manager | Valkey của bạn đã Available trong VPC thực hành. |
| `11-secret-metadata.png` | RDS, Valkey và Secrets Manager | Metadata secret do stack tạo, không hiển thị giá trị secret. |
| `12-ecs-services.png` | Bot và Runtime trên Fargate | ECS services sau khi hoàn thành Runtime, core và terminal, kèm desired/running tasks. |
| `13-ecs-task.png` | Bot và Runtime trên Fargate | Task Runtime và trạng thái container; che environment và thông tin nhạy cảm. |
| `14-target-health.png` | Đăng nhập Google và Terminal | Target group Terminal của bạn có target healthy. |
| `15-cloudfront-origin.png` | WAF, CloudFront và ALB | CloudFront distribution và VPC origin của bạn; che domain và account ID nếu chia sẻ. |
| `16-app-login.png` | Kiểm thử website và meeting | Trang đăng nhập TINA trên URL CloudFront của bạn; che email và domain nếu chia sẻ. |
| `17-test-meeting.png` | Kiểm thử website và meeting | Cuộc họp thử được phép và trạng thái bot; dùng dữ liệu giả, che thông tin người tham gia. |
| `18-test-transcript.png` | Kiểm thử website và meeting | Transcript của câu thử không nhạy cảm sau khi ASR hoạt động. |
| `19-role-policy.png` | Bảo mật, giám sát và chi phí | Role và phạm vi policy của môi trường thực hành; che định danh tài khoản. |
| `20-logs.png` | Bảo mật, giám sát và chi phí | CloudWatch log của task đã che token, thông tin người dùng và nội dung meeting. |
| `21-budget.png` | Bảo mật, giám sát và chi phí | Budget tài khoản thực hành và trạng thái cảnh báo; che email và account ID. |
| `22-cleanup-lab.png` | Dọn dẹp tài nguyên và bằng chứng | Trạng thái xóa tài nguyên của môi trường thực hành sau khi đã kiểm tra; che account ID. |
| `23-waf-acl.png` | WAF, CloudFront và ALB | Web ACL phạm vi CloudFront đã tạo, che account ID trong ARN. |
| `24-viegem-service.png` | VieGem tùy chọn và core | Nếu dùng VieGem, chụp ECS service và số task running; không hiển thị token. |
| `25-google-secret.png` | Đăng nhập Google và Terminal | Metadata của Google OAuth secret; che ARN, không hiển thị giá trị secret. |
| `26-cloudformation-full.png` | Triển khai bằng một CloudFormation | CloudFormation stack một file, danh sách tham số đã che account ID và ARN. |
