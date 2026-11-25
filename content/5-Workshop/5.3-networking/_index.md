---
aliases: ["/5-workshop/5.3-s3-vpc/"]
title: "Build a VPC and Network in the Console"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.3. </b> "
---

## Objectives

Create a **separate lab network** with two Availability Zones, six subnets, an Internet Gateway, one NAT Gateway and route tables. Then create security groups and an S3 gateway endpoint. These steps teach network operations; they do not create a TINA system by themselves.

> The values below are **examples for a new lab**, not the staging configuration. Observed staging uses VPC `10.42.0.0/16`; production uses a different VPC. Do not modify those two VPCs for the lab. If the example CIDR overlaps a network you connect to or violates account policy, choose a non-overlapping lab CIDR.

| Example name | IPv4 CIDR | Role |
| --- | --- | --- |
| `tina-ws-vpc` | `10.80.0.0/16` | Whole lab network |
| `tina-ws-public-a`, `tina-ws-public-b` | `10.80.1.0/24`, `10.80.2.0/24` | Public, two AZs |
| `tina-ws-app-a`, `tina-ws-app-b` | `10.80.11.0/24`, `10.80.12.0/24` | Private for the app, two AZs |
| `tina-ws-data-a`, `tina-ws-data-b` | `10.80.21.0/24`, `10.80.22.0/24` | Private for data, two AZs |

NAT Gateway, Elastic IP and interface endpoints can incur charges even before an application is placed in the lab. A single NAT in AZ A keeps the lab simple but provides no failover if AZ A fails.

1. [Create the VPC and six subnets](5.3.1-vpc-subnets/).
2. [Create gateways, routes, security groups and endpoint](5.3.2-gateways-routing/).

**Result:** the VPC and subnets exist and routes/associations match the table; application traffic has not been verified at this step.
