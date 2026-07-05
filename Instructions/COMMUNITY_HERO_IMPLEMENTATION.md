# Community Hero - Hyperlocal Problem Solver
## Implementation Guide & Agentic AI Architecture

**Submission Target**: vibe2ship vibe Coding Hackathon  
**Problem Statement**: Build a platform enabling citizens to identify, report, validate, track, and resolve community issues (potholes, water leaks, damaged streetlights, waste management) through collaboration, data intelligence, and agentic automation.

**Evaluation Weights**:
- Problem Solving & Impact: 20%
- Agentic Depth: 20%
- Innovation & Creativity: 20%
- Google Technologies: 15%
- Product Experience & Design: 10%
- Technical Implementation: 10%
- Completeness & Usability: 5%

---

## 📋 Executive Summary

**Vision**: An AI-powered civic engagement platform where citizens report local issues via photo + description, and an autonomous Claude-powered agent intelligently categorizes, geolocates, prioritizes, and routes issues to resolution workflows — without human intervention.

**Core MVP**: 3-day delivery focusing on **agentic depth** (the differentiator) over flashy UI.

**Key Differentiator**: Autonomous issue triage agent that reasons about context (weather, location history, image analysis) to predict criticality and recommend action, not just categorize.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CITIZEN (Frontend)                        │
│  - Report form (image + description + geomark)              │
│  - Real-time issue map & tracker                            │
│  - Impact dashboard                                          │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP/REST
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND API (Python/Node)                 │
│  - Issue storage & retrieval                                │
│  - Image upload handling (Google Drive/Sheets)              │
│  - Route to agentic loop                                    │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│           AGENTIC LOOP (Claude API via Anthropic)           │
│                                                              │
│  1. Receive: Issue report (image, description, location)   │
│  2. Analyze:                                                 │
│     - Image analysis (damage severity from photo)           │
│     - Description parsing (category extraction)             │
│     - Location context (nearby infrastructure, history)     │
│  3. Reason:                                                  │
│     - Is this a duplicate? (check location + category)     │
│     - What's the actual priority? (severity + impact)       │
│     - Should we escalate? (safety-critical?)                │
│  4. Output: Structured JSON                                 │
│     {                                                        │
│       category: "pothole" | "water_leak" | "streetlight"   │
│       severity: 1-5,                                         │
│       priority: "urgent" | "high" | "medium" | "low",       │
│       coordinates: {lat, lng},                              │
│       confidence: 0.7-0.99,                                 │
│       reasoning: "...",                                      │
│       recommended_action: "..."                             │
│     }                                                        │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA LAYER (Google Sheets)                │
│  - All issues stored in public Sheets for transparency      │
│  - Real-time update from agent                              │
│  - Historical tracking for analytics                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: HTML5 + Vanilla JS (zero-dependency, ships fast)
- **Mapping**: Google Maps API (Embedded + Places API for address validation)
- **Images**: Drag-drop file input → Base64 → Anthropic API for vision analysis
- **Storage**: Local IndexedDB for offline queue (optional, MVP can be online-only)

### Backend (Choose ONE)
#### Option A: Python (Recommended for speed)
- **Framework**: Flask or FastAPI (lightweight, perfect for MVP)
- **Anthropic SDK**: `anthropic>=1.0.0`
- **Image Processing**: PIL/Pillow for resizing before upload
- **Google Sheets**: `gspread` + service account for direct integration

#### Option B: Node.js (If you prefer JS)
- **Framework**: Express.js
- **Anthropic SDK**: `@anthropic-ai/sdk`
- **Google Sheets**: `google-spreadsheet` npm package

### Data Storage
- **Primary**: Google Sheets (free, auditable, no auth headaches, shared access for judges)
- **Backup**: SQLite for local dev (easy migration to Sheets)
- **Images**: Google Drive (via API or embed Base64 directly in Sheets for MVP)

### APIs
- **Anthropic Claude API** (Required): https://api.anthropic.com/v1/messages
  - Model: `claude-opus-4-6` (for extended thinking & vision)
  - Vision capability for image analysis
  - Tool use for structured output
