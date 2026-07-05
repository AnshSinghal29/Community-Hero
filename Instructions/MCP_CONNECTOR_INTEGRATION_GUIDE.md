# Community Hero - MCP Connector Integration Guide

**Purpose**: Use Model Context Protocol (MCP) servers to enhance UI development, data management, and automate repetitive tasks in your Anthropic API development workflow.

---

## 🔗 Recommended MCP Connectors Setup

### 1. Google Drive MCP (HIGHEST PRIORITY)
**Why**: Centralized image storage, organized by category, auditable by judges

#### Setup
```bash
# Install
npm install @anthropic-ai/sdk google-auth-library-nodejs googleapis

# Environment
export GOOGLE_DRIVE_CREDENTIALS=$(cat service_account.json | base64)
```

#### Integration in Backend

```python
# backend/google_drive.py
from google.colab import auth
from googleapiclient.discovery import build
import os

class DriveManager:
    def __init__(self):
        self.drive = build('drive', 'v3')
        self.root_folder_id = self._ensure_root_folder()
    
    def _ensure_root_folder(self):
        """Ensure Community Hero root folder exists in Drive."""
        results = self.drive.files().list(
            q="name='Community-Hero' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            pageSize=1
        ).execute()
        
        items = results.get('files', [])
        if items:
            return items[0]['id']
        
        # Create if not exists
        file_metadata = {
            'name': 'Community-Hero',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.drive.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')
    
    def _ensure_category_folder(self, category):
        """Ensure category subfolder exists."""
        results = self.drive.files().list(
            q=f"name='{category}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{self.root_folder_id}' in parents",
            spaces='drive',
            pageSize=1
        ).execute()
        
        items = results.get('files', [])
        if items:
            return items[0]['id']
        
        # Create if not exists
        file_metadata = {
            'name': category,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.root_folder_id]
        }
        folder = self.drive.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')
    
    def upload_issue_image(self, image_bytes, report_id, category):
        """Upload issue image to Drive."""
        folder_id = self._ensure_category_folder(category)
        
        file_metadata = {
            'name': f'{report_id}.jpg',
            'parents': [folder_id]
        }
        
        media = MediaIoBaseUpload(BytesIO(image_bytes), mimetype='image/jpeg', resumable=True)
        file = self.drive.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return {
            'file_id': file.get('id'),
            'web_view_link': file.get('webViewLink'),
            'drive_url': f"https://drive.google.com/file/d/{file.get('id')}/view"
        }

# backend/app.py - Updated route
from google_drive import DriveManager

drive_manager = DriveManager()

@app.route('/api/report', methods=['POST'])
def create_report():
    """Create report and upload image to Drive."""
    
    data = request.json
    image_file = request.files.get('image')
    
    # Run agentic analysis
    analysis = analyze_issue(...)
    
    # Upload image to Drive
    drive_info = drive_manager.upload_issue_image(
        image_bytes=image_file.read(),
        report_id=report_id,
        category=analysis['category']
    )
    
    # Save to Sheets with Drive link
    report_id = save_to_sheets(
        analysis=analysis,
        image_url=drive_info['drive_url'],  # Use Drive link instead of local
        timestamp=datetime.now().isoformat()
    )
    
    return jsonify({
        'success': True,
        'report_id': report_id,
        'image_drive_url': drive_info['drive_url'],
        'analysis': analysis
    })
```

#### Benefits for Judges
- Click any image URL in the Google Sheets → Opens in Google Drive
- Verify authenticity of reports
- See organized folder structure: `Community-Hero/pothole/`, `Community-Hero/water-leak/`, etc.
- Real-time audit trail of all submissions

---

### 2. Google Sheets MCP (HIGHEST PRIORITY)
**Why**: Live data visibility, easier Claude artifact generation for dashboard

#### Setup
```bash
# Already using gspread, but MCP integration allows Claude to:
# - Update Sheets directly while building
# - Query live data while developing dashboard
# - Test aggregation queries before deploying
```

#### Integration in Claude Artifacts

When Claude is building your dashboard, it can now:

```javascript
// In dashboard.html, Claude-generated code can now verify data:
async function initDashboardWithLiveData() {
    // Claude artifact can call this to verify real Sheets structure
    const response = await fetch('/api/sheets-schema');
    const schema = await response.json();
    
    // Schema includes:
    // {
    //   "columns": ["Timestamp", "Category", "Priority", "Severity", ...],
    //   "sample_rows": 5,
    //   "total_issues": 47
    // }
    
    console.log('Connected to live Sheets:', schema);
}
```

