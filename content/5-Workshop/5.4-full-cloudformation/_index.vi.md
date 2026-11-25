---
title: "Triển khai bằng một CloudFormation"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4A </b> "
---

## Một file hạ tầng

{{< workshop-file path="cloudformation/tina-full.yml" label="Tải tina-full.yml" >}}

Đây là một template gồm VPC, NAT, S3, CloudFront/WAF, ALB, RDS, Valkey, ECS Fargate, Terminal, bot, Runtime, VieGem, Agent API, Agent Reach, MCP, Flows và kho workspace. Image và model cần chuẩn bị trước. Bản này dùng để kiểm tra hạ tầng và trang mở đầu.

**Trạng thái:** template đã qua kiểm tra tĩnh, chưa được triển khai và kiểm thử toàn bộ trong tài khoản AWS mới. Không dùng cho production. Thực hiện trong tài khoản thử riêng, `us-east-1`, và theo dõi chi phí. Cách một file này tạo VPC mới: **không tạo thêm foundation/egress theo lộ trình nhiều stack trước đó**.

## 1. Chuẩn bị image ARM64

TINA có [image dựng sẵn trên GitHub Packages](https://github.com/orgs/poor-frog/packages?repo_name=TINA). Khi kiểm tra manifest của cả 12 image bên dưới, tag `latest` và tag commit `62e5350…` chỉ có `linux/amd64`. Registry trả 404 cho tag commit AWS `7d6bba8…` ở cả 12 repository. Template này dùng Fargate ARM64 và cần Runtime có backend ECS, nên đừng đưa các tag đã kiểm tra vào bước triển khai.

Nếu có bộ image dựng sẵn tương thích với bản AWS này, có thể bỏ EC2 builder và bước build. Sao chép các image ARM64 theo digest vào đúng repository ECR bên dưới, rồi dùng digest trong ECR để tạo stack. Xác nhận bộ image có Runtime backend ECS, Terminal chế độ `workspace-pilot` và VieGem có model trước khi dùng. Khi chưa có bộ image tương thích, dùng script build ở phần dưới.

Tạo trước 12 ECR repository private trong tài khoản mới, tên chính xác dưới đây. Ví dụ CloudShell:

```bash
export AWS_REGION=us-east-1 AWS_PAGER=''
for name in terminal gateway meeting-api admin-api runtime bot agent-api agent-reach agent-worker mcp flows viegem; do
  aws ecr create-repository --region "$AWS_REGION" --repository-name "tina-staging/$name" --image-tag-mutability IMMUTABLE
done
```

Chuẩn bị một EC2 Amazon Linux 2023 **Arm64** với Docker/Buildx, Git, AWS CLI, đủ RAM/dung lượng và instance role có quyền push vào các repository trên. Các bước tạo instance profile và máy builder được mô tả tại [phần builder](../5.4-data-compute/5.4.1-s3-ecr-images/); ở cách một file này, đặt builder trong **VPC public có Internet của bạn**, không tạo stack foundation ở phần đó. Ví dụ dùng máy 8 vCPU/32 GiB, đĩa 200 GiB; kiểm tra quota và chi phí trước.

Trong Session Manager của builder, tải đúng commit nguồn `7d6bba8109f6eac51c0d8241a7083e3e364cf59d` và script {{< workshop-file path="scripts/tina-ecr-build.sh" label="tina-ecr-build.sh" >}} như hướng dẫn builder. Chạy với tag mới:

```bash
export AWS_REGION=us-east-1 TINA_IMAGE_TAG=ws-v1
bash /root/tina-ecr-build.sh --source /root/tina-source --region "$AWS_REGION" --full --plan
bash /root/tina-ecr-build.sh --source /root/tina-source --region "$AWS_REGION" --full
```

`--full` build Terminal workspace-pilot, Runtime, bot, core, Agent, worker, MCP, Flows và VieGem. VieGem là model phi thương mại; xem [model card](https://huggingface.co/5CD-AI/VieGem-ASR) và điều khoản Gemma trước khi dùng. Build nặng, tải model và cần Internet; nếu lỗi phải sửa lỗi rồi dùng tag mới do ECR immutable. Script in image URI dạng `...@sha256:...`; bạn chỉ cần phần `sha256:...` của từng repository để nhập tham số template. Chưa có kiểm thử build ARM64 thực tế trong tài khoản mới.

## 2. Lấy prefix list

Trong CloudShell, lấy hai prefix list ID và ghi lại:

```bash
aws ec2 describe-managed-prefix-lists --region us-east-1 --filters Name=prefix-list-name,Values=com.amazonaws.global.cloudfront.origin-facing --query 'PrefixLists[0].PrefixListId' --output text
aws ec2 describe-managed-prefix-lists --region us-east-1 --filters Name=prefix-list-name,Values=com.amazonaws.us-east-1.s3 --query 'PrefixLists[0].PrefixListId' --output text
```

Không tiếp tục nếu kết quả là `None` hoặc sai Region.

## 3. Tạo stack trên Console

1. Vào **CloudFormation → Create stack → With new resources (standard) → Upload a template file**. Chọn `tina-full.yml` vừa tải. Console sẽ tải file lên S3 vì file lớn hơn giới hạn template inline.
2. Đặt stack name, ví dụ `tina-workshop-full`. Nhập `CloudFrontOriginPrefixListId`, `S3PrefixListId` và các digest theo tên image: `BotDigest`, `RuntimeDigest`, `AdminDigest`, `MeetingDigest`, `GatewayDigest`, `TerminalDigest`, `AgentApiDigest`, `AgentWorkerDigest`, `AgentReachDigest`, `McpDigest`, `FlowsDigest`, `VieGemDigest`.
3. Ban đầu để `WorkspaceOwnerIds` trống và `EnableVoice=false`; các digest VieNeu/LiveKit được để trống khi chưa có voice image. Xác nhận CloudFormation tạo IAM resources và submit. Chờ `CREATE_COMPLETE`; nếu thất bại, mở **Events** để tìm lỗi đầu tiên.

{{< workshop-screenshot file="26-cloudformation-full.png" description="CloudFormation stack một file, danh sách tham số đã che account ID và ARN." >}}

4. Mở tab **Outputs**, lấy `WebsiteUrl`. Mở URL và kiểm tra trang đầu TINA, sau đó xem ECS service và target group. Endpoint `/edge-health` phải trả `TINA_EDGE_READY` khi tuyến CloudFront tới ALB hoạt động.

Stack này không cấu hình đăng nhập. Terminal yêu cầu phiên đăng nhập để mở màn hình họp và workspace. Vì vậy, bước trên kiểm tra hạ tầng và trang đầu, còn kiểm thử họp, bot và phiên âm qua giao diện chưa thực hiện được.


## 4. Voice và dữ liệu khi xóa

Để bật voice, cần image `tina-staging/vieneu`, `livekit`, `livekit-agent`, bot có model wake-word đã kiểm tra và các digest tương ứng, rồi cập nhật `EnableVoice=true` và `VoicePilotRoom`. Các model wake-word tùy biến không nằm trong source công khai; phải có artifact hợp lệ hoặc tự huấn luyện. Template không tự tạo các artifact đó, vì vậy chưa thể cam kết voice hoạt động ngay sau khi tạo stack.

Khi xóa stack, bucket recordings, bucket workspace, KMS key và snapshot RDS có thể được giữ lại và tính phí; ECR tạo ngoài stack vẫn còn sau khi xóa. Xem [dọn dẹp](../5.6-cleanup-evidence/) và đối chiếu đúng tài nguyên trước khi xóa.
