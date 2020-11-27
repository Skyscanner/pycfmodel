# Change Log
All notable changes to this project will be documented in this file.

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
- Added `expand_actions`, it will return a new model expading stars to get all implied actions
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
