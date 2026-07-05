# Community Hero - Quick Reference & Claude Prompts

## 🎯 TL;DR: Why Community Hero Wins

| Criterion | How You Win | Weight |
|-----------|------------|--------|
| **Agentic Depth** | Extended thinking agent with duplicate detection + escalation logic | 20% |
| **Problem Solving** | Autonomous workflow (no human triage needed) | 20% |
| **Google Tech** | Maps API (visual) + Sheets API (data transparency) | 15% |
| **Innovation** | Prediction layer (7-day hotspot forecast) | 20% |
| **Product Experience** | Clean dashboard, real-time updates, live stats | 10% |
| **Technical** | Modular code, error handling, proper logging | 10% |
| **Completeness** | Full end-to-end with real test data | 5% |

**Total effort**: 22–28 hours over 3 days  
**Expected score**: 85–95 out of 100

---

## 🚀 Start Here: Copy-Paste Claude Prompts

Use these prompts with Claude artifacts. They're ready to go.

### Prompt 1: Build Backend (Day 1, Hour 1–3)

```
Build a Python Flask API for Community Hero civic issue tracking.

Structure:
backend/
├── app.py (main Flask app)
├── agent.py (Claude integration)
├── google_sheets.py (data storage)
└── requirements.txt

Requirements:

1. Flask app with endpoints:
   - POST /api/report
     Input: multipart form with image, description, latitude, longitude
     Returns: JSON with report_id, analysis
   - GET /api/issues?category=pothole&priority=urgent
     Returns: list of issues
   - GET /api/stats
     Returns: {total, urgent, high, resolved_pct}

2. google_sheets.py:
   - save_to_sheets(analysis, image_url, timestamp) → report_id
   - get_from_sheets(category, priority) → list
   - get_recent_reports(lat, lng, days, radius) → list (for duplicates)
   - Use gspread library

3. agent.py:
   - analyze_issue(image_base64, description, lat, lng, recent_reports) → dict
   - Uses claude-opus-4-6 with vision
   - System prompt focuses on: categorization, severity, priority, duplicate detection
   - Returns JSON with category, priority, severity_score, reasoning, confidence

4. Error handling:
   - Try/except blocks with meaningful messages
   - CORS headers enabled
   - Logging of all agent calls

5. Test locally with:
   curl -X POST http://localhost:5000/api/report \
     -F "image=@test.jpg" \
     -F "description=Test issue" \
     -F "latitude=28.6692" \
     -F "longitude=77.0669"

Respond with: app.py, agent.py, google_sheets.py, requirements.txt (4 files)
```

---

### Prompt 2: Build Dashboard (Day 2, Hour 0–2)

```
Build a single HTML dashboard for Community Hero.

File: dashboard.html (one file, self-contained)

Design:
- Header: Purple gradient, "Community Hero" title
- Layout: 2-column responsive grid (left=map, right=list+stats)

Functionality:

1. Google Maps (left side):
   - Centered on Ghaziabad (28.6692, 77.0669)
   - Fetch issues from /api/issues
   - Plot markers colored by priority:
     * Red = urgent, Orange = high, Blue = medium, Green = low
   - Click marker = infowindow with category+address
   - Click on map = open report form

2. Right sidebar stats (top):
   - Display 4 metrics: Total Issues, Urgent, High, %Resolved
   - Update every 5 seconds (auto-refresh)
   - Large numbers (24px), gray labels

3. Issues list (middle/bottom):
   - Scrollable list of all issues
   - Each card: category badge + priority badge + description + address
   - Color-coded left border by priority
   - Click card = center map on issue

4. Report Form Modal:
   - File input: "Choose Photo"
   - Textarea: "Describe the issue"
   - Text inputs: Address, Latitude, Longitude
   - Submit button: calls POST /api/report
   - Shows "Analyzing..." state
   - Success notification

5. Styling:
   - No external CSS framework (vanilla styles only)
   - Responsive (mobile-friendly)
   - Card-based UI with subtle shadows
   - Color-coded by priority (visual hierarchy)

Constants to set:
const BACKEND_URL = 'http://localhost:5000';
const GHAZIABAD_CENTER = { lat: 28.6692, lng: 77.0669 };

Return: dashboard.html (one file)
```

---

