# Community Hero - Antigravity IDE Vibe Coding Guide

**Goal**: Use Antigravity IDE's multi-agent architecture to build Community Hero in 3 days  
**Approach**: Manager View orchestration with 3 specialized agents working in parallel

---

## 📋 Prerequisites (Complete Before Day 1)

### Install Antigravity IDE
```bash
# macOS
curl -L https://antigravity.google.com/downloads/latest/macos -o Antigravity.dmg
open Antigravity.dmg

# Linux
wget https://antigravity.google.com/downloads/latest/linux -O Antigravity.tar.gz
tar -xzf Antigravity.tar.gz
./antigravity-install.sh

# Windows
# Download MSI from https://antigravity.google.com/downloads/latest/windows
```

### Setup Your API Keys
1. Get **Gemini API key**: https://ai.google.dev/
2. Get **Anthropic API key**: https://console.anthropic.com/
3. Setup **Google Cloud credentials** for Sheets/Drive APIs

```bash
# Export environment variables
export GEMINI_API_KEY="your_gemini_key"
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"
```

### Initialize Agent Skills (Optional but Recommended)
```bash
# One-time setup for agent memory system
npx agent-skills-setup-for-antigravity community-hero
```

This creates `.agent/` folder with rules, skills, and workflows.

---

## 🚀 DAY 1: Backend + Agent Setup

### Step 1: Create Project in Antigravity

1. **Open Antigravity IDE**
2. **Create new workspace**: `community-hero`
3. **Select template**: Python (or Node.js)
4. **Click "Launch Manager View"**

You'll see:
- Left panel: Project structure
- Center: File editor
- Right: Manager panel with agent controls

### Step 2: Switch to Manager View

