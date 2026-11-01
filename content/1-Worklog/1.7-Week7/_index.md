---
title: "Week 7 Worklog"
date: 2026-10-31
weight: 1
chapter: false
pre: " <b> 1.7. </b> "
---

### Week 7 Objectives

- Understand messaging and event processing in microservices, including asynchronous communication and message queues.
- Design the project's AWS architecture, identify the required services, and define the main data flows.
- Prepare a separate U4 – Retained Meeting Experience workspace and review the existing project baseline.
- Analyze U4 functional and non-functional requirements and prepare technical design and implementation planning documents.

### Tasks to be carried out this week:

| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Study synchronous and asynchronous messaging in microservices and the role of event-driven architecture. <br> - Explore Amazon SQS, Amazon SNS, and Amazon EventBridge for communication between services. <br> - Review message retries, dead-letter queues (DLQs), and fault-tolerant event processing. | 26/10/2026 | 26/10/2026 | [https://cloudjourney.awsstudygroup.com/](https://cloudjourney.awsstudygroup.com/) |
| 3 | - Design the project's AWS architecture using a VPC, public/private subnets, an Application Load Balancer, and separate EC2 workloads for Backend and ASR processing. <br> - Identify supporting services, including Amazon S3, Amazon DynamoDB, Amazon Bedrock, AWS Lambda, and Amazon CloudWatch, based on system requirements. <br> - Complete the architecture diagram and document REST API, WebSocket audio streaming, speech recognition, storage, and AI processing flows. | 27/10/2026 | 27/10/2026 |  |
| 4 | - Check local Git changes, prepare a separate U4 workspace, synchronize with main, and record the baseline commit. <br> - Review the relevant AI-DLC space and intent, inspect unit status, and follow the U4 ownership/claim workflow. <br> - Install dependencies from lockfiles and run existing backend and extension checks to record baseline issues. | 28/10/2026 | 28/10/2026 |  |
| 5 | - Review the acceptance criteria of U4's three primary stories and seven shared stories; identify dependencies on U1, U2, U3, and U5. <br> - Design meeting history, detail, export, deletion, receipt, and navigation flows, including data entities and loading/error states. <br> - Prepare functional design and traceability documents; specify NFRs for access control, pagination, retention, reliability, accessibility, and performance. | 29/10/2026 | 29/10/2026 |  |
| 6 | - Design U4 non-functional behavior, including authorization, cache invalidation, timeout recovery, secure content handling, and diagnostics. <br> - Define backend integration, IAM permissions, meeting history access patterns, and data compatibility with existing U1 records. <br> - Prepare the Code Generation Plan, module ownership, TDD implementation order, test instructions, and cross-unit coordination items for review. | 30/10/2026 | 30/10/2026 |  |

### Week 7 Achievements

- Improved understanding of event-driven communication in microservices and the role of Amazon SQS, SNS, and EventBridge.
- Produced an AWS architecture diagram and clarified the main application workflows and connections between services.
- Established a clearer U4 development baseline, ownership process, and approach to identifying pre-existing issues.
- Organized U4 acceptance criteria, functional behavior, integration dependencies, and non-functional requirements.
- Prepared the technical design and implementation plan as a basis for review and subsequent development.
