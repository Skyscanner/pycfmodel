"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from collections import Counter
from pycfmodel.model.resources.properties.policy_document import PolicyDocument


def test_one_statement():
    pd = {
        "doc": {
            "Version": "2012-10-17",
            "Statement": {
                "Effect": "Allow",
                "Principal": {"Service": ["ec2.amazonaws.com"], "AWS": "arn:aws:iam::324320755747:root"},
                "Action": ["sts:AssumeRole"],
            },
        }
    }

    document = PolicyDocument(pd["doc"])
    statement = document.statements[0]
    assert statement.effect == "Allow"


def test_multi_statements():
    pd = {
        "doc": {
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
    }

    document = PolicyDocument(pd["doc"])
    statement1 = document.statements[0]
    assert statement1.effect == "Allow"
    statement2 = document.statements[1]
    assert statement2.effect == "bar"


def test_star_resource():
    pd = {
        "PolicyDocument": {
            "Statement": [{"Action": ["*"], "Effect": "Allow", "Resource": "*", "Principal": {"AWS": ["156460612806"]}}]
        }
    }
    document = PolicyDocument(pd["PolicyDocument"])
    assert len(document.star_resource_statements()) == 1


def test_wildcard_actions():
    pd = {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": ["s3:*"],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket2/*",
                    "Principal": {"AWS": "*"},
                }
            ]
        }
    }
    document = PolicyDocument(pd["PolicyDocument"])
    assert len(document.wildcard_allowed_actions()) == 1
    assert len(document.wildcard_allowed_actions(pattern=r"^(\w*:){0,1}\*$")) == 1


def test_not_principal():
    pd = {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": ["*"],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                }
            ]
        }
    }
    document = PolicyDocument(pd["PolicyDocument"])
    assert len(document.allows_not_principal()) == 1


def test_get_iam_actions():

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

    pd = {
        "PolicyDocument": {
            "Statement": [
                {
                    "Action": ["IAM:Delete*"],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
                    "NotPrincipal": {"AWS": ["156460612806"]},
                }
            ]
        }
    }
    document = PolicyDocument(pd["PolicyDocument"])

    actions = document.get_iam_actions()

    assert Counter(correct_list) == Counter(actions)
