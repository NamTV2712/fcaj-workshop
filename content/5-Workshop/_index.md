---
title: "Workshop"
date: 2026-11-25
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Workshop: Review TINA and Practise on the AWS Console

This workshop helps you **inspect the running TINA environment**, practise creating AWS components in the Console inside a separate lab, and collect evidence that another person can review. Each step lists the expected result and where to capture a screenshot.

> **Status:** Staging configuration was checked with AWS CLI on 25 November 2026. The full workshop has not been rerun from an empty account, and a new set of Console screenshots is not available yet. A successful stack status is not evidence that the whole meeting and transcription flow works.

## Read before you start

- Use a **separate practice account** or a `tina-ws-<your-name>` lab environment. Do not create, change or delete resources in `tina-staging-*` or `tina-prod-*` while doing the lab.
- Two different activities are involved: **observing the existing staging** for evaluation, and **creating lab resources** to learn the operations. Each page states which activity is safe to perform without changing the system.
- The `static/cloudformation/tina-infrastructure.yaml` sample in the workshop repository **is not** the deployment currently running TINA staging. Do not run it for the lab: the old template and guide contain contradictions about ECR, networking, health checks and application configuration.
- Before someone can rebuild **all of TINA** from scratch, they need a reviewed template set, secret-free parameters, source/image access, configuration guidance and a test run from a clean account. This workshop does not yet provide that set; the lab steps do not prove the whole system was recreated.

## Roadmap

1. [Overview and evaluation criteria](5.1-overview/).
2. [Prepare account, tools and cost](5.2-prerequisites/).
3. [Create VPC, subnets, routes and security groups in the Console](5.3-networking/).
4. [Inspect S3, images, data, ECS and the application](5.4-data-compute/).
5. [Check security, logs and cost](5.5-security-monitoring-costs/).
6. [Clean up lab resources and submit evidence](5.6-cleanup-evidence/).

Allow roughly 2–3 hours to observe and to do the network/S3/ECR lab; preparing artifacts and redeploying the application depends on the real scope. This estimate has not been measured in a full run.

## Evidence screenshot convention

At each step, a **Screenshot needed** box states the content and file name. Take a real screenshot and save a PNG in `static/images/5-Workshop/tina/` with that exact name; when the site is rebuilt the image will appear in place. See the [list of screenshots to capture](/images/5-Workshop/tina/README.md) for the full checklist.

**Do not capture or publish** passwords, API keys, secret values, tokens, personal information or real transcripts; mask account IDs, hostnames and internal identifiers before sharing. Only capture screens you are allowed to view. Boxes still showing a notice mean the image is not available yet.
