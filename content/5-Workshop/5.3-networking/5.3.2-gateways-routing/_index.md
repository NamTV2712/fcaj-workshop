---
aliases: ["/5-workshop/5.3-s3-vpc/5.3.2-test-gwe/"]
title: "NAT, routes and endpoint"
date: 2026-11-25
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

## 1. Create the NAT Gateway with the CloudFormation CLI

The foundation stack already attached an Internet Gateway to the VPC. In CloudShell, run:

```bash
PUBLIC_SUBNETS="$(stackout tina-staging PublicSubnetIds)"
APP_ROUTES="$(stackout tina-staging AppRouteTableIds)"
IFS=, read -r PUBLIC_A PUBLIC_B <<< "$PUBLIC_SUBNETS"
IFS=, read -r ROUTE_A ROUTE_B <<< "$APP_ROUTES"
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-egress --template-file "$TINA_SRC/deploy/aws/staging-egress.yml" \
  --parameter-overrides "PublicSubnetId=$PUBLIC_A" "AppRouteTableA=$ROUTE_A" "AppRouteTableB=$ROUTE_B"
```

Verify the Internet Gateway attached to the VPC under **VPC → Internet gateways**:

{{< workshop-screenshot file="04a-igw-attached.png" description="VPC Internet Gateway in the attached state." >}}

Verify the NAT Gateway under **VPC → NAT gateways**; the stack must be `CREATE_COMPLETE` and the NAT Gateway **Available**:

{{< workshop-screenshot file="04b-nat-available.png" description="NAT Gateway created by the egress stack, with status Available." >}}

## 2. Verify Routes and the S3 Endpoint

In **VPC → Route tables**, inspect the app route tables: the `0.0.0.0/0` route points to the NAT Gateway. The public route table points to the Internet Gateway, and the data subnets have no default Internet route. Both app route tables include the S3 gateway endpoint.

{{< workshop-screenshot file="04-route-tables.png" description="App subnet route table with a default route through the NAT Gateway." >}}

Under **VPC → Endpoints**, locate the endpoint ID matching the `S3EndpointId` output from the foundation stack:

{{< workshop-screenshot file="05-s3-endpoint.png" description="S3 gateway endpoint and its associated app route tables." >}}

Security groups for the application and database will be created by the data stack in a later section. You do not need to create them manually now.

Using a single NAT Gateway shared across two AZs reduces resource count, but introduces a single-AZ dependency and may incur cross-AZ data transfer charges. See the [AWS CloudFront VPC origins documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html) for Internet Gateway and available IPv4 address requirements.
