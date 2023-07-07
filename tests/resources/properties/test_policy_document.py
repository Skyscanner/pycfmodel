import re
from ipaddress import IPv4Network

import pytest
from pytest import fixture

from pycfmodel.cloudformation_actions import CLOUDFORMATION_ACTIONS
from pycfmodel.constants import CONTAINS_STAR
from pycfmodel.model.resources.properties.policy_document import PolicyDocument


@fixture
def policy_document_one_statement():
    return PolicyDocument(
        **{
            "Version": "2012-10-17",
            "Statement": {
                "Effect": "Allow",
                "Principal": {"Service": ["ec2.amazonaws.com"], "AWS": "arn:aws:iam::324320755747:root"},
                "Action": ["sts:AssumeRole"],
            },
        }
    )


@fixture
def policy_document_multi_statement():
    return PolicyDocument(
        **{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": ["ec2.amazonaws.com"], "AWS": "arn:aws:iam::324320755747:root"},
                    "Action": ["sts:AssumeRole"],
                },
                {
                    "Effect": "Allow",
                    "Principal": {"Service": ["ec2.amazonaws.com"], "AWS": "arn:aws:iam::324320755747:root"},
                    "Action": ["sts:AssumeRole"],
                },
            ],
        }
    )


@fixture
def policy_document_star_resource():
    return PolicyDocument(
        **{"Statement": [{"Action": ["*"], "Effect": "Allow", "Resource": "*", "Principal": {"AWS": ["156460612806"]}}]}
    )


