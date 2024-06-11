from pycfmodel.model.resources.generic_resource import GenericResource
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.statement import Principal, Statement
from pycfmodel.model.resources.properties.statement_condition import StatementCondition


def test_generic_resource():
    resource = GenericResource.model_validate(
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


def test_generic_resource_with_policy_document_in_a_string_property():
    resource = GenericResource.model_validate(
        {
            "Type": "AWS::Logs::ResourcePolicy",
            "Properties": {
                "PolicyName": "guardduty-resourcepolicy",
                "PolicyDocument": '{"Version":"2008-10-17","Statement":[{"Sid":"GDAllowLogs","Effect":"Allow","Principal":{"Service":["events.amazonaws.com","delivery.logs.amazonaws.com"]},"Action":["logs:CreateLogStream"],"Resource":"*"}]}',
            },
        }
    )
    resource_policy_document = resource.Properties.PolicyDocument
    assert isinstance(resource, GenericResource)
    assert isinstance(resource_policy_document, PolicyDocument)
    assert isinstance(resource.Properties.PolicyName, str)
    assert resource_policy_document.Statement == [
        Statement(
            Sid="GDAllowLogs",
            Effect="Allow",
            Resource="*",
            Action=["logs:CreateLogStream"],
            Principal=Principal(Service=["events.amazonaws.com", "delivery.logs.amazonaws.com"]),
        )
    ]


def test_generic_resource_with_bad_json_as_string_is_converted_to_a_string_property():
    resource = GenericResource.model_validate(
        {
            "Type": "AWS::Logs::ResourcePolicy",
            "Properties": {
                "PolicyName": "guardduty-resourcepolicy",
                "PolicyDocument": '{"Ve:{}]}',
            },
        }
    )
    assert isinstance(resource, GenericResource)
    assert isinstance(resource.Properties.PolicyDocument, str)
    assert isinstance(resource.Properties.PolicyName, str)


def test_parse_generic_resource_without_properties():
    resource = GenericResource.model_validate({"Type": "AWS::SNS::Topic"})
    assert isinstance(resource, GenericResource)
    assert resource.Properties is None
    assert resource.Type == "AWS::SNS::Topic"
