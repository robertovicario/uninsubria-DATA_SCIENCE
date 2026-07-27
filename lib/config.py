# =========================
# Dependencies
# =========================

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json

# =========================
# Configurations
# =========================

# Web Scraping
N_RETRY = 10
BASE_URL = "http://www.centrometeolombardo.com/"
STATIONS_URL = f"{BASE_URL}/content.asp?CatId=273&ContentType=Stazioni"
IMG_URL = "http://rete.centrometeolombardo.com/{province}/{tag}/immagini/v.png"

# -------------------------

# Paths
ROOT_PATH = Path(__file__).resolve().parents[1]

STATIONS_JSON = ROOT_PATH / "config/stations.json"
TMP_IMG_PATH = ROOT_PATH / "tmp/img"
PATHS = [
    STATIONS_JSON,
    TMP_IMG_PATH
]

# -------------------------

# Artifacts
STATIONS = {}
with open(STATIONS_JSON, "r") as f:
    STATIONS = json.load(f)

# -------------------------

# Logging
LOCAL_TIMEZONE = ZoneInfo("Europe/Rome")

def refresh_logging():

    global NOW, ACTUAL_TIME, YEAR, MONTH, DAY, HOUR, MINUTE, LOG_TIMESTAMP
    NOW = datetime.now(LOCAL_TIMEZONE)
    ACTUAL_TIME = NOW.strftime("%Y%m%d-%H%M")
    YEAR = NOW.strftime("%Y")
    MONTH = NOW.strftime("%m")
    DAY = NOW.strftime("%d")
    HOUR = NOW.strftime("%H")
    MINUTE = NOW.strftime("%M")
    LOG_TIMESTAMP = f"[{YEAR}-{MONTH}-{DAY} @ {HOUR}:{MINUTE}]"
refresh_logging()

# -------------------------

# Google Cloud Platform (GCP)
GCP_PROJECT = "uninsubria-data-science"
BQ_DATASET = "larionow_dataset"
BQ_TABLE_NAME = "measurements"
BQ_TABLE = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_TABLE_NAME}"

# -------------------------

# AI
DEVICE = "cpu"
OCR_MODEL = "PP-OCRv5_server_rec"
OCR_FIELDS = [
    "temperature_c",
    "humidity_pct",
    "dew_point_c",
    "wind_kmh",
    "wind_dir",
    "pressure_hpa",
    "rain_mm",
    "rain_mmh"
]
WIND_DIR_VALUES = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
]

# -------------------------
