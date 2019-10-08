from datetime import date
from typing import Union, Dict, List

ResolvableStr = Union[str, Dict]
ResolvableStrOrList = Union[str, List, Dict]
ResolvableInt = Union[int, Dict]
ResolvableIntOrStr = Union[int, str, Dict]
ResolvableDate = Union[date, Dict]
ResolvableBool = Union[bool, Dict]