- **Google Maps API**: Geocoding + map display
- **Google Sheets API**: Direct write access (structured issue log)

---

## 📱 MVP Feature Breakdown

### Phase 1: Core Agentic Loop (Day 1 - 4–6 hours)

**Goal**: Build the agent, test with 5 real reports.

#### 1.1 Anthropic API Agentic Prompt

This is the **brain** of the system. Claude receives unstructured issue data and returns structured decisions.

```python
# backend/agent.py
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """
You are an autonomous civic issue triage agent for Ghaziabad, Uttar Pradesh, India.

Your role:
- Analyze citizen reports (photo + description + location)
- Determine issue category, severity, and priority
- Predict impact and recommend action
- Flag safety-critical issues for immediate escalation

Context about Ghaziabad:
- Population: ~1.7M
- Known hotspots: Sector 7-11 (infrastructure), NH-119 corridor (potholes)
- Monsoon (Jun-Sep): Water leaks peak, potholes increase
- Current season: [INJECT CURRENT SEASON]

Your analysis process (always follow this):

1. IMAGE ANALYSIS:
   - What type of damage is visible? (pothole depth, water accumulation, electrical hazard, etc.)
   - Severity score: 1 (minor cosmetic) to 5 (immediate safety risk)
   - Confidence in severity: percentage

2. CATEGORY CLASSIFICATION:
   - Pothole (road damage)
   - Water leak (pipeline/sewage)
   - Streetlight (electrical/lighting)
   - Waste management (debris, trash accumulation)
   - Other (with explanation)

3. PRIORITY DETERMINATION:
   - URGENT: Immediate safety risk (exposed wiring, major water loss, deep pothole on main road)
   - HIGH: Significant inconvenience (partial blockage, affecting >100 people/day)
   - MEDIUM: Noticeable but manageable (cosmetic pothole, minor leak)
   - LOW: Tracked but not immediate (informational, monitoring)

4. DUPLICATE DETECTION:
   - Compare against recent reports (last 7 days) within 50m radius
   - If duplicate: merge with existing report

5. REASONING & ACTION:
   - Why did you assign this priority?
   - What action should be taken next? (Public notification, Authority escalation, Monitoring)
   - Estimated resolution time (days)

Output ONLY valid JSON (no markdown, no preamble):
{
  "category": "pothole|water_leak|streetlight|waste_management|other",
  "category_confidence": 0.95,
  "severity_score": 3,
  "severity_description": "Medium pothole (5-10cm depth) on secondary road",
  "priority": "urgent|high|medium|low",
  "coordinates": {
    "latitude": 28.7349,
    "longitude": 77.0674,
    "address_inferred": "Sector 7, Ghaziabad"
  },
  "is_duplicate": false,
  "duplicate_of_report_id": null,
  "reasoning": "...",
  "estimated_resolution_days": 7,
  "recommended_action": "Authority escalation via PWD",
  "public_notification": "A pothole in Sector 7 has been reported. Please avoid the area.",
  "confidence_overall": 0.92
}
"""

def analyze_issue(image_base64: str, description: str, lat: float, lng: float, recent_reports: list) -> dict:
    """
    Send issue to Claude agent for analysis.
    
    Args:
        image_base64: Base64-encoded image
        description: Citizen's text description
        lat, lng: Coordinates from map
        recent_reports: List of last 7 days' reports for duplicate detection
    
    Returns:
        Structured JSON response from agent
    """
    
    user_message = f"""
Analyze this civic issue report:

PHOTO: [Attached image]
DESCRIPTION: {description}
LOCATION: {lat}, {lng}
RECENT_REPORTS_NEARBY: {recent_reports}

Return ONLY JSON.
"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": user_message
                    }
                ],
            }
        ],
    )
    
    # Parse JSON from response
    import json
    result_text = response.content[0].text.strip()
    
    # Remove markdown code blocks if present
    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
        if result_text.startswith("json"):
            result_text = result_text[4:]
    
    return json.loads(result_text)
```

