from pycfmodel.model.types import ResolvableStr, Resolvable
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.property import Property


class Policy(Property):
    PolicyName: ResolvableStr
    PolicyDocument: Resolvable[PolicyDocument]
