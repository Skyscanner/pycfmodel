import re

import pytest

from pycfmodel import parse
from pycfmodel.action_expander import _build_regex, _expand_action, _expand_actions
from pycfmodel.cloudformation_actions import CLOUDFORMATION_ACTIONS


@pytest.mark.parametrize(
    "action, expected_pattern",
    [
        ("", re.compile("^$", re.IGNORECASE)),
        ("*", re.compile("^.*$", re.IGNORECASE)),
        ("?", re.compile("^.{1}$", re.IGNORECASE)),
        ("a", re.compile("^a$", re.IGNORECASE)),
        ("a*", re.compile("^a.*$", re.IGNORECASE)),
        ("a?", re.compile("^a.{1}$", re.IGNORECASE)),
        ("a*a?", re.compile("^a.*a.{1}$", re.IGNORECASE)),
    ],
)
def test_build_regex(action, expected_pattern):
    assert _build_regex(action) == expected_pattern


@pytest.mark.parametrize(
    "action, expected_output",
    [
        ("ec2:RunInstances", ["ec2:RunInstances"]),
        ("ec2:Run?nstances", ["ec2:RunInstances"]),
        ("ec?:RunInstances", ["ec2:RunInstances"]),
        ("ec2:Run*", ["ec2:RunInstances", "ec2:RunScheduledInstances"]),
    ],
)
def test_expand_action(action, expected_output):
    assert _expand_action(action) == expected_output


@pytest.mark.parametrize(
    "action, expected_output",
    [
        ("ec2:RunInstances", ["ec2:RunInstances"]),
        ("ec2:Run?nstances", ["ec2:RunInstances"]),
        ("ec?:RunInstances", ["ec2:RunInstances"]),
        ("ec2:Run*", ["ec2:RunInstances", "ec2:RunScheduledInstances"]),
        (["ec2:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run?nstances"], ["ec2:RunInstances"]),
        (["ec?:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run*"], ["ec2:RunInstances", "ec2:RunScheduledInstances"]),
        (["ec2:RunInstances", "ec2:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run?nstances", "ec2:Run?nstances"], ["ec2:RunInstances"]),
        (["ec?:RunInstances", "ec?:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run*", "ec2:Run*"], ["ec2:RunInstances", "ec2:RunScheduledInstances"]),
        (["*"], CLOUDFORMATION_ACTIONS),
        (["ec2:Run*", "*"], CLOUDFORMATION_ACTIONS),
    ],
)
def test_expand_actions(action, expected_output):
    assert _expand_actions(action) == expected_output


@pytest.mark.parametrize(
    "action, reverse_expected_output",
    [
        ("ec2:RunInstances", ["ec2:RunInstances"]),
        ("ec2:Run?nstances", ["ec2:RunInstances"]),
        ("ec?:RunInstances", ["ec2:RunInstances"]),
        ("ec2:Run*", ["ec2:RunInstances", "ec2:RunScheduledInstances"]),
        (["ec2:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run?nstances"], ["ec2:RunInstances"]),
        (["ec?:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run*"], ["ec2:RunInstances", "ec2:RunScheduledInstances"]),
        (["ec2:RunInstances", "ec2:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run?nstances", "ec2:Run?nstances"], ["ec2:RunInstances"]),
        (["ec?:RunInstances", "ec?:RunInstances"], ["ec2:RunInstances"]),
        (["ec2:Run*", "ec2:Run*"], ["ec2:RunInstances", "ec2:RunScheduledInstances"]),
        (["*"], CLOUDFORMATION_ACTIONS),
        (["ec2:Run*", "*"], CLOUDFORMATION_ACTIONS),
    ],
)
def test_expand_not_actions(action, reverse_expected_output):
    expected_output = sorted(set(CLOUDFORMATION_ACTIONS) - set(reverse_expected_output))
    assert _expand_actions(action, not_action=True) == expected_output


def test_expand_actions_scenario_1():
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Parameters": {"StarParameter": {"Type": "String", "Default": "*", "Description": "Star Param"}},
        "Resources": {
            "rootRole": {
                "Type": "AWS::IAM::Role",
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"AWS": {"Fn::Sub": "arn:aws:iam::${AWS::AccountId}:root"}},
                                "Action": ["sts:AssumeRole"],
                            }
                        ],
                    },
                    "Path": "/",
                    "Policies": [
                        {
                            "PolicyName": "root",
                            "PolicyDocument": {
                                "Version": "2012-10-17",
                                "Statement": [
                                    {
                                        "Effect": "Allow",
                                        "Action": {"Ref": "StarParameter"},
                                        "Resource": {"Ref": "StarParameter"},
                                    }
                                ],
                            },
                        }
                    ],
                },
            }
        },
    }

    model = parse(template).resolve(extra_params={"AWS::AccountId": "123"}).expand_actions()
    assert (
        model.Resources["rootRole"].Properties.Policies[0].PolicyDocument.Statement[0].Action == CLOUDFORMATION_ACTIONS
    )


