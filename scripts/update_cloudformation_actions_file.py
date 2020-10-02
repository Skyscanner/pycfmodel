import os
import shutil
from pathlib import Path

from policy_sentry.shared.constants import BUNDLED_DATASTORE_FILE_PATH

actions_folder_path = Path(os.path.dirname(__file__)).parent / "pycfmodel" / "actions"

shutil.copy(BUNDLED_DATASTORE_FILE_PATH, actions_folder_path)
