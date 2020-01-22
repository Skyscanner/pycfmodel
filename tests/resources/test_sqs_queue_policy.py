"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
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
