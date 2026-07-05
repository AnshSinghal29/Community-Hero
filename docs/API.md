# Community Hero — API Documentation

Base URL: `http://localhost:5000` (development)

---

## Endpoints

### `GET /api/health`

Health check.

**Response:**
```json
{ "status": "ok", "timestamp": "2026-06-27T12:00:00" }
```

---

### `POST /api/report`

Submit a new civic issue report.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file | ✅ | Photo of the issue (JPEG/PNG) |
| `description` | string | ✅ | Citizen's description |
| `latitude` | float | ✅ | GPS latitude |
| `longitude` | float | ✅ | GPS longitude |
| `address` | string | ❌ | Human-readable address |

**Success Response (200):**
```json
{
  "success": true,
  "report_id": "GH-20260627120000",
  "analysis": {
    "category": "pothole",
    "category_confidence": 0.95,
    "severity_score": 4,
    "severity_description": "Deep pothole, 15cm, on main road",
    "priority": "urgent",
    "coordinates": {
      "latitude": 28.6692,
      "longitude": 77.0669,
      "address_inferred": "Sector 7, Ghaziabad"
    },
    "is_duplicate": false,
    "duplicate_of_report_id": null,
    "reasoning": "Image shows a deep pothole (approximately 15cm) on what appears to be a main road...",
    "estimated_resolution_days": 3,
    "recommended_action": "Immediate escalation to PWD. Safety barriers should be placed.",
    "public_notification": "A severe pothole in Sector 7 has been reported. Please drive carefully.",
    "confidence_overall": 0.92,
    "thinking": "Extended agent reasoning text..."
  }
}
```

**Error Response (400):**
```json
{ "success": false, "error": "Image file is required" }
```

**Error Response (500):**
```json
{ "success": false, "error": "Agent analysis failed: <detail>" }
```

---

### `GET /api/issues`

Fetch all reported issues.

**Query Parameters:**

| Param | Values | Description |
|-------|--------|-------------|
| `category` | `pothole`, `water_leak`, `streetlight`, `waste_management`, `other` | Filter by category |
| `priority` | `urgent`, `high`, `medium`, `low` | Filter by priority |

**Response (200):**
```json
[
  {
    "id": "GH-20260627120000",
    "timestamp": "2026-06-27T12:00:00",
    "category": "pothole",
    "priority": "urgent",
    "severity": 4,
    "latitude": 28.6692,
    "longitude": 77.0669,
    "address": "Sector 7, Ghaziabad",
    "description": "Large pothole on main road",
    "reasoning": "Agent reasoning...",
    "recommended_action": "PWD escalation",
    "image_url": "issue_image.jpg",
    "confidence": 0.92,
    "status": "open",
    "thinking": "Extended thinking summary...",
    "estimated_days": 3,
    "is_duplicate": false
  }
]
```

---

### `GET /api/stats`

Get summary statistics.

**Response (200):**
```json
{
  "total": 12,
  "urgent": 3,
  "high": 4,
  "medium": 3,
  "low": 2,
  "resolved": 2,
  "resolved_pct": 16
}
```

---

### `GET /api/predict`

AI-powered prediction of high-risk areas.

**Response (200):**
```json
{
  "hotspots": [
    {
      "latitude": 28.6692,
      "longitude": 77.0669,
      "category": "pothole",
      "count": 3,
      "reports": ["GH-001", "GH-002", "GH-003"]
    }
  ],
  "high_risk_locations": [
    {
      "latitude": 28.6720,
      "longitude": 77.0680,
      "category": "pothole",
      "confidence": 0.87,
      "reason": "Adjacent to confirmed pothole hotspot; similar road age and traffic load"
    }
  ],
  "timestamp": "2026-06-27T12:00:00"
}
```

---

## Error Codes

| HTTP Code | Meaning |
|-----------|---------|
| 200 | Success |
| 400 | Bad request (missing/invalid parameters) |
| 500 | Server error (API failure, Sheets error) |

## Rate Limits

- No hard rate limits in MVP
- Claude API has per-minute token limits — avoid rapid submissions
- Google Sheets API: 100 req/100 seconds per user

## CORS

All `/api/*` routes accept requests from any origin (`*`).
