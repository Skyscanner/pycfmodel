from pydantic import ConfigDict, field_validator

from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.types import ResolvableStr


class Tag(Property):
    """
    Tags for identifying and categorizing AWS resources. These are key-value pairs.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html)
    """

    model_config = ConfigDict(Property.model_config, coerce_numbers_to_str=True)
    Key: ResolvableStr
    Value: ResolvableStr

    @field_validator("Value", mode="before")
    def coerce_bools_to_strings(cls, v):
        if isinstance(v, bool):
            return str(v)
        return v
