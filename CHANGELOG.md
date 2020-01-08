# Change Log
All notable changes to this project will be documented in this file.

## 0.6.3 - [2020-XX-XX]
### Added
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
