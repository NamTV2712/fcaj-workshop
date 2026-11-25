#!/usr/bin/env python3
"""Assemble one CloudFormation template from TINA's pinned AWS templates.

The generated template retains the architecture and resources of the upstream
Apache-2.0 project. Run with an extracted checkout of the revision documented
in the workshop. This is an offline generator; it never calls AWS.
"""
from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path

import yaml

REVISION = "7d6bba8109f6eac51c0d8241a7083e3e364cf59d"


class CfnLoader(yaml.SafeLoader):
    pass


def cfn_tag(loader, tag, node):
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node, deep=True)
    else:
        value = loader.construct_mapping(node, deep=True)
    if tag == "GetAtt" and isinstance(value, str):
        value = value.split(".", 1)
    key = tag if tag in ("Ref", "Condition") else "Fn::" + tag
    return {key: value}


CfnLoader.add_multi_constructor("!", cfn_tag)


class CfnDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def condition_value(value, root_params):
    """CloudFormation conditions cannot refer to resources; mapped resources exist."""
    if isinstance(value, list):
        return [condition_value(x, root_params) for x in value]
    if not isinstance(value, dict):
        return value
    if "Ref" in value and value["Ref"] not in root_params and not value["Ref"].startswith("AWS::"):
        return "present"
    if any(k in value for k in ("Fn::GetAtt", "Fn::Sub", "Fn::If")):
        return "present"
    return {k: condition_value(v, root_params) for k, v in value.items()}


def static_condition(name, conditions, trail=()):
    if name in trail:
        return None

    def evaluate(expr):
        if isinstance(expr, list):
            values = [evaluate(x) for x in expr]
            return None if any(x is None for x in values) else values
        if not isinstance(expr, dict):
            return expr
        if "Condition" in expr:
            return static_condition(expr["Condition"], conditions, trail + (name,))
        if "Fn::Join" in expr:
            separator, parts = expr["Fn::Join"]
            items = evaluate(parts)
            return None if items is None else separator.join(items)
        if "Fn::Equals" in expr:
            values = evaluate(expr["Fn::Equals"])
            return None if values is None else values[0] == values[1]
        if "Fn::Not" in expr:
            values = evaluate(expr["Fn::Not"])
            return None if values is None else not values[0]
        for op in ("Fn::And", "Fn::Or"):
            if op in expr:
                partial = [evaluate(x) for x in expr[op]]
                if op == "Fn::And" and False in partial:
                    return False
                if op == "Fn::Or" and True in partial:
                    return True
                return None if None in partial else (all(partial) if op == "Fn::And" else any(partial))
        return None

    return evaluate(conditions[name])


def prune(value, conditions):
    if isinstance(value, list):
        return [prune(x, conditions) for x in value]
    if not isinstance(value, dict):
        return value
    if len(value) == 1 and "Fn::If" in value:
        name, yes, no = value["Fn::If"]
        static = static_condition(name, conditions)
        if static is not None:
            return prune(yes if static else no, conditions)
    return {k: prune(v, conditions) for k, v in value.items()}


def ref(name):
    return {"Ref": name}


def att(name, field="Arn"):
    return {"Fn::GetAtt": [name, field]}


def sub(value):
    return {"Fn::Sub": value}


def image(name, digest):
    return {"Fn::Sub": [
        "${AWS::AccountId}.dkr.ecr.${AWS::Region}.${AWS::URLSuffix}/tina-staging/"
        + name + "@${ImageDigest}", {"ImageDigest": ref(digest)}]}


def repo(name):
    return sub("arn:${AWS::Partition}:ecr:${AWS::Region}:${AWS::AccountId}:repository/tina-staging/" + name)


def namespace():
    return ref("RuntimeDiscoveryNamespace")