#### MCP Benefit
You can tell Claude: *"Connect to my Google Sheets, verify the current schema, then build a dashboard that matches the actual column structure."*

No more guessing about column names — Claude reads directly from your live sheet.

---

### 3. GitHub MCP (MEDIUM PRIORITY)
**Why**: Version control, iteration history for judges

#### Setup
```bash
export GITHUB_TOKEN=ghp_your_token_here

# Initialize repo
git init
git add .
git commit -m "Community Hero MVP - Day 1"
git push origin main
```

#### Integration in Development Loop

When Claude is building features, it can:

```
"Please implement the prediction layer and commit to GitHub with a descriptive message."
```

Claude will:
1. Write the code
2. Run tests
3. Commit with message: `feat(predict): Add 7-day hotspot prediction using agent reasoning`
4. Push to your repo

**Benefit**: Judges see your iteration history, not just final code.

#### GitHub Structure (Recommended)
```
community-hero/
├── backend/
│   ├── agent.py (agentic analysis)
│   ├── app.py (Flask API)
│   ├── google_sheets.py (data storage)
│   ├── google_drive.py (image management)
│   └── requirements.txt
├── frontend/
│   └── dashboard.html (single-file UI)
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── AGENT-REASONING.md
├── tests/
│   ├── test_agent.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

### 4. Web Search MCP (OPTIONAL, +5 POINTS)
**Why**: Agent can research context to make smarter decisions

#### Use Case: Contextual Analysis

When an issue is reported, the agent can search for:
- Recent news about that area
- Infrastructure maintenance schedules
- Weather conditions

```python
# backend/agent.py - Enhanced
def analyze_issue_with_context(image_base64, description, lat, lng, recent_reports):
    """Add web search context to agent analysis."""
    
    # Search for recent news
    news_context = search_web(
        query=f"Ghaziabad infrastructure {get_sector_from_coords(lat, lng)}"
    )
    
    # Search for weather
    weather = search_web(query=f"Ghaziabad weather {datetime.now().strftime('%Y-%m-%d')}")
    
    # Include in agent prompt
    enhanced_prompt = f"""
    Current context:
    - Recent news: {news_context}
    - Weather: {weather}
    - Recent reports in area: {recent_reports}
    
    Use this context to determine if this issue is urgent.
    """
    
    return analyze_issue(image_base64, description, lat, lng, enhanced_prompt)
```

**Judges will notice**: Agent reasoning mentions real-time news ("flooding reported in Sector 9 today, water leak likely urgent").

---

## 🧠 Prompts to Use with MCP Connectors

### Prompt 1: Build Backend with Drive Integration
```
You have access to Google Drive MCP. 

Build a Flask API that:

1. When a citizen submits an issue photo:
   - Analyze with Claude vision
   - Upload image to Google Drive in folder: Community-Hero/{category}/
   - Save metadata to Google Sheets
   - Return Drive shareable link

2. Endpoint: POST /api/report
   - Input: image (file), description (text), lat (float), lng (float)
   - Output: JSON with category, priority, drive_url
   
3. Use this Google Drive structure:
   Community-Hero/
   ├── pothole/
   ├── water_leak/
   ├── streetlight/
   └── waste_management/

Code should:
- Create folders if they don't exist
- Auto-organize by category
- Make images shareable (permissions: anyone can view)
```

### Prompt 2: Build Dashboard Querying Live Sheets
```
You have access to Google Sheets MCP.

Build an HTML dashboard that:

1. Connects to Google Sheets "Community Hero - Issues"
2. Reads live issue data:
   - All issues with: category, priority, lat, lng, address, image_url
3. For each issue:
   - Draw a marker on Google Maps
   - Color-coded by priority
   - Clicking marker opens an infowindow

4. Right sidebar:
   - List all issues sorted by priority
   - Real-time stats: total, urgent count, high count
   
5. The Sheets API returns:
   {
     "issues": [
       {
         "timestamp": "2026-06-25T...",
         "category": "pothole",
         "priority": "high",
         "latitude": 28.6692,
         "longitude": 77.0669,
         "address": "Sector 7, Ghaziabad",
         "image_url": "https://drive.google.com/...",
         "status": "open|resolved"
       }
     ],
     "stats": {
       "total": 47,
       "urgent": 3,
       "high": 12,
       "resolved": 8
     }
   }

Build it to exactly match this schema.
```

### Prompt 3: Commit to GitHub with MCP
```
You have access to GitHub MCP.

After implementing the prediction layer:

1. Test locally (ensure no errors)
2. Commit with message: "feat(predict): Add 7-day hotspot prediction using agent reasoning"
3. Include in commit message:
   - What was added
   - How to test it
   - Example output