#### 1.2 Backend API (Flask example)

```python
# backend/app.py
from flask import Flask, request, jsonify
import base64
from agent import analyze_issue
from google_sheets import save_to_sheets, get_recent_reports

app = Flask(__name__)

@app.route('/api/report', methods=['POST'])
def create_report():
    """Receive issue report, run agent, save to sheets."""
    
    data = request.json
    image_file = request.files.get('image')
    
    # Convert image to base64
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Get recent reports for context
    recent = get_recent_reports(
        latitude=data['latitude'],
        longitude=data['longitude'],
        days=7,
        radius_meters=50
    )
    
    # Run agentic analysis
    analysis = analyze_issue(
        image_base64=image_base64,
        description=data['description'],
        lat=data['latitude'],
        lng=data['longitude'],
        recent_reports=recent
    )
    
    # Save to Google Sheets
    report_id = save_to_sheets(
        analysis=analysis,
        image_url=image_file.filename,  # or upload to Drive
        timestamp=datetime.now().isoformat()
    )
    
    return jsonify({
        'success': True,
        'report_id': report_id,
        'analysis': analysis
    })

@app.route('/api/issues', methods=['GET'])
def get_issues():
    """Fetch all issues, optionally filtered."""
    category = request.args.get('category')
    priority = request.args.get('priority')
    
    issues = get_from_sheets(category=category, priority=priority)
    return jsonify(issues)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

#### 1.3 Google Sheets Integration

```python
# backend/google_sheets.py
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Load service account JSON (download from Google Cloud Console)
creds = Credentials.from_service_account_file(
    'service_account.json', scopes=SCOPES)
client = gspread.authorize(creds)

# Open shared Google Sheet
sheet = client.open('Community Hero - Issues').worksheet('Reports')

def save_to_sheets(analysis: dict, image_url: str, timestamp: str) -> str:
    """Save analyzed issue to Google Sheets."""
    
    row = [
        timestamp,
        analysis['category'],
        analysis['priority'],
        analysis['severity_score'],
        analysis['coordinates']['latitude'],
        analysis['coordinates']['longitude'],
        analysis['coordinates']['address_inferred'],
        analysis['reasoning'],
        analysis['recommended_action'],
        image_url,
        analysis['confidence_overall'],
        'open'  # status
    ]
    
    sheet.append_row(row)
    report_id = f"GH-{timestamp.replace('.', '').replace(':', '').replace('-', '')}"
    
    return report_id

def get_recent_reports(latitude: float, longitude: float, days: int = 7, radius_meters: int = 50) -> list:
    """Fetch reports near a location for duplicate detection."""
    
    all_reports = sheet.get_all_records()
    recent = []
    
    from datetime import datetime, timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    for report in all_reports:
        report_time = datetime.fromisoformat(report['Timestamp'])
        if report_time < cutoff:
            continue
        
        # Simple distance check (rough; use geopy for accuracy)
        report_lat = float(report['Latitude'])
        report_lng = float(report['Longitude'])
        
        distance = ((latitude - report_lat)**2 + (longitude - report_lng)**2)**0.5 * 111000  # rough km to m
        
        if distance < radius_meters:
            recent.append({
                'id': report.get('Report ID'),
                'category': report['Category'],
                'priority': report['Priority'],
                'distance_meters': distance
            })
    
    return recent