@fixture
def policy_document_wildcard_actions():
    return PolicyDocument(
        **{
            "Statement": [
                {
                    "Action": ["s3:*"],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket2/*",
                    "Principal": {"AWS": "*"},
                }
            ]
        }
    )


@fixture
def policy_document_not_principal():
    return PolicyDocument(
        **{
            "Statement": [
                {
                    "Action": ["iam:Delete*", "s3:GetObject*"],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                },
                {
                    "Action": ["s3:List*"],
                    "Effect": "Deny",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                },
            ]
        }
    )


@fixture
def policy_document_kms_key():
    return PolicyDocument(
        **{
            "Version": "2012-10-17",
            "Id": "key-consolepolicy-2",
            "Statement": [
                {
                    "Sid": "Enable IAM policies",
                    "Effect": "Allow",
                    "Principal": {"AWS": "arn:aws:iam::111122223333:root"},
                    "Action": "kms:*",
                    "Resource": "*",
                },
                {
                    "Sid": "Allow access for Key Administrators",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "arn:aws:iam::111122223333:user/KMSAdminUser",
                            "arn:aws:iam::111122223333:role/KMSAdminRole",
                        ]
                    },
                    "Action": [
                        "kms:Create*",
                        "kms:Describe*",
                        "kms:Enable*",
                        "kms:List*",
                        "kms:Put*",
                        "kms:Update*",
                        "kms:Revoke*",
                        "kms:Disable*",
                        "kms:Get*",
                        "kms:Delete*",
                        "kms:TagResource",
                        "kms:UntagResource",
                        "kms:ScheduleKeyDeletion",
                        "kms:CancelKeyDeletion",
                    ],
                    "Resource": "*",
                },
                {
                    "Sid": "Allow use of the key",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "arn:aws:iam::111122223333:user/ExampleUser",
                            "arn:aws:iam::111122223333:role/ExampleRole",
                            "arn:aws:iam::444455556666:root",
                        ]
                    },
                    "Action": [
                        "kms:Encrypt",
                        "kms:Decrypt",
                        "kms:ReEncrypt*",
                        "kms:GenerateDataKey*",
                        "kms:DescribeKey",
                    ],
                    "Resource": "*",
                },
                {
                    "Sid": "Allow attachment of persistent resources",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "arn:aws:iam::111122223333:user/ExampleUser",
                            "arn:aws:iam::111122223333:role/ExampleRole",
                            "arn:aws:iam::444455556666:root",
                        ]
                    },
                    "Action": ["kms:CreateGrant", "kms:ListGrants", "kms:RevokeGrant"],
                    "Resource": "*",
                    "Condition": {"Bool": {"kms:GrantIsForAWSResource": True}},
                },
            ],
        }
    )


def test_one_statement(policy_document_one_statement):
    assert policy_document_one_statement.Id is None
    assert policy_document_one_statement.Statement.Effect == "Allow"


def test_multi_statements(policy_document_multi_statement):
    assert policy_document_multi_statement.Statement[0].Effect == "Allow"
    assert policy_document_multi_statement.Statement[1].Effect == "Allow"


def test_star_resource(policy_document_star_resource):
    assert len(policy_document_star_resource.statements_with(CONTAINS_STAR)) == 1


def test_wildcard_actions(policy_document_wildcard_actions):
    assert len(policy_document_wildcard_actions.allowed_actions_with(CONTAINS_STAR)) == 1
    assert len(policy_document_wildcard_actions.allowed_actions_with(re.compile(r"^(\w*:){0,1}\*$"))) == 1


def test_not_principal(policy_document_not_principal):
    assert len(policy_document_not_principal.allowed_actions_with(CONTAINS_STAR)) == 1


def test_allowed_principals_with(policy_document_multi_statement):
    assert policy_document_multi_statement.allowed_principals_with(re.compile(r".*root")) == [
        "arn:aws:iam::324320755747:root"
    ]


def test_non_whitelisted_allowed_principals(policy_document_multi_statement):
    assert policy_document_multi_statement.non_whitelisted_allowed_principals(["arn:aws:iam::324320755747:root"]) == [
        "ec2.amazonaws.com"
    ]


def test_get_iam_actions(policy_document_not_principal):
    correct_list = [
        "iam:DeleteAccessKey",
        "iam:DeleteAccountAlias",
        "iam:DeleteAccountPasswordPolicy",
        "iam:DeleteCloudFrontPublicKey",
        "iam:DeleteGroup",
        "iam:DeleteGroupPolicy",
        "iam:DeleteInstanceProfile",
        "iam:DeleteLoginProfile",
        "iam:DeleteOpenIDConnectProvider",
        "iam:DeletePolicy",
        "iam:DeletePolicyVersion",
        "iam:DeleteRole",
        "iam:DeleteRolePermissionsBoundary",
        "iam:DeleteRolePolicy",
        "iam:DeleteSAMLProvider",
        "iam:DeleteSSHPublicKey",
        "iam:DeleteServerCertificate",
        "iam:DeleteServiceLinkedRole",
        "iam:DeleteServiceSpecificCredential",
        "iam:DeleteSigningCertificate",
        "iam:DeleteUser",
        "iam:DeleteUserPermissionsBoundary",
        "iam:DeleteUserPolicy",
        "iam:DeleteVirtualMFADevice",
    ]

    assert policy_document_not_principal.get_iam_actions() == correct_list


def test_get_allowed_actions(policy_document_not_principal):
    correct_list = [
        "iam:DeleteAccessKey",
        "iam:DeleteAccountAlias",
        "iam:DeleteAccountPasswordPolicy",
        "iam:DeleteCloudFrontPublicKey",
        "iam:DeleteGroup",
        "iam:DeleteGroupPolicy",
        "iam:DeleteInstanceProfile",
        "iam:DeleteLoginProfile",
        "iam:DeleteOpenIDConnectProvider",
        "iam:DeletePolicy",
        "iam:DeletePolicyVersion",
        "iam:DeleteRole",
        "iam:DeleteRolePermissionsBoundary",
        "iam:DeleteRolePolicy",
        "iam:DeleteSAMLProvider",
        "iam:DeleteSSHPublicKey",
        "iam:DeleteServerCertificate",
        "iam:DeleteServiceLinkedRole",
        "iam:DeleteServiceSpecificCredential",
        "iam:DeleteSigningCertificate",
        "iam:DeleteUser",
        "iam:DeleteUserPermissionsBoundary",
        "iam:DeleteUserPolicy",
        "iam:DeleteVirtualMFADevice",
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:GetObjectAttributes",
        "s3:GetObjectLegalHold",
        "s3:GetObjectRetention",
        "s3:GetObjectTagging",
        "s3:GetObjectTorrent",
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAcl",
        "s3:GetObjectVersionAttributes",
        "s3:GetObjectVersionForReplication",
        "s3:GetObjectVersionTagging",
        "s3:GetObjectVersionTorrent",
    ]

    assert policy_document_not_principal.get_allowed_actions() == correct_list


@fixture
def policy_document_not_action():
    return PolicyDocument(
        **{
            "Statement": [
                {
                    "NotAction": ["rds:*"],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                }
            ]
        }
    )


def test_get_allowed_not_actions(policy_document_not_action):
    allowed_actions = set(entry for entry in CLOUDFORMATION_ACTIONS if not entry.startswith("rds:"))
    assert policy_document_not_action.get_allowed_actions() == sorted(allowed_actions)


@fixture
def policy_document_condition_with_source_ip():
    return PolicyDocument(
        **{
            "Statement": [
                {
                    "Action": ["s3:ListBucket"],
                    "Condition": {"IpAddress": {"aws:SourceIp": ["116.202.65.160", "116.202.68.32/27"]}},
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                }
            ]
        }
    )


@fixture
def policy_document_condition_with_source_vpce():
    return PolicyDocument(
        **{
            "Statement": [
                {
                    "Action": ["s3:ListBucket"],
                    "Condition": {"IpAddress": {"aws:SourceVpce": ["vpce-123456"]}},
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "statement_effect, is_allow",
    [
        ("Allow", True),
        ("Deny", False),
    ],
)
def test_policy_document_chan_check_if_the_statement_effect_is_allow_or_deny(statement_effect: str, is_allow: bool):
    assert PolicyDocument._is_statement_effect_allow(statement_effect=statement_effect) == is_allow


def test_policy_document_condition_with_source_ip(policy_document_condition_with_source_ip: PolicyDocument):
    assert policy_document_condition_with_source_ip.Statement[0].Condition.IpAddress == {
        "aws:SourceIp": [IPv4Network("116.202.65.160/32"), IPv4Network("116.202.68.32/27")]
    }


def test_policy_document_condition_with_source_vpce(policy_document_condition_with_source_vpce: PolicyDocument):
    assert policy_document_condition_with_source_vpce.Statement[0].Condition.IpAddress == {
        "aws:SourceVpce": ["vpce-123456"]
    }


def test_policy_document_kms_key(policy_document_kms_key: PolicyDocument):
    assert policy_document_kms_key.Id == "key-consolepolicy-2"
    assert len(policy_document_kms_key.Statement) == 4
    assert policy_document_kms_key.Statement[3].Condition.Bool == {"kms:GrantIsForAWSResource": True}
