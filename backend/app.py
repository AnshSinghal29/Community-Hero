"""
app.py — Flask API for Community Hero (FREE tier: SQLite + local storage)

Endpoints:
  POST /api/report   — Submit civic issue (image + description + location)
  GET  /api/issues   — Fetch all issues (with optional filters)
  GET  /api/stats    — Summary statistics
  GET  /api/predict  — AI-powered hotspot predictions
  GET  /api/health   — Health check

Storage: SQLite (issues.db) + local /uploads/ folder — no Google APIs needed.
"""

import os
import base64
import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Local modules
from agent import analyze_issue
from database import save_to_sheets, get_from_sheets, get_recent_reports, get_stats  # SQLite (free)
from predictor import get_predictions

# ──────────────────────────────────────────────
# App Setup
# ──────────────────────────────────────────────

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ensure log and uploads directories exist
Path("logs").mkdir(exist_ok=True)
UPLOAD_FOLDER = Path(os.getenv("UPLOAD_FOLDER", "uploads"))
UPLOAD_FOLDER.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/api/report", methods=["POST"])
def create_report():
    """
    Submit a new civic issue report.

    Accepts multipart/form-data:
      - image       (file)   Required — photo of the issue
      - description (string) Required — citizen description
      - latitude    (float)  Required — GPS latitude
      - longitude   (float)  Required — GPS longitude
      - address     (string) Optional — human-readable address

    Returns JSON:
      { success, report_id, analysis }
    """
    logger.info("[REQUEST] POST /api/report")

    # ── Validate inputs ──
    image_file = request.files.get("image")
    description = request.form.get("description", "").strip()
    address = request.form.get("address", "").strip()

    try:
        lat = float(request.form.get("latitude", 0))
        lng = float(request.form.get("longitude", 0))
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid latitude/longitude"}), 400

    if not image_file:
        return jsonify({"success": False, "error": "Image file is required"}), 400

    if not description:
        return jsonify({"success": False, "error": "Description is required"}), 400

    if lat == 0 and lng == 0:
        return jsonify({"success": False, "error": "Valid coordinates are required"}), 400

    # ── Save image locally + encode ──
    try:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        # Persist image to disk
        safe_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_filename = f"{safe_ts}_{image_file.filename or 'image.jpg'}"
        img_path = UPLOAD_FOLDER / img_filename
        img_path.write_bytes(image_bytes)
        image_name = str(img_path)  # local path stored in DB
    except Exception as e:
        logger.error(f"[ERROR] Image processing failed: {e}")
        return jsonify({"success": False, "error": "Could not process image"}), 400

    # ── Check for nearby duplicates ──
    try:
        recent = get_recent_reports(lat, lng, days=7, radius_meters=50)
        logger.info(f"[AGENT] Found {len(recent)} recent reports nearby for duplicate check")
    except Exception as e:
        logger.warning(f"[WARN] Could not fetch recent reports: {e}")
        recent = []

    # ── Run agentic analysis ──
    try:
        analysis = analyze_issue(
            image_base64=image_base64,
            description=description,
            lat=lat,
            lng=lng,
            recent_reports=recent
        )
    except Exception as e:
        logger.error(f"[ERROR] Agent analysis failed: {e}")
        return jsonify({"success": False, "error": f"Agent analysis failed: {str(e)}"}), 500

    # ── Inject address into coordinates if provided ──
    if address and not analysis.get("coordinates", {}).get("address_inferred"):
        if "coordinates" in analysis:
            analysis["coordinates"]["address_inferred"] = address

    # ── Save to Google Sheets ──
    timestamp = datetime.now().isoformat()

    try:
        report_id = save_to_sheets(
            analysis=analysis,
            image_url=image_name,
            timestamp=timestamp,
            description=description
        )
    except Exception as e:
        logger.error(f"[ERROR] SQLite save failed: {e}")
        return jsonify({
            "success": True,
            "report_id": f"GH-LOCAL-{timestamp[:10]}",
            "analysis": analysis,
            "warning": f"Could not save to database: {e}"
        }), 200

    logger.info(f"[SUCCESS] Report {report_id} created: {analysis.get('category')} / {analysis.get('priority')}")

    return jsonify({
        "success": True,
        "report_id": report_id,
        "analysis": analysis
    })


@app.route("/api/issues", methods=["GET"])
def get_issues():
    """
    Fetch all issues, optionally filtered.

    Query params:
      - category: pothole|water_leak|streetlight|waste_management|other
      - priority:  urgent|high|medium|low
    """
    category = request.args.get("category")
    priority = request.args.get("priority")

    logger.info(f"[REQUEST] GET /api/issues (category={category}, priority={priority})")

    try:
        issues = get_from_sheets(category=category, priority=priority)
        return jsonify(issues)
    except Exception as e:
        logger.error(f"[ERROR] Failed to fetch issues: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def stats():
    """Return summary statistics."""
    logger.info("[REQUEST] GET /api/stats")

    try:
        data = get_stats()
        return jsonify(data)
    except Exception as e:
        logger.error(f"[ERROR] Failed to compute stats: {e}")
        return jsonify({"total": 0, "urgent": 0, "high": 0, "resolved": 0, "resolved_pct": 0}), 200


@app.route("/api/predict", methods=["GET"])
def predict():
    """
    AI-powered prediction of future high-risk areas.

    Returns:
      { hotspots, high_risk_locations, timestamp }
    """
    logger.info("[REQUEST] GET /api/predict")

    try:
        data = get_predictions()
        return jsonify(data)
    except Exception as e:
        logger.error(f"[ERROR] Prediction failed: {e}")
        return jsonify({"high_risk_locations": [], "error": str(e)}), 500


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

# ── Serve uploaded images ──
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """Serve locally-stored issue images."""
    return send_from_directory(str(UPLOAD_FOLDER.resolve()), filename)


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"

    logger.info(f"[SUCCESS] Starting Community Hero API on port {port} (FREE tier - SQLite + local storage)")
    app.run(host="0.0.0.0", port=port, debug=debug)
