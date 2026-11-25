---
aliases: ["/5-workshop/5.4-s3-onprem/5.4.1-prepare/"]
title: "S3, ECR and Images"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

## A. Observe staging buckets and images

1. Go to **CloudFormation → Stacks → tina-foundation → Resources**. Find the S3 recording resource and select its physical ID to open S3. Only view configuration; do not open, download or delete real recordings unless necessary.
2. In **S3 → Buckets**, open a bucket you are allowed to view → **Properties** and **Permissions**: note encryption, Block Public Access and the real lifecycle rules.
3. Go to **Amazon ECR → Private registry → Repositories**. Filter `tina-staging/`, open each service repository → **Images** and view image tags, digests and push times.
4. Go to **ECS → Clusters → tina-foundation-ecs → Services → the service → Tasks → the running task**. Open the task definition in use and compare the image/digest if the Console provides it. Do not capture environment values or secrets.

**Pass condition:** you know which image the application uses and which bucket is the recording component. Having a bucket or an image does not prove a recording upload succeeded.

## B. Create a lab bucket in the Console

1. Go to **S3 → Buckets → Create bucket**. Choose **General purpose**, Region `us-east-1` and a globally unique name such as `tina-ws-<random-string>-recordings` (replace the brackets).
2. Keep **Block all public access**; choose default encryption appropriate for the lab policy. Enable versioning only if you understand how to clean object versions.
3. Review the choices and choose **Create bucket**. Open it → **Properties/Permissions** to confirm.
4. Use a non-sensitive test file: **Objects → Upload → Add files → Upload**. Confirm the object appears and note its size and time. Only put sample files in the lab bucket; never upload personal recordings for the exercise.

{{< workshop-screenshot file="07-s3-lab.png" description="Lab bucket and a test object containing no sensitive data." >}}

## C. Create an ECR repository and push a lab image

1. Go to **ECR → Private registry → Repositories → Create repository**.
2. Choose private, a name such as `tina-ws/terminal`, and tag immutability/scanning per your organisation's policy; create it.
3. Open the repository → **View push commands**. AWS shows the exact Docker login, tag and push commands for that account/Region. Run them on a machine with Docker/AWS CLI; do not put the token in documents.
4. If the correct TINA source version is provided, run `make build` in the source directory; it builds the required images and may take time. Verify the actual image with `docker image ls`; with the current Compose setup the Terminal image is usually `tina/v012-terminal:dev`, but confirm against your source version.
5. Use the verified image name as the `docker tag` source, then push per **View push commands**. Return to ECR, refresh and check the tag/digest. Ensure the image architecture matches the runtime.

{{< workshop-screenshot file="08-ecr-image.png" description="Lab ECR repository showing the image tag and digest." >}}

**Pass condition:** the lab bucket contains the test file and ECR has a real image/digest. Without this, the image cannot be declared to ECS. Lab resources must not duplicate or overwrite staging names.
