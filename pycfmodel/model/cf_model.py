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
from .parameter import Parameter
from .resource_factory import ResourceFactory


class CFModel(object):

    def __init__(self, cf_script):
        self.aws_template_format_version = cf_script.get("AWSTemplateFormatVersion")
        self.description = cf_script.get("Description")
        self.metadata = cf_script.get("Metadata")
        self.mappings = cf_script.get("Mappings")
        self.conditions = cf_script.get("Conditions")
        self.outputs = cf_script.get("Outputs")

        self.parse_parameters(cf_script.get("Parameters", {}))
        self.parse_resources(cf_script.get("Resources", {}))

    def parse_parameters(self, parameters):
        """Parses and sets parameters in the model."""

        self.parameters = []
        for param_name, param_value in parameters.items():
            p = Parameter(param_name, param_value)
            if p:
                self.parameters.append(p)

    def parse_resources(self, resources):
        """Parses and sets resources in the model using a factory."""

        self.resources = {}
        resource_factory = ResourceFactory()
        for res_id, res_value in resources.items():
            r = resource_factory.create_resource(res_id, res_value)
            if r:
                if r.resource_type in self.resources:
                    self.resources[r.resource_type].append(r)
                else:
                    self.resources[r.resource_type] = [r]
