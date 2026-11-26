---
aliases: ["/5-workshop/5.3-s3-vpc/5.3.1-create-gwe/"]
title: "Create foundation"
date: 2026-11-25
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

## 1. Create the Foundation Stack in the AWS Console

If this is the first time ECS is used in your lab account, open AWS CloudShell and check whether the ECS service-linked role exists:

```bash
aws iam get-role --role-name AWSServiceRoleForECS --query 'Role.Arn' --output text
```

If the command returns `NoSuchEntity`, run the command below to create the role. If it returns `AccessDenied`, ask your AWS administrator to check and create the role using an identity with `iam:CreateServiceLinkedRole` permission for `ecs.amazonaws.com`.

```bash
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
```

After creating it, wait for IAM to propagate before continuing. If you already encountered `Unable to assume the service linked role` and the `tina-staging` stack is in `ROLLBACK_COMPLETE`, confirm it is the lab stack you just created, delete the failed stack, wait for `DELETE_COMPLETE`, and then recreate it. Stacks in `CREATE_FAILED` may offer a **Retry** button in the Console. See [Service-linked roles for Amazon ECS in the AWS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles-for-clusters.html).

If you want CloudFormation to create the role in an account that **does not yet have** `AWSServiceRoleForECS`, add the snippet below to the existing `Resources:` section of `foundation.yml`. Place `ECSServiceLinkedRole` at the same level as `Cluster`, then add `DependsOn` to the `Cluster` resource. Keep all existing `Properties` of `Cluster` unchanged. When creating the stack, acknowledge IAM resource creation if the Console prompts you.

```yaml
  ECSServiceLinkedRole:
    Type: AWS::IAM::ServiceLinkedRole
    DeletionPolicy: Retain
    Properties:
      AWSServiceName: ecs.amazonaws.com

  Cluster:
    Type: AWS::ECS::Cluster
    DependsOn: ECSServiceLinkedRole
    # Keep the existing Cluster Properties right below.
```

This role is shared across the account. If the role already exists or you recreate the stack after deleting it, use the original template together with the CloudShell check above. `Retain` keeps the role when the stack is deleted, so declaring it again may fail with a duplicate-name error. See the [CloudFormation ServiceLinkedRole documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-iam-servicelinkedrole.html).

1. Go to **CloudFormation → Stacks → Create stack**.
2. Open [foundation.yml on GitHub](https://github.com/poor-frog/TINA/blob/7d6bba8109f6eac51c0d8241a7083e3e364cf59d/deploy/aws/foundation.yml), choose **Download raw file**, and save it as `foundation.yml`. In CloudFormation, select **Upload a template file → Choose file**, pick the downloaded file, and click **Next**.

   In the **poor-frog/TINA** repo, this file lives on the `feat/s3-ephemeral-workspaces` branch at `deploy/aws/foundation.yml`. The link above points directly to commit `7d6bba8…` so you can download just this file for the Console step.

{{< workshop-screenshot file="03a-create-vpc.png" description="CloudFormation screen selecting foundation.yml to create the VPC and foundation." >}}

3. Enter **Stack name = `tina-staging`** and click **Next**. This exact name is required for the workshop because it determines the prefix of the three ECR repositories and several policies in the application templates.
4. Leave all other options at their defaults and click **Next → Submit**. Wait for `CREATE_COMPLETE`; if an error occurs, open the **Events** tab, locate the first `CREATE_FAILED` entry, and inspect the reason.
5. Open the **Outputs** tab and note `VpcId`, `PublicSubnetIds`, `AppSubnetIds`, `DataSubnetIds`, `AppRouteTableIds`, `ClusterName`, and `StagingRecordingsBucket`. The workshop uses this bucket for recordings and temporary invocation files.

{{< workshop-screenshot file="03b-create-subnets.png" description="CloudFormation Outputs of the foundation stack: VPC, subnets, cluster, and bucket; mask the account ID if shown." >}}

## 2. Verify Created Resources

1. Go to **VPC → Your VPCs** and locate the VPC matching `VpcId` from the stack Outputs.
2. Go to **Subnets** and filter by that VPC. You should see two public subnets, two app subnets, and two data subnets across two Availability Zones.

{{< workshop-screenshot file="03-vpc-subnets.png" description="Six subnets created by the foundation stack, showing VPC and Availability Zones." >}}

3. In **ECS → Clusters**, confirm that the cluster from the Outputs exists. The stack's S3 bucket has Block Public Access enabled, encryption turned on, and a lifecycle rule that expires files under `runtime-invocations/` after one day. Do not manually edit resources managed by the stack.
