import pytest

from pycfmodel.model.resources.iam_role import IAMRole
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def iam_role():
    return IAMRole(
        **{
            "Type": "AWS::IAM::Role",
            "Properties": {
                "Description": "test description",
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": {
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"], "AWS": "arn:aws:iam::111111111111:root"},
                        "Action": ["sts:AssumeRole"],
                        "Condition": {
                            "StringLike": {
                                "iam:AssociatedResourceARN": ["arn:aws:ec2:us-east-1:999999999999:instance/*"]
                            }
                        },
                    },
                },
                "Path": "/",
                "Policies": [
                    {
                        "PolicyName": "root",
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": {
                                "Effect": "Allow",
                                "Action": "*",
                                "Resource": "*",
                                "Condition": {
                                    "StringEquals": {"iam:PassedToService": "ec2.amazonaws.com"},
                                    "StringLike": {
                                        "iam:AssociatedResourceARN": [
                                            "arn:aws:ec2:us-east-1:111122223333:instance/*",
                                            "arn:aws:ec2:us-west-1:111122223333:instance/*",
                                        ]
                                    },
                                },
                            },
                        },
                    }
                ],
                "Tags": [{"Key": "test", "Value": "potatoe"}],
            },
        }
    )


def test_policies(iam_role):
    policies = iam_role.Properties.Policies
    assert len(policies) == 1
    assert policies[0].PolicyName == "root"


def test_all_conditions(iam_role):
    assert iam_role.all_statement_conditions[0].StringEquals == {"iam:PassedToService": "ec2.amazonaws.com"}
    assert iam_role.all_statement_conditions[0].StringLike == {
        "iam:AssociatedResourceARN": [
            "arn:aws:ec2:us-east-1:111122223333:instance/*",
            "arn:aws:ec2:us-west-1:111122223333:instance/*",
        ]
    }

    assert iam_role.assume_role_statement_conditions[0].StringLike == {
        "iam:AssociatedResourceARN": ["arn:aws:ec2:us-east-1:999999999999:instance/*"]
    }


def test_iam_role_policy_documents(iam_role):
    assert iam_role.policy_documents == [
        OptionallyNamedPolicyDocument(name="root", policy_document=iam_role.Properties.Policies[0].PolicyDocument)
    ]


def test_iam_role_assume_role_as_optionally_named_policy_document_list(iam_role):
    assert iam_role.assume_role_as_optionally_named_policy_document_list == [
        OptionallyNamedPolicyDocument(name=None, policy_document=iam_role.Properties.AssumeRolePolicyDocument)
    ]
