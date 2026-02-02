"""
Route53RecordSet resource for AWS CloudFormation.

Auto-generated from AWS CloudFormation schema for AWS::Route53::RecordSet.
"""

from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import ResolvableGeneric
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableBool, ResolvableInt, ResolvableStr


class Route53RecordSetProperties(CustomModel):
    """
    Properties for AWS::Route53::RecordSet.

    Properties:

    - AliasTarget: 
    - CidrRoutingConfig: 
    - Comment: 
    - Failover: 
    - GeoLocation: 
    - GeoProximityLocation: 
    - HealthCheckId: 
    - HostedZoneId: 
    - HostedZoneName: 
    - MultiValueAnswer: 
    - Name: 
    - Region: 
    - ResourceRecords: 
    - SetIdentifier: 
    - TTL: 
    - Type: 
    - Weight: 

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html)
    """

    Name: ResolvableStr
    Type: ResolvableStr
    AliasTarget: Optional[ResolvableGeneric] = None
    CidrRoutingConfig: Optional[ResolvableGeneric] = None
    Comment: Optional[ResolvableStr] = None
    Failover: Optional[ResolvableStr] = None
    GeoLocation: Optional[ResolvableGeneric] = None
    GeoProximityLocation: Optional[ResolvableGeneric] = None
    HealthCheckId: Optional[ResolvableStr] = None
    HostedZoneId: Optional[ResolvableStr] = None
    HostedZoneName: Optional[ResolvableStr] = None
    MultiValueAnswer: Optional[ResolvableBool] = None
    Region: Optional[ResolvableStr] = None
    ResourceRecords: Optional[Resolvable[List[ResolvableStr]]] = None
    SetIdentifier: Optional[ResolvableStr] = None
    TTL: Optional[ResolvableStr] = None
    Weight: Optional[ResolvableInt] = None


class Route53RecordSet(Resource):
    """
    Resource Type definition for AWS::Route53::RecordSet

    Properties:

    - Properties: A [Route53RecordSetProperties][pycfmodel.model.resources.route53_record_set.Route53RecordSetProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html)
    """

    Type: Literal["AWS::Route53::RecordSet"]
    Properties: Resolvable[Route53RecordSetProperties]
