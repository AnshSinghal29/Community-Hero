"""
google_sheets.py — Google Sheets data persistence for Community Hero

Provides:
- save_to_sheets()         Save analyzed report
- get_from_sheets()        Fetch issues (with optional filtering)
- get_recent_reports()     Fetch nearby recent reports (duplicate detection)
- get_stats()              Return summary stats
"""

import os
import math
import logging
from datetime import datetime, timedelta

import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Auth & Connection
# ──────────────────────────────────────────────

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_COLUMNS = [
    "Timestamp", "ReportID", "Category", "Priority", "Severity",
    "Latitude", "Longitude", "Address", "Description",
    "Reasoning", "RecommendedAction", "ImageURL",
    "Confidence", "Status", "ThinkingSummary",
    "EstimatedResolutionDays", "IsDuplicate"
]


def _get_sheet():
    """Return the gspread worksheet, authenticating as needed."""
    creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service_account.json")
    sheets_id = os.getenv("GOOGLE_SHEETS_ID", "")
    worksheet_name = os.getenv("GOOGLE_SHEETS_WORKSHEET", "Reports")

    if not sheets_id:
        raise EnvironmentError("GOOGLE_SHEETS_ID is not set in environment variables.")

    try:
        creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(sheets_id)

        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            # Create sheet with headers if it doesn't exist
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)
            worksheet.append_row(SHEET_COLUMNS)
            logger.info(f"[SUCCESS] Created new worksheet '{worksheet_name}' with headers")

        return worksheet

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Service account JSON not found at '{creds_file}'. "
            "Download it from Google Cloud Console and set GOOGLE_APPLICATION_CREDENTIALS."
        )


# ──────────────────────────────────────────────
# Write Operations
# ──────────────────────────────────────────────

def save_to_sheets(analysis: dict, image_url: str, timestamp: str, description: str = "") -> str:
    """
    Append an analyzed issue to Google Sheets.

    Args:
        analysis:    Dict from agent.analyze_issue()
        image_url:   Filename or Drive URL of the uploaded image
        timestamp:   ISO format timestamp string
        description: Original citizen description

    Returns:
        str: Unique report ID (format: GH-YYYYMMDDHHMMSS)
    """
    report_id = f"GH-{timestamp.replace('-', '').replace(':', '').replace('.', '')[:14]}"

    coords = analysis.get("coordinates", {})
    row = [
        timestamp,
        report_id,
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
        "open",  # default status
        (analysis.get("thinking", "")[:200] + "...") if analysis.get("thinking") else "",
        analysis.get("estimated_resolution_days", 7),
        analysis.get("is_duplicate", False)
    ]

    try:
        sheet = _get_sheet()
        sheet.append_row(row, value_input_option="USER_ENTERED")
        logger.info(f"[SUCCESS] Saved report {report_id} to Google Sheets")
        return report_id
    except Exception as e:
        logger.error(f"[ERROR] Failed to save to Sheets: {e}")
        raise


# ──────────────────────────────────────────────
# Read Operations
# ──────────────────────────────────────────────

def get_from_sheets(
    category: str = None,
    priority: str = None,
    limit: int = 200
) -> list[dict]:
    """
    Fetch all issues from Google Sheets, optionally filtered.

    Args:
        category: Filter by category (e.g. 'pothole')
        priority: Filter by priority (e.g. 'urgent')
        limit:    Maximum rows to return

    Returns:
        List of issue dicts
    """
    try:
        sheet = _get_sheet()
        records = sheet.get_all_records()
    except Exception as e:
        logger.error(f"[ERROR] Failed to fetch from Sheets: {e}")
        return []

    issues = []
    for record in records:
        if not record.get("ReportID"):
            continue  # skip header or empty rows

        # Normalise keys for frontend consumption
        issue = {
            "id":               record.get("ReportID", ""),
            "timestamp":        record.get("Timestamp", ""),
            "category":         record.get("Category", "other").lower(),
            "priority":         record.get("Priority", "low").lower(),
            "severity":         record.get("Severity", 1),
            "latitude":         _safe_float(record.get("Latitude", 0)),
            "longitude":        _safe_float(record.get("Longitude", 0)),
            "address":          record.get("Address", ""),
            "description":      record.get("Description", ""),
            "reasoning":        record.get("Reasoning", ""),
            "recommended_action": record.get("RecommendedAction", ""),
            "image_url":        record.get("ImageURL", ""),
            "confidence":       _safe_float(record.get("Confidence", 0)),
            "status":           record.get("Status", "open").lower(),
            "thinking":         record.get("ThinkingSummary", ""),
            "estimated_days":   record.get("EstimatedResolutionDays", 7),
            "is_duplicate":     record.get("IsDuplicate", False),
        }

        # Apply filters
        if category and issue["category"] != category.lower():
            continue
        if priority and issue["priority"] != priority.lower():
            continue

        issues.append(issue)

        if len(issues) >= limit:
            break

    logger.info(f"[AGENT] Fetched {len(issues)} issues from Sheets (filters: category={category}, priority={priority})")
    return issues


def get_recent_reports(
    latitude: float,
    longitude: float,
    days: int = 7,
    radius_meters: int = 50
) -> list[dict]:
    """
    Fetch recent reports near a location for duplicate detection.

    Args:
        latitude:       Center latitude
        longitude:      Center longitude
        days:           Look back window (default 7)
        radius_meters:  Search radius in meters (default 50)

    Returns:
        List of nearby recent report dicts
    """
    try:
        all_issues = get_from_sheets(limit=500)
    except Exception:
        return []

    cutoff = datetime.now() - timedelta(days=days)
    nearby = []

    for issue in all_issues:
        # Parse timestamp
        try:
            issue_time = datetime.fromisoformat(issue["timestamp"])
        except (ValueError, TypeError):
            continue

        if issue_time < cutoff:
            continue

        # Haversine distance (approximate)
        dist = _haversine(latitude, longitude, issue["latitude"], issue["longitude"])
        if dist <= radius_meters:
            nearby.append({
                "id": issue["id"],
                "category": issue["category"],
                "priority": issue["priority"],
                "distance_meters": round(dist, 1)
            })

    return nearby


def get_stats() -> dict:
    """
    Compute summary statistics from all issues.

    Returns:
        dict: {total, urgent, high, medium, low, resolved, resolved_pct}
    """
    try:
        issues = get_from_sheets(limit=500)
    except Exception:
        return {"total": 0, "urgent": 0, "high": 0, "medium": 0, "low": 0, "resolved": 0, "resolved_pct": 0}

    total = len(issues)
    urgent = sum(1 for i in issues if i["priority"] == "urgent")
    high = sum(1 for i in issues if i["priority"] == "high")
    medium = sum(1 for i in issues if i["priority"] == "medium")
    low = sum(1 for i in issues if i["priority"] == "low")
    resolved = sum(1 for i in issues if i["status"] == "resolved")
    resolved_pct = round((resolved / total) * 100) if total > 0 else 0

    return {
        "total": total,
        "urgent": urgent,
        "high": high,
        "medium": medium,
        "low": low,
        "resolved": resolved,
        "resolved_pct": resolved_pct
    }


# ──────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────

def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance in meters between two GPS points.
    Uses the Haversine formula.
    """
    R = 6_371_000  # Earth radius in metres

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _safe_float(value, default: float = 0.0) -> float:
    """Convert a value to float safely."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


if __name__ == "__main__":
    # Quick smoke test
    stats = get_stats()
    print("Stats:", stats)
    recent = get_recent_reports(28.6692, 77.0669)
    print("Recent nearby reports:", recent)