```

**Test Phase 1**: Create 5 test reports manually (use real Ghaziabad coordinates, real-looking pothole photos from online). Verify agent categorizes correctly and outputs valid JSON.

---

### Phase 2: Frontend Dashboard (Day 1–2, 4–6 hours)

**Goal**: Single-file HTML that loads issues from backend and displays them on a map + list.

#### 2.1 Single-File HTML Dashboard

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Community Hero - Ghaziabad Civic Issues</title>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&libraries=marker"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }

        header p {
            font-size: 13px;
            opacity: 0.9;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
        }

        .section {
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .section-title {
            padding: 16px;
            background: #f9f9f9;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 600;
            color: #333;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        #map {
            flex: 1;
            min-height: 500px;
        }

        .issues-list {
            flex: 1;
            overflow-y: auto;
            max-height: 600px;
        }

        .issue-card {
            padding: 14px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background 0.2s;
            border-left: 4px solid #ccc;
        }

        .issue-card:hover {
            background: #f9f9f9;
        }

        .issue-card.urgent {
            border-left-color: #e74c3c;
            background: #fdf5f5;
        }

        .issue-card.high {
            border-left-color: #f39c12;
            background: #fffaf5;
        }

        .issue-card.medium {
            border-left-color: #3498db;
            background: #f5f9ff;
        }

        .issue-card.low {
            border-left-color: #27ae60;
            background: #f5fff5;
        }

        .issue-category {
            display: inline-block;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 4px;
            background: #e8e8e8;
            color: #333;
            margin-bottom: 6px;
            text-transform: capitalize;
        }

        .issue-priority {
            display: inline-block;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 4px;
            margin-left: 6px;
            text-transform: uppercase;
        }

        .issue-priority.urgent {
            background: #e74c3c;
            color: white;
        }

        .issue-priority.high {
            background: #f39c12;
            color: white;
        }

        .issue-priority.medium {
            background: #3498db;
            color: white;
        }

        .issue-priority.low {
            background: #27ae60;
            color: white;
        }

        .issue-description {
            font-size: 13px;
            color: #555;
            margin: 6px 0;
            line-height: 1.4;
        }

        .issue-location {
            font-size: 12px;
            color: #999;
            margin-top: 6px;
        }

        .issue-card.selected {
            background: #f0f7ff;
            border-left-width: 6px;
        }

        .report-form {
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        }

        .form-group {
            margin-bottom: 16px;
        }

        label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 6px;
            color: #333;
        }

        input[type="text"],
        textarea,
        select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 13px;
            font-family: inherit;
        }

        textarea {
            resize: vertical;
            min-height: 80px;
        }

        input[type="file"] {
            padding: 8px;
        }

        button {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }

        button:hover {
            background: #764ba2;
        }

        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #999;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            padding: 16px;
            background: #f9f9f9;
            border-bottom: 1px solid #e0e0e0;
        }

        .stat {
            text-align: center;
        }

        .stat-value {
            font-size: 20px;
            font-weight: 700;
            color: #667eea;
        }

        .stat-label {
            font-size: 11px;
            color: #999;
            margin-top: 4px;
            text-transform: uppercase;
        }

        @media (max-width: 900px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>🏛️ Community Hero</h1>
        <p>AI-Powered Civic Issue Tracking for Ghaziabad</p>
    </header>

    <div class="container">
        <!-- Map Section -->
        <div class="section">
            <div class="section-title">Issue Map</div>
            <div id="map"></div>
        </div>

        <!-- Issues List -->
        <div class="section">
            <div class="stats" id="stats">
                <div class="stat">
                    <div class="stat-value" id="total-issues">0</div>
                    <div class="stat-label">Total Issues</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="urgent-count">0</div>
                    <div class="stat-label">Urgent</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="high-count">0</div>
                    <div class="stat-label">High</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="resolution-rate">0%</div>
                    <div class="stat-label">Resolved</div>
                </div>
            </div>
            <div class="section-title">Recent Issues</div>
            <div class="issues-list" id="issues-list">
                <div class="loading" id="loading">Loading issues...</div>
            </div>
        </div>
    </div>

    <!-- Report Form Modal -->
    <div id="modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:1000;overflow:auto;">
        <div class="report-form" style="margin:40px auto;max-width:500px;">
            <h2 style="margin-bottom:20px;">Report a Civic Issue</h2>
            <form id="report-form">
                <div class="form-group">
                    <label>Photo of Issue</label>
                    <input type="file" id="image" accept="image/*" required>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="description" placeholder="Describe the issue in detail..." required></textarea>
                </div>
                <div class="form-group">
                    <label>Location Address</label>
                    <input type="text" id="address" placeholder="e.g., Sector 7, Ghaziabad" required>
                </div>
                <div class="form-group">
                    <label>Latitude</label>
                    <input type="number" id="latitude" step="0.0001" required>
                </div>
                <div class="form-group">
                    <label>Longitude</label>
                    <input type="number" id="longitude" step="0.0001" required>
                </div>
                <button type="submit" id="submit-btn">Submit Report</button>
            </form>
        </div>
    </div>

    <script>
        const BACKEND_URL = 'http://localhost:5000';
        const GHAZIABAD_CENTER = { lat: 28.6692, lng: 77.0669 };

        let map;
        let markers = [];
        let issues = [];

        // Initialize map
        function initMap() {
            map = new google.maps.Map(document.getElementById('map'), {
                zoom: 13,
                center: GHAZIABAD_CENTER,
                mapTypeControl: true,
                fullscreenControl: true,
            });

            map.addListener('click', (event) => {
                document.getElementById('latitude').value = event.latLng.lat();
                document.getElementById('longitude').value = event.latLng.lng();
                document.getElementById('modal').style.display = 'block';
            });

            loadIssues();
        }

        function loadIssues() {
            fetch(`${BACKEND_URL}/api/issues`)
                .then(res => res.json())
                .then(data => {
                    issues = data;
                    renderIssues();
                    updateStats();
                    renderMarkers();
                })
                .catch(err => console.error('Error loading issues:', err));
        }

        function renderIssues() {
            const list = document.getElementById('issues-list');
            list.innerHTML = '';

            issues.forEach(issue => {
                const card = document.createElement('div');
                card.className = `issue-card ${issue.priority}`;
                card.innerHTML = `
                    <div>
                        <span class="issue-category">${issue.category}</span>
                        <span class="issue-priority ${issue.priority}">${issue.priority}</span>
                    </div>
                    <div class="issue-description">${issue.description || issue.reasoning}</div>
                    <div class="issue-location">📍 ${issue.address}</div>
                `;
                card.addEventListener('click', () => {
                    centerMapOnIssue(issue);
                });
                list.appendChild(card);
            });
        }

        function renderMarkers() {
            markers.forEach(m => m.setMap(null));
            markers = [];

            const colors = {
                urgent: '#e74c3c',
                high: '#f39c12',
                medium: '#3498db',
                low: '#27ae60'
            };

            issues.forEach(issue => {
                const marker = new google.maps.Marker({
                    position: {
                        lat: parseFloat(issue.latitude),
                        lng: parseFloat(issue.longitude)
                    },
                    map: map,
                    title: issue.category,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 10,
                        fillColor: colors[issue.priority],
                        fillOpacity: 0.8,
                        strokeColor: '#fff',
                        strokeWeight: 2
                    }
                });

                marker.addListener('click', () => {
                    const infoWindow = new google.maps.InfoWindow({
                        content: `<div style="padding:8px;"><strong>${issue.category}</strong><br>${issue.address}</div>`
                    });
                    infoWindow.open(map, marker);
                });

                markers.push(marker);
            });
        }

        function centerMapOnIssue(issue) {
            map.setCenter({
                lat: parseFloat(issue.latitude),
                lng: parseFloat(issue.longitude)
            });
            map.setZoom(16);
        }

        function updateStats() {
            const total = issues.length;
            const urgent = issues.filter(i => i.priority === 'urgent').length;
            const high = issues.filter(i => i.priority === 'high').length;
            const resolved = issues.filter(i => i.status === 'resolved').length;

            document.getElementById('total-issues').textContent = total;
            document.getElementById('urgent-count').textContent = urgent;
            document.getElementById('high-count').textContent = high;
            document.getElementById('resolution-rate').textContent = total > 0 ? Math.round((resolved / total) * 100) : 0 + '%';
        }

        // Form submission
        document.getElementById('report-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData();
            formData.append('image', document.getElementById('image').files[0]);
            formData.append('description', document.getElementById('description').value);
            formData.append('latitude', parseFloat(document.getElementById('latitude').value));
            formData.append('longitude', parseFloat(document.getElementById('longitude').value));

            const submitBtn = document.getElementById('submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Analyzing...';

            try {
                const response = await fetch(`${BACKEND_URL}/api/report`, {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.success) {
                    alert('Report submitted! Agent analysis: ' + result.analysis.priority);
                    document.getElementById('modal').style.display = 'none';
                    document.getElementById('report-form').reset();
                    loadIssues();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (err) {
                alert('Error submitting report: ' + err.message);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Report';
            }
        });

        // Close modal
        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target === document.getElementById('modal')) {
                document.getElementById('modal').style.display = 'none';
            }
        });

        // Initialize on page load
        window.addEventListener('load', initMap);
    </script>
</body>
</html>
```

