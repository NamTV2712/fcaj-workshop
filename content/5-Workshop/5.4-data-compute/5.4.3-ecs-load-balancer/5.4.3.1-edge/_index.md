---
title: "WAF, CloudFront and ALB"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.4.3.1 </b> "
---

## 1. Create a Web ACL in the AWS Console

1. Go to **AWS WAF & Shield → Web ACLs → Create web ACL**.
2. Name it `tina-workshop-acl`. For **Resource type**, select **CloudFront distributions**; Web ACLs of this type are managed in `us-east-1`. Leave the associated resources list empty because CloudFormation will attach the distribution later.
3. Under rules, you can add the AWS Managed Rules **Core rule set** for practice and keep the default action set to **Allow**. WAF rules and requests may incur charges; tune and test rules before production use. Keep the default metrics settings and click **Create web ACL**.
4. Open the newly created Web ACL and copy its **ARN**. Do not use the ARN of a Regional Web ACL.

{{< workshop-screenshot file="23-waf-acl.png" description="CloudFront-scope Web ACL created, with the account ID redacted in the ARN." >}}

{{< workshop-screenshot file="23-waf-acl(2).png" description="CloudFront-scope Web ACL details, with the account ID redacted in the ARN." >}}

## 2. Deploy CloudFront and the internal ALB

In CloudShell, replace the placeholder value with **your** Web ACL ARN:

```bash
WAF_ARN='PASTE_YOUR_CLOUDFRONT_WEB_ACL_ARN'
VPC_ID="$(stackout tina-staging VpcId)"
APP_SUBNETS="$(stackout tina-staging AppSubnetIds)"
PREFIX_ID="$(aws ec2 describe-managed-prefix-lists --region "$AWS_REGION" \
  --filters Name=prefix-list-name,Values=com.amazonaws.global.cloudfront.origin-facing \
  --query 'PrefixLists[0].PrefixListId' --output text)"
printf 'Prefix list: %s\n' "$PREFIX_ID"
```

If the prefix list prints `None` or is empty, check your Region before proceeding. Deploy the stack:

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-edge --template-file "$TINA_SRC/deploy/aws/staging-edge.yml" \
  --parameter-overrides "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "CloudFrontOriginPrefixListId=$PREFIX_ID" "WebAclArn=$WAF_ARN"
```

Wait for `CREATE_COMPLETE`, which can take a few minutes because of the CloudFront VPC origin. Open the `StageUrl` from the stack outputs with `/edge-health` appended: you should see `TINA_EDGE_READY`. Visiting the root path at this point may return `503` because Terminal has not been deployed yet.

```bash
stackout tina-ws-edge StageUrl
```

In **CloudFront → Distributions**, open the distribution from the `DistributionId` output and verify the VPC origin and deployment status:

{{< workshop-screenshot file="15-cloudfront-origin.png" description="Your CloudFront distribution and VPC origin; redact the domain and account ID if sharing." >}}

The ALB uses the **internal** scheme and has no public IP. HTTPS terminates at CloudFront, and the template forwards HTTP from CloudFront to the internal ALB; this setup is intended for the lab environment. See the [CloudFront VPC origins requirements](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html).
