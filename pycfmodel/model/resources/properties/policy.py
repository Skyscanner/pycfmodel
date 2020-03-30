from ...types import ResolvableStr, Resolvable
from .property import Property
from .policy_document import PolicyDocument


class Policy(Property):
    PolicyName: ResolvableStr
    PolicyDocument: Resolvable[PolicyDocument]
