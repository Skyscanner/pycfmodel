from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network
from typing import List, TypeVar, Union

from pycfmodel.model.base import FunctionDict

T = TypeVar("T")

Resolvable = Union[T, FunctionDict]
TOrList = Union[T, List[T]]

ResolvableStr = Resolvable[str]
ResolvableInt = Resolvable[int]
ResolvableDate = Resolvable[date]
ResolvableDatetime = Resolvable[datetime]
ResolvableBool = Resolvable[bool]

ResolvableIPv4Network = Resolvable[IPv4Network]
ResolvableIPv6Network = Resolvable[IPv6Network]
ResolvableCondition = ResolvableStr

ResolvableIntOrStr = Resolvable[Union[int, str]]


ResolvableStrOrList = TOrList[ResolvableStr]
ResolvableARNOrList = ResolvableStrOrList
ResolvableIntOrList = TOrList[ResolvableInt]
ResolvableIPOrList = TOrList[Union[ResolvableIPv4Network, ResolvableIPv6Network]]
ResolvableBoolOrList = TOrList[ResolvableBool]
ResolvableBytesOrList = TOrList[bytes]
ResolvableDatetimeOrList = TOrList[ResolvableDatetime]
