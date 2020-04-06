from typing import Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.types import ResolvableCondition


class Property(CustomModel):
    """
    This class is used for all property types that we haven't had time to implement yet.

    Properties:

    - Condition
    """

    Condition: Optional[ResolvableCondition] = None
