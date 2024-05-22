from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.policy_document import PolicyDocument as resource_policy_document
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableStr
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


class EC2VpcEndpointPolicyProperties(CustomModel):
    """
    Properties:

    - PolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - PrivateDnsEnabled: Indicate whether to associate a private hosted zone with the specified VPC.
    - RouteTableIds: One or more route table IDs.
    - SecurityGroupIds: The ID of one or more security groups to associate with the endpoint network interface.
    - ServiceName: The service name.
    - SubnetIds: The ID of one or more subnets in which to create an endpoint network interface.
    - VpcEndpointType: The type of endpoint.
    - VpcId: The ID of the VPC in which the endpoint will be used.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html)
    """

    PolicyDocument: Optional[Resolvable[resource_policy_document]] = None
    PrivateDnsEnabled: Optional[ResolvableBool] = None
    RouteTableIds: Optional[Resolvable[List[ResolvableStr]]] = None
    SecurityGroupIds: Optional[Resolvable[List[ResolvableStr]]] = None
    ServiceName: ResolvableStr
    SubnetIds: Optional[Resolvable[List[ResolvableStr]]] = None
    VpcEndpointType: Optional[ResolvableStr] = None
    VpcId: ResolvableStr


class EC2VpcEndpointPolicy(Resource):
    """
    Properties:

    - Properties: An [EC2 VPC Policy Endpoint Properties][pycfmodel.model.resources.ec2_vpc_endpoint_policy.EC2VpcEndpointPolicyProperties]
    object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html)
    """

    Type: Literal["AWS::EC2::VPCEndpoint"]
    Properties: Resolvable[EC2VpcEndpointPolicyProperties]

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        if not self.Properties.PolicyDocument:
            return []
        return [OptionallyNamedPolicyDocument(name=None, policy_document=self.Properties.PolicyDocument)]
