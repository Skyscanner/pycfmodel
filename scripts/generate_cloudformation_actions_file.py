import json
from pathlib import Path

import httpx

# From AWS Policy Generator -> https://awspolicygen.s3.amazonaws.com/policygen.html
URL = "https://awspolicygen.s3.amazonaws.com/js/policies.js"
CLOUDFORMATION_ACTIONS_FILE = Path(__file__).parent.parent / "pycfmodel/cloudformation_actions.py"


def run():
    """
    This script will obtain a list of IAM actions provided in the URL from above.
    It is not the full complete set of IAM actions.
    AWS (at this moment 06-01-2022) lacks a single source of truth for this.
    For instance, s3:HeadBucket and s3:HeadObject do not appear in the list. But it is a close approach.

    This official documentation seems to hold the complete list:
    https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html
    """
    response = httpx.get(URL)
    response.raise_for_status()
    json_response = json.loads(response.text[len("app.PolicyEditorConfig=") :])

    all_actions = set()
    for service in json_response["serviceMap"].values():
        service_prefix = service["StringPrefix"]
        for action in service["Actions"]:
            all_actions.add(f"{service_prefix}:{action}")

    body = ",\n".join(f'    "{entry}"' for entry in sorted(all_actions))

    CLOUDFORMATION_ACTIONS_FILE.write_text(f"CLOUDFORMATION_ACTIONS = [\n{body},\n]\n")


if __name__ == "__main__":
    run()
