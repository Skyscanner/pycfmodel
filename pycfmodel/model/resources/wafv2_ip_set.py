from typing import List, Literal, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.types import Resolvable, ResolvableStr, ResolvableIPOrList


class WAFv2IPSetProperties(CustomModel):
    """
    Properties for AWS::WAFv2::IPSet resource.

    Properties:

    - Addresses: List of IP addresses and address ranges in CIDR notation (e.g., "192.0.2.0/24").
    - Description: Description of the IP set.
    - IPAddressVersion: IP address version (IPV4 or IPV6).
    - Name: Name of the IP set.
    - Scope: Scope of the IP set (CLOUDFRONT or REGIONAL).
    - Tags: Key-value pairs to associate with the IP set.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html)
    """

    Addresses: ResolvableIPOrList
    Description: Optional[ResolvableStr] = None
    IPAddressVersion: ResolvableStr
    Name: Optional[ResolvableStr] = None
    Scope: ResolvableStr
    Tags: Optional[List[Tag]] = None


class WAFv2IPSet(Resource):
    """
    AWS::WAFv2::IPSet resource.

    Properties:

    - Properties: A [WAFv2IPSetProperties][pycfmodel.model.resources.wafv2_ip_set.WAFv2IPSetProperties] object.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html)
    """

    Type: Literal["AWS::WAFv2::IPSet"]
    Properties: Resolvable[WAFv2IPSetProperties]
