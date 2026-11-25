---
title: "Workshop"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Đánh giá TINA và thực hành AWS Console

Workshop này giúp bạn **kiểm tra môi trường TINA đang chạy**, thực hành tạo các thành phần AWS bằng Console trong một môi trường riêng, và thu thập bằng chứng để người khác đánh giá. Các bước có kết quả mong đợi và vị trí cần chụp ảnh.

> **Trạng thái:** Đã đối chiếu cấu hình staging qua AWS CLI ngày 25/11/2026. Chưa thực hiện lại toàn bộ workshop từ một tài khoản trống và chưa có bộ ảnh Console mới. Không xem trạng thái stack thành công là bằng chứng toàn bộ luồng họp và phiên âm đã hoạt động.

## Đọc trước khi bắt đầu

- Dùng tài khoản thực hành riêng hoặc môi trường `tina-ws-<ten-ban>`. Không tạo, thay đổi hay xóa tài nguyên trong `tina-staging-*` hoặc `tina-prod-*` nếu bạn chỉ đang làm bài thực hành.
- Có hai việc khác nhau: **quan sát staging hiện có** để đánh giá; và **tạo tài nguyên lab** để học các thao tác. Mỗi trang sẽ ghi rõ việc nào có thể làm mà không thay đổi hệ thống.
- Bản mẫu `static/cloudformation/tina-infrastructure.yaml` trong repository workshop **chưa phải** bộ triển khai TINA staging đang chạy. Không chạy template đó để thực hành: template và hướng dẫn cũ có các mâu thuẫn về ECR, mạng, health check và cấu hình ứng dụng.
- Trước khi một người khác có thể dựng lại **toàn bộ TINA** từ số 0, cần cung cấp bộ template đã rà soát, các tham số không chứa bí mật, quyền truy cập source/image, hướng dẫn cấu hình và kết quả chạy thử từ tài khoản sạch. Workshop hiện chưa có đủ bộ này; các bước lab không chứng minh đã tái tạo toàn bộ hệ thống.

## Lộ trình

1. [Tổng quan và tiêu chí đánh giá](5.1-overview/).
2. [Chuẩn bị tài khoản, công cụ và chi phí](5.2-prerequisites/).
3. [Tạo VPC, subnet, route và security group trên Console](5.3-networking/).
4. [Kiểm tra S3, image, dữ liệu, ECS và ứng dụng](5.4-data-compute/).
5. [Kiểm tra bảo mật, log và chi phí](5.5-security-monitoring-costs/).
6. [Dọn riêng tài nguyên lab và nộp bằng chứng](5.6-cleanup-evidence/).

Dành khoảng 2–3 giờ để quan sát và làm phần lab mạng, S3, ECR; phần chuẩn bị artifact và tái triển khai ứng dụng phụ thuộc phạm vi thực tế. Thời gian này là dự kiến, chưa đo bằng một lần chạy trọn vẹn.

## Quy ước ảnh minh chứng

Ở mỗi bước, khung **Ảnh cần bổ sung** ghi rõ nội dung và đường dẫn của ảnh. Chụp màn hình thật rồi lưu PNG vào `static/images/5-Workshop/tina/` với đúng tên đó; khi website được dựng lại, ảnh sẽ tự xuất hiện tại đúng vị trí. Xem [danh sách ảnh cần chụp](/images/5-Workshop/tina/README.md) để đối chiếu toàn bộ.

**Không chụp hoặc công bố** mật khẩu, API key, giá trị secret, token, thông tin cá nhân hay transcript thật; che account ID, hostname và định danh nội bộ trước khi chia sẻ. Chỉ chụp màn hình có quyền xem. Những khung còn hiện thông báo là ảnh chưa có sẵn.