In top-right corner:
- Click **"Manager"** (bird's-eye view)
- You'll see: Agents, Tasks, Implementation Plans, Artifacts

### Step 3: Create Agent Team

In Manager View, click **"+ Create Agents"**

Create 3 specialized agents:

**Agent 1: Backend Engineer**
```
Name: Backend-Engineer
Role: Python Flask API developer
Skills: Flask, API design, error handling
Primary task: Build /api/report endpoint
```

**Agent 2: AI Integration Specialist**
```
Name: AI-Integration-Specialist
Role: Claude API + Anthropic integration
Skills: Vision API, extended thinking, agentic loops
Primary task: Implement analyze_issue() function
```

**Agent 3: Data Engineer**
```
Name: Data-Engineer
Role: Google Sheets + data persistence
Skills: gspread, data validation, schema design
Primary task: Implement save_to_sheets()
```

### Step 4: Create Context File

In project root, create `CONTEXT.md`:

```markdown
# Community Hero - Agentic System Context

## Architecture
- Backend: Python Flask + Claude Anthropic API
- Frontend: HTML5 + Vanilla JS + Google Maps
- Data: Google Sheets + Google Drive
- Agents: Gemini 3 Pro (orchestration), Claude Opus (analysis)

## Key Constraints
- No hardcoded test data (use real Ghaziabad locations)
- Image must be analyzed with vision capability
- Extended thinking enabled for agent reasoning
- Duplicate detection within 50m radius, 7-day window
- All code must have error handling + logging

## Success Criteria
- Agent correctly categorizes images (80%+ accuracy)
- Data persists to Google Sheets without errors
- System responds in <3 seconds per request
- Extended thinking logged to files

## Communication Rules
- Use JSON for agent outputs (no markdown)
- Prefix logs: [AGENT], [ERROR], [SUCCESS]
- Save reasoning to: logs/agent_reasoning.jsonl
- All artifacts must be documented with docstrings
```

### Step 5: Assign Day 1 Tasks

In Manager View:

**Task 1: Backend Skeleton (Backend-Engineer)**
```
Create Flask app with these endpoints:
- POST /api/report (multipart form: image, description, lat, lng)
- GET /api/issues?category=&priority=
- GET /api/stats

Requirements:
- CORS enabled
- Error handling with meaningful HTTP codes
- Logging of all requests
- Service account auth for Google APIs

Return: app.py, requirements.txt, config.py
```

**Task 2: Agentic Analysis Function (AI-Integration-Specialist)**
```
Implement analyze_issue() function:

Input: image_base64, description, latitude, longitude, recent_reports
Output: JSON with category, severity, priority, reasoning, confidence

Use Claude Opus 4.6 with:
- Vision capability (analyze image)
- Extended thinking enabled (budget: 8000 tokens)
- System prompt from: IMPLEMENTATION.md

Function signature:
def analyze_issue(image_base64: str, description: str, lat: float, lng: float, recent_reports: list) -> dict:
    # Claude API call here
    # Extract thinking if present
    # Return structured JSON

Return: agent.py with full implementation
```

**Task 3: Google Sheets Integration (Data-Engineer)**
```
Implement google_sheets.py:

Functions:
1. save_to_sheets(analysis, image_url, timestamp) -> report_id
   - Append row to Google Sheet
   - Return unique ID (format: GH-{timestamp})

2. get_from_sheets(category=None, priority=None) -> list[dict]
   - Fetch all rows from Sheet
   - Filter by category/priority if provided

3. get_recent_reports(lat, lng, days=7, radius=50) -> list[dict]
   - For duplicate detection
   - Check last 7 days
   - Return reports within 50m radius

Column structure:
Timestamp, Category, Priority, Severity, Latitude, Longitude, Address, Reasoning, Action, ImageURL, Confidence, Status

Return: google_sheets.py, auth setup docs
```

### Step 6: Monitor Agent Progress

**In Manager View**:
- Watch task list update in real-time
- Click on any agent to see:
  - Implementation plan
  - Code diffs
  - Browser interactions (if applicable)
  - Artifacts (task breakdowns, summaries)

**Review artifacts after each agent completes**:
- [ ] Accept or request changes
- [ ] Comment on code diffs if needed
- [ ] Agent learns from your feedback

### Step 7: End-of-Day 1 Testing

When all 3 agents complete, test locally:

```bash
cd community-hero

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_SHEETS_ID=your_sheet_id

# Run Flask
python backend/app.py

# In another terminal, test endpoint
curl -X POST http://localhost:5000/api/report \
  -F "image=@test_pothole.jpg" \
  -F "description=Large pothole on main road" \
  -F "latitude=28.6692" \
  -F "longitude=77.0669"
```

**Expected output**:
```json
{
  "success": true,
  "report_id": "GH-20260625...",
  "analysis": {
    "category": "pothole",
    "priority": "urgent",
    "severity_score": 4,
    "confidence": 0.92,
    "reasoning": "Deep pothole on main road, safety hazard..."
  }
}
```

**Checkpoint**: ✅ All agents completed without errors  
**Deliverable**: Working Flask API + agent analysis + Sheets integration

---

## 🎬 DAY 2: Frontend + Live Testing

### Step 1: Create Frontend Agent

In Manager View, click **"+ Add Agent"**

```
Name: Frontend-Engineer
Role: HTML/JS/UX developer
Skills: HTML5, Vanilla JS, Google Maps API, responsive design
Primary task: Build interactive dashboard
```

### Step 2: Assign Frontend Task

**Task 1: Dashboard HTML (Frontend-Engineer)**

```
Create single-file dashboard (dashboard.html):

Features:
1. Google Map
   - Centered on Ghaziabad (28.6692, 77.0669)
   - Fetch issues from /api/issues
   - Color-coded markers (red=urgent, orange=high, blue=medium, green=low)
   - Click marker → infowindow with category + address
   - Click on map → open report form

2. Stats Panel (top-right)
   - Total Issues
   - Urgent Count
   - High Count
   - % Resolved
   - Auto-refresh every 5 seconds

3. Issues List (scrollable)
   - Each card: category badge + priority + description + location
   - Colored left border by priority
   - Click card → center map on issue

4. Report Form Modal
   - File input (image)
   - Textarea (description)
   - Text inputs (address, latitude, longitude)
   - Submit button
   - Show "Analyzing..." state
   - Success notification

5. Styling
   - Modern, clean
   - Responsive (mobile-friendly)
   - Purple gradient header
   - Color-coded cards
   - No external UI frameworks

Constants:
const BACKEND_URL = 'http://localhost:5000';
const GHAZIABAD_CENTER = { lat: 28.6692, lng: 77.0669 };

Return: dashboard.html (self-contained, single file)
```

### Step 3: Agent Works on Frontend

Watch in Manager View:
- Agent generates implementation plan (30–60 seconds)
- Agent writes code, tests, iterates
- Agent may ask clarifying questions in comments

**If agent gets stuck**: 
- Add inline comment: `// HELP: The form isn't submitting, check CORS headers on backend`
- Agent adjusts approach based on your feedback

### Step 4: Deploy & Test Locally

Once agent finishes:

```bash
# Start backend (if not running)
python backend/app.py

# Serve frontend
python -m http.server 8000

# Visit: http://localhost:8000/dashboard.html
```

**Test checklist**:
- [ ] Map displays Ghaziabad
- [ ] Stats panel shows 0 issues initially
- [ ] Click map → form opens
- [ ] Form submission works (submit test issue)
- [ ] Form closes on success
- [ ] New issue appears on map
- [ ] New issue appears in list
- [ ] Stats update in real-time
- [ ] Click issue card → map centers on it

### Step 5: Create Real Test Data

Manually create 5–10 test issues via the form:

1. **Pothole (Sector 7)** - Urgent
   - Photo: [pothole image]
   - Description: "Large pothole, 8cm deep"
   - Location: 28.6692, 77.0669

2. **Water Leak (Sector 9)** - High
   - Photo: [water leak image]
   - Description: "Pipeline leak, water accumulating"
   - Location: 28.6745, 77.0750

3. **Streetlight (Sector 11)** - Medium
   - Photo: [damaged light image]
   - Description: "Broken streetlight, exposed wiring"
   - Location: 28.6600, 77.0600

(Continue with 2–7 more realistic issues)

**Verify in Google Sheets**:
- Open your Google Sheet
- All test issues appear as rows
- Check: Timestamp, Category, Priority, Address all populated
- Click image URLs → should open in Google Drive (if images uploaded)

### Step 6: Deploy to Live URL

**Option A: Ngrok (Fastest)**
```bash
# Terminal 1: Backend running
python backend/app.py

# Terminal 2: Ngrok tunnel
ngrok http 5000
# Get URL: https://abc123.ngrok.io

# Terminal 3: Update dashboard.html
# Replace: const BACKEND_URL = 'http://localhost:5000';
# With: const BACKEND_URL = 'https://abc123.ngrok.io';

# Terminal 4: Serve frontend
python -m http.server 8000
# Visit: http://localhost:8000/dashboard.html
```

**Option B: Vercel (More professional)**
```bash
# Create vercel.json
cat > vercel.json << 'EOF'
{
  "buildCommand": "npm install",
  "outputDirectory": "."
}
EOF

vercel deploy
# Follow prompts, get shareable URL
```

### Step 7: Extended Thinking Enhancement

Create new agent task:

**Task 2: Enhanced Agent with Thinking (AI-Integration-Specialist)**

```
Update agent.py to use extended thinking:

1. Add thinking parameter to Claude API call:
   thinking={
       "type": "enabled",
       "budget_tokens": 8000
   }

2. Update system prompt to ask agent to reason about:
   - Image hazards (depth, severity, safety)
   - Duplicate detection (compare to recent_reports)
   - Citizen impact (how many people affected)
   - Escalation decision (should this be urgent?)
   - Resolution estimate (days to fix)

3. Extract thinking from response:
   response.content has blocks with type="thinking"
   Log thinking to: logs/agent_reasoning.jsonl
   Include in returned JSON: "thinking": "..."

4. Optional: Update dashboard to show reasoning
   - Click issue → display "Agent Reasoning" section
   - Show the thinking text

Test with 2–3 new test issues to verify reasoning is logged

Return: Updated agent.py with thinking enabled
```

**Checkpoint**: ✅ Dashboard + real test data + extended thinking  
**Deliverable**: Fully functional end-to-end system with agent reasoning visible

---

## 🎁 DAY 3: Innovation + Differentiators + Polish

### Step 1: Create Prediction Agent

**Agent 4: ML/Analytics Engineer**

```
Name: ML-Analytics-Engineer
Role: Data analysis + predictions
Skills: Data aggregation, pattern recognition, forecasting
Primary task: Implement hotspot prediction
```

### Step 2: Assign Prediction Task

**Task 1: Prediction Endpoint (ML-Analytics-Engineer)**

```
Create GET /api/predict endpoint:

Logic:
1. Fetch all issues from Google Sheets (last 7 days)
2. Group by location (cluster nearby issues)
3. Find hotspots (3+ reports same category within 50m)
4. Use Claude agent to predict high-risk areas

Agent reasoning:
- "Sector 7 has 3 potholes in 7 days → more likely upcoming due to monsoon"
- "Water leaks near old infrastructure areas → higher risk"
- Use seasonal context (monsoon = more water leaks)

Return JSON:
{
  "high_risk_locations": [
    {
      "latitude": 28.6692,
      "longitude": 77.0669,
      "category": "pothole",
      "confidence": 0.89,
      "reason": "3 potholes reported nearby; monsoon increases risk"
    }
  ],
  "timestamp": "2026-06-25T..."
}

Update dashboard.html:
- Plot predicted locations as yellow/dashed circles
- Label: "PREDICTED"
- Show reason on hover

Return: Updated agent.py + backend route + dashboard changes
```

### Step 3: Voice Input Feature

**Task 2: Voice Reporting (Frontend-Engineer)**

```
Add voice recording to dashboard.html:

In report form, add:
1. "🎤 Record Voice Report" button
2. Click starts recording (Web Speech API)
3. Recording indicator (red dot, "Recording...")
4. Transcription appears in description field
5. User can edit before submitting

Implementation:
- Use navigator.mediaDevices.getUserMedia() OR
- Web Speech API: navigator.mediaDevices.getDisplayMedia()
- Language: 'en-IN' for Indian English
- Stop button after recording
- Display transcript in textarea

Test: Record "Large pothole on sector 7 main road"
→ Should appear in description field automatically

Return: Updated dashboard.html with voice input
```

### Step 4: Documentation Generation

**Task 3: Documentation (Backend-Engineer)**

```
Create comprehensive docs:

1. README.md
   - Problem statement
   - Solution overview
   - Tech stack
   - Quick start (setup + run locally)
   - Evaluation evidence mapping

2. API.md
   - All endpoints documented
   - Request/response examples
   - Error codes
   - Rate limiting (if applicable)

3. ARCHITECTURE.md
   - System diagram (ASCII or Mermaid)
   - Data flow explanation
   - Agentic reasoning flowchart
   - Database schema

4. DEPLOYMENT.md
   - Ngrok setup (testing)
   - Vercel setup (production)
   - Environment variables needed
   - Troubleshooting

5. Update GEMINI.md (agent identity file)
   - Project name, version
   - Agent personality (helpful, precise, testing-first)
   - Custom rules (always test, log reasoning, verify)

Return: README.md, API.md, ARCHITECTURE.md, DEPLOYMENT.md
```

### Step 5: Record Demo Video

**Task 4: Demo Video Instructions**

```
Create 2–3 minute video walkthrough:

Script:
1. Intro (20 sec):
   "This is Community Hero, an AI-powered civic issue tracker"
   "Citizens report issues, we prioritize with AI"

2. Report an issue (40 sec):
   - Click map → form opens
   - Upload pothole photo
   - Write: "Large pothole on sector 7 main road"
   - Submit
   - Show "Analyzing..."
   - Show result: URGENT, pothole, severity 4

3. View dashboard (40 sec):
   - Show all issues on map (color-coded)
   - Show stats updating
   - Click issue → map centers
   - Show Google Sheets data (transparency)

4. Show agent reasoning (20 sec):
   - Click issue → show "Agent Reasoning"
   - Read reasoning out loud

5. Outro (10 sec):
   "Claude API for analysis, Google Sheets for transparency, Maps for visualization"

Tools:
- Use Loom, OBS, or QuickTime
- Upload to YouTube (unlisted)
- Get link

Return: YouTube link (put in README)
```

### Step 6: Final Polish & Testing

**In Manager View, create cleanup task**:

```
Final Polish Task:

1. Code Quality
   - Add docstrings to all functions
   - Add type hints to Python code
   - Fix any linting errors
   - Add comments for complex logic

2. Error Handling
   - Verify all endpoints have try/except
   - Test with invalid inputs
   - Verify error messages are helpful
   - Log all errors

3. UI Polish
   - Test on mobile (responsive check)
   - Add loading spinners
   - Add success/error notifications
   - Smooth transitions

4. Performance
   - Verify response time < 3 seconds
   - Check image file sizes
   - Optimize dashboard loading

5. Final Verification
   - All 5+ test issues visible on map
   - Agent reasoning logged and visible
   - Predictions endpoint working
   - Voice input functional (if implemented)
   - Documentation complete
   - Demo video uploaded

Return: Polished, production-ready code
```

### Step 7: Commit & Deploy

```bash
# Final commit
git add -A
git commit -m "feat(final): Extended thinking + prediction + voice + polish"

# Deploy
vercel deploy  # Or keep Ngrok running

# Verify live system works
curl https://your-domain.vercel.app/api/stats
# Should return valid JSON with your test data
```

**Final Checkpoint**: ✅ Everything working, documented, demoed  
**Deliverable**: Submission-ready Community Hero

---

## 📊 Manager View Workflow Summary

### What You See in Manager View:

**Left Panel (Task Queue)**:
- [ ] Backend Skeleton
- [ ] Agentic Analysis
- [ ] Sheets Integration
- [ ] Frontend Dashboard
- [ ] Extended Thinking
- [ ] Prediction Layer
- [ ] Voice Input
- [ ] Documentation
- [ ] Final Polish

**Center Panel (Implementation Plans)**:
- Agent's approach/strategy (high-level)
- Breakdown of what they'll do
- Time estimate
- Risk assessment

**Right Panel (Artifacts)**:
- **Task List**: What agent plans to do (checklist)
- **Implementation Plan**: Detailed roadmap
- **Code Diffs**: Changes made (accept/reject)
- **Browser Screenshots**: Agent testing in real browser
- **Logs**: Terminal output, errors, successes
- **Summaries**: Agent's summary of work done

### How to Manage Agents:

**If agent finishes a task**:
- Review artifacts (click diff)
- If good: ✅ Accept (or do nothing, auto-accept)
- If needs changes: Add comment, agent reads and adjusts

**If agent gets stuck**:
- Add comment: `"The Flask route isn't working. Check that CORS is enabled."`
- Agent re-reads your feedback
- Agent adjusts approach

**If you want multiple agents working simultaneously**:
- Manager View allows this natively
- One agent works on backend, one on frontend, one on docs
- No manual coordination needed
- All artifacts sync in real-time

---

## 🎯 Day-by-Day Checklist

### ✅ Day 1 End
- [ ] Antigravity open with 3 agents assigned
- [ ] `CONTEXT.md` created with project guidelines
- [ ] 3 agents complete their tasks (backend, agent, sheets)
- [ ] Local testing works (Flask API responds)
- [ ] All agents' artifacts reviewed
- [ ] 1 commit: "feat(backend): Flask API + Claude agent + Sheets"

### ✅ Day 2 End
- [ ] Frontend agent created and assigned
- [ ] Dashboard.html generated by agent
- [ ] Local testing passes (form submission works)
- [ ] 5+ real test issues created manually
- [ ] Google Sheets populated with data
- [ ] Extended thinking added to agent
- [ ] Live URL deployed (Ngrok or Vercel)
- [ ] All artifacts reviewed
- [ ] 1 commit: "feat(frontend): Dashboard + extended thinking"

### ✅ Day 3 End
- [ ] Prediction agent created
- [ ] Hotspot prediction endpoint working
- [ ] Voice input added to frontend
- [ ] Documentation complete (README, API, Architecture)
- [ ] Demo video recorded and uploaded
- [ ] Final polish completed
- [ ] All systems tested end-to-end
- [ ] All artifacts reviewed
- [ ] 1 commit: "feat(final): Prediction + voice + documentation"

---

## 🔥 Pro Tips for Antigravity Vibe Coding

### 1. Use Clear Task Specifications
Instead of: "Build the API"  
Better: "Create POST /api/report endpoint that accepts multipart form with image, description, lat, lng. Validate inputs. Call Claude API with vision. Return JSON with category, priority, reasoning."

### 2. Review Agent Artifacts Immediately
- Don't wait until end of day
- Review after each task completion
- Agent learns from your feedback
- Comment on code diffs to train agent style

### 3. Let Agents Iterate
- If agent's first try isn't perfect, don't fix it
- Add comment: "This approach is close but needs [specific change]"
- Agent will refactor based on your guidance
- This builds agent's understanding of your preferences

### 4. Use Browser Artifacts
- Antigravity shows browser screenshots
- Agent tested dashboard in real browser before committing
- You see what it looks like without running locally (sometimes)
- If broken, agent sees it and fixes

### 5. Multi-Agent Power
- Assign 3 agents to 3 tasks simultaneously
- Don't wait for one to finish before starting next
- Manager View orchestrates in background
- You review all in parallel

### 6. Terminal Control
- Agents can run `pip install`, `python app.py`, `curl`, `git` commands
- Artifact shows terminal output
- If test fails, you see the error
- Agent sees error and fixes

### 7. Feedback Loop
**This is the vibe coding secret**:
```
Agent writes code → You review → You comment
→ Agent reads comment → Agent refactors → You review again
→ Agent learns your style → Agent writes better code
→ Repeat for 3 days
```

By Day 3, agent knows your patterns and needs less guidance.

---

## 🆘 If Something Goes Wrong

### Agent Says "I Need Clarification"
→ Agent is asking a real question in artifacts  
→ Answer clearly in a comment  
→ Agent uses your answer to proceed

### Agent's Code Has a Bug
→ Review code diff  
→ Comment: `"Line 42: This should be != not =="`  
→ Agent fixes and re-commits

### Endpoint Returns 500 Error
→ Check browser artifacts (agent shows error)  
→ Add comment with the error message  
→ Agent debugs

### Image Upload Fails
→ Check CORS headers in Flask  
→ Add comment: `"Frontend sends multipart form-data, make sure Flask accepts it"`  
→ Agent adds CORS headers

### Google Sheets Not Updating
→ Check service account has editor access  
→ Add comment: `"gspread auth failing, verify JSON path"`  
→ Agent debugs auth

---

## 📚 Antigravity Resources

- **Official Docs**: https://antigravityaiide.com/
- **Getting Started**: https://codelabs.developers.google.com/getting-started-google-antigravity
- **Agent Skills Setup**: https://github.com/Dokhacgiakhoa/Agent-skills-setup-for-AntiGravity
- **Community**: Official Antigravity Discord/Forums

---

## 🎉 You're Ready

You now have:
- ✅ 3-day timeline
- ✅ 4 agents to manage
- ✅ Clear task specifications
- ✅ Manager View workflow
- ✅ Testing & deployment strategy

**Start Day 1 in 1 hour. By Day 3, you'll have a winning submission.**

The magic of Antigravity: **You manage agents, agents build code.**

**Let's go. 🚀**

---

**Last Updated**: June 25, 2026  
**Status**: Ready for Antigravity Vibe Coding
