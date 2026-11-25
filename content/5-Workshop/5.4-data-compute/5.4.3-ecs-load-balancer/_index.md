---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.3-test-endpoint/"]
title: "ECS, task definitions and load balancer"
date: 2026-11-25
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

Inspect staging service desired/running counts, deployments, tasks, task definitions and log links. Find the internal ALB and target groups through `tina-staging-edge`. At inspection time the terminal and gateway targets were healthy; the terminal health path was `/api/auth/providers` and the gateway path was `/health`.

A new ECS cluster alone is not a complete TINA deployment. Portable task definitions, image digests, dependency order, service discovery, secrets and integration settings must first be supplied and tested. Fargate tasks do not support a GPU resource requirement.
