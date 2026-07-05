# FREE API Alternatives - Quick Setup Guide

**Time to implement**: 2–3 hours  
**Cost**: $0

---

## 🚀 30-Second Overview

| What | Was Using | Now Using | Cost |
|------|-----------|-----------|------|
| AI Analysis | Claude Opus 4.6 | Claude 3.5 Haiku | Free |
| Maps | Google Maps API | OpenStreetMap + Leaflet | Free |
| Database | Google Sheets | SQLite (local) | Free |
| Storage | Google Drive | Local file system | Free |

---

## ⏱️ Quick Setup (3 Steps)

### Step 1: Get Free Anthropic API Key (5 minutes)

1. Go to: https://console.anthropic.com/
2. Sign up (no credit card needed)
3. Create API key → Copy it
4. Open `.env` file in your project:

```
ANTHROPIC_API_KEY=sk-ant-v0-YOUR-FREE-KEY-HERE
```

**That's it!** You get 100K tokens/month free (enough for ~50 reports/day)

---

### Step 2: Update in Antigravity IDE (1 hour)

**Open Antigravity IDE Manager View**

Create new agent:

```
Name: Cost-Optimization-Engineer
Role: Replace paid APIs with free alternatives
Skills: Database migration, API integration, optimization
Primary task: Implement free tier changes
```

**Assign this task**:

```
TASK: Migrate Community Hero to Free APIs

1. Backend Changes:
   
   a) Replace google_sheets.py with database.py:
      - Use SQLite (built-in Python)
      - Functions: save_to_db(), get_from_db(), get_stats()
      - Table: issues with columns: id, timestamp, category, priority, severity_score, latitude, longitude, address, description, reasoning, recommended_action, image_url, confidence, status
      
   b) Update backend/app.py:
      - Change imports from "gspread" to "database"
      - All get_from_sheets() → get_from_db()
      - All save_to_sheets() → save_to_db()
      - Image uploads go to /uploads/ folder (local)
      - Database initializes automatically

   c) Update backend/agent.py:
      - Change model from "claude-opus-4-6" to "claude-3-5-haiku-20241022"
      - Keep all vision capability
      - Reduce max_tokens from 2000 to 1024 (Haiku is efficient)
      - Keep extended thinking (if implemented)

2. Frontend Changes:
   
   Replace dashboard.html:
   - Use Leaflet (free map library from CDN)
   - Use OpenStreetMap tiles (no API key needed)
   - Keep all functionality: markers, colors, click-to-report, real-time updates
   - No changes to the report form or stats panel
   - Only the map part changes (Google Maps → Leaflet)

3. Configuration:
   
   Update .env:
   - Remove: GOOGLE_SHEETS_ID, GOOGLE_MAPS_API_KEY, service_account.json needs
   - Keep: ANTHROPIC_API_KEY (free tier)
   - Add: UPLOAD_FOLDER=./uploads

4. Verification:

   Test locally:
   - python backend/app.py (Flask starts)
   - Create test issue with image
   - Image saves to /uploads/
   - Issue appears in SQLite (issues.db)
   - Frontend loads with Leaflet map
   - No API key errors in console
   - /api/stats returns JSON from database
   - All color-coded markers work
   - Click issue → map centers

Return: Updated database.py, app.py, agent.py, dashboard.html, requirements.txt
```

---

### Step 3: Verify Everything Works (30 minutes)

Once agent finishes, test locally:

```bash
# Terminal 1: Backend
cd community-hero/backend
pip install -r requirements.txt
python app.py
# Should see: "Running on http://localhost:5000"

# Terminal 2: Frontend
cd community-hero/frontend
python -m http.server 8000
# Open: http://localhost:8000/dashboard.html
```

**Test checklist**:
- [ ] Map displays (should be green/brown OpenStreetMap, not Google)
- [ ] Stats show 0 issues initially
- [ ] Click map → form opens
- [ ] Submit test image + description
- [ ] Form says "Analyzing..."
- [ ] Agent responds with category/priority
- [ ] Issue appears on map
- [ ] Check `/uploads/` folder → image file there
- [ ] Check `issues.db` file exists

**Verify database**:
```bash
# In project root
sqlite3 issues.db "SELECT * FROM issues;"
# Should show your test issue as a row
```

---

## 📋 What Changed (High-Level)

### Before (Paid APIs)
```python
# backend/google_sheets.py
import gspread
sheet = client.open('Community Hero').worksheet('Reports')
sheet.append_row([...])  # $$$

# frontend/dashboard.html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY"></script>
```

### After (Free APIs)
```python
# backend/database.py
import sqlite3
conn = sqlite3.connect('issues.db')
cursor.execute('INSERT INTO issues VALUES (...)')  # FREE

# frontend/dashboard.html
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
```

**Same functionality, zero cost.**

---

## 🎯 Files You Need to Know

**Files that change**:
```
community-hero/
├── backend/
│   ├── app.py ← UPDATED (use database.py instead of google_sheets.py)
│   ├── agent.py ← UPDATED (use Haiku instead of Opus)
│   ├── database.py ← NEW FILE (replaces google_sheets.py)
│   ├── google_sheets.py ← DELETE (not needed)
│   └── requirements.txt ← UPDATED (remove gspread)
├── frontend/
│   └── dashboard.html ← UPDATED (use Leaflet instead of Google Maps)
└── .env ← UPDATED (only ANTHROPIC_API_KEY needed)
```

**Files that stay the same**:
```
├── CONTEXT.md
├── README.md
├── uploads/ ← NEW (auto-created)
└── issues.db ← NEW (auto-created)
```

---

## 💰 Cost Breakdown

