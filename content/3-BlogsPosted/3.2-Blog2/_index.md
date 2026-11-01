---
title: "Blog 2"
date: 2026-10-28
weight: 2
chapter: false
pre: " <b> 3.2. </b> "
---

# From Meeting Transcripts to Notion Tasks: When DynamoDB Streams, Lambda, and Bedrock Work Together

**Published: October 28, 2026**

Having a complete transcript after a meeting does not necessarily solve the follow-up problem. A transcript might contain thousands of words, while the most useful information is often much simpler: Who is responsible for which task? What is the deadline? Which action items still need attention?

Manually listening to recordings, reading through long transcripts, deciding what needs to be done, writing it down, and creating tasks in a project management tool is time-consuming and error-prone. Important items get forgotten, deadlines are missed, and context is lost between the meeting and the task tracker.

One practical approach is to combine **Amazon DynamoDB Streams, AWS Lambda, and Amazon Bedrock** to extract action items automatically and synchronize them with Notion. This post walks through the architecture, implementation considerations, a Python code example, idempotency strategies, human-in-the-loop confirmation, cost considerations, and how to extend the pattern to other tools.

![Architecture illustration: from transcripts to Notion tasks](/images/3-BlogsPosted/Blog2.jpg)

---

## 1. How Does the Architecture Work?

Imagine that someone says during a meeting:

> "Lan will finish the login API by October 30."

After the meeting ends, the system can follow this workflow:

### Amazon DynamoDB and DynamoDB Streams

The backend updates the meeting status to `COMPLETED` in DynamoDB. DynamoDB Streams captures the data change, and AWS Lambda can be configured to process the stream event.

The useful separation here is that the backend does not need to invoke the entire AI workflow directly. Post-meeting analysis can run independently, and the main application remains responsive.

### AWS Lambda

Lambda acts as the coordinator. It receives the stream event, retrieves the corresponding transcript from Amazon S3, and prepares the content for AI processing.

Instead of copying a long transcript into Notion, the Lambda function asks a model available through Amazon Bedrock to identify relevant action items.

### Amazon Bedrock

The language model turns conversational content into structured data. For example:

- **Task:** Complete the login API
- **Assignee:** Lan
- **Deadline:** October 30
- **Source:** The relevant transcript segment

After receiving the response, Lambda validates the data and calls the Notion API to create an item in a task database.

### Why This Design Works

- **Event-driven**: No polling. The pipeline starts automatically when meeting metadata changes in DynamoDB.
- **Serverless**: No EC2 instances to manage. You pay only for the compute and API calls you actually use.
- **Decoupled**: Transcript storage, AI extraction, and task creation are separate concerns. You can replace Bedrock with another model, or Notion with another task tool, without rewriting the whole pipeline.
- **Observable**: Each step emits logs and metrics to Amazon CloudWatch, making failures easy to debug.

---

## 2. How It Works Step by Step

### Step 1: Meeting Metadata Lands in DynamoDB

When a meeting finishes, an item is written (or updated) in a DynamoDB table called `Meetings`:

| meeting_id (PK) | status | transcript_s3_url | created_at |
|-----------------|--------|-------------------|------------|
| mtg-2026-10-28-001 | completed | s3://meeting-transcripts/mtg-001.txt | 2026-10-28T10:00:00Z |

The `status` field moves from `pending` to `completed`. DynamoDB Streams captures this change.

### Step 2: Lambda Extracts Action Items with Bedrock

A Lambda function (`process-meeting-transcript`) is triggered by the stream. It:

1. Reads the `meeting_id` and `transcript_s3_url` from the stream record.
2. Downloads the transcript from S3.
3. Calls Amazon Bedrock with a prompt such as:

> You are an assistant that extracts action items from meeting transcripts.
>
> Transcript:
> {{transcript}}
>
> Return a JSON array of action items. Each item must have: title, description, assignee, due_date, priority.
> Only include items that are clearly actionable. Ignore general discussion.

4. Parses the JSON response from Bedrock.

### Step 3: Human Confirmation

Before creating tasks in Notion, the extracted action items are paused for review. Options include:

- Storing proposed tasks in a `ProposedTasks` DynamoDB table with `status = pending_review`.
- Sending a notification (Slack, email, or internal dashboard) with the proposed tasks and Approve/Reject buttons.
- Only writing to Notion after an approver marks the item as `approved`.

### Step 4: Create Tasks in Notion

Once confirmed, a Lambda function calls the Notion API (`POST https://api.notion.com/v1/pages`) to create a page in the Notion database:

- **Title**: Action item title
- **Assignee**: Person responsible
- **Due date**: When it should be completed
- **Priority**: High / Medium / Low
- **Related meeting**: Link back to the original meeting record

### Step 5: Idempotency

To avoid creating duplicate tasks if the Lambda is retried or the stream event is delivered twice:

- Each proposed task set is stored with a unique `meeting_id` + `batch_id` key.
- Before writing to Notion, the function checks whether tasks for this `meeting_id` already exist in the `ProposedTasks` table.
- Notion page creation records the `notion_page_id` back to DynamoDB so the same meeting is not processed again.

---

