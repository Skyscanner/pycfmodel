"""
Copyright 2018 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from pycfmodel.model.intrinsic_function_resolver import IntrinsicFunctionResolver
from .parameter import Parameter
from .condition import Condition
from .resource_factory import ResourceFactory


class CFModel(object):

    def __init__(self, cf_script):
        self.aws_template_format_version = cf_script.get("AWSTemplateFormatVersion")
        self.description = cf_script.get("Description")
        self.metadata = cf_script.get("Metadata")

        self.default_parameters = self._parse_parameters(cf_script.get("Parameters", {}))
        self.mappings = cf_script.get("Mappings")
        self.conditions = self._parse_conditions(cf_script.get("Conditions", {}))
        self.resources = self._parse_resources(cf_script.get("Resources", {}))
        self.outputs = self._parse_outputs(cf_script.get("Outputs", {}))

        self.resolve()

    def _parse_parameters(self, template_params):
        """Parses and sets parameters in the model."""
        parameters = {
            # Default pseudo parameters
            "AWS::AccountId": Parameter("AWS::AccountId", "123456789012"),
            "AWS::NotificationARNs": Parameter("AWS::NotificationARNs", []),
            "AWS::NoValue": Parameter("AWS::NoValue", None),
            "AWS::Partition": Parameter("AWS::Partition", "aws"),
            "AWS::Region": Parameter("AWS::Region", "eu-west-1"),
            "AWS::StackId": Parameter("AWS::StackId", ""),
            "AWS::StackName": Parameter("AWS::StackName", ""),
            "AWS::URLSuffix": Parameter("AWS::URLSuffix", "amazonaws.com"),
        }

        for param_name, param_value in template_params.items():
            parameters[param_name] = Parameter(param_name, param_value)

        return parameters

    def _parse_conditions(self, template_conditions):
        conditions = {}
        for condition_name, condition_value in template_conditions.items():
            conditions[condition_name] = Condition(condition_name, condition_value)
        return conditions

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

    def _parse_outputs(self, template_outputs):
        outputs = {}
        for output_name, output_value in template_outputs.items():
            outputs[output_name] = Condition(output_name, output_value)
        return outputs

    def resolve(self, custom_pseudo_parameters={}, custom_parameters={}, import_values={}):
        params = {
            **self.default_parameters,
            **custom_pseudo_parameters,
            **import_values,
            **custom_parameters,
        }

        intrinsic_function_resolver = IntrinsicFunctionResolver(params, self.mappings)
        for resource in self.resources:
            intrinsic_function_resolver.resolve(function)