### Prompt 3: Add Extended Thinking (Day 2, Hour 7–9)

```
Enhance agent.py to use Claude's extended thinking for agentic depth.

Update analyze_issue() function:

1. Add thinking parameter:
   thinking={
       "type": "enabled",
       "budget_tokens": 8000
   }

2. Update system prompt to ask:
   - "What specific hazards are visible in the image?"
   - "Is this a duplicate of reports in this area?"
   - "What citizen impact does this have?"
   - "Should this be escalated for immediate action?"
   - "How many days to resolve?"

3. Extract thinking from response:
   - response.content has blocks with type="thinking"
   - Log thinking to logs/agent_reasoning.jsonl
   - Include in returned JSON: "thinking": "..."

4. Validate output:
   - Verify thinking text shows actual reasoning (not gibberish)
   - Resolution estimate should be realistic (1–30 days)

5. Optional: Update dashboard to display reasoning
   - Click issue card → show "Agent Reasoning" section
   - Display the thinking text

Return: Updated agent.py with thinking enabled
```

---

### Prompt 4: Add Prediction Layer (Day 3, Hour 0–2)

```
Add a prediction endpoint to predict high-risk areas.

New endpoint: GET /api/predict

Logic:
1. Analyze all issues from the last 7 days
2. Group by location (cluster nearby issues)
3. Find patterns:
   - 3+ reports of same category within 50m = hotspot
   - More reports in rainy areas = increased water leak risk
   - Aging infrastructure areas = more potholes
4. Use Claude agent to predict:
   - Which other areas are at HIGH risk
   - Confidence level (0.7–0.99)
   - Reasoning for prediction

Return JSON:
{
  "high_risk_locations": [
    {
      "latitude": 28.6692,
      "longitude": 77.0669,
      "category": "pothole",
      "confidence": 0.89,
      "reason": "3 potholes reported nearby this week; monsoon season increases risk"
    }
  ],
  "timestamp": "2026-06-25T12:00:00Z"
}

Update dashboard to show predictions:
- Plot as yellow/dashed circles (different from reported issues)
- Label: "PREDICTED"
- Show reason on hover

Return: Updated agent.py with predict function + dashboard changes
```

---

### Prompt 5: Add Voice Input (Day 3, Hour 2–3)

```
Add voice reporting feature to dashboard.html.

In the report form:
1. Add button: "🎤 Record Voice Report"
2. Click starts recording (Web Speech API)
3. Recording appears in description field as transcription
4. User can edit before submitting

Implementation:
- Use navigator.mediaDevices.getUserMedia() or
- Use Web Speech API: const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)()
- Set language to 'en-IN' for Indian English
- Show recording indicator (red dot, "Recording...")
- Stop button
- Display transcript in textarea

Test: Record "Large pothole on sector 7 main road" → should appear in description

Return: Updated dashboard.html with voice recording
```

---

## 📋 Critical Files Checklist

By end of Day 3, you need these files in GitHub:

```
community-hero/
├── backend/
│   ├── app.py ✅
│   ├── agent.py ✅ (with extended thinking)
│   ├── google_sheets.py ✅
│   ├── requirements.txt ✅
│   └── logs/ (auto-created)
│
├── frontend/
│   └── dashboard.html ✅ (with voice input, optional)
│
├── docs/
│   ├── README.md ✅
│   ├── ARCHITECTURE.md ✅
│   └── API.md ✅
│
├── tests/
│   └── test_reports.json (5+ test cases)
│
├── .env.example ✅
├── .gitignore ✅
├── service_account.json (not in git, in .gitignore)
└── demo_video.mp4 (link in README)
```

---

## 🔑 Environment Variables (Set Before Day 1)

Create `.env` file:
```bash
# Anthropic
export ANTHROPIC_API_KEY=sk-ant-v0-...

# Google
export GOOGLE_SHEETS_ID=1a2b3c4d...  # Your sheet ID
export GOOGLE_DRIVE_FOLDER_ID=xyz...  # Community Hero folder in Drive

# Maps API
export GOOGLE_MAPS_API_KEY=AIza...

# GitHub (for MCP commits, optional)
export GITHUB_TOKEN=ghp_...

# Flask
export FLASK_ENV=development
export FLASK_DEBUG=1
```

