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
import pytest

from pycfmodel.model.resources.sns_topic_policy import SNSTopicPolicy


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
