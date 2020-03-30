import pytest

from pycfmodel.model.resources.sqs_queue_policy import SQSQueuePolicy


@pytest.fixture()
def sqs_queue_policy():
    return SQSQueuePolicy(
        **{
            "Type": "AWS::SQS::QueuePolicy",
            "Properties": {
                "Queues": [{"Ref": "queue1"}],
                "PolicyDocument": {
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "NotAction": ["sqs:Break*"],
                            "Principal": {"AWS": "arn:aws:iam::111111111111:user/dave.mustaine"},
                            "Resource": "*",
                        }
                    ]
                },
            },
        }
    )


def test_sqs_queue(sqs_queue_policy):
    assert len(sqs_queue_policy.Properties.Queues) == 1
    assert sqs_queue_policy.Properties.PolicyDocument.Statement[0].Effect == "Allow"
    assert sqs_queue_policy.Properties.PolicyDocument.Statement[0].NotAction[0] == "sqs:Break*"
