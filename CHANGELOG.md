# Change Log
All notable changes to this project will be documented in this file.

## 0.22.0
### Fixes
- KeyPolicy made optional for KMS Key resource type.

## 0.21.2
### Fixes
- Add the BypassPolicyLockoutSafetyCheck and Origin fields in the KMS resource
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.21.1
### Fixes
- Documentation building.
### Updates
- Update `CLOUDFORMATION_ACTIONS`.
- Actions versions.
- ReadMe badges.

## 0.21.0
### Fixes
- Fix resolving conditions recursively [#114](https://github.com/Skyscanner/pycfmodel/pull/114)
### Enhancements
- Compatible with Python3.11 [#110](https://github.com/Skyscanner/pycfmodel/pull/110)
- Compatible with Python3.12 [#115](https://github.com/Skyscanner/pycfmodel/pull/115)
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.20.3
### Fixes
- Fix resolver find_in_map for maps with bool values. [#112](https://github.com/Skyscanner/pycfmodel/pull/112)
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.20.2
### Fixes
- Fix model for IAM Role which was missing `Description` and `Tags`.
- Fix README.md tabs on list of available models.
### Updates
- Update `CLOUDFORMATION_ACTIONS`.
- Updated tests accordingly for IAM Role

## 0.20.1
### Fixes
- Fix docs that were failing to get updated/generated
### Improvements
- Add tests for docs so they don't get outdated
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.20.0
### Additions
- New `RDSDBSecurityGroup` and `RDSDBSecurityGroupIngress` resources [#103]
### Improvements
- IAM Role is able to return its `AssumeRolePolicyDocument` as a list of `OptionallyNamedPolicyDocument`. [#102](https://github.com/Skyscanner/pycfmodel/pull/102)
### Updates
- Compatible with Python3.10 [#100](https://github.com/Skyscanner/pycfmodel/pull/100)
- Update `CLOUDFORMATION_ACTIONS`.

## 0.19.1
### Fixes
- `Effect` on `Statement` is **required**. [#101](https://github.com/Skyscanner/pycfmodel/pull/97)
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.19.0
### Improvements
- Able to parse PolicyDocument that are implicit in string properties. [#97](https://github.com/Skyscanner/pycfmodel/pull/97)

## 0.18.2
### Fixes
- Fix obtaining `policy_documents` for resources without properties. [#98](https://github.com/Skyscanner/pycfmodel/pull/96)
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.18.1
### Fixes
- `Properties` can now be optional for Generic. See [PR #96](https://github.com/Skyscanner/pycfmodel/pull/96)
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.18.0 - [2022-04-01]
### Fixes
- Removes `smart_union` flag from Generic. See [PR #95](https://github.com/Skyscanner/pycfmodel/pull/95)

## 0.17.1 - [2022-03-02]
### Additions
- Add `assume_role_statement_conditions` property for `IAMRole` to include statements on `AssumeRolePolicyDocuments`.
- Update `CLOUDFORMATION_ACTIONS`.

## 0.17.0 - [2022-03-02]
### Additions
- `KMSKey` to use default `policy_documents` property instead of returning an empty list.
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.16.3 - [2022-02-24]
### Fixes
- Fix `resolve` for `bool`s that can be `str` such as `"true"` or `"false"` or similar, by making `ResolvableBool` to be resolvable to `SemiStrictBool`.
### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.16.2 - [2022-02-16]
### Fixes
- `resolve` was converting to string booleans, this is incompatible since 0.14.0 because bool were converted to StrictBooleans.

### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.16.1 - [2022-02-16]
### Fixes
- AWS KMS Key policies can contain an `Id` field in a `PolicyDocument`. The model for `PolicyDocument` has been updated accordingly to support this.

### Updates
- Update `CLOUDFORMATION_ACTIONS`.

## 0.16.0 - [2022-02-11]
### Additions
- Added `all_statement_conditions` property to `Resource`. This enables a list of all IAM Conditions defined in a Resource to be captured and used.

## 0.15.0 - [2022-02-10]
### Additions
- `Resource` class is able to run `policy_documents` when it's not a mapped resource and return a valid list of `OptionallyNamedPolicyDocument`.
- Update `CLOUDFORMATION_ACTIONS`.

## 0.14.0 - [2022-02-03]
### Additions
- Added `Principal` property.
- Modified `Statement` property to work with `Principal` property
- Added `Generic` property. Any property under this class will be cast to an existing model of `pycfmodel` if possible.
- Modified `GenericResource`, `ESDomainProperties`, `OpenSearchDomainProperties` and `S3BucketProperties` to work with `Generic` property
- Update `CLOUDFORMATION_ACTIONS`

## 0.13.0 - [2022-01-14]
### Additions
- Added `ESDomain` resource.
- Added `OpenSearchDomain` resource.
- Update `CLOUDFORMATION_ACTIONS`

## 0.12.0 - [2022-01-13]
### Fixes
- `Transform` field of a CloudFormation template can now correctly handle both string and list of strings (see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-section-structure.html)
- Support the usage of `aws:sourceVpce` in `IpAddress` conditions. When comparing conditions however, `pycfmodel` will block any comparison with something that is not an IPv4 or IPv6 address.

### Additions
- Update `CLOUDFORMATION_ACTIONS`.

## 0.11.1 - [2022-01-10]
### Additions
- Update `CLOUDFORMATION_ACTIONS`.
- Add documentation regarding missing IAM actions.

## 0.11.0 - [2021-09-21]
### Additions
- Add `S3Bucket` resource.
- Add `Tags` property for any usage of resource tagging.

## 0.10.4 - [2021-08-13]
### Fixes
- Update `CLOUDFORMATION_ACTIONS`
- Add `MultiRegion` and `KeySpec` properties in `KMSKeyProperties`

## 0.10.3 - [2021-08-12]
### Fixes
- Update condition handling for `IpAddress` to handle `IPv*Network` comparison with `subnet_of` method.

## 0.10.2 - [2021-08-05]
### Fixes
- Update evaluators on Conditions when `arg_b` is of type List, to match AWS sema\ntics.
- Update `IPv4Network` and `IPv6Network` to not be strict when parsing strings.  
  Before:
  ```
  A ValueError is raised if address does not represent a valid IPv4 or IPv6 address, or if the network has host bits set.
  ```
  After:
  ```
  A ValueError is raised if address does not represent a valid IPv4 or IPv6 address.
  ```

## 0.10.1 - [2021-07-23]
### Fixes
- Fix bug when calling `resolve` on `CFModel` with default (empty dict) `Conditions`

## 0.10.0 - [2021-06-14]
### Additions
- Resolver able to handle AWS SSM values in templates.
### Fixes
- Update `CLOUDFORMATION_ACTIONS`

## 0.9.1 - [2021-05-06]
### Fixes
- Update `CLOUDFORMATION_ACTIONS`
- `StatementCondition` only builds evaluator if `eval` is called.

## 0.9.0 - [2021-05-05]
### Improvements
- Add `StatementCondition` class, with a function resolver as a replacement for `ConditionDict`.
### Removes
- Removes constants `CONDITION_MODIFIERS` and `CONDITION_FUNCTIONS` from `pycfmodel/constants.py`
- Removes `is_conditional_dict` from `pycfmodel/utils.py`
### Fixes
- Update `CLOUDFORMATION_ACTIONS`
- Change Metadata dict values to accept any type.  

## 0.8.4 - [2021-04-27]
### Fixes
- Fix to ensure all `Statement.Effect` fields are always capitalized
- Update `CLOUDFORMATION_ACTIONS`

## 0.8.3 - [2021-02-15]
### Fixes
- Fix to `policy_documents` method on `EC2 VPC Endpoint` resource type for when no policy document is added to the resource.

## 0.8.2 - [2021-02-11]
### Additions
- Add `EC2 VPC Endpoint Policy` resource.
### Changes
- Update list of all CloudFormation actions.

## 0.8.1 - [2020-11-27]
### Additions
- New property `policy_documents` to Resources
- New `model.utils` module
- New helper dataclass: `model.utils.OptionallyNamedPolicyDocument`
### Improvements
- Added basic tests for the resources that didn't have
### Changes
- `_build_regex` moved to `utils` and renamed to `regex_from_cf_string`
### Fixes
- Fixed IAMGroup model


## 0.8.0 - [2020-11-23]
### Additions
- New function `pycfmodel.model.resources.properties.policy_document.PolicyDocument.get_allowed_actions`
### Improvements
- Improve action expansion to support `NotAction`
- Improve Cloudformation action file generator
- Update Cloudformation actions to latest
- Improved tests
- New optional parameters added to `pycfmodel.model.resources.properties.statement.Statement.get_action_list`
- New optional parameters added to `pycfmodel.action_expander._expand_action`
- New optional parameters added to `pycfmodel.action_expander._expand_actions`
### Fixes
- Fix isort testing issue


## 0.7.2 - [2020-09-01]
### Improvements
- Added all cloudformation actions file (script to generate them and test to check for new actions)
- Added `expand_actions`, it will return a new model expanding stars to get all implied actions
- Added `get_expanded_action_list` to Statement to get all implied actions


## 0.7.1 - [2020-04-06]
### Improvements
- Refactor `SecurityGroupIngress`, `SecurityGroupEgress`, `SecurityGroupIngressProp` and `SecurityGroupEgressProp`.
- `SecurityGroupEgress` also supports `ipv4_slash_zero` and `ipv6_slash_zero`.


## 0.7.0 - [2020-03-25]
### Improvements
- `CidrIp` and `CidrIpv6` properties of Security Group ingress and egress now use type `IPv4Network` and `IPv6Network` respectively.
- This has led to modified `ipv4_slash_zero` and `ipv6_slash_zero` functions.


## 0.6.4 - [2020-02-27]
### Fixes
- Allow multiple operands in `or` and `and` functions. 


## 0.6.3 - [2020-01-08]
### Added
- Added support for `Rules` section in template
- Added tests for `allowed_principals_with` and `non_whitelisted_allowed_principals`
### Fixes
- Fix types in `allowed_principals_with`, `non_whitelisted_allowed_principals` and `PSEUDO_PARAMETERS`.


## 0.6.2 - [2019-12-20]
### Improvements
- Added the `resources_filtered_by_type` function in `CFModel` class


## 0.6.1 - [2019-12-09]
### Fixes
- Fix CloudFormation conditions which were logically boolean to now successfully be evaluated as boolean.


## 0.6.0 - [2019-11-25]
### Improvements
- Improve equal function

### Breaking Changes
- Resolver now returns strings for most primitives


## 0.5.1 - [2019-11-25]
### Improvements
- Add `NO_ECHO_WITH_VALUE` param value


## 0.5.0

### Improvements
- Implements pydantic for all classes.
- Change the template parser, now it uses pydantic.
- Adds a resolve method to process cloudformation intrinsic functions.
- Adds lots of tests
### Breaking changes
- API has been rewritten from scratch.
