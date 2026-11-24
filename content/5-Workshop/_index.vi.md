---
title: "Workshop"
date: 2026-11-24
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Triển khai và kiểm chứng TINA trên AWS

#### Tổng quan

Workshop này biến bản Proposal của TINA thành buổi thực hành. Proposal mô tả hệ thống đóng gói container trên **Amazon ECS với AWS Fargate** tại `us-east-1`, gồm 5 dịch vụ — **Web serving, Bot, STT (VieGem), TTS (VieNeu) và Agent** — cùng phối hợp tham gia cuộc họp, phiên âm trực tiếp, trả lời câu hỏi và gửi email follow-up. Amazon S3 lưu bản ghi âm, RDS lưu transcript, ElastiCache chứa trạng thái trực tiếp, Amazon Bedrock vận hành agent, còn Cognito/SES/CloudFront/WAF/ALB đảm nhiệm định danh, email và định tuyến biên.

Repository đã có sẵn **bản build đóng gói**: CI đẩy image container (các tag `:prod`, `:demo`, `:latest`) và bộ deploy cung cấp `make plan` / `make all`. Nhiệm vụ ngày mai của bạn vì thế không phải xây lại từ đầu, mà là **pull code, khởi chạy bản deploy có sẵn, đối chiếu từng dịch vụ với kiến trúc và chụp ảnh làm bằng chứng**.

| Thành phần workshop | Vai trò trong kiến trúc TINA |
| --- | --- |
| `make plan` | Kiểm tra read-only project, profile và `viegem_device` trước khi chạy worker |
| `make all` | Cài model, build service, khởi chạy và kiểm chứng ASR |
| Terminal UI (mặc định cổng `13000`) | Task Web serving — Next.js, API và WebSocket gateway |
| API gateway (mặc định cổng `18056`) | Route backend dùng bởi Terminal và Chrome extension |
| Cổng `23000` / `28056` | Chỉ dùng cho bản `tina-production` OrbStack được cấu hình sẵn — kiểm tra bằng `make plan` và `make all` |
| ASR control (cổng `18007`) | Host controller khởi động/dừng worker Gipformer và VieGem |
| VieGem `18005` / Gipformer `18002` | Worker STT — phiên âm tiếng Việt |
| Image ECR / GHCR | Image container cho Web, Bot, STT, TTS, Agent |
| CloudWatch / Budgets | Log, metric, alarm và cảnh báo chi phí theo proposal |

#### Chuẩn bị trước ngày thực hành

1. **Windows:** dùng **WSL2** với Docker Desktop tích hợp Linux/WSL và driver NVIDIA. Deploy native Windows Python/PowerShell **không được hỗ trợ**.
2. **macOS:** khởi động OrbStack hoặc Docker Desktop trước; Apple Silicon dùng PyTorch MPS native cho VieGem.
3. Cài **Docker Engine 26+**, Compose hỗ trợ `up --wait`, **Python 3.10+** và **make**.
4. Cài **Dotenvx** (`npm install --global @dotenvx/dotenvx` hoặc Homebrew tap trên macOS).
5. Xin file private **`.env.keys`** từ chủ sở hữu qua kênh bảo mật. Key tự tạo sẽ không giải mã được cấu hình repo. Không commit hay dán key vào đâu.
6. Chuẩn bị URL repo: `https://github.com/poor-frog/TINA.git`.

#### Hướng dẫn thực hành ngày 25/11/2026

**Bước 0 — Pull code**

1. Clone và vào thư mục:
   ```
   git clone https://github.com/poor-frog/TINA.git
   cd TINA
   ```
2. Đặt `.env.keys` ở gốc repo, rồi chạy `chmod 600 .env.keys`.
3. **Ảnh cần chụp:** `w0-clone.png` (repo vừa clone), `w0-env-key.png` (có file key, che giá trị).

**Bước 1 — Xem trước bản deploy (read-only)**

1. Chạy `make plan` — lệnh này chỉ hiển thị project, profile và `viegem_device` đề xuất, **không khởi động worker**.
2. Xác nhận profile là `automation,asr,dashboard,viegem` và ghi lại thiết bị chọn (MPS trên Apple Silicon, CUDA Docker trên WSL2/NVIDIA, hoặc CPU rõ ràng với `TINA_VIEGEM_DEVICE=cpu`).
3. **Ảnh cần chụp:** `w1-plan.png` (toàn bộ output `make plan`).

**Bước 2 — Khởi chạy toàn bộ hệ thống**

