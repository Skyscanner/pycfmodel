from typing import Union

from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.security_group_egress_prop import SecurityGroupEgressProp
from pycfmodel.model.resources.properties.security_group_ingress_prop import SecurityGroupIngressProp
from pycfmodel.model.resources.properties.statement import Statement
from pycfmodel.model.resources.properties.statement_condition import StatementCondition
from pycfmodel.model.resources.properties.tag import Tag

Properties = Union[
    Policy, PolicyDocument, SecurityGroupEgressProp, SecurityGroupIngressProp, Statement, StatementCondition, Tag
]
