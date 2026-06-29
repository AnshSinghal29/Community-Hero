"""
database.py — SQLite data persistence for Community Hero (FREE alternative to Google Sheets)

Completely free, no API keys needed.
Provides identical interface to google_sheets.py so app.py needs minimal changes.
"""

import sqlite3
import math
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path("issues.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS issues (
    id                      TEXT PRIMARY KEY,
    timestamp               TEXT NOT NULL,
    category                TEXT DEFAULT 'other',
    priority                TEXT DEFAULT 'medium',
    severity_score          INTEGER DEFAULT 3,
    latitude                REAL DEFAULT 0,
    longitude               REAL DEFAULT 0,
    address                 TEXT DEFAULT '',
    description             TEXT DEFAULT '',
    reasoning               TEXT DEFAULT '',
    recommended_action      TEXT DEFAULT '',
    image_url               TEXT DEFAULT '',
    confidence              REAL DEFAULT 0.5,
    status                  TEXT DEFAULT 'open',
    thinking_summary        TEXT DEFAULT '',
    estimated_resolution_days INTEGER DEFAULT 7,
    is_duplicate            INTEGER DEFAULT 0
);
"""


# ──────────────────────────────────────────────
# Init
# ──────────────────────────────────────────────

def init_db():
    """Create the issues table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(SCHEMA)
        conn.commit()
    logger.info(f"[SUCCESS] SQLite database ready at {DB_PATH.resolve()}")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ──────────────────────────────────────────────
# Write
# ──────────────────────────────────────────────

def save_to_sheets(analysis: dict, image_url: str, timestamp: str, description: str = "") -> str:
    """
    Save analyzed issue to SQLite.
    Function name kept identical to google_sheets.py for drop-in compatibility.

    Returns:
        str: Unique report ID (format: GH-YYYYMMDDHHMMSS)
    """
    report_id = "GH-" + timestamp.replace("-", "").replace(":", "").replace(".", "")[:14]
    coords = analysis.get("coordinates", {})

    with _get_conn() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO issues
            (id, timestamp, category, priority, severity_score,
             latitude, longitude, address, description, reasoning,
             recommended_action, image_url, confidence, status,
             thinking_summary, estimated_resolution_days, is_duplicate)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            report_id,
            timestamp,
            analysis.get("category", "other"),
            analysis.get("priority", "medium"),
            analysis.get("severity_score", 3),
            coords.get("latitude", 0),
            coords.get("longitude", 0),
            coords.get("address_inferred", ""),
            description,
            analysis.get("reasoning", ""),
            analysis.get("recommended_action", ""),
            image_url,
            analysis.get("confidence_overall", 0.5),
            "open",
            (analysis.get("thinking", "")[:200] + "...") if analysis.get("thinking") else "",
            analysis.get("estimated_resolution_days", 7),
            1 if analysis.get("is_duplicate") else 0
        ))
        conn.commit()

    logger.info(f"[SUCCESS] Saved {report_id} to SQLite")
    return report_id


# ──────────────────────────────────────────────
# Read
# ──────────────────────────────────────────────

def get_from_sheets(
    category: str = None,
    priority: str = None,
    limit: int = 200
) -> list[dict]:
    """
    Fetch issues from SQLite, optionally filtered.
    Function name kept identical to google_sheets.py for drop-in compatibility.
    """
    query = "SELECT * FROM issues WHERE 1=1"
    params = []

    if category:
        query += " AND LOWER(category) = ?"
        params.append(category.lower())
    if priority:
        query += " AND LOWER(priority) = ?"
        params.append(priority.lower())

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    with _get_conn() as conn:
        rows = conn.execute(query, params).fetchall()

    issues = []
    for row in rows:
        r = dict(row)
        issues.append({
            "id":                   r.get("id", ""),
            "timestamp":            r.get("timestamp", ""),
            "category":             r.get("category", "other"),
            "priority":             r.get("priority", "medium"),
            "severity":             r.get("severity_score", 3),
            "latitude":             r.get("latitude", 0),
            "longitude":            r.get("longitude", 0),
            "address":              r.get("address", ""),
            "description":          r.get("description", ""),
            "reasoning":            r.get("reasoning", ""),
            "recommended_action":   r.get("recommended_action", ""),
            "image_url":            r.get("image_url", ""),
            "confidence":           r.get("confidence", 0.5),
            "status":               r.get("status", "open"),
            "thinking":             r.get("thinking_summary", ""),
            "estimated_days":       r.get("estimated_resolution_days", 7),
            "is_duplicate":         bool(r.get("is_duplicate", 0)),
        })

    logger.info(f"[AGENT] Fetched {len(issues)} issues from SQLite")
    return issues


def get_recent_reports(
    latitude: float,
    longitude: float,
    days: int = 7,
    radius_meters: int = 50
) -> list[dict]:
    """
    Fetch recent reports near a location for duplicate detection.
    Uses Haversine distance in Python (SQLite doesn't have trig natively).
    """
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()

    # Rough bounding box first (fast SQL filter)
    lat_delta = radius_meters / 111000
    lng_delta = radius_meters / (111000 * math.cos(math.radians(latitude)))

    with _get_conn() as conn:
        rows = conn.execute("""
            SELECT * FROM issues
            WHERE timestamp > ?
              AND latitude  BETWEEN ? AND ?
              AND longitude BETWEEN ? AND ?
        """, (
            cutoff,
            latitude - lat_delta, latitude + lat_delta,
            longitude - lng_delta, longitude + lng_delta
        )).fetchall()

    nearby = []
    for row in rows:
        r = dict(row)
        dist = _haversine(latitude, longitude, r["latitude"], r["longitude"])
        if dist <= radius_meters:
            nearby.append({
                "id":               r.get("id"),
                "category":         r.get("category"),
                "priority":         r.get("priority"),
                "distance_meters":  round(dist, 1)
            })

    return nearby


def get_stats() -> dict:
    """Return summary statistics."""
    with _get_conn() as conn:
        total    = conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
        urgent   = conn.execute("SELECT COUNT(*) FROM issues WHERE priority='urgent'").fetchone()[0]
        high     = conn.execute("SELECT COUNT(*) FROM issues WHERE priority='high'").fetchone()[0]
        medium   = conn.execute("SELECT COUNT(*) FROM issues WHERE priority='medium'").fetchone()[0]
        low      = conn.execute("SELECT COUNT(*) FROM issues WHERE priority='low'").fetchone()[0]
        resolved = conn.execute("SELECT COUNT(*) FROM issues WHERE status='resolved'").fetchone()[0]

    resolved_pct = round((resolved / total) * 100) if total > 0 else 0

    return {
        "total":        total,
        "urgent":       urgent,
        "high":         high,
        "medium":       medium,
        "low":          low,
        "resolved":     resolved,
        "resolved_pct": resolved_pct
    }


# ──────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────

def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return great-circle distance in metres."""
    R = 6_371_000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# Auto-init on import
init_db()


if __name__ == "__main__":
    stats = get_stats()
    print("Stats:", stats)
    issues = get_from_sheets(limit=5)
    print(f"Last {len(issues)} issues:", [i["id"] for i in issues])