def test_resolve_scenario_2():
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "IAM role for Lambda",
        "Parameters": {"LambdaFunctionName": {"Description": "Name of the lambda function", "Type": "String"}},
        "Resources": {
            "lambdaRole": {
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Statement": [
                            {
                                "Action": "sts:AssumeRole",
                                "Effect": "Allow",
                                "Principal": {"Service": ["lambda.amazonaws.com"]},
                            }
                        ],
                        "Version": "2012-10-17",
                    },
                    "Path": "/",
                    "Policies": [
                        {
                            "PolicyDocument": {
                                "Statement": [
                                    {
                                        "Action": ["lambda:*"],
                                        "Effect": "Allow",
                                        "Resource": [
                                            {
                                                "Fn::Sub": (
                                                    "arn:aws:lambda:*:${AWS::AccountId}:function:${LambdaFunctionName}"
                                                )
                                            }
                                        ],
                                    }
                                ],
                                "Version": "2012-10-17",
                            },
                            "PolicyName": "lambda_permissions",
                        },
                        {
                            "PolicyDocument": {
                                "Statement": [
                                    {
                                        "Action": ["xray:PutTraceSegments", "xray:PutTelemetryRecords"],
                                        "Effect": "Allow",
                                        "Resource": ["*"],
                                    }
                                ],
                                "Version": "2012-10-17",
                            },
                            "PolicyName": "AWSXrayWriteOnlyAccess",
                        },
                        {
                            "PolicyDocument": {
                                "Statement": [
                                    {
                                        "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                                        "Effect": "Allow",
                                        "Resource": ["*"],
                                    }
                                ],
                                "Version": "2012-10-17",
                            },
                            "PolicyName": "Logging",
                        },
                    ],
                    "RoleName": {"Fn::Sub": "${LambdaFunctionName}-role"},
                },
                "Type": "AWS::IAM::Role",
            }
        },
    }
    model = (
        parse(template)
        .resolve(extra_params={"AWS::AccountId": "123", "LambdaFunctionName": "test-lambda"})
        .expand_actions()
    )
    assert model.Resources["lambdaRole"].Properties.AssumeRolePolicyDocument.Statement[0].Action == ["sts:AssumeRole"]

    assert model.Resources["lambdaRole"].Properties.Policies[0].PolicyDocument.Statement[0].Action == [
        "lambda:AddLayerVersionPermission",
        "lambda:AddPermission",
        "lambda:CreateAlias",
        "lambda:CreateEventSourceMapping",
        "lambda:CreateFunction",
        "lambda:DeleteAlias",
        "lambda:DeleteEventSourceMapping",
        "lambda:DeleteFunction",
        "lambda:DeleteFunctionConcurrency",
        "lambda:DeleteFunctionEventInvokeConfig",
        "lambda:DeleteLayerVersion",
        "lambda:DeleteProvisionedConcurrencyConfig",
        "lambda:DisableReplication",
        "lambda:EnableReplication",
        "lambda:GetAccountSettings",
        "lambda:GetAlias",
        "lambda:GetEventSourceMapping",
        "lambda:GetFunction",
        "lambda:GetFunctionConcurrency",
        "lambda:GetFunctionConfiguration",
        "lambda:GetFunctionEventInvokeConfig",
        "lambda:GetLayerVersion",
        "lambda:GetLayerVersionPolicy",
        "lambda:GetPolicy",
        "lambda:GetProvisionedConcurrencyConfig",
        "lambda:InvokeAsync",
        "lambda:InvokeFunction",
        "lambda:ListAliases",
        "lambda:ListEventSourceMappings",
        "lambda:ListFunctionEventInvokeConfigs",
        "lambda:ListFunctions",
        "lambda:ListLayerVersions",
        "lambda:ListLayers",
        "lambda:ListProvisionedConcurrencyConfigs",
        "lambda:ListTags",
        "lambda:ListVersionsByFunction",
        "lambda:PublishLayerVersion",
        "lambda:PublishVersion",
        "lambda:PutFunctionConcurrency",
        "lambda:PutFunctionEventInvokeConfig",
        "lambda:PutProvisionedConcurrencyConfig",
        "lambda:RemoveLayerVersionPermission",
        "lambda:RemovePermission",
        "lambda:TagResource",
        "lambda:UntagResource",
        "lambda:UpdateAlias",
        "lambda:UpdateEventSourceMapping",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:UpdateFunctionEventInvokeConfig",
    ]
    assert model.Resources["lambdaRole"].Properties.Policies[1].PolicyDocument.Statement[0].Action == [
        "xray:PutTelemetryRecords",
        "xray:PutTraceSegments",
    ]
    assert model.Resources["lambdaRole"].Properties.Policies[2].PolicyDocument.Statement[0].Action == [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
    ]
