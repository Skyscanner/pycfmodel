import json
from pathlib import Path

import httpx

URL = "https://awspolicygen.s3.amazonaws.com/js/policies.js"

response = httpx.get(URL)

response.raise_for_status()

json_response = json.loads(response.text[len("app.PolicyEditorConfig=") :])


ALL_ACTIONS = set()
for service in json_response["serviceMap"].values():
    service_prefix = service["StringPrefix"]
    for action in service["Actions"]:
        ALL_ACTIONS.add(f"{service_prefix}:{action}")


cloudformation_actions_file = Path(__file__).parent.parent / "pycfmodel/cloudformation_actions.py"
cloudformation_actions_file.write_text(f"CLOUDFORMATION_ACTIONS = {sorted(ALL_ACTIONS)}")
