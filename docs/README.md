# Community Hero — AI-Powered Civic Issue Tracker

> **Hackathon**: vibe2ship Vibe Coding Hackathon  
> **Track**: Agentic AI + Google Technologies  
> **Target Score**: 90–95/100

---

## 🏛️ What is Community Hero?

Community Hero is an autonomous civic engagement platform where citizens of Ghaziabad report local infrastructure issues — potholes, water leaks, broken streetlights, waste management — via **photo + description**, and a **Claude-powered AI agent** intelligently categorizes, prioritizes, and routes them to resolution workflows, _without any human intervention_.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **🤖 Agentic Analysis** | Claude Opus analyzes issue photos using vision + extended thinking |
| **🗺️ Real-time Map** | Google Maps with color-coded markers (urgent/high/medium/low) |
| **📊 Live Stats** | Auto-refreshing dashboard with issue counts and resolution rate |
| **🧠 Extended Thinking** | Agent reasons about severity, duplicates, and escalation |
| **🔮 Predictions** | AI predicts future hotspots based on 7-day patterns |
| **🎤 Voice Input** | Record descriptions using Web Speech API (en-IN) |
| **📋 Google Sheets** | All data stored publicly for full transparency |
| **🔍 Duplicate Detection** | 50m radius, 7-day window deduplication |

---

## 🏗️ Architecture

```
Citizen (Browser)
      │ HTTP/REST (multipart form)
      ▼
Flask Backend (Python)
      │
      ├── agent.py ──────────► Claude Opus 4 (Vision + Extended Thinking)
      │                              │
      │                         JSON Analysis
      │                              │
      ├── google_sheets.py ◄──────────
      │         │
      │    Sheets API
      │         ▼
      │   Google Sheets (public)
      │
      └── predictor.py ────────► Claude (hotspot predictions)
```

---

## 🛠️ Tech Stack

- **Backend**: Python Flask + `anthropic` SDK
- **AI**: Claude Opus 4.5 (vision + extended thinking)
- **Data**: Google Sheets via `gspread`
- **Frontend**: HTML5 + Vanilla JS + Google Maps API
- **Auth**: Google Service Account
- **Deployment**: Local (Flask) + Ngrok / Vercel

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
pip install -r backend/requirements.txt
```

### 2. Environment Variables

```bash
cp .env.example .env
# Fill in your keys:
# - ANTHROPIC_API_KEY
# - GOOGLE_SHEETS_ID
# - GOOGLE_MAPS_API_KEY (in frontend/dashboard.html)
# - GOOGLE_APPLICATION_CREDENTIALS (path to service_account.json)
```

### 3. Google Cloud Setup

1. Create a Google Cloud project
2. Enable **Sheets API** and **Drive API**
3. Create a **Service Account** → download `service_account.json`
4. Create a Google Sheet: **"Community Hero - Issues"**
5. Share the sheet with your service account email

### 4. Run Backend

```bash
cd backend
python app.py
# → Starts on http://localhost:5000
```

### 5. Open Dashboard

```bash
# Edit frontend/dashboard.html — set MAPS_API_KEY and BACKEND_URL
# Then open in browser (or serve with python -m http.server 8000)
open frontend/dashboard.html
```

---

## 📡 API Endpoints

### `POST /api/report`
Submit a civic issue report.

```
Content-Type: multipart/form-data
Fields: image (file), description, latitude, longitude, address
```

```json
{
  "success": true,
  "report_id": "GH-20260627120000",
  "analysis": {
    "category": "pothole",
    "priority": "urgent",
    "severity_score": 4,
    "confidence_overall": 0.92,
    "reasoning": "Deep pothole on main road...",
    "recommended_action": "Authority escalation via PWD",
    "thinking": "Extended agent reasoning..."
  }
}
```

### `GET /api/issues`
Fetch all issues.

Query params: `?category=pothole&priority=urgent`

### `GET /api/stats`
```json
{ "total": 12, "urgent": 3, "high": 4, "resolved": 2, "resolved_pct": 16 }
```

### `GET /api/predict`
AI-predicted high-risk areas.

```json
{
  "high_risk_locations": [
    { "latitude": 28.67, "longitude": 77.07, "category": "pothole", "confidence": 0.87, "reason": "..." }
  ]
}
```

### `GET /api/health`
Health check.

---

## 📊 Evaluation Evidence

| Criterion | Implementation |
|-----------|---------------|
| **Agentic Depth (20%)** | Extended thinking (8k tokens), duplicate detection, escalation logic |
| **Problem Solving (20%)** | Autonomous triage — no human in the loop |
| **Google Tech (15%)** | Maps API (visual) + Sheets API (transparent data) |
| **Innovation (20%)** | Prediction layer, voice input, extended thinking visible |
| **Product Experience (10%)** | Dark-mode dashboard, real-time updates, animations |
| **Technical (10%)** | Modular code, Haversine distance, error handling, logging |
| **Completeness (5%)** | Full end-to-end with real Ghaziabad test data |

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | From console.anthropic.com |
| `GOOGLE_SHEETS_ID` | ✅ | Your Google Sheet ID |
| `GOOGLE_APPLICATION_CREDENTIALS` | ✅ | Path to service_account.json |
| `GOOGLE_MAPS_API_KEY` | ✅ | In frontend/dashboard.html |
| `FLASK_PORT` | ❌ | Default: 5000 |

---

## 📁 File Structure

```
community-hero/
├── backend/
│   ├── app.py           — Flask API (4 endpoints)
│   ├── agent.py         — Claude Anthropic integration
│   ├── google_sheets.py — gspread data persistence
│   ├── predictor.py     — Hotspot prediction layer
│   └── requirements.txt
├── frontend/
│   └── dashboard.html   — Single-file dashboard
├── docs/
│   ├── README.md
│   ├── API.md
│   └── ARCHITECTURE.md
├── tests/
│   └── test_reports.json — 6 Ghaziabad test cases
├── .env.example
├── .gitignore
└── CONTEXT.md
```

---

## 🎬 Demo Video

> [YouTube Link — record and paste here]

---

## 👤 Author

[Your Name] | [LinkedIn] | [GitHub]

---

## 📄 License

MIT
