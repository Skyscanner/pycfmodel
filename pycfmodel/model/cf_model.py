import logging
from datetime import date
from typing import Any, ClassVar, Collection, Dict, List, Optional, Type, Union

from pydantic import Field, model_validator
from typing_extensions import Annotated

from pycfmodel.action_expander import expand_actions
from pycfmodel.constants import AWS_NOVALUE
from pycfmodel.model.base import CustomModel
from pycfmodel.model.parameter import Parameter
from pycfmodel.model.resources.dynamic_resource import get_or_create_dynamic_model, is_dynamic_generation_enabled
from pycfmodel.model.resources.generic_resource import GenericResource
from pycfmodel.model.resources.resource import Resource
from pycfmodel.model.resources.types import ResourceModels
from pycfmodel.model.types import Resolvable
from pycfmodel.resolver import _extended_bool, resolve

logger = logging.getLogger(__name__)

AllResourcesType = Annotated[Union[ResourceModels, GenericResource], Field(union_mode="left_to_right")]


class CFModel(CustomModel):
    """
    Template that describes AWS infrastructure.

    Properties:

    - AWSTemplateFormatVersion
    - Conditions: Conditions that control behaviour of the template.
    - Description: Description for the template.
    - Mappings: A 3 level mapping of keys and associated values.
    - Metadata: Additional information about the template.
    - Outputs: Output values of the template.
    - Parameters: Parameters to the template.
    - Resources: Stack resources and their properties.
    - Rules
    - Transform: For serverless applications, specifies the version of the AWS Serverless Application Model (AWS SAM) to use.

    More info at [AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)
    """

    AWSTemplateFormatVersion: Optional[date] = None
    Conditions: Optional[Dict] = {}
    Description: Optional[str] = None
    Mappings: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = {}
    Metadata: Optional[Dict[str, Any]] = None
    Outputs: Optional[Dict[str, Dict[str, Union[str, Dict]]]] = {}
    Parameters: Optional[Dict[str, Parameter]] = {}
    Resources: Dict[str, Resolvable[AllResourcesType]] = {}
    Rules: Optional[Dict] = {}
    Transform: Optional[Union[str, List[str]]] = None

    @model_validator(mode="wrap")
    @classmethod
    def _parse_resources_with_dynamic_generation(cls, data: Any, handler) -> "CFModel":
        """
        Parse resources using dynamic model generation when enabled.

        This model validator pre-processes resources to use dynamically generated models
        for resource types that are not explicitly modeled in pycfmodel.
        """
        if not isinstance(data, dict):
            return handler(data)

        resources = data.get("Resources")
        if not resources or not isinstance(resources, dict):
            return handler(data)

        if not is_dynamic_generation_enabled():
            return handler(data)

        # Get the set of explicitly modeled resource types
        existing_resource_types = {
            klass.model_fields["Type"].annotation.__args__[0] for klass in ResourceModels.__args__[0].__args__
        }

        # Store dynamic resources to inject after normal parsing
        dynamic_resources = {}
        remaining_resources = {}

        for resource_name, resource_data in resources.items():
            # If it's already a Resource instance, keep it
            if isinstance(resource_data, Resource):
                dynamic_resources[resource_name] = resource_data
                continue

            # If it's not a dict, pass through
            if not isinstance(resource_data, dict):
                remaining_resources[resource_name] = resource_data
                continue

            resource_type = resource_data.get("Type")

            # If it's an explicitly modeled type, let normal Pydantic parsing handle it
            if resource_type in existing_resource_types:
                remaining_resources[resource_name] = resource_data
                continue

            # Try dynamic generation for unmodeled types
            dynamic_model = get_or_create_dynamic_model(resource_type)
            if dynamic_model is not None:
                try:
                    parsed_instance = dynamic_model.model_validate(resource_data)
                    dynamic_resources[resource_name] = parsed_instance
                    continue
                except Exception as e:
                    logger.debug(f"Failed to parse {resource_type} with dynamic model: {e}")

            # Fall back to normal parsing (will use GenericResource)
            remaining_resources[resource_name] = resource_data

        # Create a modified data dict with only the remaining resources
        modified_data = dict(data)
        modified_data["Resources"] = remaining_resources

        # Let the default handler parse the remaining data
        model = handler(modified_data)

        # Merge dynamic resources into the parsed model
        if dynamic_resources:
            model.Resources.update(dynamic_resources)

        return model

    PSEUDO_PARAMETERS: ClassVar[Dict[str, Union[str, List[str]]]] = {
        # default pseudo parameters
        "AWS::AccountId": "123456789012",
        "AWS::NotificationARNs": [],
        "AWS::NoValue": AWS_NOVALUE,
        "AWS::Partition": "aws",
        "AWS::Region": "eu-west-1",
        "AWS::StackId": "",
        "AWS::StackName": "",
        "AWS::URLSuffix": "amazonaws.com",
    }

    def resolve(self, extra_params=None) -> "CFModel":
        """
        Resolve all intrinsic functions on the template.

        Arguments:
            extra_params: Values of parameters passed to the Cloudformation.

        Returns:
            A new CFModel.
        """
        extra_params = {} if extra_params is None else extra_params
        # default parameters
        params = {}
        for key, parameter in self.Parameters.items():
            passed_value = extra_params.pop(key, None)
            ref_value = parameter.get_ref_value(passed_value)
            if ref_value is not None:
                params[key] = ref_value

        extended_parameters = {**self.PSEUDO_PARAMETERS, **params, **extra_params}
        dict_value = self.model_dump()

        conditions = dict_value.pop("Conditions", {})
        resolved_conditions = {}
        for key, value in conditions.items():
            resolved_conditions.update(
                {key: _extended_bool(resolve(value, extended_parameters, self.Mappings, resolved_conditions))}
            )

        resources = dict_value.pop("Resources")
        resolved_resources = {
            key: resolve(value, extended_parameters, self.Mappings, resolved_conditions)
            for key, value in resources.items()
            if value.get("Condition") is None
            or (value.get("Condition") is not None and resolved_conditions.get(value["Condition"], True))
        }
        return CFModel(**dict_value, Conditions=resolved_conditions, Resources=resolved_resources)

    def expand_actions(self) -> "CFModel":
        """
        Returns a model which has expanded all wildcards (`*`) to get all implied actions for every resource.
        For example:\n
          - a model containing `s3:*` will be expanded to list all the possible S3 actions.
          - a model containing `s3:Get*` will be expanded to all the `Get*` actions only.

        This method can handle the cases of both `Action` and `NotAction`.

        [Known AWS Actions](https://github.com/Skyscanner/pycfmodel/blob/master/pycfmodel/cloudformation_actions.py).
        These known actions can be updated by executing:

        ```
        python3 scripts/generate_cloudformation_actions_file.py
        ```
        """
        dict_value = self.model_dump()

        resources = dict_value.pop("Resources")
        expanded_resources = {key: expand_actions(value) for key, value in resources.items()}

        return CFModel(**dict_value, Resources=expanded_resources)

    def resources_filtered_by_type(
        self, allowed_types: Collection[Union[str, Type[Resource]]]
    ) -> Dict[str, Dict[str, Resource]]:
        """
        Filtered resources based on types.

        Arguments:
            allowed_types: Collection of desired types.

        Returns:
            Dictionary where key is the logical id and value is the resource.
        """
        result = {}
        allowed_resource_classes = tuple(x for x in allowed_types if isinstance(x, type))
        for resource_name, resource in self.Resources.items():
            if isinstance(resource, allowed_resource_classes) or resource.Type in allowed_types:
                result[resource_name] = resource
        return result
