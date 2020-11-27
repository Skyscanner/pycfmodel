import pytest

from pycfmodel.model.resources.sns_topic_policy import SNSTopicPolicy
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def sns_topic_policy():
    return SNSTopicPolicy(
        **{
            "Type": "AWS::SNS::TopicPolicy",
            "Properties": {
                "PolicyDocument": {
                    "Id": "MyTopicPolicy",
                    "Version": "2012-10-17",
                    "Statement": {
                        "Sid": "My-statement-id",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "sns:Publish",
                        "Resource": "*",
                    },
                },
                "Topics": [{"Ref": "MySNSTopic"}],
            },
        }
    )


def test_sns_topic_policy(sns_topic_policy):
    assert len(sns_topic_policy.Properties.Topics) == 1
    assert sns_topic_policy.Properties.PolicyDocument.Statement.Effect == "Allow"


def test_sns_policy_documents(sns_topic_policy):
    assert sns_topic_policy.policy_documents == [
        OptionallyNamedPolicyDocument(name=None, policy_document=sns_topic_policy.Properties.PolicyDocument)
    ]
