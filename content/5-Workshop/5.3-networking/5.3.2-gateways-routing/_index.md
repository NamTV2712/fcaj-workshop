---
aliases: ["/5-workshop/5.3-s3-vpc/5.3.2-test-gwe/"]
title: "Gateways, routing and security groups"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

Create and attach an Internet Gateway; create a public NAT gateway in a public subnet with a lab Elastic IP. Create route tables: public default route to the IGW, app default route to NAT, and no Internet default route for data subnets. Associate the matching subnets explicitly. Create restricted security groups and an S3 gateway endpoint associated with the appropriate lab route tables. See the Vietnamese page for individual Console selections and evidence names.
