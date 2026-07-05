# Community Hero - API Documentation

**Base URL**: `http://localhost:5000` (development) or `https://your-domain.com` (production)

**Authentication**: None (for MVP). Add JWT tokens in production.

**Response Format**: All responses are JSON.

---

## 📝 Endpoints

### 1. Report Issue

**Endpoint**: `POST /api/report`

**Description**: Submit a new civic issue for AI analysis and storage.

**Request**:
```http
POST /api/report HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data

image: <binary file>
description: Large pothole on main road
latitude: 28.6692
longitude: 77.0669
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | File (JPEG/PNG) | Yes | Photo of the issue |
| `description` | String (0-500 chars) | Yes | Citizen's description |
| `latitude` | Float | Yes | Latitude coordinate |
| `longitude` | Float | Yes | Longitude coordinate |

**Response** (200 OK):
```json
{
  "success": true,
  "report_id": "GH-20260625120145",
  "analysis": {
    "category": "pothole",
    "category_confidence": 0.95,
    "severity_score": 4,
    "severity_description": "Deep pothole (5-10cm) on main road",
    "priority": "urgent",
    "coordinates": {
      "latitude": 28.6692,
      "longitude": 77.0669,
      "address_inferred": "Sector 7, Ghaziabad"
    },
    "is_duplicate": false,
    "duplicate_of_report_id": null,
    "reasoning": "Deep pothole on high-traffic main road, immediate safety hazard. Vehicle damage likely.",
    "estimated_resolution_days": 3,
    "recommended_action": "PWD emergency repair request",
    "public_notification": "A pothole in Sector 7 has been reported. Please exercise caution.",
    "confidence_overall": 0.92
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "error": "Missing required parameter: image",
  "code": "VALIDATION_ERROR"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "success": false,
  "error": "Grok API request failed",
  "code": "API_ERROR",
  "details": "Connection timeout"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/report \
  -F "image=@pothole.jpg" \
  -F "description=Large pothole on main road" \
  -F "latitude=28.6692" \
  -F "longitude=77.0669"
```

**Response Time**: 1-2 seconds (Grok API processing)

---

### 2. Get All Issues

**Endpoint**: `GET /api/issues`

**Description**: Fetch all reported issues with optional filtering.

**Request**:
```http
GET /api/issues?category=pothole&priority=urgent HTTP/1.1
Host: localhost:5000
```

**Query Parameters**:
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `category` | String | No | Filter by category | `pothole` |
| `priority` | String | No | Filter by priority | `urgent` |
| `limit` | Integer | No | Max results (default 100) | `50` |
| `offset` | Integer | No | Pagination offset (default 0) | `0` |
| `status` | String | No | Filter by status | `open` or `resolved` |

**Valid Categories**: `pothole`, `water_leak`, `streetlight`, `waste_management`, `other`

**Valid Priorities**: `urgent`, `high`, `medium`, `low`

**Response** (200 OK):
```json
[
  {
    "id": "GH-20260625120145",
    "timestamp": "2026-06-25T12:01:45.123456",
    "category": "pothole",
    "priority": "urgent",
    "severity_score": 4,
    "latitude": 28.6692,
    "longitude": 77.0669,
    "address": "Sector 7, Ghaziabad",
    "description": "Large pothole on main road",
    "reasoning": "Deep pothole on high-traffic road, safety hazard",
    "recommended_action": "PWD emergency repair",
    "image_url": "/uploads/2026-06-25T120145.jpg",
    "confidence": 0.92,
    "status": "open",
    "is_duplicate": false,
    "duplicate_of_id": null,
    "created_at": "2026-06-25T12:01:45",
    "resolved_at": null,
    "resolution_notes": null
  },
  {
    "id": "GH-20260625115030",
    "timestamp": "2026-06-25T11:50:30.654321",
    "category": "water_leak",
    "priority": "high",
    "severity_score": 3,
    "latitude": 28.6745,
    "longitude": 77.0750,
    "address": "Sector 9, Ghaziabad",
    "description": "Pipeline leak, water accumulating",
    "reasoning": "Active water loss, potential contamination risk",
    "recommended_action": "Water department inspection",
    "image_url": "/uploads/2026-06-25T115030.jpg",
    "confidence": 0.88,
    "status": "open",
    "is_duplicate": false,
    "duplicate_of_id": null,
    "created_at": "2026-06-25T11:50:30",
    "resolved_at": null,
    "resolution_notes": null
  }
]
```

**Example Requests**:
```bash
# Get all issues
curl http://localhost:5000/api/issues

# Get only urgent potholes
curl http://localhost:5000/api/issues?category=pothole&priority=urgent

# Get resolved issues
curl http://localhost:5000/api/issues?status=resolved

# Pagination: Get 50 issues starting from offset 100
curl http://localhost:5000/api/issues?limit=50&offset=100
```

**Response Time**: <200ms (database query)

---

### 3. Get Statistics

**Endpoint**: `GET /api/stats`

**Description**: Get summary statistics about all issues.

**Request**:
```http
GET /api/stats HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "total_issues": 47,
  "urgent_count": 3,
  "high_count": 12,
  "medium_count": 18,
  "low_count": 14,
  "by_category": {
    "pothole": 18,
    "water_leak": 12,
    "streetlight": 10,
    "waste_management": 5,
    "other": 2
  },
  "by_status": {
    "open": 39,
    "in_progress": 5,
    "resolved": 3
  },
  "resolved_percentage": 6.38,
  "average_resolution_days": 2.5,
  "duplicate_count": 5,
  "unique_locations_count": 42,
  "last_issue_reported": "2026-06-25T12:05:00",
  "timestamp": "2026-06-25T12:10:00"
}
```

**Example**:
```bash
curl http://localhost:5000/api/stats
```

**Response Time**: <100ms (aggregated query)

---

### 4. Get Predictions (Hotspot Forecast)

**Endpoint**: `GET /api/predict`

**Description**: Get AI predictions for high-risk areas in the next 7 days.

**Request**:
```http
GET /api/predict HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "forecast_window_days": 7,
  "high_risk_locations": [
    {
      "latitude": 28.6692,
      "longitude": 77.0669,
      "location_name": "Sector 7 Main Road",
      "category": "pothole",
      "confidence": 0.89,
      "reasoning": "3 potholes reported in this area in 7 days. Upcoming monsoon increases risk by 40%.",
      "risk_level": "high",
      "recommended_action": "Preventive maintenance + monitoring"
    },
    {
      "latitude": 28.6745,
      "longitude": 77.0750,
      "location_name": "Sector 9 Water Pipeline",
      "category": "water_leak",
      "confidence": 0.76,
      "reasoning": "Aging infrastructure. Recent water loss pattern detected. Season change increases stress.",
      "risk_level": "high",
      "recommended_action": "Infrastructure inspection + preventive repair"
    },
    {
      "latitude": 28.6600,
      "longitude": 77.0600,
      "location_name": "Sector 11 Street",
      "category": "streetlight",
      "confidence": 0.71,
      "reasoning": "2 streetlight failures in area. Electrical grid aging patterns detected.",
      "risk_level": "medium",
      "recommended_action": "Electrical audit + replacement planning"
    }
  ],
  "summary": "3 high-risk areas identified. Concentrated in Sectors 7, 9, 11. Primary risk: monsoon season + aging infrastructure.",
  "timestamp": "2026-06-25T12:10:00"
}
```

**Example**:
```bash
curl http://localhost:5000/api/predict
```

**Response Time**: 3-5 seconds (Grok API analysis)

---

### 5. Get Single Issue

**Endpoint**: `GET /api/issues/<report_id>`

**Description**: Fetch details of a specific issue.

**Request**:
```http
GET /api/issues/GH-20260625120145 HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "id": "GH-20260625120145",
  "timestamp": "2026-06-25T12:01:45.123456",
  "category": "pothole",
  "priority": "urgent",
  "severity_score": 4,
  "latitude": 28.6692,
  "longitude": 77.0669,
  "address": "Sector 7, Ghaziabad",
  "description": "Large pothole on main road",
  "reasoning": "Deep pothole on high-traffic road, safety hazard for vehicles and motorcycles",
  "recommended_action": "PWD emergency repair request",
  "image_url": "/uploads/2026-06-25T120145.jpg",
  "confidence": 0.92,
  "status": "open",
  "is_duplicate": false,
  "duplicate_of_id": null,
  "created_at": "2026-06-25T12:01:45",
  "resolved_at": null,
  "resolution_notes": null,
  "nearby_issues": [
    {
      "id": "GH-20260624150030",
      "category": "pothole",
      "distance_meters": 45,
      "priority": "high",
      "description": "Smaller pothole 45m away"
    }
  ]
}
```

**Error Response** (404 Not Found):
```json
{
  "success": false,
  "error": "Issue not found",
  "code": "NOT_FOUND"
}
```

**Example**:
```bash
curl http://localhost:5000/api/issues/GH-20260625120145
```

---

## 🔄 Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid parameters |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Grok API down |

---

## ⚠️ Error Handling

All errors return JSON with this format:

```json
{
  "success": false,
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": "Additional context (optional)"
}
```

**Common Errors**:
- `VALIDATION_ERROR` — Missing/invalid parameters
- `API_ERROR` — Grok API request failed
- `DATABASE_ERROR` — Database operation failed
- `FILE_ERROR` — Image upload failed
- `RATE_LIMIT_ERROR` — Too many requests
- `NOT_FOUND` — Resource doesn't exist

---

## 🔐 Rate Limiting

- **Limit**: 60 requests per minute per IP
- **Reset**: 1 minute sliding window
- **Header**: `X-RateLimit-Remaining` in response

If limit exceeded:
```json
{
  "success": false,
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_ERROR",
  "retry_after_seconds": 30
}
```

---

## 📊 Data Types

### Issue Object
```json
{
  "id": "GH-20260625120145",           // Unique report ID
  "timestamp": "2026-06-25T12:01:45",  // ISO 8601 datetime
  "category": "pothole",               // Issue category
  "priority": "urgent",                // Priority level
  "severity_score": 4,                 // 1-5 scale
  "latitude": 28.6692,                 // Float coordinate
  "longitude": 77.0669,                // Float coordinate
  "address": "Sector 7, Ghaziabad",   // Location name
  "description": "...",                // Citizen description
  "reasoning": "...",                  // AI analysis
  "recommended_action": "...",         // Suggested next step
  "image_url": "/uploads/file.jpg",   // Image path
  "confidence": 0.92,                  // 0-1 confidence score
  "status": "open",                    // open/in_progress/resolved
  "is_duplicate": false,               // Duplicate flag
  "duplicate_of_id": null,             // Parent issue ID if duplicate
  "created_at": "2026-06-25T12:01:45",// Creation time
  "resolved_at": null,                 // Resolution time
  "resolution_notes": null             // Authority notes
}
```

### Analysis Object
```json
{
  "category": "pothole",               // Issue type
  "category_confidence": 0.95,         // Classification confidence
  "severity_score": 4,                 // 1-5 severity
  "priority": "urgent",                // Priority level
  "confidence_overall": 0.92,          // Overall confidence
  "reasoning": "...",                  // Explanation
  "recommended_action": "...",         // Next step
  "estimated_resolution_days": 3,      // Estimate
  "is_duplicate": false,               // Duplicate check
  "coordinates": { ... }               // Location info
}
```

---

## 🧪 Testing

### Using cURL

```bash
# Report issue
curl -X POST http://localhost:5000/api/report \
  -F "image=@test.jpg" \
  -F "description=Test pothole" \
  -F "latitude=28.6692" \
  -F "longitude=77.0669"

