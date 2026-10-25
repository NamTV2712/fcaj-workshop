---
title: "Event 4"
date: 2026-10-24
weight: 1
chapter: false
pre: " <b> 4.4. </b> "
---

# Event Takeaways: "First Cloud AI Journey Meet Up"

### Event Objectives

- Explore practical applications of **Cloud Computing, Artificial Intelligence and AI Agents** through real-world industry presentations.
- Learn how businesses use AWS services to build Voice AI systems, manage cloud resources and improve application security.
- Understand approaches to deploying AI Agents in production, including runtime environments, memory management and security controls.
- Explore how AI Agents can support software development, code review, system monitoring and automated workflows.
- Gain practical insights from industry engineers and Tech Leads, and connect with the Cloud and AI community.

### Speakers

The event featured five technical sessions delivered by engineers and technology leaders working in Cloud, AI and software development:

- **Kiet Tran** – Revve AI, speaker of **"Hear, Think, Speak – Building a Vietnamese Voice-AI Contact Center on AWS"**.
- **Long Huynh** – Styl Solution, speaker of **"AWS Resource Access Manager"**.
- **Thinh Nguyen** – Styl Solution, speaker of **"AWS Pentest with AWS Continuum / Security Agent"**.
- **Xuan An** – Leader of AWS Student Builder Group HCMUTE, speaker of **"Amazon Bedrock AgentCore"**.
- **Khoa Kieu** – Tech Lead at ACB, and **Nghi Danh** – AWS Community Builder, speakers of **"Kiro Crew"**.

The meet up took place from **9:00 AM to 12:00 PM on October 24, 2026**, on the 26th floor of Bitexco Financial Tower in Ho Chi Minh City.

### Key Highlights

#### Hear, Think, Speak – Building a Vietnamese Voice-AI Contact Center on AWS

- Explored the architecture of Voice AI systems built on AWS.
- Learned about the importance of reducing latency to approximately **1.8 seconds** to make voice conversations feel more natural.
- Observed a live demonstration of an AI system conducting an initial Cloud Engineer interview over a phone call in Vietnamese.
- Gained a better understanding of the challenges involved in building real-time voice interactions.

#### AWS Resource Access Manager

- Learned how **AWS Resource Access Manager (AWS RAM)** enables resources to be shared across accounts within an AWS Organization.
- Explored how centralized resource sharing can simplify network administration and reduce unnecessary duplication.
- Understood the relationship between IAM policies and Service Control Policies (SCPs) in managing access permissions.
- Recognized the importance of defining permission boundaries and applying least-privilege principles in multi-account environments.

#### AWS Pentest with AWS Continuum / Security Agent

- Explored approaches to identifying security issues earlier in the software development process.
- Learned how Terraform code can be reviewed and security checks can be integrated into GitLab/GitHub Pull Requests.
- Discovered how Security Agents can help automate security testing in SIT/UAT environments before production deployment.
- Understood the benefits of integrating security checks into development workflows instead of waiting until the final deployment stage.

#### Amazon Bedrock AgentCore

- Explored **Amazon Bedrock AgentCore** and its role in supporting AI Agents in production environments.
- Learned about AgentCore Runtime and the use of lightweight MicroVM environments on EC2 Spot to help optimize operating costs.
- Studied the distinction between synchronous Short-term Memory and asynchronous Long-term Memory.
- Understood how memory mechanisms help AI Agents retain relevant information and maintain context across interactions.
- Recognized that deploying AI Agents requires more than an LLM; runtime infrastructure, memory, security and operational controls are also important.

#### Kiro Crew

- Explored how AI Agents can operate continuously to support code reviews and system checks.
- Learned how Kiro Crew can create Artifacts by gathering real-world data, organizing information and generating visualizations directly in the chat interface.
- Studied **Context Window management**, including Auto Compact when context usage reaches approximately 70–90%.
- Learned about breaking down context usage to examine token consumption across different components.
- Explored Memory management techniques to remove outdated information and avoid unnecessary context growth.
- Understood the importance of Guardrails to prevent dangerous actions, protect infrastructure and reduce the risk of exposing secrets or server credentials.

### What I Learned

#### Voice AI and Real-Time Applications

- Voice AI systems must balance response quality, latency and the natural flow of conversations.
- Real-time applications require careful consideration of the entire interaction pipeline, not just the underlying AI model.
- Practical demonstrations helped me understand how AI can be applied to customer support and recruitment workflows.

