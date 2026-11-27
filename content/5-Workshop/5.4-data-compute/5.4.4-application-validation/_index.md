---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.4-dns-simulation/"]
title: "Validate the application"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

## 1. Check the website and sign-in

If you used the [single-stack template](../../5.4-full-cloudformation/), get `WebsiteUrl` from Outputs to verify the landing page. The combined stack does not configure sign-in until you attach Google OAuth, so the post-sign-in checks on this page apply primarily to the multi-stack path (or after completing Command 5 of the single-stack path).

Retrieve the CloudFront URL created in your account:

```bash
stackout tina-ws-edge StageUrl
```

Open the URL in your browser. Verify that the TINA page loads, then sign in with the Google test user you registered. Capture a screenshot of the sign-in page from your own environment:

{{< workshop-screenshot file="16-app-login.png" description="TINA sign-in page on your CloudFront URL; redact email addresses and domains if sharing." >}}

If sign-in fails, verify that the Google OAuth client belongs to the right project, the callback URI matches `StageUrl` exactly, the user is listed under Test users, the secret JSON has the exact two keys, and Terminal is `Running`. Inspect the Terminal logs without exposing secret values.

## 2. Run a test meeting

Create a test meeting with the consent of all participants. In TINA, create a meeting through the UI, enter the test meeting URL, and start it. Watch the bot join, confirm the bot task appears in ECS, and verify the meeting status updates. The meeting provider, lobby admission, or participant permissions can affect whether the bot can enter the room; if it fails to join, record the error and check the bot logs, runtime logs, Fargate quotas, NAT gateway, and meeting room policy.

{{< workshop-screenshot file="17-test-meeting.png" description="Consented test meeting and bot status; use dummy data and redact participant details." >}}

If you enabled VieGem properly and audio streaming succeeds, speak a non-sensitive test phrase, wait for the transcript to appear, and verify its accuracy. If ASR is not enabled or no transcript appears, record **Not passed / Not tested**—do not fabricate screenshots.

{{< workshop-screenshot file="18-test-transcript.png" description="Transcript of a non-sensitive test phrase once ASR is working." >}}

End the meeting and confirm that the bot task stops. If recording is enabled, check the test meeting's object metadata in your own bucket; do not include private audio or transcripts in any report.

## 3. Record actual results

| Check | Expected result | Observation |
| --- | --- | --- |
| Web | CloudFront URL renders Terminal | Pass/Fail and timestamp |
| Sign-in | Google test user signs in to TINA | Pass/Fail, without recording secrets |
| ECS | Runtime, core, and Terminal are stable; target is healthy | desired/running counts, events |
| Meeting | Bot joins the test room and stops after the meeting | Actual result |
| Transcription | Transcript appears when ASR is configured | Pass/Fail or not configured |

A `CREATE_COMPLETE` stack only confirms that the infrastructure was provisioned—it does not replace this application validation. Compare your actual results against the reference screenshots above and record each check in the table before proceeding to cleanup.