**Deploy**: Save as `dashboard.html`, open in browser, connect to backend.

---

### Phase 3: Polish & Differentiators (Day 2–3)

#### 3.1 Extended Thinking Prompt (Agentic Depth)

Claude's extended thinking capability allows the agent to "reason out loud" before responding — judges love seeing this.

```python
# Add to agent.py
def analyze_issue_with_thinking(image_base64: str, description: str, lat: float, lng: float, recent_reports: list) -> dict:
    """Use extended thinking for deeper reasoning."""
    
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=16000,  # Allow more tokens for thinking
        thinking={
            "type": "enabled",
            "budget_tokens": 10000  # Allocate 10k tokens to thinking
        },
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"""Analyze this civic issue with extended thinking.

Photo Analysis:
- What hazards are visible?
- Estimate severity (1-5)
- Consider seasonal factors

Reasoning:
- Is this a duplicate?
- What's the actual citizen impact?
- Should this be escalated?

Output: Valid JSON only"""
                    }
                ],
            }
        ],
    )
    
    # Extract thinking + response
    thinking = ""
    response_text = ""
    
    for block in response.content:
        if block.type == "thinking":
            thinking = block.thinking
        elif block.type == "text":
            response_text = block.text
    
    # Log thinking for transparency
    print(f"Agent Reasoning:\n{thinking}\n")
    
    return json.loads(response_text)
```

