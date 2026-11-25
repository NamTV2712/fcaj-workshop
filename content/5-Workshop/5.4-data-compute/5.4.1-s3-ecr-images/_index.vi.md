---
aliases: ["/vi/5-workshop/5.4-s3-onprem/5.4.1-prepare/"]
title: "S3, ECR và image"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

## A. Quan sát bucket và image staging

1. Vào **CloudFormation → Stacks → tina-foundation → Resources**. Tìm tài nguyên S3 recording và chọn physical ID để mở S3. Chỉ xem cấu hình; không mở, tải hay xóa bản ghi thật khi không cần.
2. Trong **S3 → Buckets**, mở bucket được phép xem → **Properties** và **Permissions**: ghi nhận mã hóa, Block Public Access và lifecycle thực tế.
3. Vào **Amazon ECR → Private registry → Repositories**. Lọc `tina-staging/`, mở repository của từng service → **Images** và xem image tag, digest, thời điểm push.
4. Vào **ECS → Clusters → tina-foundation-ecs → Services → service cần xem → Tasks → task đang chạy**. Mở task definition được dùng và đối chiếu image/digest nếu Console cung cấp. Không chụp các giá trị môi trường hoặc secret.

**Đạt:** biết ứng dụng dùng image nào và bucket nào là thành phần recording. Có bucket hoặc image không chứng minh upload recording thành công.

## B. Tạo một bucket lab bằng Console

1. Vào **S3 → Buckets → Create bucket**. Chọn **General purpose**, Region `us-east-1` và tên duy nhất toàn cầu, ví dụ `tina-ws-<chuoi-ngau-nhien>-recordings` (thay phần trong ngoặc).
2. Giữ **Block all public access**; chọn mã hóa mặc định phù hợp chính sách lab. Chỉ bật versioning nếu bạn hiểu cách dọn các object version.
3. Kiểm tra lựa chọn, chọn **Create bucket**. Mở bucket → **Properties/Permissions** để xác nhận.
4. Dùng một tệp thử không nhạy cảm: **Objects → Upload → Add files → Upload**. Kiểm tra object xuất hiện, ghi kích thước và thời gian. Chỉ đưa tệp mẫu vào bucket lab; không upload recording cá nhân làm bài.

{{< workshop-screenshot file="07-s3-lab.png" description="Bucket lab và object thử không chứa dữ liệu nhạy cảm." >}}

## C. Tạo ECR repository và push một image lab

1. Vào **ECR → Private registry → Repositories → Create repository**.
2. Chọn private, tên ví dụ `tina-ws/terminal`; chọn tag immutability và scan theo chính sách tổ chức, rồi tạo repository.
3. Mở repository → **View push commands**. AWS hiển thị chính xác lệnh đăng nhập Docker, tag và push cho account/Region đó. Chạy lệnh trên máy đã cài Docker/AWS CLI, không đưa token vào tài liệu.
4. Nếu được cấp source TINA đúng phiên bản, ở thư mục source dùng `make build`; lệnh này build các image cần thiết và có thể mất thời gian. Kiểm tra image thực tế bằng `docker image ls`; với Compose hiện tại, image Terminal mặc định thường là `tina/v012-terminal:dev`, nhưng phải xác nhận theo phiên bản source của bạn.
5. Dùng đúng tên image vừa kiểm tra làm nguồn `docker tag`, sau đó push theo **View push commands**. Quay lại ECR, refresh và kiểm tra tag/digest. Chú ý kiến trúc image phải phù hợp runtime.

{{< workshop-screenshot file="08-ecr-image.png" description="Repository ECR lab hiển thị image tag và digest." >}}

**Đạt:** bucket lab chứa tệp thử và ECR có image/digest thực tế. Chưa có điều này thì không thể khai báo image đó cho ECS. Tài nguyên lab không được tạo trùng tên/ghi đè staging.

