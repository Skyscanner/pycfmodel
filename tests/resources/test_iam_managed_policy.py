import pytest

from pycfmodel.model.resources.iam_managed_policy import IAMManagedPolicy
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def iam_managed_policy():
    return IAMManagedPolicy(
        **{
            "Type": "AWS::IAM::ManagedPolicy",
            "Properties": {
                "Path": "/",
                "ManagedPolicyName": "ManagedPolicy",
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


def test_policies(iam_managed_policy):
    assert "ManagedPolicy" == iam_managed_policy.Properties.ManagedPolicyName


def test_iam_managedpolicy_policy_documents(iam_managed_policy):
    assert iam_managed_policy.policy_documents == [
        OptionallyNamedPolicyDocument(
            name="ManagedPolicy", policy_document=iam_managed_policy.Properties.PolicyDocument
        )
    ]