1. Chạy `make all`: cài model, build service, khởi chạy và kiểm chứng ASR bằng audio probe đã xác thực.
2. Đợi thông báo ready với 2 URL. Với fresh clone là:
   - Terminal UI: `http://127.0.0.1:13000`
   - API gateway: `http://127.0.0.1:18056`
   Nếu bạn dùng bản `tina-production` có thể là `23000` / `28056` — hãy tin vào URL do `make all` in ra.
3. Giữ API key do `make all` in ra bí mật; chụp ảnh phải che giá trị.
4. **Ảnh cần chụp:** `w2-make-all-start.png`, `w2-make-all-ready.png` (thấy URL, che key).

**Bước 3 — Kiểm tra các dịch vụ trong kiến trúc**

1. Liệt kê container đang chạy: `docker ps` (hoặc `docker compose ps`). Xác định Web, Bot, STT (VieGem/Gipformer), TTS, Agent và cổng của chúng.
2. Kiểm tra log lỗi: `docker logs <ten-container>` cho từng service.
3. Mở URL **Terminal UI** do `make all` in ra, đăng nhập Google và xác nhận Terminal UI tải được (user đầu tiên trở thành admin).
4. Xác nhận API gateway phản hồi:
   ```
   export API=http://127.0.0.1:18056   # 28056 trên tina-production
   export API_KEY=tina_...             # lấy từ make all / provision-token
   curl -sS -o /dev/null -w '%{http_code}\n' "$API/health"
   curl -sS -H "X-API-Key: $API_KEY" "$API/meetings"
   ```
5. **Ảnh cần chụp:** `w3-docker-ps.png`, `w3-logs.png`, `w3-terminal-ui.png`, `w3-gateway.png`.

**Bước 4 — Kiểm tra luồng AI và dữ liệu**

1. Settings → Models: xác nhận model phiên âm (VieGem hoặc Gipformer) đã được chọn và công tắc tài khoản đang bật.
2. Xác nhận worker được khởi động và UI hiển thị trạng thái vật lý tách biệt với trạng thái bật của tài khoản.
3. Mở giao diện cuộc họp, kiểm tra transcript trực tiếp, ghi chú, tóm tắt và dropdown ngôn ngữ **Tiếng Việt / English / Song ngữ**.
4. Đối chiếu S3/RDS/ElastiCache/Bedrock/SES với bản deploy đang chạy (task definition, cấu hình môi trường, log CloudWatch) thay vì chỉ tin vào sơ đồ.
5. **Ảnh cần chụp:** `w4-models.png`, `w4-worker-state.png`, `w4-transcript.png`, `w4-language.png`, `w4-cloudwatch.png`.

**Bước 5 — Kiểm tra chi phí và bảo mật theo proposal**

1. Xác nhận WAF đứng trước CloudFront và chỉ HTTPS được mở ra Internet.
2. Xác nhận IAM task role tối thiểu quyền, bí mật nằm trong Secrets Manager/KMS.
3. Xác nhận AWS Budgets có alert ở 50%, 80% và 100% hạn mức tháng.
4. **Ảnh cần chụp:** `w5-waf.png`, `w5-iam.png`, `w5-budgets.png`.

**Bước 6 — Dừng môi trường**

1. Chạy `make down` — lệnh này cũng dừng/xóa LaunchAgent MPS native nhưng giữ file model.
2. Xác nhận không còn container/worker thuộc quyền quản lý và không sót tài nguyên phát sinh chi phí.
3. **Ảnh cần chụp:** `w6-make-down.png`, `w6-after-down.png`.

#### Mẹo khi làm lần đầu

* Nếu `make all` lỗi ở bước kiểm tra GPU/driver/kernel, **không có fallback CPU tự động** — hãy sửa WSL2/NVIDIA hoặc dùng rõ `TINA_VIEGEM_DEVICE=cpu make all`.
* Registry phiên âm mới mặc định chọn VieGem; preferences cá nhân/toàn cục đã có thì giữ nguyên.
* `make down` giữ database, bản ghi âm và workspace — chỉ dừng dịch vụ thuộc quyền quản lý.
* Không đưa `.env.keys`, API key hay OAuth secret vào ảnh/chài liệu.

#### Nội dung

1. [Tổng quan workshop](5.1-workshop-overview/)
2. [Chuẩn bị](5.2-prerequiste/)
3. [Pull và deploy code](5.3-s3-vpc/)
4. [Kiểm tra các dịch vụ](5.4-s3-onprem/)
5. [Kiểm tra chi phí & bảo mật](5.5-policy/)
6. [Dọn dẹp](5.6-cleanup/)