#### 3.2 Prediction Layer (Innovation Bonus)

Add a secondary agent that predicts future issues based on patterns.

```python
# backend/predictor.py
def predict_hotspots() -> list:
    """Predict which areas will have issues in next 7 days."""
    
    all_reports = get_from_sheets()
    
    # Group by location + category
    patterns = {}
    for report in all_reports:
        key = (report['latitude'], report['longitude'], report['category'])
        if key not in patterns:
            patterns[key] = []
        patterns[key].append(report)
    
    # Find hotspots (3+ reports in 7 days)
    hotspots = [loc for loc, reports in patterns.items() if len(reports) >= 3]
    
    # Use agent to predict
    prediction_prompt = f"""
    Based on these reported hotspots in Ghaziabad:
    {hotspots}
    
    Predict which other locations are at high risk for issues in the next 7 days.
    Consider: seasonality, infrastructure age, weather patterns.
    
    Return JSON:
    {{
      "high_risk_locations": [
        {{"lat": ..., "lng": ..., "category": "...", "confidence": 0.9, "reason": "..."}}
      ]
    }}
    """
    
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prediction_prompt}]
    )
    
    return json.loads(response.content[0].text)
```

#### 3.3 Voice Input (Optional UI Boost)

Add voice reporting for accessibility.

```javascript
// In dashboard.html, add to form:
<div class="form-group">
    <label>Or Record a Voice Report</label>
    <button type="button" id="voice-btn" style="background:#667eea;">🎤 Start Recording</button>
</div>

<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-IN';

document.getElementById('voice-btn').addEventListener('click', () => {
    recognition.start();
});

recognition.addEventListener('result', (event) => {
    const text = event.results[0][0].transcript;
    document.getElementById('description').value = text;
});
</script>
```

---

## 📊 Submission Checklist

