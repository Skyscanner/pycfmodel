import pytest

from pycfmodel.model.resources.iam_user import IAMUser
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def iam_user():
    return IAMUser(
        **{
            "Type": "AWS::IAM::User",
            "Properties": {
                "Path": "/",
                "UserName": "TestUser",
                "LoginProfile": {"Password": "ThisMyBestP@ssword", "PasswordResetRequired": False},
                "Policies": [
                    {
                        "PolicyName": "BadPolicy",
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Action": ["lambda:AddPermission", "ssm:SendCommand", "kms:Decrypt"],
                                    "Resource": "*",
                                }
                            ],
                        },
                    }
                ],
            },
        }
    )


def test_policies(iam_user):
    assert len(iam_user.Properties.Policies) == 1
    assert iam_user.Properties.Policies[0].PolicyName == "BadPolicy"


def test_iam_role_policy_documents(iam_user):
    assert iam_user.policy_documents == [
        OptionallyNamedPolicyDocument(name="BadPolicy", policy_document=iam_user.Properties.Policies[0].PolicyDocument)
    ]


def test_credential_check(iam_user):
    assert iam_user.has_hardcoded_credentials()
