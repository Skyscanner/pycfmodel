import json
import os
from pathlib import Path

iam_definition_path = Path(os.path.dirname(__file__)) / "iam-definition.json"

iam_definition_data = json.loads(iam_definition_path.read_bytes())
