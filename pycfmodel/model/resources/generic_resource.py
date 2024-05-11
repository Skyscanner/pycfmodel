from typing import Optional

from pydantic import ConfigDict

from pycfmodel.model.generic import Generic
from pycfmodel.model.resources.resource import Resource


class GenericResource(Resource):
    """This class is used for all resource types that don't have a dedicated class."""

    Type: str
    Properties: Optional[Generic] = None

    model_config = ConfigDict(extra="allow")
