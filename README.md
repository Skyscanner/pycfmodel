# pycfmodel

![Build Status](https://github.com/Skyscanner/pycfmodel/workflows/PyPI%20release/badge.svg)
[![PyPI version](https://badge.fury.io/py/pycfmodel.svg)](https://badge.fury.io/py/pycfmodel)
[![Documentation Status](https://readthedocs.org/projects/pycfmodel/badge/?version=latest)](https://pycfmodel.readthedocs.io/en/latest/?badge=latest)
![License](https://img.shields.io/github/license/skyscanner/pycfmodel)

*A python model for Cloud Formation scripts.*

**pycfmodel** makes it easier to work with CloudFormation scripts in Python by
creating a model comprised of python objects. Objects have various helper
functions which help with performing common tasks related to parsing and
inspecting CloudFormation scripts.

`pip install pycfmodel`

## Currently Supported

* AWSTemplateFormatVersion
* Conditions
* Description
* Mappings
* Metadata
* Outputs
* Parameters
* Resources:
    * Properties:
        * Policy
        * Policy Document
        * Principal
        * Security Group Egress Prop
        * Security Group Ingress Prop
        * Statement
        * Tag
    * EC2 VPC Endpoint Policy
    * Generic Resource
    * IAM Group
    * IAM Managed Policy
    * IAM Policy
    * IAM Role
    * IAM User
    * KMS Key
    * OpenSearch Service (legacy ElasticSearch resource)
        * Elasticsearch Domain
    * OpenSearch Service
        * OpenSearchService Domain
    * S3 Bucket
    * S3 Bucket Policy
    * Security Group
    * Security Group Egress
    * Security Group Ingress
    * SNS Topic Policy
    * SQS Queue Policy
* Transform

## Example

```python
from pycfmodel import parse

template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {"StarParameter": {"Type": "String", "Default": "*", "Description": "Star Param"}},
    "Resources": {
        "rootRole": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": {"Fn::Sub": "arn:aws:iam::${AWS::AccountId}:root"}},
                            "Action": ["sts:AssumeRole"],
                        }
                    ],
                },
                "Path": "/",
                "Policies": [
                    {
                        "PolicyName": "root",
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Action": {"Ref": "StarParameter"},
                                    "Resource": {"Ref": "StarParameter"},
                                }
                            ],
                        },
                    }
                ],
            },
        }
    },
}

model = parse(template).resolve(extra_params={"AWS::AccountId": "123"})
rootRole = model.Resources["rootRole"]
policy = rootRole.Properties.Policies[0]
statement = policy.PolicyDocument.Statement[0]

assert statement.Action == "*"
assert statement.Resource == "*"
assert rootRole.Properties.AssumeRolePolicyDocument.Statement[0].Principal == {"AWS": "arn:aws:iam::123:root"}
```

## Local Development Commands

```bash
make install-dev
make coverage
make test
make freeze
```

If the test `tests/test_constants.py::test_cloudformation_actions` is failing, it can be resolved by updating the known
AWS Actions:

```bash
python3 scripts/generate_cloudformation_actions_file.py
```
