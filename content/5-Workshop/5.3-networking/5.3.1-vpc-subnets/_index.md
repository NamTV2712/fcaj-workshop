---
aliases: ["/5-workshop/5.3-s3-vpc/5.3.1-create-gwe/"]
title: "Create a VPC and Subnets in the Console"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

## 1. Create the VPC

1. Select Region `us-east-1`; go to **VPC → Your VPCs → Create VPC**.
2. Choose **VPC only**. Set **Name tag** to `tina-ws-vpc`, **IPv4 CIDR** to `10.80.0.0/16`, leave IPv6 unassigned and tenancy **Default**; choose **Create VPC**.

{{< workshop-screenshot file="03a-create-vpc.png" description="Lab VPC creation form with name and CIDR before confirming." >}}

3. Select the new VPC → **Actions → Edit VPC settings**. Enable **DNS resolution** and **DNS hostnames**, then save.
4. Record the VPC ID in private notes. From here on, always check the VPC ID column before selecting resources.

## 2. Create six subnets

1. Go to **VPC → Subnets → Create subnet** and select the lab VPC.
2. Add the subnets below. Choose one AZ for group A and a different one for group B; in `us-east-1` these can be `us-east-1a` and `us-east-1b` if your account offers them.

| Name | AZ | CIDR |
| --- | --- | --- |
| `tina-ws-public-a` | A | `10.80.1.0/24` |
| `tina-ws-public-b` | B | `10.80.2.0/24` |
| `tina-ws-app-a` | A | `10.80.11.0/24` |
| `tina-ws-app-b` | B | `10.80.12.0/24` |
| `tina-ws-data-a` | A | `10.80.21.0/24` |
| `tina-ws-data-b` | B | `10.80.22.0/24` |

{{< workshop-screenshot file="03b-create-subnets.png" description="Lab subnet creation form with VPC, name, AZ and CIDR." >}}

3. Choose **Create subnet** and wait until all are **Available**. Depending on the AWS UI you may add subnets one at a time or multiple rows in one form.
4. Filter by the lab VPC, confirm three subnets in each AZ and no overlapping ranges. Record the six subnet IDs.

{{< workshop-screenshot file="03-vpc-subnets.png" description="Six subnets of the lab VPC with CIDR and Availability Zone." >}}

A subnet reaches the Internet only when attached to a suitable route table and its resources have the required IP configuration; the name `public` does not create connectivity by itself. NAT will be placed in the public subnet in the next step.
