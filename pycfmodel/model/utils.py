from dataclasses import dataclass
from typing import Optional

from pycfmodel.model.resources.properties.policy_document import PolicyDocument


@dataclass
class OptionallyNamedPolicyDocument:
    name: Optional[str]
    policy_document: PolicyDocument
