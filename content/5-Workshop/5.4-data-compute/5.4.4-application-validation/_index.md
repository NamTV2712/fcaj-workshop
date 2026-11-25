---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.4-dns-simulation/"]
title: "Validate the System and Prepare for Redeployment"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

## A. Validate the running application

1. In **CloudFormation → Stacks → tina-staging-edge → Outputs**, find `StageUrl`. Only authorised people may open this URL; do not paste an internal URL into a public report.
2. Open the staging URL in a browser. Compare the HTTP status/login page with the test target. On 25 November 2026, a HEAD request to this URL returned `200`; that is only an access check and does not prove login or the meeting flow.

{{< workshop-screenshot file="16-app-login.png" description="Login page or web response of the test environment." >}}

3. If permitted and you have a test account, sign in using the method actually configured. Use a test meeting and fake data agreed by all participants; do not record or capture people or private content.
4. Check in order: create or join a test meeting → bot joins → audio reaches the self-hosted STT endpoint → transcript appears → stop the meeting → inspect results/storage according to granted permissions.

{{< workshop-screenshot file="17-test-meeting.png" description="Test meeting and bot joining, using permitted fake data." >}}

{{< workshop-screenshot file="18-test-transcript.png" description="Transcript of the test meeting; no private content." >}}

5. Record **Expected**, **Actual**, the time and **Pass/Fail/Blocked** for each step. If permission, a model, a meeting URL or test data is missing, record **Blocked** with the reason; do not replace it with fake images or results.

| Check | Pass when | Evidence |
| --- | --- | --- |
| Web access | Staging URL opens and responds appropriately | Screenshot of the test page after masking private data |
| ECS/ALB | Services stable and relevant targets `healthy` | Service + target health screenshots |
| Test meeting | Bot joins the permitted test room | Redacted screenshot or log |
| Transcription | Fake content appears per the agreed criteria | Fake transcript screenshot + timestamp |
| Data write | Test file is found where the system really stores it | Object metadata, no private data captured |

## B. Make the workshop redeployable from scratch

Before asking a reviewer to rebuild the whole system, the instructor must prepare:

1. An accessible source commit/tag and matching image/digest set, including CPU architecture, pull access and build guidance.
2. Templates or manifests for the **whole** stack, deployment order and parameter/output lists; no account IDs, passwords, tokens or real secrets. Templates currently in AWS can be viewed via **CloudFormation → stack → Template** and reviewed before being packaged.
3. Documentation for role/SG/service discovery setup, DB migration, DNS/certificate, secrets, STT, models and cost/quota. State clearly what is mandatory and what is optional.
4. A rerun from a clean lab account; record times, commands, screenshots and fixed errors. Repeat the application check and lab cleanup end to end.
5. Only then publish the guide with pinned versions. Do not push source/images/templates to a public place before the project owner permits it and the content is reviewed.

### Real inputs to cross-check

To build a parameter table, open each stack in **CloudFormation → Stacks → select stack → Parameters**, then compare **Outputs** and **Resources** of related stacks. Record parameter names and their source; do not copy secret values or account identifiers into public documents. The names below were checked against staging templates on 25 November 2026:

| Stack | Some inputs to prepare | Check next |
| --- | --- | --- |
| `tina-foundation` | Current template declares no parameters | Review hardcoded CIDRs and names before turning it into a template usable in another account. Do not both create manually and let the template create the same resource. |
| `tina-staging-egress` | `PublicSubnetId`, `AppRouteTableA`, `AppRouteTableB` | Take them from the foundation of your own lab environment. |
| `tina-staging-edge` | `VpcId`, `AppSubnetIds`, `WebAclArn`, `CloudFrontOriginPrefixListId` | Identify ARN/prefix-list sources appropriate to Region and lab; check VPC origin configuration. |
| `tina-staging-datastores` | `VpcId`, `DataSubnetIds`, `DeployValkey` | Check subnet groups, database, cache and secret provisioning. |
| `tina-staging-bot` | `ClusterName`, `BotRepositoryArn`, `BotImage`, `InvocationBucket`, `ProbeInvocation` | Determine image digest, task run permissions and suitable storage. |
| `tina-staging-runtime` | `VpcId`, `AppSubnetIds`, `ClusterName`, `RuntimeImage`, `BotTaskDefinitionArn` plus Valkey/workspace parameters | Review all Parameters; identify optional ones, roles, storage and service discovery. |
| `tina-staging-core` | `VpcId`, `AppSubnetIds`, `ClusterName`, images, `PostgresHost`, `ValkeyHost`, `RecordingsBucket`, secret ARNs and internal URLs | Cross-check STT, TTS, runtime, agent, MCP and migration in full. |
| `tina-staging-terminal` | `StageUrl`, `ListenerArn`, `TerminalImage`, `GoogleSecretArn`, `InternalSecretArn` plus VPC/subnet/SG parameters | Prepare a valid OAuth callback; never publish secrets or private URLs. |
| `tina-staging-viegem`, `tina-staging-voice`, `tina-staging-agent-api`, `tina-staging-agent-reach`, `tina-staging-mcp`, `tina-staging-flows` | Image, cluster, subnets, service discovery and connection parameters per stack | Review the full list in the Console; verify parameters and dependencies against the real release. |

This is a **survey** table, not a tested deployment order; some stacks reference each other and optional features can change dependencies. Before exporting templates or sharing screenshots, review hardcoded ARNs, domains, account IDs and every sensitive value.

The old `static/cloudformation/tina-infrastructure.yaml` does not satisfy the list above, and a `CREATE_COMPLETE` stack from one template is not evidence that application features work.

Use only test data; do not put real documents or recordings into the workshop.
