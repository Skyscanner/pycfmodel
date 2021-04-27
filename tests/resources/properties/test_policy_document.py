import re

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
                    "Effect": "bar",
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
                    "Action": [
                        "iam:Delete*",
                        "s3:GetObject*",
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                },
                {
                    "Action": [
                        "s3:List*",
                    ],
                    "Effect": "Deny",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                },
            ]
        }
    )


def test_one_statement(policy_document_one_statement):
    assert policy_document_one_statement.Statement.Effect == "Allow"


def test_multi_statements(policy_document_multi_statement):
    assert policy_document_multi_statement.Statement[0].Effect == "Allow"
    assert policy_document_multi_statement.Statement[1].Effect == "Bar"


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
        "s3:GetObjectLegalHold",
        "s3:GetObjectRetention",
        "s3:GetObjectTagging",
        "s3:GetObjectTorrent",
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAcl",
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
                    "NotAction": [
                        "rds:*",
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                },
            ]
        }
    )


def test_get_allowed_not_actions(policy_document_not_action):
    allowed_actions = set(entry for entry in CLOUDFORMATION_ACTIONS if not entry.startswith("rds:"))
    assert policy_document_not_action.get_allowed_actions() == sorted(allowed_actions)
