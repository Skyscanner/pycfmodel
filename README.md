# pycfmodel
[![Build Status](https://travis-ci.org/Skyscanner/pycfmodel.svg?branch=master)](https://travis-ci.org/Skyscanner/pycfmodel)
*A python model for Cloud Formation scripts.*

**pycfmodel** makes it easier to work with CloudFormation scripts in Python by
creating a model comprised of python objects. Objects have various helper
functions which help with performing common tasks related to parsing and
inspecting CloudFormation scripts.

`pip install pycfmodel`

## Currently Supported Models
* parameters
* resources
    * Generic Resource
    * IAM Group
    * IAM Managed Policy
    * IAM role
    * S3 Bucket Policy
    * Security Group Egress
    * Security Group Ingress
    * Security Group
    * SNS Topic Policy
    * SQS Queue Policy
* properties
    * Policy Document
    * Policy
    * Principal
    * Security Group Egress Property
    * Security Group Ingress Property
    * Statement

## Example
```python
import pycfmodel

template = {
  "Resources": {
    "S3Bucket" : {
      "Type" : "AWS::S3::Bucket",
      "Properties" : {
        "BucketName" : "fakebucketfakebucket"
      }
    },

    "S3BucketPolicyWithNotAction": {
      "Type": "AWS::S3::BucketPolicy",
      "Properties": {
        "Bucket": {
          "Ref": "S3Bucket"
        },
        "PolicyDocument": {
          "Statement": [
            {
              "Action": [
                "s3:*"
              ],
              "Effect": "Allow",
              "Resource": "arn:aws:s3:::fakebucketfakebucket/*",
              "Principal": {
                "AWS": "*"
              }
            }
          ]
        }
      }
    }
  }
}

parsed_cf = pycfmodel.parse(template)
for resource in parsed_cf.resources.get("AWS::S3::BucketPolicy", []):
    if resource.policy_document.wildcard_allowed_actions(pattern=r"^(\w*:){0,1}\*$"):
        print(resource.logical_id)
```
## Local Development Commands
```
make install-dev
make coverage
make test
make freeze
```
