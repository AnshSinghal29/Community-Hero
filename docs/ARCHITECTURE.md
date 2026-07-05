# Community Hero — System Architecture

## Overview

Community Hero is a 3-layer full-stack application for AI-powered civic issue tracking.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CITIZEN (Browser)                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │            dashboard.html (Vanilla JS)                   │    │
│  │  ┌──────────────┐  ┌────────────────┐  ┌─────────────┐  │    │
│  │  │  Google Maps │  │  Issues List   │  │ Report Form │  │    │
│  │  │  (markers)   │  │  (real-time)   │  │ + Voice     │  │    │
│  │  └──────────────┘  └────────────────┘  └─────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/REST (multipart form)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  BACKEND API (Python Flask)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  POST /api/report  GET /api/issues  GET /api/stats       │   │
│  │  GET /api/predict  GET /api/health                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                    │                │                             │
│            ┌───────┘        ┌───────┘                            │
│            ▼                ▼                                     │
│  ┌─────────────────┐  ┌───────────────────────┐                 │
│  │   agent.py      │  │   google_sheets.py     │                 │
│  │                 │  │                        │                 │
│  │  ┌───────────┐  │  │  save_to_sheets()      │                 │
│  │  │ Claude    │  │  │  get_from_sheets()     │                 │
│  │  │ Opus 4.5  │  │  │  get_recent_reports()  │                 │
│  │  │ Vision +  │  │  │  get_stats()           │                 │
│  │  │ Extended  │  │  └────────────┬──────────┘                 │
│  │  │ Thinking  │  │               │                             │
│  │  └───────────┘  │               │ gspread                    │
│  └─────────────────┘               ▼                             │
│                           ┌──────────────────┐                   │
│  ┌────────────────────┐   │  Google Sheets   │                   │
│  │   predictor.py     │   │  (public)        │                   │
│  │   find_hotspots()  │   └──────────────────┘                   │
│  │   predict_future() │                                           │
│  └─────────┬──────────┘                                          │
│            │ Claude API                                           │
│            ▼                                                      │
│  ┌─────────────────┐                                             │
│  │  Predictions    │                                             │
│  └─────────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Issue Report Flow
```
1. Citizen clicks map / opens form
2. Uploads photo + description + GPS coordinates
3. POST /api/report with multipart data
4. Backend:
   a. Encodes image to base64
   b. Fetches recent nearby reports (duplicate detection)
   c. Calls analyze_issue() → Claude Opus with extended thinking
   d. Claude analyzes image + text → returns JSON
   e. Saves to Google Sheets
   f. Returns report_id + analysis to client
5. Dashboard refreshes (auto every 5 seconds)
```

### Agentic Reasoning Flow
```
Input: image + description + lat/lng + recent_reports
           │
           ▼
┌─────────────────────────────┐
│  Claude Extended Thinking   │ ◄── budget_tokens: 8000
│                             │
│  1. IMAGE ANALYSIS          │
│     - What damage is seen?  │
│     - Severity 1-5          │
│                             │
│  2. CATEGORY                │
│     - pothole / water_leak  │
│     - streetlight / waste   │
│                             │
│  3. PRIORITY                │
│     - URGENT / HIGH         │
│     - MEDIUM / LOW          │
│                             │
│  4. DUPLICATE CHECK         │
│     - Compare to nearby     │
│       reports in 50m/7 days │
│                             │
│  5. ACTION                  │
│     - Escalate / Monitor    │
│     - Notify citizens       │
└─────────────────────────────┘
           │
           ▼
Output JSON: {category, priority, severity, reasoning, thinking, ...}
           │
           ▼
Google Sheets (Timestamp, ReportID, Category, Priority, ...)
```

## Database Schema (Google Sheets)

| Column | Type | Example |
|--------|------|---------|
| Timestamp | ISO string | 2026-06-27T12:30:00 |
| ReportID | string | GH-20260627123000 |
| Category | string | pothole |
| Priority | string | urgent |
| Severity | number | 4 |
| Latitude | number | 28.6692 |
| Longitude | number | 77.0669 |
| Address | string | Sector 7, Ghaziabad |
| Description | string | Large pothole... |
| Reasoning | string | Agent reasoning... |
| RecommendedAction | string | PWD escalation |
| ImageURL | string | image.jpg |
| Confidence | number | 0.92 |
| Status | string | open |
| ThinkingSummary | string | Extended thinking... |
| EstimatedResolutionDays | number | 7 |
| IsDuplicate | boolean | false |

## Prediction Logic

```
All issues (7 days) → Cluster by lat/lng/category (50m resolution)
                           │
                    3+ reports in cluster?
                           │
                           ▼ YES
                      HOTSPOT identified
                           │
                           ▼
                   Claude predicts:
                   - Adjacent high-risk areas
                   - Confidence scores
                   - Reasoning (monsoon, age of infrastructure)
                           │
                           ▼
                   Dashed yellow circles on map
```

## Duplicate Detection

```python
# Haversine distance calculation
def _haversine(lat1, lon1, lat2, lon2) -> float:
    # Returns distance in meters
    # If < 50m AND same 7-day window → likely duplicate

# Agent also compares against recent_reports in its reasoning
```
