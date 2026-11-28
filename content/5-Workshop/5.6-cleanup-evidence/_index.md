---
aliases: ["/5-workshop/5.6-cleanup/"]
title: "Cleanup and evidence"
date: 2026-11-25
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

## 1. Confirm resources belong to the workshop

The deletion commands below remove your lab environment and test data. Proceed only after saving anything you need to keep and verifying the account, Region, and stack names. Do not delete resources belonging to other environments. Before deleting stacks, end any active meetings, wait for bot tasks to stop, and terminate the EC2 builder created during the lab.

## 2. Delete stacks in reverse dependency order

In CloudShell, delete each stack and wait for it to finish before deleting the next. Omit `tina-ws-viegem` if you did not deploy it:

```bash
for s in tina-ws-terminal tina-ws-core tina-ws-viegem tina-ws-runtime tina-ws-bot tina-ws-edge tina-ws-data tina-ws-egress; do
  aws cloudformation delete-stack --region "$AWS_REGION" --stack-name "$s"
  aws cloudformation wait stack-delete-complete --region "$AWS_REGION" --stack-name "$s"
done
```

If an error occurs, stop and read **CloudFormation → Events** to resolve the dependency instead of continuing blindly. CloudFront distributions can take time to delete. Do not delete the foundation stack yet if repositories managed by it still contain images: ECR can reject deleting non-empty repositories.

## 3. Review ECR, buckets, snapshots, and roles

1. **ECR:** For the three repositories `tina-staging/bot`, `tina-staging/runtime`, and `tina-staging/meeting-api`, select all lab images and click **Delete**. Then delete the foundation stack:

   ```bash
   aws cloudformation delete-stack --region "$AWS_REGION" --stack-name tina-staging
   aws cloudformation wait stack-delete-complete --region "$AWS_REGION" --stack-name tina-staging
   ```

2. The remaining four ECR repositories were created manually via CLI, so they are not deleted automatically; in the Console, select `tina-staging/terminal`, `gateway`, `admin-api`, and `viegem` and delete them once you are sure you no longer need the images.
3. **S3:** The foundation stack uses `DeletionPolicy: Retain`, so the recordings bucket and its objects remain. In S3, identify the exact bucket from your saved outputs, download anything you want to keep, and then choose **Empty → Delete** if you want to remove all test data. Never delete a bucket solely because its name looks similar.
4. **RDS → Snapshots:** The data stack retains a final snapshot when deleting the database. Keep it if you need to restore later, or delete the test snapshot after reviewing it. Retained snapshots and buckets can continue to incur charges.
5. **WAF:** Delete the `tina-workshop-acl` Web ACL after the edge stack is removed. **Secrets Manager:** The manually created Google secret remains; delete it according to your policy if no longer needed. Optionally delete remaining log groups once you no longer need evidence.
6. After the builder instance is terminated, remove the role from its instance profile and delete the exact IAM resources created for the lab. For example:

   ```bash
   aws iam remove-role-from-instance-profile --instance-profile-name tina-workshop-builder-profile --role-name tina-workshop-builder-role
   aws iam delete-instance-profile --instance-profile-name tina-workshop-builder-profile
   aws iam delete-role-policy --role-name tina-workshop-builder-role --policy-name TinaEcrPush
   aws iam detach-role-policy --role-name tina-workshop-builder-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
   aws iam delete-role --role-name tina-workshop-builder-role
   ```

7. Re-check **EC2/EBS, NAT/EIP, ECS, RDS, ElastiCache, CloudFront, WAF, S3, ECR, and Billing** to confirm no unintended test resources remain.

{{< workshop-screenshot file="22-cleanup-lab.png" description="Resource cleanup status of the lab environment after verification; redact the account ID." >}}

## 4. Evidence for evaluation

Record the date, commit `8a2b79e884bc0833f9075d4e795b20d347cef9c2`, the status of each step, any errors encountered, and how they were resolved. Screenshots must be genuine captures placed at their corresponding steps; do not include secrets, real transcripts, or personal information in public documentation.
