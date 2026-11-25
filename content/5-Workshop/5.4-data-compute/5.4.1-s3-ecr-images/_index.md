---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.1-prepare/"]
title: "S3, ECR and images"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

> The detailed, step-by-step Console instructions are currently maintained in Vietnamese. Use the site language selector to open the corresponding Vietnamese page.

Use the staging CloudFormation resources list to locate the recordings bucket and ECR repositories; inspect metadata without downloading real recordings. In a lab account, create a private, globally unique bucket with public access blocked, upload a non-sensitive test object, and create a private ECR repository. Use ECR ? repository ? View push commands to tag and push an image built from the authorized source release. Confirm its tag and digest.