## 3. Example: Lambda Handler (Python)

```python
import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime")
dynamodb = boto3.resource("dynamodb")

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
NOTION_API_KEY = os.environ["NOTION_API_KEY"]
PROPOSED_TABLE = os.environ["PROPOSED_TASKS_TABLE"]

def extract_action_items(transcript: str) -> list:
    prompt = f"""Extract action items from this meeting transcript.
Return ONLY a JSON array. Each item: {{"title": "...", "description": "...", "assignee": "...", "due_date": "...", "priority": "High|Medium|Low"}}
Transcript:
{transcript}"""

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    result = json.loads(response["body"].read())
    return json.loads(result["content"][0]["text"])

def save_proposed_tasks(meeting_id: str, items: list):
    table = dynamodb.Table(PROPOSED_TABLE)
    table.put_item(Item={
        "meeting_id": meeting_id,
        "status": "pending_review",
        "items": items,
        "created_at": json.dumps({"__type": "timestamp", "iso": str(__import__("datetime").datetime.utcnow())})
    })

def already_processed(meeting_id: str) -> bool:
    table = dynamodb.Table(PROPOSED_TABLE)
    resp = table.get_item(Key={"meeting_id": meeting_id})
    return "Item" in resp

def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"] not in ("INSERT", "MODIFY"):
            continue

        meeting_id = record["dynamodb"]["Keys"]["meeting_id"]["S"]
        status = record["dynamodb"]["NewImage"].get("status", {}).get("S")
        s3_url = record["dynamodb"]["NewImage"].get("transcript_s3_url", {}).get("S")

        if status != "completed" or not s3_url:
            continue

        # Idempotency check
        if already_processed(meeting_id):
            continue

        bucket, key = parse_s3_url(s3_url)
        transcript = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8")

        items = extract_action_items(transcript)

        # Pause for human confirmation before writing to Notion
        save_proposed_tasks(meeting_id, items)

        # After confirmation (separate step), call create_notion_tasks(items)

    return {"statusCode": 200}
```

---

## 4. Idempotency and Human Confirmation

| Concern | How it is handled |
|---------|-------------------|
| Duplicate processing | DynamoDB table stores `processed_meeting_ids`; Lambda checks before creating Notion tasks. |
| Stream redelivery | Same `meeting_id` produces the same proposed tasks; Notion creation is gated behind confirmation. |
| Wrong task created | Human review step lets an approver edit or reject items before they reach Notion. |
| Partial failure | Proposed tasks are stored in DynamoDB first; Notion creation is a separate, retryable step. |
| LLM hallucination | Fields not clearly supported by the transcript remain empty rather than being inferred. |

---

## 5. Cost Considerations

* **Amazon S3**: Pay per GB stored and per request. Transcripts are small text files, so cost is negligible.
* **DynamoDB**: Pay per read/write request and storage. Ideal for lightweight meeting metadata.
* **AWS Lambda**: Pay per invocation and duration. Short Python functions keep cost low.
* **Amazon Bedrock**: Pay per input/output token processed by the model. Long transcripts cost more; consider summarizing very long transcripts before sending to Bedrock.
* **Notion API**: Free tier is available for small teams; paid plans for higher limits.

---

## 6. Extending the Pattern

The same architecture can be extended to:

- **Jira, Asana, Trello, or ClickUp**: Replace the Notion API call with the respective task tool API.
- **Email transcripts**: Replace S3 + DynamoDB with an SES inbound email handler.
- **Call center transcripts**: Replace meeting audio with contact center recordings from Amazon Connect.
- **Scheduled reports**: Add a weekly Lambda that scans all `pending_review` items and sends a summary email.

---

## 7. Conclusion

This architecture turns meeting transcripts into structured, trackable work without manual copy-paste. By combining DynamoDB Streams, AWS Lambda, Amazon Bedrock, and the Notion API, you get a serverless pipeline that:

* Starts automatically when a meeting ends.
* Extracts action items using generative AI.
* Keeps humans in the loop before tasks are created.
* Avoids duplicates with idempotency checks.

The same pattern can be extended to other document sources (email, support tickets, call center transcripts) and other task destinations (Jira, Asana, Trello, or a custom database).

---

![Figure 2. DynamoDB stream shards and AWS Lambda event processing. Source: AWS Database Blog.]( /images/3-BlogsPosted/Blog2_2.jpg)

*Figure 2. DynamoDB stream shards and AWS Lambda event processing. Source: AWS Database Blog.*

## References

1. [AWS – DynamoDB Streams and Lambda Triggers](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html)
2. [Amazon Bedrock – Structured Outputs](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html)
3. [Notion – Create a Page API](https://developers.notion.com/reference/post-page)
4. [AWS Lambda – Documentation](https://docs.aws.amazon.com/lambda/)

---

**Bài viết đã đăng trên AWS Study Group:** [https://www.facebook.com/groups/awsstudygroupfcj/permalink/2318521822246110/?rdid=ZaQ8iG8gfsmGlEWb#](https://www.facebook.com/groups/awsstudygroupfcj/permalink/2318521822246110/?rdid=ZaQ8iG8gfsmGlEWb#)
