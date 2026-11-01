---
title: "Từ Bản transcript Cuộc họp sang Nhiệm vụ Notion với DynamoDB Streams, Lambda và Bedrock"
date: 2026-10-28
weight: 1
chapter: false
pre: " <b> 3.2. </b> "
---

# Từ Bản transcript Cuộc họp sang Nhiệm vụ Notion với DynamoDB Streams, Lambda và Bedrock

Cuộc họp sinh ra rất nhiều nội dung spoken, nhưng chuyển nội dung đó thành các mục làm việc có cấu trúc và có thể thực hành vẫn là một quá trình thủ công và dễ bị lỗi. Mọi người phải nghe bản ghi âm, đọc bản transcript, quyết định việc cần làm, ghi lại và tạo nhiệm vụ trong công cụ quản lý dự án.

Bài viết này mô tả một kiến trúc hướng sự kiện tự động phản ứng khi cuộc họp kết thúc: nó trích xuất các mục hành động từ bản transcript bằng Amazon Bedrock, và tạo các nhiệm vụ có cấu trúc trong Notion. Thiết kế cũng bao gồm tính idempotency (để cùng một cuộc họp không được xử lý hai lần) và xác nhận của con người (để các nhiệm vụ quan trọng được xem xét trước khi tạo).

---

## Tổng quan Kiến trúc

Quy trình làm việc hoàn toàn không máy chủ và hướng sự kiện:

1. **Bản transcript cuộc họp lưu trong Amazon S3** – Khi bản ghi âm cuộc họp được xử lý, bản transcript (văn bản thuần hoặc JSON) được tải lên một thùng S3.
2. **DynamoDB Streams** – Một bảng DynamoDB theo dõi siêu dữ liệu cuộc họp (meeting_id, trạng thái, vị trí transcript). Một mục mới hoặc thay đổi trạng thái kích hoạt sự kiện DynamoDB Stream.
3. **AWS Lambda** – Một hàm Lambda tiêu thụ sự kiện stream, đọc transcript từ S3 và gọi Amazon Bedrock để trích xuất các mục hành động.
4. **Amazon Bedrock** – Một mô hình ngôn ngữ lớn (ví dụ, một mô hình Claude qua Bedrock) phân tích transcript và trả về danh sách các mục hành động với người phụ trách, hạn mức và mức độ ưu tiên.
5. **Notion API** – Một hàm Lambda thứ hai (hoặc cùng một hàm) gọi Notion API để tạo các nhiệm vụ có cấu trúc trong cơ sở dữ liệu Notion.
6. **Xác nhận của con người** – Trước khi các nhiệm vụ được ghi vào Notion, các mục hành động đã trích xuất được gửi lại để xem xét (ví dụ, qua bước phê duyệt hoặc hàng đợi xem xét). Các nhiệm vụ chỉ được ghi vào Notion sau khi được xác nhận.

### Tại sao thiết kế này

* **Hướng sự kiện**: Không cần polling. Đường ống bắt đầu tự động khi siêu dữ liệu cuộc họp thay đổi trong DynamoDB.
* **Không máy chủ**: Không cần quản lý EC2 instances. Bạn chỉ trả tiền cho thời gian compute và gọi API bạn thực sự sử dụng.
* **Tách rời**: Lưu trữ transcript, trích xuất AI và tạo nhiệm vụ là các vấn đề riêng biệt. Bạn có thể thay thế Bedrock bằng một mô hình khác, hoặc Notion bằng một công cụ quản lý nhiệm vụ khác,Without viết lại toàn bộ đường ống.

---

## Cách Hoạt Dụng Bước Bước

### Bước 1: Siêu dữ liệu cuộc họp đến DynamoDB

Khi một cuộc họp kết thúc, một mục được ghi (hoặc cập nhật) trong một bảng DynamoDB gọi là `Meetings`:

| meeting_id (PK) | status | transcript_s3_url | created_at |
|-----------------|--------|-------------------|------------|
| mtg-2026-10-28-001 | completed | s3://meeting-transcripts/mtg-001.txt | 2026-10-28T10:00:00Z |

Trường `status` chuyển từ `pending` sang `completed`. DynamoDB Streams bắt nắm sự thay đổi này.

### Bước 2: Lambda trích xuất các mục hành động với Bedrock

Một hàm Lambda (`process-meeting-transcript`) được kích hoạt bởi stream. Nó:

1. Đọc `meeting_id` và `transcript_s3_url` từ bản ghi stream.
2. Tải xuống transcript từ S3.
3. Gọi Amazon Bedrock với một prompt như:

> Bạn là một trợ trích xuất các mục hành động từ bản transcript cuộc họp.
> 
> Bản transcript:
> {{transcript}}
>
> Trả về một mảng JSON của các mục hành động. Mỗi mục phải có: title, description, assignee, due_date, priority.
> Chỉ bao gồm các mục rõ ràng là có thể thực hành. Bỏ qua cuộc thảo luận chung.

4. Phân tích phản hồi JSON từ Bedrock.

### Bước 3: Xác nhận của con người

Trước khi ghi các nhiệm vụ vào Notion, các mục hành động đã trích xuất được tạm dừng để xem xét. Các tùy chọn bao gồm:

* Lưu các nhiệm vụ được đề xuất vào một bảng DynamoDB gọi là `ProposedTasks` với `status = pending_review`.
* Gửi một thông báo (Slack, email, hoặc bảng thông báo nội bộ) với các nhiệm vụ được đề xuất và các nút Approve/Reject.
* Chỉ ghi vào Notion sau khi một người phê duyệt đánh dấu mục là `approved`.

