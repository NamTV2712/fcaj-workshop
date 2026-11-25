---
title: "Workshop"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

# Workshop: Review TINA and practice on AWS Console

This workshop explains how to inspect the existing TINA staging environment and create a separate network/S3/ECR lab. Findings below were checked using AWS CLI on 25 November 2026; application end-to-end behavior and a complete rebuild in a clean account have not yet been verified. Screenshots named in the Vietnamese pages are requested evidence, not existing images.

**Do not deploy the old** `static/cloudformation/tina-infrastructure.yaml` as a recreation of staging: it does not match the deployed stack, and the complete, portable release artifacts are not yet provided. Do not change or delete staging/production resources while doing the lab.

1. [Overview](5.1-overview/)
2. [Prerequisites](5.2-prerequisites/)
3. [VPC and networking](5.3-networking/)
4. [Data, images, ECS and application](5.4-data-compute/)
5. [Security, monitoring and costs](5.5-security-monitoring-costs/)
6. [Cleanup and evidence](5.6-cleanup-evidence/)
