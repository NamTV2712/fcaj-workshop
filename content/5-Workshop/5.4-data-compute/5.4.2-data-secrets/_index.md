---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.2-create-interface-enpoint/"]
title: "Data, secrets and optional services"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

Inspect the staging PostgreSQL and Valkey resources, their private subnet groups and security groups, and secret metadata without revealing values. Optionally create a private lab DB subnet group and RDS database; create a lab cache only if needed and costed. Creating Cognito, Bedrock or SES resources does not by itself integrate them with TINA. SES in the inspected account was in sandbox at the time of review.
