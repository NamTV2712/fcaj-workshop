---
aliases: ["/5-workshop/5.6-cleanup/"]
title: "Cleanup and Evidence Set"
date: 2026-11-25
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

## Before deleting

Only clean up **lab resources you created yourself**, after confirming the account, Region, names, tags, ownership and that the data can be deleted. Never delete stacks, buckets, databases, images or VPCs named `tina-staging-*`, `tina-prod-*` or belonging to anyone else. Deleting buckets/objects, images and databases loses data unless a copy exists; check retention/snapshot requirements first.

## Console cleanup order for the lab

1. **ECS → Clusters**: delete **lab** services/tasks after confirming the correct cluster and that no users remain; wait for related resources to detach from target groups. Delete the lab cluster if empty and no longer needed.
2. **EC2 → Load Balancers/Target Groups** and **CloudFront**: if you created lab resources, delete them in dependency order; CloudFront may need to be disabled and fully deployed before deletion.
3. **RDS → Databases** and **ElastiCache**: decide on snapshots/data retention per the lab owner, then delete only the lab resources. Wait for deletion to finish; check remaining snapshots and storage because they can still incur charges.
4. **S3 → Buckets**: confirm only lab test files remain. Delete objects/versions or the bucket only when the data owner allows data loss; versioned buckets need version/delete-marker handling.
5. **ECR → Repositories**: delete lab repositories and images only after confirming no service needs them.
6. **VPC → Endpoints**: delete lab endpoints; **NAT gateways**: delete the lab NAT and wait; **Elastic IPs**: release only the lab's Elastic IP. Do not release an address attached to another system.
7. Remove lab subnet associations/routes if needed, delete lab subnets, route tables and security groups; detach and delete the lab Internet Gateway, then the lab VPC. If AWS reports a dependency, identify it exactly before continuing.
8. Review **VPC**, **ECS**, **RDS**, **ElastiCache**, **S3**, **ECR**, **CloudFront** and Billing/Cost Explorer to ensure no lab component is still charging unexpectedly. Cost Explorer is not real-time.

{{< workshop-screenshot file="22-cleanup-lab.png" description="Evidence that lab resources were cleaned within the practice scope." >}}

If you created a CloudFormation stack in the lab, open **CloudFormation → Stacks → lab stack → Delete** and watch **Events**. A stack may retain resources due to deletion policy, snapshots or a non-empty bucket; check and handle them with the right permissions after deletion. Do not use bulk delete commands on similarly named resources.

## Evidence set for the reviewer

- Source/release link and a commit or digest the reviewer is allowed to access.
- Component table with state, timestamps, Expected/Actual/Verdict; state clearly what ran and what remains Blocked.
- Real screenshots using the suggested names on each page, with secrets and private information masked.
- Test report with fake data, known limitations, cost estimate and proof that lab resources were cleaned.
- If a clean rerun was not possible, state which artifact/configuration is missing; do not mark the whole deployment complete.

## Capture and save screenshots on Windows

1. Open the exact AWS Console page named in the step. Check that service name, Region, state and time are readable; collapse areas containing unnecessary information.
2. Press `Windows + Shift + S`, select the screen region; open the Snipping Tool notification to view the image. You can also open Snipping Tool first and choose **New**.
3. Before sharing, crop or mask with a solid colour the account ID, email, internal hostname, token, secret, personal information and meeting content. Recheck the image after masking.
4. Choose **Save as** and save a PNG in `D:/Project/fcj-workshop-template/static/images/5-Workshop/tina/`. Create the `tina` folder if missing; use the name suggested on each page, for example `03-vpc-subnets.png`.
5. Reopen the saved image to verify. Image slots are already marked in each page: save with the correct name and rebuild the site; you do not need to edit Markdown. If `hugo server` does not show a new image, restart it. Do not use screenshots from another environment to represent this lab's results.