# Get all issues
curl http://localhost:5000/api/issues

# Get stats
curl http://localhost:5000/api/stats

# Get predictions
curl http://localhost:5000/api/predict
```

### Using Python

```python
import requests

# Report issue
with open('pothole.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/report',
        files={'image': f},
        data={
            'description': 'Large pothole',
            'latitude': 28.6692,
            'longitude': 77.0669
        }
    )
print(response.json())

# Get issues
response = requests.get('http://localhost:5000/api/issues?priority=urgent')
print(response.json())

# Get stats
response = requests.get('http://localhost:5000/api/stats')
print(response.json())
```

### Using JavaScript

```javascript
// Report issue
const formData = new FormData();
formData.append('image', document.querySelector('input[type=file]').files[0]);
formData.append('description', 'Large pothole');
formData.append('latitude', 28.6692);
formData.append('longitude', 77.0669);

fetch('http://localhost:5000/api/report', {
  method: 'POST',
  body: formData
})
.then(r => r.json())
.then(data => console.log(data));

// Get all issues
fetch('http://localhost:5000/api/issues')
  .then(r => r.json())
  .then(data => console.log(data));

// Get stats
fetch('http://localhost:5000/api/stats')
  .then(r => r.json())
  .then(data => console.log(data));
```

---

**Last Updated**: June 25, 2026  
**API Version**: 1.0  
**Status**: Production Ready ✅
