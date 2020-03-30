from typing import Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.types import ResolvableCondition


class Property(CustomModel):
    Condition: Optional[ResolvableCondition] = None