#### AWS Resource Management and Security

- AWS RAM supports resource sharing across accounts, helping simplify administration in multi-account environments.
- IAM policies and SCPs serve different purposes and can work together to establish appropriate access restrictions.
- Security checks can be integrated into development workflows to identify potential issues before deployment.
- Automated security testing can help teams identify risks earlier and reduce reliance on purely manual checks.

#### AI Agent Architecture

A production-ready AI Agent requires more than a Large Language Model. Important components include:

- **LLM:** Processes requests and generates responses.
- **Runtime:** Provides an environment in which the Agent can execute.
- **Tools and APIs:** Allow the Agent to interact with external systems.
- **Memory and Context:** Help retain relevant information across interactions.
- **Security and Guardrails:** Restrict unsafe operations and protect sensitive resources.
- **Monitoring and Cost Management:** Help track usage, performance and operating expenses.

I gained additional insight into how Agent runtime and memory systems support reliable AI applications in production.

#### AI Coding and Context Management

- AI Agents can assist with recurring software development tasks, including code review and system checks.
- Context Window management is important because excessive context can increase token usage and operating costs.
- Memory should be organized and maintained instead of retaining every piece of information indefinitely.
- Guardrails are necessary when AI Agents can execute tools or interact with infrastructure.
- AI automation should be designed with clear boundaries and appropriate human oversight.

### Applying to Work

- Explore using AI Agents to support code review, issue investigation and automated checks in software development projects.
- Research AWS multi-account access management and apply least-privilege principles when designing cloud infrastructure.
- Investigate how automated security checks can be integrated into GitHub/GitLab workflows.
- Explore **Amazon Bedrock AgentCore** and other Agent runtime options when designing AI Agents for production environments.
- Consider memory and context management strategies to control token consumption and maintain relevant information.
- Design Guardrails and permission controls before allowing AI Agents to execute sensitive operations.
- Evaluate AI solutions based on reliability, latency, security and operating costs, rather than focusing only on response quality.

### Event Experience

Attending the **First Cloud AI Journey Meet Up** at Bitexco Financial Tower was a valuable learning experience. The five sessions covered practical challenges in Voice AI, AWS resource management, security automation, AI Agent infrastructure and AI-assisted software development.

#### Learning from Real-World Applications

- The Voice AI demonstration showed how AI can support natural, real-time interactions in practical business scenarios.
- The AWS RAM and Security Agent sessions highlighted the importance of access control and security throughout the development process.
- The Amazon Bedrock AgentCore session provided a clearer view of the infrastructure and memory mechanisms needed to operate AI Agents in production.
- The Kiro Crew session was especially interesting because it demonstrated how AI Agents can assist with continuous code review and system checks.

#### Understanding Production Challenges

- Building an AI Agent involves more than connecting an LLM to a prompt; runtime, memory, tools and security must also be considered.
- Context Window and Memory management affect both system quality and operating costs.
- Agents that can interact with real systems need clear permissions and safeguards to prevent unintended actions.
- Automated workflows should be designed to balance efficiency with reliability and human control.

#### Networking and Personal Development

- The meet up gave me an opportunity to learn from engineers and Tech Leads working on real-world Cloud and AI solutions.
- The technical discussions encouraged me to explore AI Agent architecture and production deployment in greater depth.
- The experience also reminded me to be more proactive in networking, asking questions and exchanging ideas with the technology community.

#### Lessons Learned

- **AI Agents need more than a model:** runtime, tools, memory, security and monitoring are all important parts of the system.
- **Low latency matters:** real-time applications must provide responses quickly enough to support natural user interactions.
- **Security should be integrated early:** automated checks and appropriate access controls help reduce risks before deployment.
- **Context and Memory require management:** retaining relevant information while controlling token usage is an important design consideration.
- **Automation requires guardrails:** AI Agents should operate within clearly defined permissions and boundaries.
- **Production readiness involves trade-offs:** reliability, security, cost and performance must be considered together.

### Some Event Photos

<!-- Add photos from the First Cloud AI Journey Meet Up here. -->

> Overall, the First Cloud AI Journey Meet Up helped me connect technical concepts with real-world applications in Cloud and AI. The sessions broadened my understanding of Voice AI, AWS security, Agent runtime architecture and AI-assisted software development. I also gained a stronger appreciation for context management, security guardrails and cost optimization when deploying AI Agents in production. Most importantly, the event motivated me to keep learning, connect with the community and apply these insights to future projects.
