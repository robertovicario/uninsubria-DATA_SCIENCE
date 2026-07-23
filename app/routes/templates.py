# =========================
# Dependencies
# =========================

from flask import Blueprint, render_template

# =========================
# Flask
# =========================

templates_bp = Blueprint('templates', __name__)

# =========================
# Templates
# =========================

@templates_bp.route('/')
def home():
    return render_template('pages/home.html')

@templates_bp.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html')
