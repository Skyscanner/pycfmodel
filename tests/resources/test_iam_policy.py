import pytest

from pycfmodel.model.resources.iam_policy import IAMPolicy
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def iam_policy():
    return IAMPolicy(
        **{
            "Type": "AWS::IAM::Policy",
            "Properties": {
                "PolicyName": "Policy",
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
            },
        }
    )


def test_policies(iam_policy):
    assert "Policy" == iam_policy.Properties.PolicyName


def test_iam_managedpolicy_policy_documents(iam_policy):
    assert iam_policy.policy_documents == [
        OptionallyNamedPolicyDocument(name="Policy", policy_document=iam_policy.Properties.PolicyDocument)
    ]
