"""
ELBv2Listener resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::ElasticLoadBalancingV2::Listener.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable
from pycfmodel.model.types import ResolvableBool
from pycfmodel.model.types import ResolvableInt
from pycfmodel.model.types import ResolvableModel
from pycfmodel.model.types import ResolvableStr


class AuthenticateCognitoConfig(CustomModel):
    """
    Specifies information required when integrating with Amazon Cognito to authenticate users.
    """

    UserPoolArn: ResolvableStr
    UserPoolClientId: ResolvableGeneric
    UserPoolDomain: ResolvableStr
    AuthenticationRequestExtraParams: Optional[ResolvableGeneric] = None
    OnUnauthenticatedRequest: Optional[ResolvableStr] = None
    Scope: Optional[ResolvableStr] = None
    SessionCookieName: Optional[ResolvableStr] = None
    SessionTimeout: Optional[ResolvableStr] = None


ResolvableAuthenticateCognitoConfig = ResolvableModel(AuthenticateCognitoConfig)


class AuthenticateOidcConfig(CustomModel):
    """
    Specifies information required using an identity provide (IdP) that is compliant with OpenID Connect (OIDC) to authenticate users.
    """

    AuthorizationEndpoint: ResolvableStr
    ClientId: ResolvableStr
    Issuer: ResolvableStr
    TokenEndpoint: ResolvableStr
    UserInfoEndpoint: ResolvableStr
    AuthenticationRequestExtraParams: Optional[ResolvableGeneric] = None
    ClientSecret: Optional[ResolvableStr] = None
    OnUnauthenticatedRequest: Optional[ResolvableStr] = None
    Scope: Optional[ResolvableStr] = None
    SessionCookieName: Optional[ResolvableStr] = None
    SessionTimeout: Optional[ResolvableStr] = None
    UseExistingClientSecret: Optional[ResolvableBool] = None


ResolvableAuthenticateOidcConfig = ResolvableModel(AuthenticateOidcConfig)


class Certificate(CustomModel):
    """
    Specifies an SSL server certificate to use as the default certificate for a secure listener.
    """

    CertificateArn: Optional[ResolvableGeneric] = None


ResolvableCertificate = ResolvableModel(Certificate)


class FixedResponseConfig(CustomModel):
    """
    Specifies information required when returning a custom HTTP response.
    """

    StatusCode: ResolvableStr
    ContentType: Optional[ResolvableStr] = None
    MessageBody: Optional[ResolvableStr] = None


ResolvableFixedResponseConfig = ResolvableModel(FixedResponseConfig)


class JwtValidationActionAdditionalClaim(CustomModel):
    """
    Information about an additional claim to validate.
    """

    Format: ResolvableStr
    Name: ResolvableStr
    Values: Resolvable[List[ResolvableStr]]


ResolvableJwtValidationActionAdditionalClaim = ResolvableModel(JwtValidationActionAdditionalClaim)


class JwtValidationConfig(CustomModel):
    """
    
    """

    Issuer: ResolvableStr
    JwksEndpoint: ResolvableStr
    AdditionalClaims: Optional[Resolvable[List[JwtValidationActionAdditionalClaim]]] = None


ResolvableJwtValidationConfig = ResolvableModel(JwtValidationConfig)


class ListenerAttribute(CustomModel):
    """
    Information about a listener attribute.
    """

    Key: Optional[ResolvableStr] = None
    Value: Optional[ResolvableStr] = None


ResolvableListenerAttribute = ResolvableModel(ListenerAttribute)


class MutualAuthentication(CustomModel):
    """
    The mutual authentication configuration information.
    """

    AdvertiseTrustStoreCaNames: Optional[ResolvableStr] = None
    IgnoreClientCertificateExpiry: Optional[ResolvableBool] = None
    Mode: Optional[ResolvableStr] = None
    TrustStoreArn: Optional[ResolvableStr] = None


ResolvableMutualAuthentication = ResolvableModel(MutualAuthentication)


class RedirectConfig(CustomModel):
    """
    Information about a redirect action.
    """

    StatusCode: ResolvableStr
    Host: Optional[ResolvableStr] = None
    Path: Optional[ResolvableStr] = None
    Port: Optional[ResolvableStr] = None
    Protocol: Optional[ResolvableStr] = None
    Query: Optional[ResolvableStr] = None


ResolvableRedirectConfig = ResolvableModel(RedirectConfig)


class TargetGroupStickinessConfig(CustomModel):
    """
    Information about the target group stickiness for a rule.
    """

    DurationSeconds: Optional[ResolvableInt] = None
    Enabled: Optional[ResolvableBool] = None


ResolvableTargetGroupStickinessConfig = ResolvableModel(TargetGroupStickinessConfig)


class TargetGroupTuple(CustomModel):
    """
    Information about how traffic will be distributed between multiple target groups in a forward rule.
    """

    TargetGroupArn: Optional[ResolvableStr] = None
    Weight: Optional[ResolvableInt] = None


ResolvableTargetGroupTuple = ResolvableModel(TargetGroupTuple)


class ForwardConfig(CustomModel):
    """
    Information for creating an action that distributes requests among multiple target groups.
    """

    TargetGroupStickinessConfig: Optional[ResolvableTargetGroupStickinessConfig] = None
    TargetGroups: Optional[Resolvable[List[TargetGroupTuple]]] = None


ResolvableForwardConfig = ResolvableModel(ForwardConfig)


class Action(CustomModel):
    """
    Specifies an action for a listener rule.
    """

    Type: ResolvableStr
    AuthenticateCognitoConfig: Optional[ResolvableAuthenticateCognitoConfig] = None
    AuthenticateOidcConfig: Optional[ResolvableAuthenticateOidcConfig] = None
    FixedResponseConfig: Optional[ResolvableFixedResponseConfig] = None
    ForwardConfig: Optional[ResolvableForwardConfig] = None
    JwtValidationConfig: Optional[ResolvableJwtValidationConfig] = None
    Order: Optional[ResolvableInt] = None
    RedirectConfig: Optional[ResolvableRedirectConfig] = None
    TargetGroupArn: Optional[ResolvableStr] = None


ResolvableAction = ResolvableModel(Action)


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

    DefaultActions: Resolvable[List[Action]]
    LoadBalancerArn: ResolvableStr
    AlpnPolicy: Optional[Resolvable[List[ResolvableStr]]] = None
    Certificates: Optional[Resolvable[List[Certificate]]] = None
    ListenerAttributes: Optional[Resolvable[List[ListenerAttribute]]] = None
    MutualAuthentication: Optional[ResolvableMutualAuthentication] = None
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
