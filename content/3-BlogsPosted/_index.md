---
title: "Blogs Posted"
date: 2026-10-22
weight: 3
chapter: false
pre: " <b> 3. </b> "
---

During my internship at AWS First Cloud AI Journey, I spent time researching articles from the AWS Blog, combining hands-on lab experience and daily learning to write technical blog posts. Each blog post focuses on a specific topic, helping me consolidate knowledge, share experiences, and introduce solutions and best practices on AWS. My goal is to contribute practical, accessible content to the AWS Study Group community that can be applied directly to real-world work.

The following blog posts were shared on AWS Study Group:

### [Blog 1 - Amazon Transcribe vs OpenAI Whisper: Which Speech-to-Text Solution Fits Vietnamese?](3.1-Blog1/)

Amazon Transcribe and OpenAI Whisper approach the same speech-to-text problem from two different directions: a fully managed AWS service and an open-source model that teams can self-host. The post compares Vietnamese recognition quality, deployment models, operating costs, and the trade-offs between convenience and control. It also walks through practical AWS architectures, from batch transcription to near-real-time streaming, and explains how to evaluate results objectively with Word Error Rate (WER) and Character Error Rate (CER). Rather than assuming one option is better, the article shows how to benchmark both solutions on the same Vietnamese dataset and choose based on accuracy, budget, and operational requirements.

### [Blog 2 - From Meeting Transcripts to Notion Tasks with DynamoDB Streams, Lambda and Bedrock](3.2-Blog2/)

The post describes an event-driven pipeline that starts automatically when a meeting transcript is marked as completed in DynamoDB. DynamoDB Streams triggers AWS Lambda, which reads the transcript from Amazon S3, calls Amazon Bedrock to extract action items, and stores the proposed tasks for human review before creating them in Notion. The article explains each step in detail, including the Lambda handler, prompt design, idempotency checks, human confirmation, and cost considerations. It also discusses how the same pattern can be extended to email, support tickets, call-center transcripts, and other task management tools, making it a reusable blueprint for serverless automation.

### [Blog 3 - Amazon Nova 2.5 Sonic: From Voice Assistants to Task-Performing Voice Agents](3.3-Blog3/)

The post examines Amazon Nova 2.5 Sonic, a speech-to-speech model on Amazon Bedrock that aims to replace the traditional STT → LLM → TTS pipeline with a single real-time model. It covers low-latency voice interaction, barge-in, tool calling, asynchronous tool use, and cross-modal sessions, then shows how Nova Sonic can be combined with AgentCore Runtime, Gateway, Lambda, and DynamoDB to build a complete voice agent. The article also discusses practical use cases, current language limitations, cost and operational considerations, and when a simpler transcription service such as Amazon Transcribe is still the better choice.
