# =========================
# Dependencies
# =========================

from flask import Blueprint
from loguru import logger

# =========================
# Configuration
# =========================

logger.add('logs/app.log', rotation='2 MB')

# -------------------------

index_bp = Blueprint('index', __name__, url_prefix='/api')

# =========================
# Endpoints
# =========================