### Code Deliverables
- [ ] `backend/agent.py` — Agentic analysis loop (extended thinking)
- [ ] `backend/app.py` — Flask API
- [ ] `backend/google_sheets.py` — Data storage
- [ ] `dashboard.html` — Single-file frontend
- [ ] `requirements.txt` — Dependencies
- [ ] `service_account.json` — Google Sheets auth (in `.gitignore`)

### Data & Setup
- [ ] Google Sheets created & shared publicly (judges can view live data)
- [ ] Google Maps API key configured
- [ ] Anthropic API key set in environment
- [ ] 5–10 real test reports with actual Ghaziabad locations
- [ ] Docker Compose file for local dev (optional but impressive)

### Demo & Documentation
- [ ] 2-minute video walkthrough (agent analysis → map → dashboard)
- [ ] README with setup instructions
- [ ] API documentation (endpoints, schemas)
- [ ] Agent reasoning samples (show extended thinking output)
- [ ] Performance metrics (agent accuracy, response time)

### Evaluation Evidence
| Criterion | How to Win |
|-----------|-----------|
| Problem Solving & Impact | Autonomous agent resolves issues without human review |
| Agentic Depth | Use extended thinking, show reasoning, implement duplicate detection |
| Innovation | Prediction layer + voice input |
| Google Tech | Maps + Sheets integration, live public access |
| Product Experience | Clean UI, real-time updates, impact stats |
| Technical Impl. | Clean code, error handling, modular architecture |
| Completeness | Full workflow (report → analysis → storage → display) |

---

## 🔗 Recommended MCP Connectors for UI Enhancement

Since you mentioned using an AI assistant to build the frontend, integrate these MCP connectors to make the development smoother and UI more polished:

### 1. **Google Drive MCP** (Already in your environment)
- **Use Case**: Store and retrieve issue photos directly in Google Drive folders
- **Integration Point**: When a citizen uploads a photo, auto-organize by category (Pothole/WaterLeak/etc) in Drive
- **Benefit**: Judges can audit all submitted images; transparent data storage

```python
# Add to backend
from google.colab import auth
from googleapiclient.discovery import build

drive = build('drive', 'v3')

# Auto-create folder structure
category_folder = drive.files().list(
    q=f"name='CommunityHero-{category}' and mimeType='application/vnd.google-apps.folder'",
    spaces='drive'
).execute()
```

### 2. **Google Sheets MCP** (Recommended upgrade)
- **Use Case**: Real-time sheet updates instead of manual API calls
- **Integration Point**: Agent writes directly to Sheets; dashboard fetches via API
- **Benefit**: Easier debugging, judges see raw data in real-time

### 3. **GitHub MCP** (For version control)
- **Use Case**: Auto-commit changes, track iteration history
- **Integration Point**: Claude commits agent improvements, test results
- **Benefit**: Shows judges your development process

### 4. **Web Search MCP** (Optional for context)
- **Use Case**: Agent can search for news about Ghaziabad infrastructure to add context
- **Integration Point**: When analyzing high-priority issues, agent searches for related news
- **Benefit**: Adds real-world intelligence to predictions

---

## 🚀 Deployment Options (Demo Day Ready)

### Option A: Local + Ngrok (Fastest)
```bash
python backend/app.py
ngrok http 5000
# Share ngrok URL in demo
```

### Option B: Heroku (Free tier ending soon)
```bash
heroku create community-hero-app
heroku config:set ANTHROPIC_API_KEY=sk-...
git push heroku main
```

### Option C: Vercel + Serverless (Recommended)
```bash
# Frontend: Vercel (dashboard.html)
vercel deploy

# Backend: Vercel Functions (Python)
# Deploy agent.py as /api/analyze endpoint
```

---

## 📝 Prompts to Pass to Your AI Assistant (Claude)

When building with Claude API artifacts, use these structured prompts:

### Prompt 1: Build Backend
```
Build a Python Flask API with these requirements:

1. POST /api/report
   - Accept FormData with: image (file), description (text), latitude (float), longitude (float)
   - Call Claude Anthropic API with vision capabilities
   - Use this system prompt: [PASTE SYSTEM_PROMPT from agent.py above]
   - Return JSON response with category, priority, severity, coordinates

2. GET /api/issues
   - Query parameters: category, priority, limit
   - Return all issues from Google Sheets

3. Use Google Sheets API (gspread) for data persistence
   - Append rows with: timestamp, category, priority, severity, lat, lng, address, reasoning, action, status

Include error handling, CORS headers, and logging.
Model: claude-opus-4-6
```

