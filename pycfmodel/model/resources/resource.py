from typing import Any, ClassVar, Dict, List, Optional

from pycfmodel.model.base import CustomModel
from pycfmodel.model.generic import Generic
from pycfmodel.model.parameter import Parameter
from pycfmodel.model.resources.properties.policy import Policy
from pycfmodel.model.resources.properties.policy_document import PolicyDocument
from pycfmodel.model.resources.properties.statement_condition import StatementCondition
from pycfmodel.model.types import ResolvableCondition, ResolvableStr, ResolvableStrOrList
from pycfmodel.model.utils import OptionallyNamedPolicyDocument


class Resource(CustomModel):
    TYPE_VALUE: ClassVar[str]
    Type: str
    Condition: Optional[ResolvableCondition] = None
    CreatePolicy: Optional[Dict] = None
    DeletionPolicy: Optional[ResolvableStr] = None
    DependsOn: Optional[ResolvableStrOrList] = None
    Metadata: Optional[Dict] = None
    UpdatePolicy: Optional[Dict] = None
    UpdateReplacePolicy: Optional[ResolvableStr] = None

    def has_hardcoded_credentials(self) -> bool:
        if not self.Metadata or not self.Metadata.get("AWS::CloudFormation::Authentication"):
            return False

        for auth in self.Metadata["AWS::CloudFormation::Authentication"].values():
            if not all(
                [
                    auth.get("accessKeyId", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("password", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                    auth.get("secretKey", Parameter.NO_ECHO_NO_DEFAULT) == Parameter.NO_ECHO_NO_DEFAULT,
                ]
            ):
                return True

        return False

    @property
    def policy_documents(self) -> List[OptionallyNamedPolicyDocument]:
        """
        Returns a list with all the optionally named policy documents in this resource within its properties.
        Every resource has a Properties field, if not, it's a malformed CloudFormation template.
        """
        policy_documents = []

        if self.Properties is None:
            return policy_documents

        properties_list = []
        for field in self.Properties.model_fields_set:
            properties_list.append(getattr(self.Properties, field))

        self.obtain_policy_documents(policy_documents=policy_documents, properties=properties_list)
        return policy_documents

    def obtain_policy_documents(self, policy_documents: List, properties: List[Any]):
        """
        Obtains recursively all the optionally named policy documents within a given list of properties.
        """
        for property_type in properties:
            if isinstance(property_type, PolicyDocument):
                policy_documents.append(OptionallyNamedPolicyDocument(policy_document=property_type, name=None))
            elif isinstance(property_type, Policy):
                policy_documents.append(
                    OptionallyNamedPolicyDocument(
                        name=property_type.PolicyName, policy_document=property_type.PolicyDocument
                    )
                )
            elif isinstance(property_type, OptionallyNamedPolicyDocument):
                policy_documents.append(property_type)
            elif isinstance(property_type, list):
                self.obtain_policy_documents(policy_documents=policy_documents, properties=property_type)
            elif isinstance(property_type, Generic):
                properties_list = []
                for field in property_type.model_fields_set:
                    properties_list.append(getattr(property_type, field))

                self.obtain_policy_documents(policy_documents=policy_documents, properties=properties_list)

    @property
    def all_statement_conditions(self) -> List[StatementCondition]:
        conditions = []
        for pd in self.policy_documents:
            pd_statements = pd.policy_document.statement_as_list()
            for statement in pd_statements:
                if statement.Condition:
                    conditions.append(statement.Condition)
        return conditions
