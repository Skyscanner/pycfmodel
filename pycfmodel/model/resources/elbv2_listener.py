"""
ELBv2Listener resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::ElasticLoadBalancingV2::Listener.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableInt, ResolvableStr


class ELBv2ListenerProperties(CustomModel):
    """
    Properties for AWS::ElasticLoadBalancingV2::Listener.

    Properties:

    - AlpnPolicy: [TLS listener] The name of the Application-Layer Protocol Negotiation (ALPN) pol...
    - Certificates: The default SSL server certificate for a secure listener. You must provide exact...
    - DefaultActions: The actions for the default rule. You cannot define a condition for a default ru...
    - ListenerAttributes: The listener attributes. Attributes that you do not modify retain their current ...
    - LoadBalancerArn: The Amazon Resource Name (ARN) of the load balancer.
    - MutualAuthentication: The mutual authentication configuration information.
    - Port: The port on which the load balancer is listening. You can't specify a port for a...
    - Protocol: The protocol for connections from clients to the load balancer. For Application ...
    - SslPolicy: [HTTPS and TLS listeners] The security policy that defines which protocols and c...

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html)
    """

    DefaultActions: Resolvable[List[ResolvableGeneric]]
    LoadBalancerArn: ResolvableStr
    AlpnPolicy: Optional[Resolvable[List[ResolvableStr]]] = None
    Certificates: Optional[Resolvable[List[ResolvableGeneric]]] = None
    ListenerAttributes: Optional[Resolvable[List[ResolvableGeneric]]] = None
    MutualAuthentication: Optional[ResolvableGeneric] = None
    Port: Optional[ResolvableInt] = None
    Protocol: Optional[ResolvableStr] = None
    SslPolicy: Optional[ResolvableStr] = None


class ELBv2Listener(Resource):
    """
    Specifies a listener for an Application Load Balancer, Network Load Balancer, or Gateway Load Balancer.

    Properties:

    - Properties: A [ELBv2ListenerProperties][pycfmodel.model.resources.elbv2_listener.ELBv2ListenerProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html)
    """

    Type: Literal["AWS::ElasticLoadBalancingV2::Listener"]
    Properties: Resolvable[ELBv2ListenerProperties]