def replace(value, prefix, resources, conditions, params):
    """Rename local names and replace stack parameters with resource references."""
    if isinstance(value, list):
        return [replace(x, prefix, resources, conditions, params) for x in value]
    if not isinstance(value, dict):
        return value
    if len(value) == 1 and "Ref" in value:
        name = value["Ref"]
        if name in params:
            return copy.deepcopy(params[name])
        return ref(prefix + name if name in resources else name)
    if len(value) == 1 and "Condition" in value:
        name = value["Condition"]
        return {"Condition": prefix + name if name in conditions else name}
    if len(value) == 1 and "Fn::GetAtt" in value:
        name, field = value["Fn::GetAtt"]
        return att(prefix + name if name in resources else name, field)
    if len(value) == 1 and "Fn::Sub" in value:
        expr = value["Fn::Sub"]
        template, existing = (expr, {}) if isinstance(expr, str) else (expr[0], expr[1])
        mappings = {k: replace(v, prefix, resources, conditions, params) for k, v in existing.items()}

        def variable(match):
            token = match.group(1)
            if token in existing or token.startswith("!") or token.startswith("AWS::"):
                return match.group(0)
            name, sep, attribute = token.partition(".")
            if name in resources:
                return "${" + prefix + name + (sep + attribute if sep else "") + "}"
            if name in params and not sep:
                mappings[name] = copy.deepcopy(params[name])
            return match.group(0)

        template = re.sub(r"\$\{([^}]+)\}", variable, template)
        return {"Fn::Sub": [template, mappings]} if mappings else {"Fn::Sub": template}
    transformed = {}
    for key, val in value.items():
        if key == "Condition" and isinstance(val, str) and val in conditions:
            transformed[key] = prefix + val
        elif key == "DependsOn" and (isinstance(val, str) or (isinstance(val, list) and all(isinstance(x, str) for x in val))):
            deps = [val] if isinstance(val, str) else val
            mapped = [prefix + x if x in resources else x for x in deps]
            transformed[key] = mapped[0] if isinstance(val, str) else mapped
        elif key == "Fn::If":
            transformed[key] = [prefix + val[0] if val[0] in conditions else val[0]] + [
                replace(x, prefix, resources, conditions, params) for x in val[1:]
            ]
        else:
            transformed[key] = replace(val, prefix, resources, conditions, params)
    return transformed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="TINA checkout or extracted ZIP")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    aws = args.source / "deploy" / "aws"
    docs = {}
    for prefix, filename in {
        "Foundation": "foundation.yml", "Egress": "staging-egress.yml",
        "Data": "staging-data.yml", "Edge": "staging-edge.yml", "Bot": "ecs-bot.yml",
        "Runtime": "staging-runtime.yml", "Workspace": "staging-workspace-s3.yml",
        "VieGem": "staging-viegem.yml", "Voice": "staging-voice.yml",
        "Core": "staging-core.yml", "Reach": "staging-agent-reach.yml",
        "Agent": "staging-agent-api.yml", "Mcp": "staging-mcp.yml",
        "Flows": "staging-flows.yml", "Terminal": "staging-terminal.yml",
    }.items():
        docs[prefix] = yaml.load((aws / filename).read_text(encoding="utf-8"), Loader=CfnLoader)

    cluster = ref("FoundationCluster")
    vpc = ref("FoundationVpc")
    app = [ref("FoundationAppA"), ref("FoundationAppB")]
    data_subnets = [ref("FoundationDataA"), ref("FoundationDataB")]
    app_sg = att("DataAppSecurityGroup", "GroupId")
    valkey_sg = att("DataValkeySecurityGroup", "GroupId")
    valkey_host = att("DataValkey", "PrimaryEndPoint.Address")
    valkey_secret = ref("DataValkeyAuth")
    db_host = att("DataPostgres", "Endpoint.Address")
    db_secret = att("DataPostgres", "MasterUserSecret.SecretArn")
    bucket = ref("FoundationStagingRecordings")
    edge_url = sub("https://${EdgeDistribution.DomainName}")
    runtime_url = "http://runtime.tina-staging.local:8090"
    bot_image = image("bot", "BotDigest")
    runtime_image = image("runtime", "RuntimeDigest")
    agent_image = image("agent-api", "AgentApiDigest")
    worker_image = image("agent-worker", "AgentWorkerDigest")
    voice_value = lambda v: {"Fn::If": ["EnableVoiceResources", v, ""]}

    common = {"ClusterName": cluster, "VpcId": vpc, "AppSubnetIds": app}
    mappings = {
      "Foundation": {},
      "Egress": {"PublicSubnetId": ref("FoundationPublicA"), "AppRouteTableA": ref("FoundationAppRoutesA"), "AppRouteTableB": ref("FoundationAppRoutesB")},
      "Data": {"VpcId": vpc, "DataSubnetIds": data_subnets, "DeployValkey": "true"},
      "Edge": {"VpcId": vpc, "AppSubnetIds": app, "CloudFrontOriginPrefixListId": ref("CloudFrontOriginPrefixListId"), "WebAclArn": att("WebAcl")},
      "Bot": {"ClusterName": cluster, "BotImage": bot_image, "BotRepositoryArn": repo("bot"), "InvocationBucket": bucket},
      "Runtime": {**common, "AppSecurityGroupId": app_sg, "RuntimeImage": runtime_image, "RuntimeRepositoryArn": repo("runtime"),
          "RuntimeTaskRoleArn": att("BotRuntimeTaskRole"), "BotTaskDefinitionArn": ref("BotBotTaskDefinition"), "BotImage": bot_image,
          "InvocationBucket": bucket, "ValkeyHost": valkey_host, "ValkeySecretArn": valkey_secret,
          "WorkspaceWorkerImage": worker_image, "WorkspaceStorage": "s3",
          "EphemeralWorkspaceTaskDefinitionArn": ref("WorkspaceEphemeralWorkspaceTaskDefinition"),
          "EphemeralWorkspaceTaskRoleArn": att("WorkspaceEphemeralWorkspaceTaskRole"),
          "EphemeralWorkspaceExecutionRoleArn": att("WorkspaceEphemeralWorkspaceExecutionRole"),
          "EphemeralWorkspaceSecurityGroupId": att("WorkspaceEphemeralWorkspaceSecurityGroup", "GroupId"),
          "NovaWorkspaceTaskDefinitionArn": ref("WorkspaceNovaWorkspaceTaskDefinition"),
          "NovaWorkspaceTaskRoleArn": att("WorkspaceNovaWorkspaceTaskRole"), "NovaWorkspaceOwnerIds": ref("WorkspaceOwnerIds"),
          "WorkspaceS3BrokerRoleArn": att("WorkspaceWorkspaceS3BrokerRole"),
          "WorkspaceS3Bucket": ref("WorkspaceWorkspaceStoreBucket"), "WorkspaceS3DataKeyArn": att("WorkspaceWorkspaceDataKey"),
          "DraftWorkerImage": agent_image, "DraftValkeySecurityGroupId": valkey_sg},
      "Workspace": {**common, "RuntimeTaskRoleArn": att("BotRuntimeTaskRole"), "AgentApiTaskRoleArn": att("AgentVoiceModelRole"),
          "NovaWorkerImage": worker_image, "WorkerImage": worker_image, "ValkeyHost": valkey_host,
          "ValkeySecretArn": valkey_secret, "ValkeySecurityGroupId": valkey_sg, "InvocationBucket": bucket,
          "EnableEgressProxy": "true", "ProxyImage": runtime_image, "ProxyRepositoryArn": repo("runtime"),
          "ServiceNamespaceId": namespace(), "S3PrefixListId": ref("S3PrefixListId")},
      "VieGem": {**common, "AppSecurityGroupId": app_sg, "ServiceNamespaceId": namespace(),
          "VieGemImage": image("viegem", "VieGemDigest"), "VieGemRepositoryArn": repo("viegem"), "DesiredCount": 1},
      "Voice": {**common, "AppSecurityGroupId": app_sg, "ServiceNamespaceId": namespace(),
          "VieNeuImage": image("vieneu", "VieNeuDigest"), "LiveKitImage": image("livekit", "LiveKitDigest"),
          "AgentImage": image("livekit-agent", "LiveKitAgentDigest"), "DesiredCount": 1},
      "Core": {**common, "AppSecurityGroupId": app_sg, "RuntimeClientSecurityGroupId": att("RuntimeRuntimeClients", "GroupId"),
          "ServiceNamespaceId": namespace(), "RuntimeUrl": runtime_url, "AdminImage": image("admin-api", "AdminDigest"),
          "MeetingImage": image("meeting-api", "MeetingDigest"), "GatewayImage": image("gateway", "GatewayDigest"),
          "PostgresHost": db_host, "PostgresSecretArn": db_secret, "ValkeyHost": valkey_host, "ValkeySecretArn": valkey_secret,
          "RecordingsBucket": bucket, "TranscriptionUrl": "http://viegem.tina-staging.local:8000/v1/audio/transcriptions",
          "TranscriptionTokenArn": ref("VieGemToken"), "TtsUrl": "http://voice.tina-staging.local:8000",
          "TtsTokenArn": ref("VoiceTtsToken"), "TtsProfileKeyArn": ref("VoiceTtsProfileKey"),
          "LiveKitAgentUrl": "http://voice.tina-staging.local:8080",
          "AgentApiUrl": "http://agent-api.tina-staging.local:8100", "McpUrl": "http://mcp.tina-staging.local:8010",
          "McpGatewayTargetGroupArn": ref("McpGatewayTargets"), "McpOriginSecurityGroupId": att("EdgeOriginSecurityGroup", "GroupId"),
          "VoicePilotRoom": ref("VoicePilotRoom")},
      "Reach": {**common, "ServiceNamespaceId": namespace(), "AgentReachImage": image("agent-reach", "AgentReachDigest")},
      "Agent": {**common, "AppSecurityGroupId": app_sg, "CoreIngressSecurityGroupId": att("CoreCoreIngress", "GroupId"),
          "CoreClientSecurityGroupId": att("CoreCoreClients", "GroupId"), "RuntimeClientSecurityGroupId": att("RuntimeRuntimeClients", "GroupId"),
          "ServiceNamespaceId": namespace(), "AgentApiImage": agent_image, "RuntimeUrl": runtime_url,
          "ValkeyHost": valkey_host, "ValkeySecretArn": valkey_secret, "ValkeySecurityGroupId": valkey_sg,
          "InvocationBucket": bucket, "CoreInternalSecretArn": ref("CoreInternalSecret"),
          "AgentReachUrl": "http://agent-reach.tina-staging.local:8080", "AgentReachClientSecurityGroupId": att("ReachAgentApiClients", "GroupId"),
          "EnableVoiceCompletion": ref("EnableVoice"), "EnableDurableWorkspace": "true", "WorkspacePilotUserIds": ref("WorkspaceOwnerIds"),
          "WorkspaceBedrockOwner": ref("WorkspaceOwnerIds"), "WorkspaceStorage": "s3", "WorkspaceS3Bucket": ref("WorkspaceWorkspaceStoreBucket"),
          "WorkspaceS3DataKeyArn": att("WorkspaceWorkspaceDataKey"), "WorkspaceS3SecretsKeyArn": att("WorkspaceWorkspaceSecretsKey"),
          "WorkspaceS3Users": ref("WorkspaceOwnerIds"), "WorkspaceRuntimeSecurityGroupId": att("WorkspaceEphemeralWorkspaceSecurityGroup", "GroupId"),
          "DraftPilotUserIds": ref("WorkspaceOwnerIds")},
      "Mcp": {**common, "ServiceNamespaceId": namespace(), "CoreIngressSecurityGroupId": att("CoreCoreIngress", "GroupId"),
          "CoreClientSecurityGroupId": att("CoreCoreClients", "GroupId"), "ListenerArn": ref("EdgeListener"),
          "PublicOrigin": edge_url, "McpImage": image("mcp", "McpDigest")},
      "Flows": {**common, "AppSecurityGroupId": app_sg, "CoreClientSecurityGroupId": att("CoreCoreClients", "GroupId"),
          "ServiceNamespaceId": namespace(), "PostgresHost": db_host, "PostgresSecretArn": db_secret,
          "CoreAdminTokenArn": ref("CoreAdminToken"), "CoreInternalSecretArn": ref("CoreInternalSecret"),
          "FlowsImage": image("flows", "FlowsDigest"), "FlowsRepositoryArn": repo("flows")},
      "Terminal": {**common, "CoreClientSecurityGroupId": att("CoreCoreClients", "GroupId"),
          "AlbSecurityGroupId": att("EdgeOriginSecurityGroup", "GroupId"), "ListenerArn": ref("EdgeListener"), "StageUrl": edge_url,
          "TerminalImage": image("terminal", "TerminalDigest"), "TerminalRepositoryArn": repo("terminal"),
          "AdminTokenArn": ref("CoreAdminToken"), "InternalSecretArn": ref("CoreInternalSecret"),
          "WorkspacePilotStage": "routines", "WorkspacePilotUserIds": ref("WorkspaceOwnerIds")},
    }

    result = {"AWSTemplateFormatVersion": "2010-09-09",
      "Description": "TINA workshop: network, ECS Fargate, data, web, agent, workspace and optional voice. Source " + REVISION,
      "Metadata": {"AWSToolsMetrics": {"AWSAgentToolkit": "aws-cloudformation@3"},
                   "com.aws.cloudformation.Context": {"arch": "One isolated evaluation stack; the operator supplies image digests.",
                     "must": "Retain private data; use only reviewed ARM64 images and a fresh account; activate workspace for explicit user IDs."}},
      "Parameters": {}, "Conditions": {"EnableVoiceResources": {"Fn::Equals": [ref("EnableVoice"), "true"]}}, "Resources": {}, "Outputs": {}}
    params = result["Parameters"]
    params["CloudFrontOriginPrefixListId"] = {"Type": "String", "Description": "CloudFront origin-facing managed prefix list ID in us-east-1."}
    params["S3PrefixListId"] = {"Type": "String", "Description": "S3 managed prefix list ID in us-east-1."}
    params["WorkspaceOwnerIds"] = {"Type": "String", "Default": "", "AllowedPattern": "(|[1-9][0-9]*(,[1-9][0-9]*)*)", "Description": "Explicit TINA user IDs, comma separated; set after first sign-in."}
    params["EnableVoice"] = {"Type": "String", "Default": "false", "AllowedValues": ["true", "false"]}
    params["VoicePilotRoom"] = {"Type": "String", "Default": "", "AllowedPattern": "(|[a-z]{3}-[a-z]{4}-[a-z]{3})"}
    for key in ["Bot", "Runtime", "Admin", "Meeting", "Gateway", "Terminal", "AgentApi", "AgentWorker", "AgentReach", "Mcp", "Flows", "VieGem"]:
        params[key + "Digest"] = {"Type": "String", "AllowedPattern": "sha256:[a-f0-9]{64}", "Description": "ARM64 image digest for " + key}
    for key in ["VieNeu", "LiveKit", "LiveKitAgent"]:
        params[key + "Digest"] = {"Type": "String", "Default": "", "AllowedPattern": "(|sha256:[a-f0-9]{64})", "Description": "Required when voice is enabled: ARM64 image digest for " + key}

    for prefix, doc in docs.items():
        resources = set(doc.get("Resources", {}))
        conditions = set(doc.get("Conditions", {}))
        mapped = dict(mappings[prefix])
        for name, param in doc.get("Parameters", {}).items():
            if name not in mapped:
                if "Default" not in param:
                    raise ValueError(f"Unmapped required parameter {prefix}.{name}")
                default = param["Default"]
                if param["Type"] == "CommaDelimitedList":
                    default = str(default).split(",")
                elif isinstance(default, (int, float)):
                    default = str(default)
                mapped[name] = default
        for name, cond in doc.get("Conditions", {}).items():
            transformed_condition = replace(cond, prefix, resources, conditions, mapped)
            if prefix == "Core" and name == "WithVoice":
                transformed_condition = {"Fn::Equals": [ref("EnableVoice"), "true"]}
            result["Conditions"][prefix + name] = condition_value(transformed_condition, params)
        for name, resource in doc.get("Resources", {}).items():
            if prefix == "Foundation" and name in {"BotImages", "RuntimeImages", "MeetingApiImages"}:
                continue
            transformed = replace(resource, prefix, resources, conditions, mapped)
            if prefix == "Voice":
                if "Condition" in transformed:
                    raise ValueError("Voice resource has an unexpected condition")
                transformed["Condition"] = "EnableVoiceResources"
            result["Resources"][prefix + name] = transformed

    result["Resources"]["WebAcl"] = {
        "Type": "AWS::WAFv2::WebACL", "Metadata": {"com.aws.cloudformation.Context": {"why": "Filter common requests at the CloudFront edge.", "must": "Keep CloudFront scope and review rules before production."}},
        "Properties": {"Scope": "CLOUDFRONT", "DefaultAction": {"Allow": {}},
          "VisibilityConfig": {"SampledRequestsEnabled": True, "CloudWatchMetricsEnabled": True, "MetricName": "TinaWorkshopAcl"},
          "Rules": [{"Name": "AWSManagedRulesCommonRuleSet", "Priority": 0, "OverrideAction": {"None": {}},
                     "Statement": {"ManagedRuleGroupStatement": {"VendorName": "AWS", "Name": "AWSManagedRulesCommonRuleSet"}},
                     "VisibilityConfig": {"SampledRequestsEnabled": True, "CloudWatchMetricsEnabled": True, "MetricName": "TinaCommonRules"}}]}}
    for name, resource in list(result["Resources"].items()):
        condition = resource.get("Condition")
        static = static_condition(condition, result["Conditions"]) if condition else None
        if static is False:
            del result["Resources"][name]
            continue
        if static is True:
            resource.pop("Condition")
        result["Resources"][name] = prune(resource, result["Conditions"])

    def add_dependencies(name, *dependencies):
        resource = result["Resources"][name]
        existing = resource.get("DependsOn", [])
        if isinstance(existing, str):
            existing = [existing]
        resource["DependsOn"] = list(dict.fromkeys(existing + list(dependencies)))

    # Standalone upstream stacks previously supplied this ordering implicitly.
    add_dependencies("EgressNat", "FoundationVpcGateway")
    add_dependencies("EdgeOrigin", "FoundationVpcGateway")
    add_dependencies("CoreCoreService", "McpMcpRule")
    add_dependencies("AgentAgentApi", "WorkspaceAgentApiWorkspaceS3Policy")
    add_dependencies("VoiceVoice", "CoreCoreService")
    for name, resource in result["Resources"].items():
        if resource.get("Type") == "AWS::ECS::Service":
            add_dependencies(name, "EgressAppEgressA", "EgressAppEgressB", "FoundationS3GatewayEndpoint")
    result["Outputs"] = {
      "WebsiteUrl": {"Description": "CloudFront URL for this TINA instance.", "Value": edge_url},
      "EcsCluster": {"Description": "ECS cluster for this instance.", "Value": cluster},
      "RecordingsBucket": {"Description": "Retained recordings bucket.", "Value": bucket},
      "WorkspaceBucket": {"Description": "Retained and versioned workspace bucket.", "Value": ref("WorkspaceWorkspaceStoreBucket")},
      "PublicMcpUrl": {"Description": "Authenticated read-only MCP endpoint.", "Value": {"Fn::Sub": ["${Origin}/mcp", {"Origin": edge_url}]}}}
    text = "# SPDX-License-Identifier: Apache-2.0\n# Generated from TINA AWS templates at " + REVISION + "\n" + yaml.dump(result, Dumper=CfnDumper, sort_keys=False, allow_unicode=True, width=110)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"Wrote {args.output}: {len(result['Resources'])} resources, {len(result['Parameters'])} parameters, {len(text.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()
