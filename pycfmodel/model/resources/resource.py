from typing import Dict, ClassVar, Optional

from pydantic import validator

from pycfmodel.model.base import CustomModel
from pycfmodel.model.parameter import Parameter
from pycfmodel.model.types import ResolvableCondition, ResolvableStr, ResolvableStrOrList


class Resource(CustomModel):
    TYPE_VALUE: ClassVar[str]
    Type: str
    Condition: Optional[ResolvableCondition] = None
    CreatePolicy: Optional[Dict] = None
    DeletionPolicy: Optional[ResolvableStr] = None
    DependsOn: Optional[ResolvableStrOrList] = None
    Metadata: Optional[Dict] = None
    UpdatePolicy: Optional[Dict] = None
    UpdateReplacePolicy: Optional[ResolvableStr] = None

    @validator("Type")
    def check_type(cls, value):
        if value != cls.TYPE_VALUE:
            raise ValueError(f"Value needs to be {cls.TYPE_VALUE}")
        return value

    def has_hardcoded_credentials(self) -> bool:
        if not self.Metadata or not self.Metadata.get("AWS::CloudFormation::Authentication"):
            return False

        for auth in self.Metadata["AWS::CloudFormation::Authentication"].values():
            if not all(
                [
                    auth.get("accessKeyId", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("password", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("secretKey", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                ]
            ):
                return True

        return False
