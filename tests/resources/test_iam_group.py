import pytest

from pycfmodel.model.resources.iam_group import IAMGroup
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def iam_group():
    return IAMGroup(
        **{
            "Type": "AWS::IAM::Group",
            "Properties": {
                "Path": "/",
                "GroupName": "GroupName",
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


def test_policies(iam_group):
    policies = iam_group.Properties.Policies
    assert len(policies) == 1
    assert policies[0].PolicyName == "BadPolicy"


def test_iamgroup_policy_documents(iam_group):
    assert iam_group.policy_documents == [
        OptionallyNamedPolicyDocument(name="BadPolicy", policy_document=iam_group.Properties.Policies[0].PolicyDocument)
    ]
