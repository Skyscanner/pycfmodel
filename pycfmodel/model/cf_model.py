"""
Copyright 2018-2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from deprecation import deprecated

from .intrinsic_function_resolver import IntrinsicFunctionResolver
from .parameter import Parameter
from .resource_factory import ResourceFactory


class CFModel(object):

    def __init__(self, cf_script):
        self.aws_template_format_version = cf_script.get("AWSTemplateFormatVersion")
        self.description = cf_script.get("Description")
        self.metadata = cf_script.get("Metadata")

        self.default_parameters = self._parse_parameters(cf_script.get("Parameters", {}))
        self.mappings = cf_script.get("Mappings")
        self.conditions = cf_script.get("Conditions")
        self.resources = self._parse_resources(cf_script.get("Resources", {}))
        self.outputs = cf_script.get("Outputs")

        self.computed_parameters = {}
        self.computed_conditions = {}

        self.resolve()

    def _parse_parameters(self, template_params):
        """Parses and sets parameters in the model."""
        return {
            param_name: Parameter(param_name, param_value)
            for param_name, param_value in template_params.items()
        }

    def _parse_resources(self, template_resources):
        """Parses and sets resources in the model using a factory."""
        resources = {}
        resource_factory = ResourceFactory()
        for res_id, res_value in template_resources.items():
            r = resource_factory.create_resource(res_id, res_value)
            if r:
                if r.resource_type in resources:
                    resources[r.resource_type].append(r)
                else:
                    resources[r.resource_type] = [r]
        return resources

    @deprecated(deprecated_in="0.4.0", details="Use has_identifiers_with / has_wildcard_identifiers")
    @property
    def parameters(self):
        return self.default_parameters.values()

    def resolve(self, custom_pseudo_parameters={}, import_values={}, custom_parameters={}):
        self.computed_parameters = {
            # default pseudo parameters
            **{
                "AWS::AccountId": "123456789012",
                "AWS::NotificationARNs": [],
                "AWS::NoValue": None,
                "AWS::Partition": "aws",
                "AWS::Region": "eu-west-1",
                "AWS::StackId": "",
                "AWS::StackName": "",
                "AWS::URLSuffix": "amazonaws.com",
            },
            # default parameters
            **{
                key: parameter.default
                for key, parameter in self.default_parameters.items()
                if parameter.default
            },
            **custom_pseudo_parameters,
            **import_values,
            **custom_parameters,
        }

        intrinsic_function_resolver = IntrinsicFunctionResolver(self.computed_parameters, self.mappings)
        for resource_type in self.resources.values():
            for resource in resource_type:
                resource.resolve(intrinsic_function_resolver)
