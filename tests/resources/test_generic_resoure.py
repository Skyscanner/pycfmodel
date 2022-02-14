from pycfmodel.model.resources.generic_resource import GenericResource
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.statement_condition import StatementCondition


def test_generic_resource():
    resource = GenericResource.parse_obj(
        {
            "Type": "AWS::ECR::RegistryPolicy",
            "Properties": {
                "PolicyText": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "ReplicationAccessCrossAccount1",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::210987654321:root"},
                            "Action": ["ecr:CreateRepository", "ecr:ReplicateImage"],
                            "Condition": {"StringEquals": {"aws:username": "jamesbond"}},
                            "Resource": "arn:aws:ecr:us-west-2:123456789012:repository/*",
                        },
                        {
                            "Sid": "DeleteAccessCrossAccount2",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::111222333444:root"},
                            "Action": ["ecr:DeleteRepository"],
                            "Condition": {"IpAddress": {"aws:SourceIp": "203.0.113.0/24"}},
                            "Resource": "arn:aws:ecr:us-west-2:123456789012:repository/*",
                        },
                    ],
                }
            },
        }
    )
    assert isinstance(resource, GenericResource)
    assert isinstance(resource.Properties.PolicyText, PolicyDocument)
    assert resource.all_statement_conditions == [
        StatementCondition(StringEquals={"aws:username": "jamesbond"}),
        StatementCondition(IpAddress={"aws:SourceIp": "203.0.113.0/24"}),
    ]
