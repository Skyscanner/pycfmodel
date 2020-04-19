from datetime import date
from ipaddress import IPv4Network, IPv6Network
from typing import List, TypeVar, Union

from pycfmodel.model.base import ConditionDict, FunctionDict

T = TypeVar("T")
Resolvable = Union[T, FunctionDict]

ResolvableStr = Resolvable[str]
ResolvableInt = Resolvable[int]
ResolvableDate = Resolvable[date]
ResolvableBool = Resolvable[bool]
ResolvableStrOrList = Resolvable[Union[str, List]]
ResolvableIntOrStr = Resolvable[Union[int, str]]
ResolvableIPv4Network = Resolvable[IPv4Network]
ResolvableIPv6Network = Resolvable[IPv6Network]

ResolvableCondition = Union[ConditionDict, ResolvableStr]
