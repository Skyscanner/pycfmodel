import re
from collections import Counter

import pytest

from pycfmodel.constants import CONTAINS_STAR
from pycfmodel.model.resources.properties.policy_document import PolicyDocument


@pytest.fixture()
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


@pytest.fixture()
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


@pytest.fixture()
def policy_document_star_resource():
    return PolicyDocument(
        **{"Statement": [{"Action": ["*"], "Effect": "Allow", "Resource": "*", "Principal": {"AWS": ["156460612806"]}}]}
    )


@pytest.fixture()
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


@pytest.fixture()
def policy_document_not_principal():
    return PolicyDocument(
        **{
            "Statement": [
                {
                    "Action": ["IAM:Delete*"],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                }
            ]
        }
    )


def test_one_statement(policy_document_one_statement):
    assert policy_document_one_statement.Statement.Effect == "Allow"


def test_multi_statements(policy_document_multi_statement):
    assert policy_document_multi_statement.Statement[0].Effect == "Allow"
    assert policy_document_multi_statement.Statement[1].Effect == "bar"


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
        "IAM:DeleteAccountPasswordPolicy",
        "IAM:DeleteServiceLinkedRole",
        "IAM:DeleteRole",
        "IAM:DeleteOpenIDConnectProvider",
        "IAM:DeleteGroup",
        "IAM:DeleteRolePolicy",
        "IAM:DeleteSSHPublicKey",
        "IAM:DeleteLoginProfile",
        "IAM:DeleteServiceSpecificCredential",
        "IAM:DeleteUserPolicy",
        "IAM:DeleteVirtualMFADevice",
        "IAM:DeletePolicyVersion",
        "IAM:DeleteGroupPolicy",
        "IAM:DeleteAccountAlias",
        "IAM:DeleteSigningCertificate",
        "IAM:DeleteUser",
        "IAM:DeletePolicy",
        "IAM:DeleteSAMLProvider",
        "IAM:DeleteAccessKey",
        "IAM:DeleteServerCertificate",
        "IAM:DeleteInstanceProfile",
    ]

    assert Counter(correct_list) == Counter(policy_document_not_principal.get_iam_actions())