### Prompt 2: Build Frontend Dashboard
```
Build a single-file HTML dashboard that:

1. Displays Google Maps centered on Ghaziabad (28.6692, 77.0669)
2. Shows markers for all issues from /api/issues endpoint
   - Color-coded by priority: red (urgent), orange (high), blue (medium), green (low)
   - Clicking marker shows infowindow with category + address
   
3. Right sidebar lists all issues in a scrollable list
   - Each issue card shows category, priority, description, location
   - Clicking card centers map on that issue
   
4. Top stats panel shows:
   - Total issues
   - Urgent count
   - High count
   - % resolved

5. Click on map to open a report form:
   - File input for image
   - Text input for description
   - Lat/lng inputs (or auto-fill from click location)
   - Submit button calls POST /api/report

6. Styling: Modern, clean, responsive
   - Purple gradient header
   - White cards with subtle shadows
   - Color-coded priority badges

No external UI libraries (just vanilla JS + Maps API).
```

### Prompt 3: Agentic Reasoning
```
Enhance the agent analysis with extended thinking:

1. Add thinking capability to Claude API call (budget_tokens: 10000)
2. Have Claude reason through:
   - What hazards are visible in the image?
   - Is this a duplicate of recent reports?
   - What's the actual citizen impact?
   - Should this be escalated for immediate action?
3. Respond with a JSON object containing:
   - category, severity_score, priority
   - is_duplicate, confidence_overall
   - reasoning (explanation of the agent's logic)
   
Use model: claude-opus-4-6 with thinking enabled.
```

---

## ⏱️ Timeline & Task Breakdown

### Day 1 (Today)
- [ ] **2 hours**: Set up Python/Flask backend skeleton + Google Sheets auth
- [ ] **2 hours**: Implement agent.py with Anthropic Claude API integration
- [ ] **2 hours**: Test agent with 5 real Ghaziabad test cases
- **Deliverable**: Working `/api/report` endpoint that analyzes images & returns JSON

### Day 2
- [ ] **3 hours**: Build dashboard.html with map + issues list
- [ ] **1 hour**: Connect dashboard to backend API
- [ ] **1 hour**: Deploy to Vercel/Ngrok for live demo
- [ ] **1 hour**: Add extended thinking for agentic reasoning
- **Deliverable**: Fully functional end-to-end system

### Day 3
- [ ] **1 hour**: Build prediction layer (optional, +5–10 points)
- [ ] **1 hour**: Add voice input (optional, +5 points)
- [ ] **1 hour**: Polish UI, add animations
- [ ] **1 hour**: Record demo video
- **Deliverable**: Submission-ready with all bonus features

---

## 🎯 Winning Strategy Summary

1. **Agentic Depth**: Use extended thinking visibly. Judges want to see the agent *reasoning*, not just pattern-matching.
2. **Real Data**: Use actual Ghaziabad locations (your hometown!). Make it feel authentic.
3. **Autonomous Workflow**: No human in the loop. Agent decides category + priority + action. That's the differentiator.
4. **Clean Code**: Focus on clarity over flashiness. Good architecture beats CSS animations.
5. **Demo Clarity**: 2-minute video showing: upload photo → agent analyzes → issue appears on map + stats update.

---

## 📚 Resources

- Anthropic API Docs: https://docs.anthropic.com
- Claude Vision Guide: https://docs.anthropic.com/en/docs/vision
- Google Maps API: https://developers.google.com/maps
- Google Sheets API: https://developers.google.com/sheets/api
- Flask Quickstart: https://flask.palletsprojects.com/quickstart/

---

**Last Updated**: June 25, 2026  
**Version**: 1.0 (MVP Ready)

Good luck with the hackathon! 🚀
