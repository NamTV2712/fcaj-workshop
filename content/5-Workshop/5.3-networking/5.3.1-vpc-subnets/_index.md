---
aliases: ["/5-workshop/5.3-s3-vpc/5.3.1-create-gwe/"]
title: "Create VPC and subnets"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

In VPC ? Your VPCs, create a VPC for the lab and enable DNS resolution and DNS hostnames. In VPC ? Subnets, add public (`10.80.1.0/24`, `10.80.2.0/24`), app (`10.80.11.0/24`, `10.80.12.0/24`) and data (`10.80.21.0/24`, `10.80.22.0/24`) subnets across two available AZs. Verify each subnet belongs to the lab VPC and record its ID privately.
