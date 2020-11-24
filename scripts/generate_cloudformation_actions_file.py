import json
from pathlib import Path

import httpx

URL = "https://awspolicygen.s3.amazonaws.com/js/policies.js"
CLOUDFORMATION_ACTIONS_FILE = Path(__file__).parent.parent / "pycfmodel/cloudformation_actions.py"


def run():
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