**Before**:
- Anthropic: $15/1M tokens (~$5–10/month for this project)
- Google Maps: $7 per 1000 requests (~$10–20/month)
- Google Sheets/Drive: Free tier, but complex setup
- **Total**: ~$20–30/month + setup hassle

**After**:
- Anthropic: Free 100K tokens/month
- Maps: Free (OpenStreetMap)
- Database: Free (SQLite)
- Storage: Free (local)
- **Total**: $0/month + zero setup hassle ✅

---

## 🔧 Common Questions

**Q: Will the free Haiku tier be fast enough?**  
A: Yes! Haiku is designed for fast categorization tasks. Opus is overkill for this project. Haiku is actually faster (1–2 sec vs 2–3 sec).

**Q: What if I run out of free tokens?**  
A: 100K tokens = ~50 issues/day. If you submit 50+ issues in one day during hackathon, you hit the limit. Solution: Get a paid API key later (takes 2 minutes to switch).

**Q: Is SQLite safe for production?**  
A: For a hackathon MVP? Yes. For actual production? Use PostgreSQL. But for now, perfect.

**Q: Can I migrate to Google Sheets later?**  
A: Yes. Just export SQLite to CSV, upload to Google Sheets manually. Takes 5 minutes.

**Q: Will judges see the database?**  
A: Yes! When you submit, include:
   - `issues.db` (SQLite database file)
   - `/uploads/` folder (all test images)
   - Judges can open both and verify data integrity

---

## 🚀 The Antigravity Prompt (Copy-Paste Ready)

Use this exact prompt in your Antigravity IDE Manager View:

```
I want to convert Community Hero to use free APIs. Here's what to do:

1. Create backend/database.py:
   - SQLite integration with these functions:
     - init_db() → creates issues table
     - save_to_db(analysis, image_path, timestamp) → saves to SQLite, returns report_id
     - get_from_db(category=None, priority=None, limit=100) → fetches from SQLite
     - get_recent_reports(lat, lng, days=7, radius=50) → for duplicate detection
     - get_stats() → returns {total, urgent, high, resolved}
   
   Table schema:
   - id (TEXT PRIMARY KEY)
   - timestamp (TEXT)
   - category (TEXT)
   - priority (TEXT)
   - severity_score (INTEGER)
   - latitude (REAL)
   - longitude (REAL)
   - address (TEXT)
   - description (TEXT)
   - reasoning (TEXT)
   - recommended_action (TEXT)
   - image_url (TEXT - local path)
   - confidence (REAL)
   - status (TEXT)

2. Update backend/app.py:
   - Replace "import gspread" with "from database import *"
   - All endpoints now use database functions
   - Images save to /uploads/ folder locally
   - No more Google Sheets API calls
   - Keep all error handling

3. Update backend/agent.py:
   - Change model to "claude-3-5-haiku-20241022"
   - Keep vision capability
   - Reduce max_tokens to 1024
   - Keep extended thinking if present

4. Create frontend/dashboard.html:
   - Use Leaflet library (free, from CDN)
   - Use OpenStreetMap tiles (free, no API key)
   - Keep all functionality exactly the same:
     - Stats panel (total, urgent, high, resolved %)
     - Issues list with color-coded cards
     - Map with colored markers
     - Click map to report
     - Form submission
     - Real-time updates
   - Only difference: Google Maps → Leaflet maps

5. Update requirements.txt:
   - Remove: gspread, google-auth-oauthlib, google-auth-httplib2
   - Keep: flask, flask-cors, anthropic, python-dotenv
   - SQLite is built-in (no install needed)

6. Create .env with only:
   ANTHROPIC_API_KEY=sk-ant-v0-...

Test locally:
- python app.py
- Open dashboard.html
- Submit test image
- Verify in /uploads/ and issues.db

Return: All updated files with no Google API dependencies
```

---

## ✅ After Implementation Checklist

- [ ] ANTHROPIC_API_KEY is free tier key (sk-ant-v0-...)
- [ ] `database.py` created with SQLite functions
- [ ] `app.py` updated to use database.py
- [ ] `agent.py` using claude-3-5-haiku-20241022
- [ ] `dashboard.html` using Leaflet (no Google Maps)
- [ ] `.env` only has ANTHROPIC_API_KEY
- [ ] `/uploads/` folder created (auto on first run)
- [ ] `issues.db` file created (auto on first run)
- [ ] `google_sheets.py` deleted
- [ ] No Google Cloud credentials needed
- [ ] No service_account.json file needed
- [ ] Test image uploads work
- [ ] SQLite stores data correctly
- [ ] Map displays with Leaflet
- [ ] All stats show correct counts
- [ ] No API key errors in console

---

## 🎉 You're Done!

You now have a **fully functional, zero-cost Community Hero** that:
- ✅ Uses free Claude API (100K tokens/month)
- ✅ Uses free OpenStreetMap (unlimited)
- ✅ Uses free SQLite (unlimited)
- ✅ Uses local storage (unlimited)
- ✅ Works offline (no internet for DB)
- ✅ Runs on your machine (full control)
- ✅ Impressive for judges (shows smart optimization)

**Cost: $0/month**  
**Time to implement: 2–3 hours in Antigravity**  
**Ready to submit: YES ✅**

---

## 🚀 Next Steps

1. **Read**: FREE_API_ALTERNATIVES.md (full technical details)
2. **Copy-paste**: The Antigravity prompt above
3. **Monitor**: Agent builds in Manager View
4. **Test**: Verify everything works locally
5. **Commit**: Push to GitHub
6. **Submit**: You're winning with zero API costs

**Good luck! 🏛️**

---

**Last Updated**: June 25, 2026  
**Status**: Ready to implement (copy-paste prompt into Antigravity)
