from typing import Optional

from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.types import ResolvableBool, ResolvableStr


class Tag(Property):
    """
    Tags for identifying and categorizing AWS resources. These are key-value pairs.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html)
    """

    Key: ResolvableStr
    Value: ResolvableStr
    PropagateAtLaunch: Optional[ResolvableBool]
