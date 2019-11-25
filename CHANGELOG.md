# Change Log
All notable changes to this project will be documented in this file.

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