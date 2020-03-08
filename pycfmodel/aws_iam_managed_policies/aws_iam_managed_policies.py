"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import boto3

from pathlib import Path

from pycfmodel.constants import REGEX_AWS_MANAGED_ARN
from pycfmodel.model.resources.iam_managed_policy import IAMManagedPolicy

client = boto3.client("iam")
destination_folder = Path(__file__).parent

for response in client.get_paginator("list_policies").paginate(Scope="AWS"):
    for policy in response["Policies"]:
        policy_version_response = client.get_policy_version(
            PolicyArn=policy["Arn"], VersionId=policy["DefaultVersionId"]
        )
        print(f"Dumping {policy['Arn']}")
        destination_file = destination_folder / (REGEX_AWS_MANAGED_ARN.match(policy["Arn"]).group(1) + ".json")
        destination_file.parent.mkdir(parents=True, exist_ok=True)
        destination_file.write_text(
            IAMManagedPolicy(
                **{
                    "Arn": policy["Arn"],
                    "Properties": {
                        "ManagedPolicyName": policy["PolicyName"],
                        "Path": policy_version_response["PolicyVersion"]["Path"],
                        "PolicyDocument": policy_version_response["PolicyVersion"]["Document"],
                    },
                }
            ).json()
        )
