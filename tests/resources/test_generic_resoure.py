from pycfmodel.model.resources.generic_resource import GenericResource
from pycfmodel.model.resources.properties.policy_document import PolicyDocument


def test_generic_resource():
    resource = GenericResource.parse_obj(
        {
            "Type": "AWS::ECR::RegistryPolicy",
            "Properties": {
                "PolicyText": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "ReplicationAccessCrossAccount",
                            "Effect": "Allow",
                            "Principal": {"AWS": "arn:aws:iam::210987654321:root"},
                            "Action": ["ecr:CreateRepository", "ecr:ReplicateImage"],
                            "Resource": "arn:aws:ecr:us-west-2:123456789012:repository/*",
                        }
                    ],
                }
            },
        }
    )
    assert isinstance(resource, GenericResource)
    assert isinstance(resource.Properties.PolicyText, PolicyDocument)
