---
title: "From Meeting Transcripts to Notion Tasks with DynamoDB Streams, Lambda and Bedrock"
date: 2026-10-28
weight: 1
chapter: false
pre: " <b> 3.2. </b> "
---

# From Meeting Transcripts to Notion Tasks with DynamoDB Streams, Lambda and Bedrock

Meetings generate a lot of spoken content, but turning that speech into structured, actionable work items is still a manual and error-prone process. Someone has to listen to the recording, read the transcript, decide what needs to be done, write it down, and create a task in a project management tool.

This post describes an event-driven architecture that reacts automatically when a meeting ends: it extracts action items from the meeting transcript using Amazon Bedrock, and creates structured tasks in Notion. The design also covers idempotency (so the same meeting is not processed twice) and human confirmation (so important tasks are reviewed before they are created).

---

## Architecture Overview

The workflow is fully serverless and event-driven:

1. **Meeting transcript stored in Amazon S3** – When a meeting recording is processed, the transcript (plain text or JSON) is uploaded to an S3 bucket.
2. **DynamoDB Streams** – A DynamoDB table tracks meeting metadata (meeting ID, status, transcript location). A new item or status change triggers a DynamoDB Stream event.
3. **AWS Lambda** – A Lambda function consumes the stream event, reads the transcript from S3, and invokes Amazon Bedrock to extract action items.
4. **Amazon Bedrock** – A large language model (for example, a Claude model via Bedrock) analyzes the transcript and returns a list of action items with assignee, due date, and priority.
5. **Notion API** – A second Lambda function (or the same function) calls the Notion API to create structured tasks in a Notion database.
6. **Human confirmation** – Before tasks are written to Notion, the extracted action items are sent back for review (for example, via an approval step or a review queue). Tasks are only created after confirmation.

### Why this design

* **Event-driven**: No polling. The pipeline starts automatically when meeting metadata changes in DynamoDB.
* **Serverless**: No EC2 instances to manage. You pay only for the compute and API calls you actually use.
* **Decoupled**: Transcript storage, AI extraction, and task creation are separate concerns. You can replace Bedrock with another model, or Notion with another task tool, without rewriting the whole pipeline.

---

## How It Works Step by Step

### Step 1: Meeting metadata lands in DynamoDB

When a meeting finishes, an item is written (or updated) in a DynamoDB table called `Meetings`:

| meeting_id (PK) | status | transcript_s3_url | created_at |
|-----------------|--------|-------------------|------------|
| mtg-2026-10-28-001 | completed | s3://meeting-transcripts/mtg-001.txt | 2026-10-28T10:00:00Z |

The `status` field moves from `pending` to `completed`. DynamoDB Streams captures this change.

### Step 2: Lambda extracts action items with Bedrock

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

### Step 3: Human confirmation

Before creating tasks in Notion, the extracted action items are paused for review. Options include:

* Storing proposed tasks in a `ProposedTasks` DynamoDB table with `status = pending_review`.
* Sending a notification (Slack, email, or internal dashboard) with the proposed tasks and Approve/Reject buttons.
* Only writing to Notion after an approver marks the item as `approved`.

### Step 4: Create tasks in Notion

Once confirmed, a Lambda function calls the Notion API (`POST https://api.notion.com/v1/pages`) to create a page in the Notion database:

* **Title**: Action item title
* **Assignee**: Person responsible
* **Due date**: When it should be completed
* **Priority**: High / Medium / Low
* **Related meeting**: Link back to the original meeting record

### Step 5: Idempotency

To avoid creating duplicate tasks if the Lambda is retried or the stream event is delivered twice:

* Each proposed task set is stored with a unique `meeting_id` + `batch_id` key.
* Before writing to Notion, the function checks whether tasks for this `meeting_id` already exist in the `ProposedTasks` table.
* Notion page creation records the `notion_page_id` back to DynamoDB so the same meeting is not processed again.

---

## Example: Lambda Handler (Python)

```python
import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime")
notion = boto3.client("lambda")  # or use requests to Notion API directly

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
NOTION_API_KEY = os.environ["NOTION_API_KEY"]

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

def create_notion_tasks(items: list):
    for item in items:
        notion.invoke_function(
            FunctionName="create-notion-task",
            Payload=json.dumps(item)
        )

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

## Idempotency and Human Confirmation

| Concern | How it is handled |
|---------|-------------------|
| Duplicate processing | DynamoDB table stores `processed_meeting_ids`; Lambda checks before creating Notion tasks. |
| Stream redelivery | Same `meeting_id` produces the same proposed tasks; Notion creation is gated behind confirmation. |
| Wrong task created | Human review step lets an approver edit or reject items before they reach Notion. |
| Partial failure | Proposed tasks are stored in DynamoDB first; Notion creation is a separate, retryable step. |

---

## Cost Considerations

* **Amazon S3**: Pay per GB stored and per request. Transcripts are small text files, so cost is negligible.
* **DynamoDB**: Pay per read/write request and storage. Ideal for lightweight meeting metadata.
* **AWS Lambda**: Pay per invocation and duration. Short Python functions keep cost low.
* **Amazon Bedrock**: Pay per input/output token processed by the model. Long transcripts cost more; consider summarizing very long transcripts before sending to Bedrock.
* **Notion API**: Free tier is available for small teams; paid plans for higher limits.

---

## Conclusion

This architecture turns meeting transcripts into structured, trackable work without manual copy-paste. By combining DynamoDB Streams, AWS Lambda, Amazon Bedrock, and the Notion API, you get a serverless pipeline that:

* Starts automatically when a meeting ends.
* Extracts action items using generative AI.
* Keeps humans in the loop before tasks are created.
* Avoids duplicates with idempotency checks.

The same pattern can be extended to other document sources (email, support tickets, call center transcripts) and other task destinations (Jira, Asana, Trello, or a custom database).

---

## References

1. [Amazon DynamoDB Streams – Documentation](https://docs.aws.amazon.com/dynamodb/latest/developerguide/Streams.html)
2. [AWS Lambda – Documentation](https://docs.aws.amazon.com/lambda/)
3. [Amazon Bedrock – Documentation](https://docs.aws.amazon.com/bedrock/)
4. [Notion API – Documentation](https://developers.notion.com/)
5. [AWS Step Functions – Optional orchestration alternative](https://docs.aws.amazon.com/step-functions/)
