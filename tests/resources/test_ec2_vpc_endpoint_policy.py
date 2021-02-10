import pytest

from pycfmodel.model.resources.ec2_vpc_endpoint_policy import EC2VpcEndpointPolicy
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


@pytest.fixture()
def ec2_vpc_endpoint_policy():
    return EC2VpcEndpointPolicy(
        **{
            "Type": "AWS::EC2::VPCEndpoint",
            "Properties": {
                "PolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": ["s3:GetObject"],
                            "Resource": "*",
                        }
                    ],
                },
                "RouteTableIds": [{"Ref": "routetableA"}, {"Ref": "routetableB"}],
                "ServiceName": "com.amazonaws.eu-west-1.s3",
                "VpcId": "vpc-123-abc",
            },
        }
    )


def test_ec2_vpc_endpoint(ec2_vpc_endpoint_policy: EC2VpcEndpointPolicy):
    assert ec2_vpc_endpoint_policy.Properties.ServiceName == "com.amazonaws.eu-west-1.s3"
    assert ec2_vpc_endpoint_policy.Properties.VpcId == "vpc-123-abc"
    assert len(ec2_vpc_endpoint_policy.Properties.RouteTableIds) == 2
    assert ec2_vpc_endpoint_policy.Properties.PolicyDocument.Statement[0].Effect == "Allow"
    assert ec2_vpc_endpoint_policy.Properties.PolicyDocument.Statement[0].Resource == "*"


def test_ec2_vpc_endpoint_policy_documents(ec2_vpc_endpoint_policy):
    assert ec2_vpc_endpoint_policy.policy_documents == [
        OptionallyNamedPolicyDocument(name=None, policy_document=ec2_vpc_endpoint_policy.Properties.PolicyDocument)
    ]
