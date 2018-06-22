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
from .resource import Resource
from .properties.security_group_ingress_prop import SecurityGroupIngressProp
from .properties.security_group_egress_prop import SecurityGroupEgressProp


class SecurityGroup(Resource):

    def __init__(self, logical_id, value):
        """
        "GroupName" : String,
        "GroupDescription" : String,
        "SecurityGroupEgress" : [ Security Group Rule, ... ],
        "SecurityGroupIngress" : [ Security Group Rule, ... ],
        "Tags" :  [ Resource Tag, ... ],
        "VpcId" : String
        """
        super().__init__(logical_id, value)

        self.group_name = None
        self.security_group_egress = []
        self.security_group_ingress = []
        self.tags = []
        self.vpc_id = None

        self._set_security_group_ingress(
            value.get("Properties", {}).get("SecurityGroupIngress"),
        )
        self._set_security_group_egress(
            value.get("Properties", {}).get("SecurityGroupEgress"),
        )
        self.set_generic_keys(
            value.get("Properties", {}),
            ["SecurityGroupIngress", "SecurityGroupEgress"],
        )

    def _set_security_group_ingress(self, sgi):
        if not sgi:
            return
        if isinstance(sgi, list):
            self.security_group_ingress = [
                SecurityGroupIngressProp(s)
                for s in sgi
            ]
            return
        elif isinstance(sgi, dict):
            self.security_group_ingress = [SecurityGroupIngressProp(sgi)]
            return

        # TODO: handle refs etc.

    def _set_security_group_egress(self, sge):
        if not sge:
            return
        if isinstance(sge, list):
            self.security_group_egress = [
                SecurityGroupEgressProp(s)
                for s in sge
            ]
            return
        elif isinstance(sge, dict):
            self.security_group_egress = [SecurityGroupEgressProp(sge)]
            return

        # TODO: handle refs etc.
