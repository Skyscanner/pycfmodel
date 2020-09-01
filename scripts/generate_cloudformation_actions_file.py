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


with open(Path(__file__).parent.parent / "pycfmodel/artifacts/cloudformation_actions.json", "w") as json_file:
    json.dump(sorted(ALL_ACTIONS), json_file)
