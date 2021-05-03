from datetime import date, datetime
from ipaddress import IPv4Network, IPv6Network
from typing import List, TypeVar, Union

from pycfmodel.model.base import FunctionDict

T = TypeVar("T")

Resolvable = Union[T, FunctionDict]
InstanceOrListOf = Union[T, List[T]]

ResolvableStr = Resolvable[str]
ResolvableArn = ResolvableStr
ResolvableCondition = ResolvableStr
ResolvableInt = Resolvable[int]
ResolvableDate = Resolvable[date]
ResolvableDatetime = Resolvable[datetime]
ResolvableBool = Resolvable[bool]

ResolvableIPv4Network = Resolvable[IPv4Network]
ResolvableIPv6Network = Resolvable[IPv6Network]

ResolvableIntOrStr = Resolvable[Union[int, str]]


ResolvableStrOrList = InstanceOrListOf[ResolvableStr]
ResolvableArnOrList = InstanceOrListOf[ResolvableArn]
ResolvableIntOrList = InstanceOrListOf[ResolvableInt]
ResolvableIPOrList = InstanceOrListOf[Union[ResolvableIPv4Network, ResolvableIPv6Network]]
ResolvableBoolOrList = InstanceOrListOf[ResolvableBool]
ResolvableBytesOrList = InstanceOrListOf[bytes]
ResolvableDatetimeOrList = InstanceOrListOf[ResolvableDatetime]