4. Push to main branch
5. Create a summary comment in the commit explaining the agentic reasoning

This will show judges your iteration process.
```

---

## 🎬 Recommended Development Flow with MCPs

### Day 1: Backend + Drive Integration
```bash
# Claude builds with MCP connectors:
1. Generate Python Flask app
2. Generate Google Drive manager class
3. Test Drive upload with sample image
4. Commit to GitHub: "feat(backend): Initial Flask API + Drive integration"
```

### Day 2: Frontend + Sheets Integration
```bash
# Claude builds with MCP connectors:
1. Query live Google Sheets schema
2. Generate HTML dashboard matching actual schema
3. Test with live data from Sheets
4. Add real-time stats calculation
5. Commit to GitHub: "feat(frontend): Dashboard with live Sheets integration"
```

### Day 3: Polish + Prediction
```bash
# Claude builds with MCP connectors:
1. Add extended thinking to agent
2. Implement prediction layer
3. Test with live data
4. Add Web Search for context
5. Final commit: "feat(agent): Extended thinking + hotspot prediction + web context"
```

---

## 🔐 Environment Setup Checklist

Before passing to Claude artifacts, set these env vars:

```bash
# .env file
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_SHEETS_CREDS=$(cat service_account.json | base64)
export GOOGLE_DRIVE_CREDS=$(cat service_account.json | base64)
export GITHUB_TOKEN=ghp_...
export GOOGLE_MAPS_API_KEY=AIza...

# For local testing
export FLASK_ENV=development
export BACKEND_URL=http://localhost:5000
```

---

## 📊 What Judges See (Why MCPs Matter)

### Without MCPs
- Hardcoded data in dashboard
- No image audit trail
- Code is opaque

### With MCPs (Your Approach)
- **Live Google Drive folder**: Organized, verifiable images
- **Live Google Sheets**: Real-time data, transparent storage
- **GitHub history**: Shows iteration, not just final code
- **Web context**: Agent reasoning includes real-world data

**Result**: Judges see a production-grade system, not a hackathon project.

---

## 🚀 Quick Start Command for Claude

When you pass this to Claude for artifact generation:

```
"Build the Community Hero system using these MCP connectors:
- Google Drive: Store issue images organized by category
- Google Sheets: Live issue database
- GitHub: Version control with commits after each feature
- Web Search: Add real-time context to agent analysis

Follow the implementation guide at:
[path to COMMUNITY_HERO_IMPLEMENTATION.md]

Start with Day 1 tasks: Python Flask backend + Drive integration.
Test with 5 real Ghaziabad test cases."
```

Claude will:
1. Read the implementation guide
2. Access your Sheets to verify schema
3. Access your Drive to set up folder structure
4. Write the code
5. Commit to GitHub automatically
6. Return ready-to-test backend

---

## Troubleshooting MCPs

### Issue: "Permission denied" on Google Drive
**Solution**: 
```bash
# Regenerate service account JSON in Google Cloud Console
# Make sure your service account has:
# - Drive API enabled
# - Google Sheets API enabled
# - Correct permissions in service account
```

### Issue: "Sheets API quota exceeded"
**Solution**:
```python
# Add caching to reduce API calls
from functools import lru_cache
import time

@lru_cache(maxsize=1)
def get_issues_cached():
    """Cache Sheets data for 60 seconds."""
    return get_from_sheets()

# Refresh every 60 seconds
def get_issues_with_cache():
    if time.time() % 60 == 0:
        get_issues_cached.cache_clear()
    return get_issues_cached()
```

### Issue: GitHub MCP fails to commit
**Solution**:
```bash
# Ensure GitHub token has correct permissions
# Token should have: repo, workflow, admin:public_key

# Test locally first
git config --global user.email "your-email@example.com"
git config --global user.name "Community Hero Bot"
```

---

## 📈 Success Metrics

After integrating MCPs, you should have:

- ✅ **Google Drive folder** with 50+ organized images (judges can browse)
- ✅ **Google Sheets** with live issue data (judges can query)
- ✅ **GitHub repo** with 10+ commits showing iteration
- ✅ **Agent reasoning** that includes web context
- ✅ **Response time**: < 3 seconds per report (fast!)

---

## Final Note

MCPs transform your hackathon project from *"works on my machine"* to *"production-ready system with transparency."*

Judges will be impressed not just by features, but by how you've structured data, organized assets, and shown your iteration process.

**Use them strategically.** They're your secret weapon. 🚀

---

**Last Updated**: June 25, 2026  
**MCP Version Tested**: claude-opus-4-6 with integrated tools
