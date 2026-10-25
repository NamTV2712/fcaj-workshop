---
title: "Worklog Tuần 5"
date: 2026-10-17
weight: 1
chapter: false
pre: " <b> 1.5. </b> "
---
### Mục tiêu tuần 5:

* Tìm hiểu quản lý quyền truy cập, bảo mật và tự động hóa vận hành tài nguyên AWS.
* Thực hành Infrastructure as Code, quản lý hệ thống và triển khai ứng dụng.
* Tìm hiểu kết nối mạng VPC, giám sát bảo mật, sao lưu và lưu trữ dữ liệu trên AWS.

### Các công việc cần triển khai trong tuần này:

| Thứ | Công việc                                                                                                                                                                                                                                                                                                                                                                             | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu                                                                 |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------ | --------------------------------------------------------------------------------- |
| 2    | - Thực hành quản lý quyền truy cập EC2 bằng IAM kết hợp với Tags; tìm hiểu AWS Systems Manager để quản lý dịch vụ và tự động hóa tác vụ, đồng thời sử dụng Session Manager để truy cập và quản lý phiên làm việc.  - Tìm hiểu cách khởi tạo và quản lý hạ tầng AWS dưới dạng mã (Infrastructure as Code) bằng AWS CloudFormation. | 12/10/2026       | 12/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 3    | - Tìm hiểu và thiết lập đăng nhập một lần (Single Sign-On – Amazon SSO) cho AWS Organizations.  - Thực hành giới hạn quyền người dùng bằng IAM Permissions Boundaries và hạn chế việc chuyển giao IAM Role bằng các điều kiện trong policy.                                                                                                               | 13/10/2026       | 13/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 4    | - Thực hành kiểm tra các tiêu chuẩn bảo mật và tổng hợp phát hiện bảo mật bằng AWS Security Hub; tìm hiểu cách bảo vệ ứng dụng và API bằng AWS WAF.  - Tìm hiểu và thiết lập kế hoạch sao lưu, quản lý bản sao lưu tài nguyên bằng AWS Backup.                                                                                                  | 14/10/2026       | 14/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 5    | - Tìm hiểu và thực hành kết nối các VPC bằng VPC Peering để hỗ trợ giao tiếp giữa các mạng riêng ảo.  - Tìm hiểu AWS Transit Gateway để quản lý tập trung kết nối giữa nhiều VPC và các mạng liên quan.                                                                                                                                               | 15/10/2026       | 15/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 6    | - Thực hành triển khai ứng dụng bằng Docker và sử dụng AWS CodePipeline để xây dựng quy trình triển khai ứng dụng tự động.  - Tìm hiểu AWS Storage Gateway – File Gateway để kết nối môi trường lưu trữ file với AWS, hỗ trợ lưu trữ và truy cập dữ liệu trên cloud.                                                                          | 16/10/2026       | 16/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |

### Kết quả đạt được tuần 5:

* Hiểu cách quản lý quyền truy cập EC2 bằng IAM và Tags, giới hạn quyền với Permissions Boundaries và kiểm soát việc chuyển giao IAM Role bằng điều kiện.
* Tìm hiểu cơ chế đăng nhập một lần với Amazon SSO và quản lý hệ thống bằng AWS Systems Manager, Session Manager.
* Hiểu nguyên lý Infrastructure as Code và cách sử dụng AWS CloudFormation để khởi tạo, quản lý hạ tầng.
* Nắm được vai trò của AWS Security Hub trong kiểm tra bảo mật, AWS WAF trong bảo vệ ứng dụng/API và AWS Backup trong quản lý sao lưu.
* Hiểu cách kết nối các VPC bằng VPC Peering và quản lý kết nối mạng tập trung bằng AWS Transit Gateway.
* Thực hành triển khai ứng dụng bằng Docker, tìm hiểu quy trình CI/CD và tự động hóa triển khai với AWS CodePipeline.
* Tìm hiểu AWS Storage Gateway – File Gateway và cách tích hợp lưu trữ file với AWS Cloud.
