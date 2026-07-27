# =========================
# Dependencies
# =========================

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if PROJECT_ROOT.name == "jobs":
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_extract import extract_data
from data_transform import transform_data
from data_load import load_data
from lib import config as the_config
from lib import utils as the_utils

# =========================
# Configurations
# =========================

# Paths
for path in the_config.PATHS:
    the_utils.ensure_path(path)

# =========================
# Pipeline
# =========================

def run_pipeline() -> None:

    the_config.refresh_logging()
    stations = extract_data()
    new_data = transform_data(stations, verbose=False)
    load_data(new_data)

if __name__ == "__main__":
    run_pipeline()

# -------------------------
