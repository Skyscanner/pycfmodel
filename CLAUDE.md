# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**pycfmodel** is a Python library that provides a model for parsing and working with AWS CloudFormation templates. It converts CloudFormation JSON/YAML into Python objects with helper functions for common tasks like resolving intrinsic functions, expanding IAM actions, and filtering resources.

Core functionality:
- Parse CloudFormation templates into Python objects using `parse(template)`
- Resolve CloudFormation intrinsic functions (Ref, Fn::Sub, Fn::Join, etc.) via `.resolve()`
- Expand IAM action wildcards (e.g., `s3:*` → all S3 actions) via `.expand_actions()`
- Filter resources by type using `.resources_filtered_by_type()`

## Development Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Setup
```bash
make install-dev          # Install all development dependencies
```

### Testing
```bash
make test                 # Run linting and unit tests
make unit                 # Run only unit tests
uv run pytest -svvv tests # Run tests with verbose output
uv run pytest tests/path/to/test.py::test_name  # Run a specific test
make coverage             # Run tests with coverage report
```

### Linting and Formatting
```bash
make lint                 # Run all linters (isort, black, ruff)
make format               # Format code with isort and black
```

### Dependency Management

**Important:** This is an open-source project. Always use the public PyPI repository, not internal package registries. If your uv config has a custom default index (e.g., artifactory), override it when updating the lock file:

```bash
make lock                 # Update uv.lock file
make lock-upgrade         # Upgrade all dependencies and update uv.lock

# If you have a custom default index configured, use:
uv lock --default-index https://pypi.org/simple
```

### Documentation
```bash
make install-docs         # Install documentation dependencies
make test-docs            # Build docs to verify no issues
```

### Updating AWS Actions
If `tests/test_constants.py::test_cloudformation_actions` fails:
```bash
make install-cloudformation-update  # Install dependencies for the update script
make cloudformation-update          # Fetch latest IAM actions and update the file
```
This fetches the latest IAM actions from AWS and updates `pycfmodel/cloudformation_actions.py`.

## Architecture

### Core Components

**CFModel** (`pycfmodel/model/cf_model.py`)
- Main model representing a CloudFormation template
- Contains: Parameters, Resources, Conditions, Mappings, Outputs, Metadata, etc.
- Key methods:
  - `resolve(extra_params=None)`: Resolves all intrinsic functions (Ref, Fn::Sub, Fn::Join, etc.)
  - `expand_actions()`: Expands IAM action wildcards to full action lists
  - `resources_filtered_by_type(allowed_types)`: Filters resources by type

**Resolver** (`pycfmodel/resolver.py`)
- Handles CloudFormation intrinsic function resolution
- Supports: Ref, Fn::Sub, Fn::Join, Fn::Split, Fn::Select, Fn::If, Fn::FindInMap, Fn::And, Fn::Or, Fn::Not, Fn::Equals, Fn::Base64
- Partially implemented: Fn::GetAtt, Fn::GetAZs
- Uses pseudo-parameters (AWS::AccountId, AWS::Region, etc.) with defaults that can be overridden via `extra_params`

**Action Expander** (`pycfmodel/action_expander.py`)
- Expands IAM action wildcards (e.g., `s3:Get*`, `s3:*`) to explicit action lists
- Handles both `Action` and `NotAction` in policy statements
- Uses `CLOUDFORMATION_ACTIONS` list as source of truth for known AWS actions

### Resource Models

Resource classes in `pycfmodel/model/resources/`:
- Each AWS resource type has a dedicated model (e.g., IAM roles, S3 buckets, security groups)
- All inherit from `Resource` base class
- Support for Generic resources via `GenericResource` for unknown types
- Key resource types:
  - IAM: IAMRole, IAMUser, IAMGroup, IAMPolicy, IAMManagedPolicy
  - S3: S3Bucket, S3BucketPolicy
  - Security: SecurityGroup, SecurityGroupIngress, SecurityGroupEgress
  - Networking: EC2VPCEndpointPolicy
  - WAF: WAFv2IPSet
  - Other: KMSKey, SNSTopicPolicy, SQSQueuePolicy, OpenSearchServiceDomain

### Properties

Property models in `pycfmodel/model/resources/properties/`:
- **PolicyDocument**: Represents IAM policy documents with Version and Statement list
- **Statement**: IAM policy statements with Effect, Action/NotAction, Resource/NotResource, Principal, Condition
- **StatementCondition**: Complex condition logic for policy statements (supports 50+ condition operators)
- **SecurityGroupIngressProp/SecurityGroupEgressProp**: Network rule definitions
- **Tag**: Key-value tags for resources

### Type System

The codebase uses Pydantic v2 for validation:
- All models inherit from `CustomModel` (based on Pydantic's `BaseModel`)
- `Resolvable[T]` type wrapper allows values to be either resolved or contain intrinsic functions
- Models support CloudFormation's special types (Ref, Fn::Sub, etc.) via custom validation

## Testing Patterns

- Tests are organized in `tests/` mirroring the `pycfmodel/` structure
- Resource tests in `tests/resources/` test each resource type
- Property tests in `tests/resources/properties/` test property models
- `test_resolver.py` contains extensive resolver tests for all intrinsic functions
- `test_action_expander.py` tests IAM action expansion logic
- Use `pytest-repeat` for flaky tests (e.g., `@pytest.mark.repeat(10)`)
- Tests marked with `@pytest.mark.actions` check the full IAM actions list (can be slow, skip with `-m "not actions"`)

## Code Style

- Line length: 120 characters
- Python version: 3.9+
- Formatting: Black and isort (compatible settings)
- Linting: Ruff with Pyflakes and pycodestyle rules
- Type hints are used throughout but not strictly enforced

## Key Patterns

**Adding a new resource type:**
1. Create model in `pycfmodel/model/resources/` inheriting from `Resource`
2. Add the resource class to `ResourceModels` union in `pycfmodel/model/resources/types.py`
3. Create tests in `tests/resources/`
4. Update README.md with the new resource in "Currently Supported" section

**Adding a new property type:**
1. Create model in `pycfmodel/model/resources/properties/` inheriting from `Property`
2. Reference it in the appropriate resource model
3. Add tests in `tests/resources/properties/`

**Resolver limitations:**
- `Fn::GetAtt` returns placeholder string `"GETATT"` (not fully implemented)
- `Fn::GetAZs` returns placeholder string `"GETAZS"` (not fully implemented)
- Conditions within resources are partially supported
- SSM parameter resolution requires values passed in `extra_params` or returns `UNDEFINED_PARAM_*`