### Bước 4: Tạo nhiệm vụ trong Notion

Sau khi được xác nhận, một hàm Lambda gọi Notion API (`POST https://api.notion.com/v1/pages`) để tạo một trang trong cơ sở dữ liệu Notion:

* **Tiêu đề**: Tiêu đề mục hành động
* **Người phụ trách**: Người phụ trách nhiệm vụ
* **Hạn mức**: Khi nào nên hoàn thành
* **Mức độ ưu tiên**: Cao / Trung bình / Thấp
* **Cuộc họp liên quan**: Đường link ngược lại bản ghi cuộc họp gốc

### Bước 5: Tính idempotency

Để tránh tạo các nhiệm vụ trùng lặp nếu Lambda bị thử lại hoặc sự kiện stream được gửi hai lần:

* Mỗi bộ nhiệm vụ được đề xuất được lưu với một khóa duy nhất `meeting_id` + `batch_id`.
* Trước khi ghi vào Notion, hàm kiểm tra xem các nhiệm vụ cho `meeting_id` này đã tồn tại trong bảng `ProposedTasks` hay chưa.
* Notion page ghi lại `notion_page_id` vào DynamoDB để cuộc họp không được xử lý lại.

---

## Ví dụ: Xử lý Lambda (Python)

```python
import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime")
notion = boto3.client("lambda")  # hoặc dùng requests để gọi Notion API trực tiếp

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
NOTION_API_KEY = os.environ["NOTION_API_KEY"]

def extract_action_items(transcript: str) -> list:
    prompt = f"""Trích xuất các mục hành động từ bản transcript cuộc họp này. 
Trả về CHỈ một mảng JSON. Mỗi mục: {{"title": "...", "description": "...", "assignee": "...", "due_date": "...", "priority": "Cao|Trung bình|Thấp"}}
Bản transcript:
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
        
        # Kiểm tra tính idempotency
        if already_processed(meeting_id):
            continue
        
        bucket, key = parse_s3_url(s3_url)
        transcript = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8")
        
        items = extract_action_items(transcript)
        
        # Tạm dừng để xác nhận của con người trước khi ghi vào Notion
        save_proposed_tasks(meeting_id, items)
        
        # Sau khi xác nhận (bước riêng biệt), gọi create_notion_tasks(items)
    
    return {"statusCode": 200}
```

---

## Tính Idempotency và Xác nhận của Con người

| Lo | Cách xử lý |
|-----|-------------|
| Xử lý trùng lặp | Bảng DynamoDB lưu `processed_meeting_ids`; Lambda kiểm tra trước khi tạo Notion tasks. |
| Stream gửi lại | Cùng `meeting_id` tạo ra cùng các nhiệm vụ được đề xuất; Ghi Notion bị khóa bước trước khi xác nhận. |
| Tạo nhầm nhiệm vụ | Bước xem xét của con người cho phép người phê duyệt chỉnh sửa hoặc từ chối các mục trước khi chúng đến Notion. |
| Thất bại một phần | Các nhiệm vụ được đề xuất được lưu trong DynamoDB trước; Ghi Notion là một bước riêng biệt, có thể thử lại. |

---

## Cân nhắc về Chi phí

* **Amazon S3**: Trả tiền theo GB lưu trữ và mỗi yêu cầu. Các bản transcript là các tệp văn bản nhỏ, do đó chi phí gần như không đáng kể.
* **DynamoDB**: Trả tiền mỗi yêu cầu đọc/ghi và lưu trữ. Lý tưởng cho siêu dữ liệu cuộc họp nhẹ.
* **AWS Lambda**: Trả tiền mỗi lần gọi và thời gian. Các hàm Python ngắn gọn giữ chi phí thấp.
* **Amazon Bedrock**: Trả tiền mỗi token đầu vào/đầu ra được mô hình xử lý. Transcript rất dài tốn kém hơn; hãy cân nhắc tóm tắt các transcript rất dài trước khi gửi đến Bedrock.
* **Notion API**: Gói miễn phí có sẵn cho các nhóm nhỏ; gói trả phí cho giới hạn cao hơn.

---

## Kết luận

Kiến trúc này chuyển đổi bản transcript cuộc họp thành các công việc có cấu trúc và có thể theo dõi mà không cần sao chép thủ công. Bằng cách kết hợp DynamoDB Streams, AWS Lambda, Amazon Bedrock và Notion API, bạn có một đường ống không máy chủ mà:

* Bắt đầu tự động khi một cuộc họp kết thúc.
* Trích xuất các mục hành động bằng AI sinh tạo.
* Giữ con người trong vòng lặp trước khi các nhiệm vụ được tạo.
* Tránh các bản sao chép bằng cách kiểm tra tính idempotency.

Mô hình tương tự có thể được mở rộng cho các nguồn tài liệu khác (email,票 các vé hỗ trợ, bản ghi cuộc gọi trung tâm chăm sóc khách hàng) và các điểm đến nhiệm vụ khác (Jira, Asana, Trello, hoặc cơ sở dữ liệu tùy chỉnh).

---

## Tài liệu tham khảo

1. [Amazon DynamoDB Streams – Tài liệu](https://docs.aws.amazon.com/dynamodb/latest/developerguide/Streams.html)
2. [AWS Lambda – Tài liệu](https://docs.aws.amazon.com/lambda/)
3. [Amazon Bedrock – Tài liệu](https://docs.aws.amazon.com/bedrock/)
4. [Notion API – Tài liệu](https://developers.notion.com/)
5. [AWS Step Functions – Giải pháp điều phối thay thế](https://docs.aws.amazon.com/step-functions/)
