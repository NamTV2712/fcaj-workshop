---
title: "Worklog Tuần 4"
date: 2026-10-10
weight: 1
chapter: false
pre: " <b> 1.4. </b> "
---
### Mục tiêu tuần 4:

* Củng cố kiến thức Linux/WSL, Bash, process, service và networking.
* Tìm hiểu Docker, Nginx, CI/CD, Kubernetes, monitoring và AI infrastructure.
* Thực hành các dịch vụ AWS liên quan đến EC2, Lambda, CloudWatch, Route 53, migration và quản lý tài nguyên.
* Xem lại proposal và specification của project để hiểu rõ hơn kiến trúc và hướng phát triển.

### Các công việc cần triển khai trong tuần này:

| Thứ | Công việc                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu                                                                 |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------ | --------------------------------------------------------------------------------- |
| 2    | - Học và thực hành **Linux/WSL**: quản lý file/thư mục, path, wildcard, `grep`, `find`, `sed`, `awk`, pipe/redirect, permission, user/group, environment variable và `$PATH`. <br> - Tìm hiểu process/PID, signal, foreground/background, `nohup`, stdin/stdout/stderr, Python virtual environment, dependency với `pip`, Git và SSH. <br> - Tìm hiểu networking/IP/port, HTTP với `curl`, archive, disk/RAM và cấu trúc filesystem Linux như `/etc`, `/var`, `/mnt`, `/proc`. | 05/10/2026       | 05/10/2026         |                                                                                   |
| 3    | - Tìm hiểu **symlink, disk/filesystem/mount** và Bash scripting với variables, arguments, `if`, `for/while`, function và exit code. <br> - Học logging, `journalctl`, `systemd` và cách quản lý application như một Linux service: start/stop/restart, auto-start khi boot và theo dõi log. <br> - Xem lại **proposal và specification của project** để hiểu rõ hơn mục tiêu, kiến trúc và các thành phần chính của project. | 06/10/2026       | 06/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 4    | - Học Linux/DevOps với `systemd`, `cron`, `tmux`, Docker/Docker Compose, port/volume/network, firewall và các nguyên tắc security cơ bản. <br> - Tìm hiểu GPU/CUDA, `nvidia-smi`, performance monitoring, `lsof`, `strace`, Nginx, FastAPI production deployment, EC2/EBS/VPC, CI/CD, Container Registry và Kubernetes. <br> - Tìm hiểu model serving, vLLM, distributed training, MLOps, observability, Linux internals; đồng thời tìm hiểu **AWS CloudWatch** và **Hybrid DNS với Route 53 Resolver**. | 07/10/2026       | 07/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 5    | - Thực hành **Using AWS CLI on Amazon EC2 (Windows/Ubuntu)** để thao tác và quản lý tài nguyên AWS bằng command line. <br> - Thực hành **AWS Lambda** để tự động shutdown server và gửi thông báo tới **Slack**. <br> - Xây dựng hệ thống monitoring bằng **Amazon CloudWatch và Grafana**, theo dõi metrics và trực quan hóa dữ liệu qua dashboard. | 08/10/2026       | 08/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 6    | - Thực hành **AWS VM Import/Export** để tìm hiểu quy trình migrate virtual server hiện có lên AWS. <br> - Thực hành migration database với **AWS DMS và Schema Conversion Tool (SCT)**, gồm chuyển đổi schema và di chuyển dữ liệu. <br> - Sử dụng **Tags và Resource Groups** để phân loại, gom nhóm và quản lý tài nguyên AWS hiệu quả hơn. | 09/10/2026       | 09/10/2026         | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |

### Kết quả đạt được tuần 4:

* Củng cố kiến thức Linux/WSL, Bash scripting, process, networking và Linux service.
* Sử dụng và hiểu vai trò của các công cụ Linux như `grep`, `find`, `sed`, `awk`, `curl`, `journalctl`, `systemctl`, `cron`, `tmux`, `lsof` và `strace`.
* Hiểu các thành phần cơ bản của Docker/Docker Compose gồm image, container, port, volume và network.
* Có kiến thức nền tảng về Nginx, FastAPI deployment, CI/CD, Kubernetes, GPU/CUDA, vLLM, MLOps và observability.
* Hiểu thêm về Linux internals gồm process, syscall, file descriptor, namespace và cgroups.
* Hiểu rõ hơn proposal, specification, kiến trúc và định hướng phát triển của project.
* Thực hành quản lý EC2 bằng AWS CLI, automation với Lambda và monitoring bằng CloudWatch/Grafana.
* Tìm hiểu Hybrid DNS với Amazon Route 53 Resolver.
* Hiểu quy trình migration server bằng VM Import/Export và migration database bằng DMS/SCT.
* Biết cách sử dụng Tags và Resource Groups để tổ chức và quản lý tài nguyên AWS.
