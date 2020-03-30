from typing import Optional

from ...types import ResolvableCondition
from ...base import CustomModel


class Property(CustomModel):
    Condition: Optional[ResolvableCondition] = None
