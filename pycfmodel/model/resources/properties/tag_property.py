from typing import Optional

from pycfmodel.model.resources.properties.tag import Tag
from pycfmodel.model.types import ResolvableBool


class TagProperty(Tag):
    """
    TagProperty specifies a tag for the Tags property of AWS::AutoScaling::AutoScalingGroup.
    TagProperty adds tags to all associated instances in an Auto Scaling group.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html)
    """

    PropagateAtLaunch: Optional[ResolvableBool]
