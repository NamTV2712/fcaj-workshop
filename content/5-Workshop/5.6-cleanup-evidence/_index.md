---
aliases: ["/5-workshop/5.6-cleanup/"]
title: "Cleanup and evidence"
date: 2026-11-25
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

Remove only resources you created for this lab, after checking account, Region, ownership, dependencies and data-retention requirements. Review ECS, ALB/CloudFront, RDS/cache, S3/ECR, endpoints, NAT, Elastic IP and VPC in dependency order. Never delete existing staging or production resources. A deleted stack can leave retained resources and snapshots behind.

The review package should contain the accessible release version, timestamped expected/actual results, real redacted screenshots, cost observations and cleanup evidence; mark the complete rebuild Blocked until it has been rehearsed.
