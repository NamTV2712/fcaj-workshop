---
title: "Week 11 Worklog"
date: 2026-11-24
weight: 11
chapter: false
pre: " <b> 1.11. </b> "
---
### Week 11 Objectives:

* Evaluate test results, identify bottlenecks and optimize the cost of TINA's AWS architecture.
* Accelerate live Vietnamese-to-English translation and complete the CI/CD pipeline for AWS deployment.
* Perform basic security checks (WAF, IAM) and trial cost-saving options: stopping services outside working hours, Fargate Spot and VPC endpoints.

### Tasks to be carried out this week:

| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Accelerate live VI-to-EN phrase translation with batch draining and lower latency. <br> - Add speaker/turn context, tail priority, language persistence and a copy-clean EN badge. <br> - Update the `meeting-translation.v2` contract docs for batch and context behavior. <br> - Merge PR #26 (`enhance/streamming_translate_Vi2En`). | 23/11/2026 | 23/11/2026 |  |
| 3 | - Switch to direct HTTP translation, clean up ephemeral workers and add a soft STT thought bubble. <br> - Fix concurrency syntax in GitHub Actions, publish `tina-tts`, make gipformer opt-in and add `workflow_dispatch`. <br> - Declare `TINA_DIRECT_TRANSLATE` in `config.v1` and free extra disk space for the bot build. <br> - Evaluate test results and identify bottlenecks in the translation and deployment flow. | 24/11/2026 | 24/11/2026 |  |
| 4 | - Publish `livekit-agent`, clean ECR manifests and promote `demo`/`latest` tags. <br> - Rename the aws-demo kit and workflow to `aws`. <br> - Promote the `:prod` tag instead of `:demo` across workflows and AWS deploy. <br> - Review cost optimization options: stop Web/Agent/RDS/ElastiCache outside working hours, use Fargate Spot for Bot/STT/TTS and VPC endpoints for S3/ECR. | 25/11/2026 | 25/11/2026 |  |
| 5 | - Perform basic security checks: WAF web ACL, least-privilege IAM task roles, Secrets Manager and KMS. <br> - Cross-check the production AWS setup (ECS/Fargate, ALB, CloudFront, Cognito, SES) with the proposal design. <br> - Track cost with AWS Budgets and Cost Explorer, updating the estimate in the proposal. | 26/11/2026 | 26/11/2026 |  |
| 6 | - Consolidate evaluation results and update the proposal and architecture docs. <br> - Wrap up the week, update the worklog and prepare for the project demo/final review. | 27/11/2026 | 27/11/2026 |  |

### Week 11 Achievements:

* Accelerated and stabilized the live VI-to-EN translation flow via PR #26: batch draining, speaker/turn context, tail priority and language persistence.
* Switched to direct HTTP translation, cleaned up ephemeral workers and updated the `meeting-translation.v2` contract documentation.
* Completed the CI/CD pipeline on GitHub Actions/GHCR: published `tina-tts` and `livekit-agent`, cleaned ECR manifests, promoted the `:prod` tag, renamed the AWS kit/workflow and added `workflow_dispatch`.
* Reviewed cost optimization options from the proposal: stopping services outside working hours, Fargate Spot for meeting tasks, VPC endpoints for S3/ECR and AWS Budgets alerts.
* Performed basic security checks with WAF and least-privilege IAM task roles; cross-checked the production setup against the designed architecture.
* Gained a clearer process for bottleneck evaluation, regression testing and keeping architecture documentation in sync with the project.
