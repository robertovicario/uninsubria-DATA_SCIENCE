# =========================
# Dependencies
# =========================

from glob import glob
from loguru import logger
import numpy as np
from pathlib import Path
from paddleocr import TextRecognition
from typing import Any
import cv2
import os
import paddle
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if PROJECT_ROOT.name == "jobs":
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib import config as the_config
from lib import utils as the_utils

# -------------------------

paddle.disable_signal_handler()

# =========================
# Configurations
# =========================

# Models
MODEL_OCR = TextRecognition(
    model_name=the_config.OCR_MODEL,
    device=the_config.DEVICE
)

# =========================
# Methods
# =========================

def transform_data(
    stations: dict[str, dict[str, Any]],
    verbose: bool = False
) -> list[dict[str, Any]]:

    logger.info(
f"""\n
# =========================
# (2) TRANSFORMATION
# =========================
"""
    )

    # TMP Images (1)
    images = sorted(glob(os.path.join(the_config.TMP_IMG_PATH, "*.png")))
    total_img = len(images)

    # -------------------------

    new_data = []
    for i, img_file in enumerate(images, start=1):

        # Filename
        filename = os.path.basename(img_file)
        station, date, hour, minute = the_utils.parse_filename(filename)
        year, month, day = date.split("-")
        metadata = stations[station]
        city = metadata["city"]
        province = metadata["province"]
        lat = metadata["lat"]
        lon = metadata["lon"]
        elevation = metadata["elevation_m"]
        logger.debug(f"{the_config.LOG_TIMESTAMP} [{i:02d}/{total_img:02d}]")
        logger.debug(f"{the_config.LOG_TIMESTAMP} STATION: {city}")

        # -------------------------

        try:

            # OpenCV Image
            img_cv = cv2.imread(img_file)
            if img_cv is None:
                logger.error(f"{the_config.LOG_TIMESTAMP} Unable to read img_cv: {filename}\n")
                continue

            img_cv = cv2.resize(
                img_cv,
                None,
                fx=2,
                fy=2,
                interpolation=cv2.INTER_LINEAR
            )

        except Exception as e:
            logger.error(f"{the_config.LOG_TIMESTAMP} {str(e)}\n")
            continue

        # -------------------------

        try:

            # ROIs Extraction (1)
            hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
            green_mask = cv2.inRange(
                hsv,
                np.array([35, 50, 50]),
                np.array([85, 255, 255]),
            )
            blue_mask = cv2.inRange(
                hsv,
                np.array([90, 50, 50]),
                np.array([130, 255, 255]),
            )

            # -------------------------

            # ROIs Extraction (2)
            green_rois = the_utils.extract_rois(img_cv, green_mask, "green")
            blue_rois  = the_utils.extract_rois(img_cv, blue_mask, "blue")
            all_rois = sorted(green_rois + blue_rois, key=lambda r: r["bbox"][0])

            # -------------------------

            # OCR Prediction
            pieces = the_utils.get_pieces(img_cv, green_mask, all_rois)
            values = the_utils.ocr_predict(
                MODEL_OCR,
                the_config.OCR_FIELDS,
                pieces,
                verbose=verbose
            )

        except Exception as e:
            logger.error(f"{the_config.LOG_TIMESTAMP} {str(e)}\n")
            continue

        # -------------------------

        try:

            # Data Appending
            records = {
                "filename": filename,
                "date": date,
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "minute": minute,
                "station": station,
                "city": city,
                "province": province,
                "lat": lat,
                "lon": lon,
                "elevation_m": elevation
            }
            fields = {
                "temperature_c": the_utils.parse_float,
                "humidity_pct": the_utils.parse_int,
                "dew_point_c": the_utils.parse_float,
                "wind_kmh": the_utils.parse_float,
                "wind_dir": the_utils.normalize_wind_dir,
                "pressure_hpa": the_utils.parse_float,
                "rain_mm": the_utils.parse_float,
                "rain_mmh": the_utils.parse_float,
            }

            for field, parser in fields.items():

                try:
                    records[field] = parser(values[field])
                except Exception as e:
                    records[field] = None
                    logger.warning(f"{the_config.LOG_TIMESTAMP} {str(e)}")
            new_data.append(records)

        except Exception as e:
            logger.error(f"{the_config.LOG_TIMESTAMP} {str(e)}\n")
            continue
        logger.success(f"{the_config.LOG_TIMESTAMP} TRANSFORMED: {filename}\n")

    # -------------------------

    return new_data

# -------------------------