Then in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY')
SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
```

---

## 🎬 Demo Video Script (2–3 minutes)

Use this script for your demo video:

```
[Intro - 20 seconds]
"Hi, I'm building Community Hero, an AI-powered civic issue tracker for Ghaziabad.

Problem: Citizens report potholes, water leaks, and other infrastructure issues, 
but there's no centralized, intelligent way to categorize and prioritize them.

Solution: An autonomous Claude-powered agent that analyzes issue photos, 
determines priority, and recommends action — all without human intervention."

[Report an Issue - 40 seconds]
"Let me show you how it works. I'll click on the map to report an issue."
[Click map, form opens]

"I'll upload a photo of a pothole..."
[Upload image]

"...write a description..."
[Type: "Large pothole on Sector 7 main road, car-sized"]

"...and submit."
[Click Submit]

"The agent is now analyzing the image. It's examining:
- The pothole depth from the photo
- The location context (it's on a main road)
- Recent reports nearby (this is a hotspot)
- The weather and season"
[Wait for response]

"The agent determined this is URGENT priority, with high severity. 
It's recommending immediate authority escalation because it's a safety hazard."

[View Dashboard - 40 seconds]
"Now let me show you the dashboard. Here are all reported issues in Ghaziabad."
[Show map with markers]

"I can see:
- Red markers for urgent issues
- Orange for high priority
- Green for low priority"

"All issues are here in real-time. Let me click one to see details."
[Click marker, show infowindow]

"And here's the stats panel — total issues, urgent count, resolved percentage."
[Show stats updating]

[Show Agent Reasoning - 20 seconds]
"This is where it gets interesting. Let me show you the agent's actual reasoning."
[Click issue, show reasoning section]

"The agent evaluated this pothole and thought:
'This is a deep pothole on a main road, high vehicle traffic. 
Recent monsoon has caused 3 similar issues in this sector.
Severity: 4/5. Priority: URGENT. Action: PWD escalation.'

This is Claude's extended thinking in action."

[Tech Stack - 10 seconds]
"Under the hood:
- Python Flask backend
- Claude Anthropic API for agentic analysis
- Google Sheets for transparent data storage
- Google Maps for visualization"

[Outro - 10 seconds]
"Community Hero makes civic engagement smarter and faster.
Thanks for watching."
```

---

## 🎯 Winning Strategy

### 1. Maximize Agentic Depth (20%)
- ✅ Use extended thinking (Claude thinks before responding)
- ✅ Implement duplicate detection (agent compares to recent reports)
- ✅ Escalation logic (agent decides if urgent)
- ✅ **Show reasoning visibly** (judges want to see the thinking)

**Expected judges' reaction**: "Wow, the agent isn't just classifying, it's actually reasoning"

### 2. Maximize Problem Solving (20%)
- ✅ Autonomous workflow (no human bottleneck)
- ✅ Real test data (5+ Ghaziabad issues, not dummy data)
- ✅ Measurable impact (stats show improvements)

**Expected judges' reaction**: "This would actually work for a city"

### 3. Maximize Google Tech (15%)
- ✅ Maps API: Real-time visualization of all issues
- ✅ Sheets API: All data publicly accessible (judges can audit)
- ✅ Drive API: Organized image archive (optional)

**Expected judges' reaction**: "Everything is transparent and auditable"

### 4. Maximize Innovation (20%)
- ✅ Prediction layer: Forecast hotspots (beats basic reporting)
- ✅ Voice input: Accessible reporting (beats text-only)
- ✅ Extended thinking: Agent reasons out loud (beats simple categorization)

**Expected judges' reaction**: "They didn't just solve the problem, they went beyond it"

---

## ⏱️ Time Breakdown

| Task | Hours | Day |
|------|-------|-----|
| Setup + Environment | 1 | 1 |
| Flask Backend | 2 | 1 |
| Agent + Extended Thinking | 2 | 1 |
| Google Sheets Integration | 2 | 1 |
| Dashboard Frontend | 2 | 2 |
| Testing + Real Data | 2 | 2 |
| Deployment | 1 | 2 |
| Prediction Layer | 2 | 3 |
| Voice Input | 1 | 3 |
| Documentation | 2 | 3 |
| Demo Video | 1 | 3 |
| Polish + Bugfixes | 1 | 3 |
| **Total** | **22–28** | **3 days** |

---

## 🔗 MCP Connectors to Use

### When Claude Builds the Code

1. **Google Drive MCP**: Auto-upload images to organized folders
2. **Google Sheets MCP**: Verify live schema before building dashboard
3. **GitHub MCP**: Auto-commit after each feature
4. **Web Search MCP**: Agent searches for infrastructure context

Tell Claude:
```
"You have access to MCP connectors:
- Google Drive: Store issue images
- Google Sheets: Access live data schema
- GitHub: Commit after each feature
- Web Search: Find context about reported locations

Use them to enhance the system."
```

---

## 🎁 Bonus Features (If Time Allows)

1. **Duplicate Detection Animation**
   - When agent detects duplicate, show: "Merged with existing report #GH-..."
   - Visual indication on dashboard

2. **Heatmap Mode**
   - Toggle view: markers → heatmap
   - Show density of issues by area

3. **Time-Series Analysis**
   - Show "issues reported this week" as line chart
   - Demonstrate impact

4. **Auto-Email Summary**
   - Daily email to admin: "5 new issues reported, 2 urgent"
   - Use SendGrid or similar

5. **Citizen Notifications**
   - Citizens get SMS/email when issue status changes
   - Builds community engagement

---

## ❌ Common Mistakes to Avoid

1. **Hardcoded test data**
   - ❌ Dashboard shows dummy issues
   - ✅ Real Ghaziabad locations with real photos

2. **Agent categorization without reasoning**
   - ❌ Returns "pothole" with no explanation
   - ✅ Returns "pothole" + reasoning + confidence

3. **No error handling**
   - ❌ If Sheets API fails, app crashes
   - ✅ Graceful fallback, logging, retry logic

4. **Dashboard not responsive**
   - ❌ Doesn't work on mobile
   - ✅ Responsive grid, touch-friendly

5. **No video demo**
   - ❌ Judges have to imagine how it works
   - ✅ 2-minute video showing full workflow

6. **Ugly code with no comments**
   - ❌ Judges can't understand architecture
   - ✅ Clean code, docstrings, logging

7. **Deploying at last minute**
   - ❌ Day 3 at 11:59 PM, crashes
   - ✅ Deployed Day 2, tested thoroughly

---

## 📚 Resources to Bookmark

- **Anthropic Docs**: https://docs.anthropic.com
- **Claude Vision**: https://docs.anthropic.com/en/docs/vision
- **Google Maps API**: https://developers.google.com/maps
- **Google Sheets API**: https://developers.google.com/sheets/api
- **Flask Docs**: https://flask.palletsprojects.com/
- **Gspread Docs**: https://docs.gspread.org/

---

## 💬 Key Talking Points for Submission

When presenting:

> "Community Hero uses Claude's extended thinking capability to autonomously analyze civic issues. The agent reasons about image analysis, location context, and duplicate detection — making prioritization decisions without human intervention. All data is stored transparently in Google Sheets, and the dashboard leverages Google Maps for real-time visualization. The system is designed to scale from one city to thousands."

---

## 🏆 Expected Outcome

**If you follow this guide**:
- ✅ Full working system
- ✅ Production-quality code
- ✅ Real test data with Ghaziabad locations
- ✅ Extended thinking agent (agentic depth)
- ✅ Prediction layer (innovation)
- ✅ Live deployments
- ✅ Professional documentation
- ✅ 2-minute demo video

**Expected score**: 85–95/100  
**Competitive advantage**: Agentic depth + real data + innovation

---

## 📞 Last-Minute Help

**If you're stuck on Day 2 evening**:
- Deploy what you have (even if incomplete)
- Focus on: working agent + basic dashboard
- Skip: prediction, voice input
- Still competitive because agent is solid

**If agent categorization is wrong**:
- Refine system prompt (tell Claude exactly what "urgent" means)
- Add more context (weather, season, time of day)
- Test with different images

**If dashboard doesn't update**:
- Check browser console for errors
- Verify backend returns valid JSON
- Test endpoint with `curl` first

**If deadline is tomorrow**:
- Priority 1: Working agent
- Priority 2: Dashboard that displays results
- Priority 3: Everything else

You've got this! 🚀

---

**Last Updated**: June 25, 2026  
**Version**: 1.0 — Ready for Launch
