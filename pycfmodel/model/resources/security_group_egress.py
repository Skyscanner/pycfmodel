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
from .resource import Resource


class SecurityGroupEgress(Resource):
    def __init__(self, logical_id, value):
        """
        "CidrIp" : String,
        "CidrIpv6" : String,
        "Description" : String,
        "DestinationPrefixListId" : String,
        "DestinationSecurityGroupId" : String,
        "FromPort" : Integer,
        "GroupId" : String,
        "IpProtocol" : String,
        "ToPort" : Integer
        """
        super().__init__(logical_id, value)

        self.cidr_ip = None
        self.cidr_ipv6 = None
        self.description = None
        self.destination_prefix_list_id = None
        self.destination_security_group_id = None
        self.from_port = None
        self.group_id = None
        self.ip_protocol = None
        self.to_port = None

        self.set_generic_keys(value.get("Properties", {}), [])

    def ipv4_slash_zero(self) -> bool:
        if not self.cidr_ip or not isinstance(self.cidr_ip, str):
            return False
        return self.cidr_ip.endswith("/0")

    def ipv6_slash_zero(self) -> bool:
        if not self.cidr_ipv6 or not isinstance(self.cidr_ipv6, str):
            return False
        return self.cidr_ipv6.endswith("/0")
