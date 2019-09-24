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
from collections import defaultdict
from typing import Dict

from .resource_factory import create_resource
from .parameter import Parameter


class CFModel:
    def __init__(self, cf_script: Dict):
        self.aws_template_format_version = cf_script.get("AWSTemplateFormatVersion")
        self.description = cf_script.get("Description")
        self.metadata = cf_script.get("Metadata")

        self._parse_parameters(cf_script.get("Parameters", {}))
        self.mappings = cf_script.get("Mappings")
        self.conditions = cf_script.get("Conditions")
        self._parse_resources(cf_script.get("Resources", {}))
        self.outputs = cf_script.get("Outputs")

    def _parse_parameters(self, template_params):
        """Parses and sets parameters in the model."""
        self.parameters = [Parameter(param_name, param_value) for param_name, param_value in template_params.items()]

    def _parse_resources(self, template_resources):
        """Parses and sets resources in the model using a factory."""
        resources = defaultdict(list)
        for res_id, res_value in template_resources.items():
            r = create_resource(res_id, res_value)
            resources[r.resource_type].append(r)
        self.resources = dict(resources)
