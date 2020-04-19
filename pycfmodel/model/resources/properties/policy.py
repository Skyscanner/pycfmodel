from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.property import Property
from pycfmodel.model.types import Resolvable, ResolvableStr


class Policy(Property):
    """
    Contains information about an attached policy.

    Properties:

    - PolicyDocument: A [policy document][pycfmodel.model.resources.properties.policy_document.PolicyDocument] object.
    - PolicyName: The friendly name (not ARN) identifying the policy.
    """

    PolicyName: ResolvableStr
    PolicyDocument: Resolvable[PolicyDocument]
