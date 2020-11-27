import pytest

from pycfmodel.model.resources.iam_role import IAMRole
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def iam_role():
    return IAMRole(
        **{
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": {
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"], "AWS": "arn:aws:iam::111111111111:root"},
                        "Action": ["sts:AssumeRole"],
                    },
                },
                "Path": "/",
                "Policies": [
                    {
                        "PolicyName": "root",
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": {"Effect": "Allow", "Action": "*", "Resource": "*"},
                        },
                    }
                ],
            },
        }
    )


def test_policies(iam_role):
    policies = iam_role.Properties.Policies
    assert len(policies) == 1
    assert policies[0].PolicyName == "root"


def test_iamrole_policy_documents(iam_role):
    assert iam_role.policy_documents == [
        OptionallyNamedPolicyDocument(name="root", policy_document=iam_role.Properties.Policies[0].PolicyDocument)
    ]
