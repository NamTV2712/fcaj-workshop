---
aliases: ["/5-workshop/5.3-s3-vpc/"]
title: "VPC and networking on the Console"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

Create an isolated example VPC `10.80.0.0/16` with two Availability Zones and six subnets, or choose another non-overlapping CIDR. This lab network is not the existing staging VPC. NAT gateways, Elastic IPs and interface endpoints can incur costs.

- [Create VPC and subnets](5.3.1-vpc-subnets/)
- [Create gateways, routes, security groups and an S3 endpoint](5.3.2-gateways-routing/)
