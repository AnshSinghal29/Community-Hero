"""
predictor.py — Hotspot prediction layer for Community Hero

Analyzes historical issue patterns and uses Claude to predict
high-risk areas for the next 7 days.
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta

from agent import predict_future_issues
from database import get_from_sheets

logger = logging.getLogger(__name__)

# Cluster resolution (degrees) — ~50m
CLUSTER_SIZE_DEG = 0.0005
MIN_REPORTS_FOR_HOTSPOT = 3
LOOKBACK_DAYS = 7


def _cluster_key(lat: float, lng: float) -> tuple:
    """Round coords to cluster resolution."""
    return (
        round(lat / CLUSTER_SIZE_DEG) * CLUSTER_SIZE_DEG,
        round(lng / CLUSTER_SIZE_DEG) * CLUSTER_SIZE_DEG
    )


def find_hotspots(issues: list) -> list:
    """
    Group issues by location+category cluster and find dense areas.

    Args:
        issues: List of issue dicts from Google Sheets

    Returns:
        List of hotspot dicts (lat, lng, category, count, reports)
    """
    cutoff = datetime.now() - timedelta(days=LOOKBACK_DAYS)
    clusters: dict[tuple, list] = defaultdict(list)

    for issue in issues:
        try:
            ts = datetime.fromisoformat(issue.get("timestamp", ""))
        except (ValueError, TypeError):
            continue

        if ts < cutoff:
            continue

        lat = issue.get("latitude", 0)
        lng = issue.get("longitude", 0)
        cat = issue.get("category", "other")

        key = (_cluster_key(lat, lng), cat)
        clusters[key].append(issue)

    hotspots = []
    for (loc, cat), reports in clusters.items():
        if len(reports) >= MIN_REPORTS_FOR_HOTSPOT:
            hotspots.append({
                "latitude": loc[0],
                "longitude": loc[1],
                "category": cat,
                "count": len(reports),
                "reports": [r.get("id") for r in reports]
            })

    hotspots.sort(key=lambda h: h["count"], reverse=True)
    return hotspots


def get_predictions() -> dict:
    """
    Full prediction pipeline:
    1. Fetch all recent issues
    2. Find hotspots (3+ reports same category, same area, 7 days)
    3. Call Claude to predict adjacent high-risk areas
    4. Return combined JSON

    Returns:
        dict with "hotspots" (confirmed) and "high_risk_locations" (predicted)
    """
    logger.info("[AGENT] Running prediction pipeline...")

    try:
        all_issues = get_from_sheets(limit=500)
    except Exception as e:
        logger.error(f"[ERROR] Could not fetch issues for prediction: {e}")
        return {
            "hotspots": [],
            "high_risk_locations": [],
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

    hotspots = find_hotspots(all_issues)
    logger.info(f"[AGENT] Found {len(hotspots)} confirmed hotspots")

    # Call Claude prediction agent
    predictions = predict_future_issues(hotspots)

    return {
        "hotspots": hotspots,
        "high_risk_locations": predictions.get("high_risk_locations", []),
        "timestamp": datetime.now().isoformat()
    }
