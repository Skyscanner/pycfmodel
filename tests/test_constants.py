import json

import httpx
import pytest

from pycfmodel.cloudformation_actions import CLOUDFORMATION_ACTIONS


@pytest.mark.actions
def test_cloudformation_actions():
    response = httpx.get("https://awspolicygen.s3.amazonaws.com/js/policies.js")
    response.raise_for_status()
    json_response = json.loads(response.text[len("app.PolicyEditorConfig=") :])

    ALL_ACTIONS = set()
    for service in json_response["serviceMap"].values():
        service_prefix = service["StringPrefix"]
        for action in service["Actions"]:
            ALL_ACTIONS.add(f"{service_prefix}:{action}")

    assert ALL_ACTIONS == set(CLOUDFORMATION_ACTIONS)
