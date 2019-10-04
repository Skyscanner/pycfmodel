from pydantic import BaseModel, Extra, validator

from .resource import Resource


class GenericResource(Resource):
    """This class is used for all resource types that we haven't had time to implement yet"""

    Type: str

    class Config(BaseModel.Config):
        extra = Extra.allow

    @validator("Type")
    def check_type(cls, value):
        return value
