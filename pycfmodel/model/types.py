from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network
from typing import List, TypeVar, Union

from pycfmodel.model.base import FunctionDict

IPNetwork = Union[IPv4Network, IPv6Network]

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
ResolvableCondition = ResolvableStr


TOrList = Union[T, List[T]]


IPOrList = TOrList[IPNetwork]
StrOrList = TOrList[ResolvableStr]
ARNOrList = TOrList[ResolvableStr]
IntOrList = TOrList[ResolvableInt]
BytesOrList = TOrList[bytes]
DatetimeOrList = TOrList[datetime]
