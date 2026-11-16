---
title: "Week 9 Worklog"
date: 2026-11-14
weight: 9
chapter: false
pre: " <b> 1.9. </b> "
---
### Week 9 Objectives:

* Get familiar with and contribute to TINA — a self-hosted, real-time meeting bot and transcription system.
* Implement and improve the meeting voice assistant, Knowledge graph, and CI/test infrastructure.
* Work with branches/PRs following the project's review process and CI standards.

### Tasks to be carried out this week:

| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Get familiar with the TINA repository: read README, AGENTS.md, CONTRIBUTING.md and learn the architecture (meeting bot, ASR, translation, Knowledge graph, voice assistant). <br> - Prepare the development environment: install Dotenvx, configure the private key, run `make plan` / `make all`. <br> - Study the retrieval & playback flow of the meeting voice assistant and start improving accuracy and playback experience. | 09/11/2026 | 09/11/2026 |  |
| 3 | - Harden the self-hosted voice assistant runtime; improve grounded answers and stage diagnostics. <br> - Show LiveKit voice defaults without selecting a meeting. <br> - Fix preserving ASR audio across the 30-second window. <br> - Add a dedicated Knowledge sidebar & graph; share the root Dotenvx key with TTS. | 10/11/2026 | 10/11/2026 |  |
| 4 | - Restore PR #9 CI gates, stabilize the local voice preview fixture, clear Python CI failures and install TTS test dependencies. <br> - Merge PR #9: add the self-hosted meeting voice assistant and Knowledge graph. <br> - Stabilize tests: renamed speaker transcript event, subscribe acknowledgement, meeting knowledge proposal edit. <br> - Merge PR #10: fix speaker mapping in CI. | 11/11/2026 | 11/11/2026 |  |
| 5 | - Expand the governed meeting voice assistant: clarification/progress handling, owner-reviewed task and decision drafts, scoped approved actions, multi-meeting retrieval, deterministic calculations, and spoken source navigation — keeping meeting-source checks and playback receipts authoritative. <br> - Update gateway voice navigation route test coverage. <br> - Mark voice session identifiers as strings. <br> - Include trained TINA wakeword models in the repository. | 12/11/2026 | 13/11/2026 |  |
| 6 | - Compact Knowledge YAML metadata in the UI. <br> - Review all changes and update project documentation (README, extension guide, contract docs). <br> - Wrap up the week and update the worklog. | 13/11/2026 | 13/11/2026 |  |

### Week 9 Achievements:

* Understood TINA's architecture and development workflow; set up the self-hosted environment (Docker/WSL2, Dotenvx, Terminal on port 23000 and API gateway on port 28056).
* Built and merged the self-hosted meeting voice assistant together with the Knowledge graph (PR #9), including a dedicated Knowledge sidebar/graph.
* Improved grounded voice answers, stage diagnostics, LiveKit defaults, and retrieval/playback of the voice assistant.
* Included trained TINA wakeword models; fixed ASR audio being lost across the 30-second window and marked voice session identifiers as strings.
* Restored and stabilized CI: PR #9/#10, Python/TTS test dependencies, speaker mapping, and subscribe/speaker/transcript event tests.
* Expanded the governed voice assistant with clarification handling, owner-reviewed drafts, scoped actions, deterministic calculations, and spoken source navigation.
* Learned the project's PR/review workflow and how to protect secrets (Dotenvx, never commit the private key).
