---
title: "Google sign-in and Terminal"
date: 2026-11-25
weight: 4
chapter: false
pre: " <b> 5.4.3.4 </b> "
---

## 1. Create your OAuth client

1. Run `stackout tina-ws-edge StageUrl` in CloudShell and copy **your** CloudFront HTTPS URL without a trailing `/`.
2. Open the [Google Cloud Console](https://console.cloud.google.com/) and create or select a Google Cloud project you manage. Go to **Google Auth Platform → Branding/Audience**, configure your application details, and select **Testing** if you are only testing; add your Google account under **Test users**. Google may rename menu labels in its console UI.
3. Go to **Clients → Create client → Web application**. Add an **Authorized redirect URI** matching `https://<your-cloudfront-domain>/api/auth/callback/google`. Save it to obtain your client ID and client secret. Refer to [Google OAuth for web server applications](https://developers.google.com/identity/protocols/oauth2/web-server) if you run into URI errors. Public or production usage may require a domain you own and Google app verification.
4. In CloudShell, create a temporary file readable only by its owner and open it in an editor:

```bash
umask 077
GOOGLE_JSON="$(mktemp)"
nano "$GOOGLE_JSON"
```

Enter the JSON below, replacing the placeholders with **your real client ID and client secret**; do not send this content, commit it to Git, or include it in screenshots. In `nano`, press `Ctrl+O` then Enter to save, and `Ctrl+X` to exit:

```json
{"client_id":"PASTE_GOOGLE_CLIENT_ID","client_secret":"PASTE_GOOGLE_CLIENT_SECRET"}
```

Create the secret from the file, capture only its ARN, and delete the temporary file. If a secret with the same name already exists, stop and inspect it instead of overwriting it:

```bash
if GOOGLE_SECRET_ARN="$(aws secretsmanager create-secret --region "$AWS_REGION" \
  --name tina-workshop-google --secret-string "file://$GOOGLE_JSON" \
  --query ARN --output text)"; then
  rm -f -- "$GOOGLE_JSON"
  unset GOOGLE_JSON
else
  echo "Failed to create secret; inspect and securely delete the temporary file: $GOOGLE_JSON"
fi
```

To verify in the Console, go to **Secrets Manager → Secrets → tina-workshop-google** and inspect the metadata only—do not click **Retrieve secret value**:

{{< workshop-screenshot file="25-google-secret.png" description="Metadata of the Google OAuth secret; redact the ARN and do not display the secret value." >}}

## 2. Deploy the website

In CloudShell, use the secret ARN you just created. If your CloudShell session was restarted, re-run the initialization block from [Prerequisites](../../../5.2-prerequisites/) and the `image` helper from the [deployment overview](../), restore `CLUSTER`, `VPC_ID`, `APP_SUBNETS`, and `INTERNAL_SECRET_ARN` as in the previous pages, and retrieve the secret ARN with `aws secretsmanager describe-secret --secret-id tina-workshop-google --query ARN --output text`.

```bash
aws cloudformation deploy --region "$AWS_REGION" \
  --stack-name tina-ws-terminal --template-file "$TINA_SRC/deploy/aws/staging-terminal.yml" \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "ClusterName=$CLUSTER" "VpcId=$VPC_ID" "AppSubnetIds=$APP_SUBNETS" \
    "CoreClientSecurityGroupId=$(stackout tina-ws-core ClientSecurityGroupId)" \
    "AlbSecurityGroupId=$(stackout tina-ws-edge OriginSecurityGroupId)" \
    "ListenerArn=$(stackout tina-ws-edge ListenerArn)" "StageUrl=$(stackout tina-ws-edge StageUrl)" \
    "TerminalImage=$(image terminal)" "TerminalRepositoryArn=$(repoarn terminal)" \
    "AdminTokenArn=$(stackout tina-ws-core AdminTokenArn)" \
    "InternalSecretArn=$INTERNAL_SECRET_ARN" "GoogleSecretArn=$GOOGLE_SECRET_ARN"
```

The Terminal image is built in `meetings` mode; leave `WorkspacePilotUserIds` empty by default. Wait for the stack to finish and the task to reach `Running`. In **EC2 → Target groups**, open the target group returned in the Terminal stack's `TargetGroupArn` output, select **Targets**, and wait until it reports **healthy**:

{{< workshop-screenshot file="14-target-health.png" description="Your Terminal target group showing a healthy target." >}}

Open your `StageUrl`. In a fresh instance, the first user to sign in may receive administrator privileges, so sign in with your Google test user before sharing the URL. Then continue to [application validation](../../5.4.4-application-validation/).
