# Grok API - Quick Setup (5 Minutes)

---

## 🎯 Direct Link to Get API Key

👉 **https://console.x.ai**

**Do this**:
1. Sign up (email or Google)
2. Go to API Keys
3. Click "Create API Key"
4. Copy the key (starts with `xai-`)
5. Done!

---

## 📝 Update `.env` File

**Location**: `c:\Community Hero\.env`

**Content**:
```env
XAI_API_KEY=xai-YOUR-KEY-HERE
UPLOAD_FOLDER=./uploads
DATABASE_PATH=./issues.db
FLASK_ENV=development
FLASK_DEBUG=1
GROK_MODEL=grok-3-fast
```

Replace `xai-YOUR-KEY-HERE` with your actual key.

---

## 🔧 Update `requirements.txt`

**File**: `c:\Community Hero\backend\requirements.txt`

**Change**:
```
BEFORE:
anthropic

AFTER:
openai
```

---

## 💻 Update `backend/agent.py`

**Replace the entire file** with this:

```python
# backend/agent.py
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize Grok client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv('XAI_API_KEY'),
    base_url="https://api.x.ai/v1"
)

GROK_MODEL = os.getenv('GROK_MODEL', 'grok-3-fast')

SYSTEM_PROMPT = """You are an autonomous civic issue triage agent for Ghaziabad, Uttar Pradesh, India.

Your role:
- Analyze citizen reports (photo + description + location)
- Determine issue category, severity, and priority
- Predict impact and recommend action

Context about Ghaziabad:
- Known hotspots: Sector 7-11 (infrastructure), NH-119 corridor (potholes)
- Monsoon (Jun-Sep): Water leaks peak, potholes increase

Analysis process:

1. IMAGE ANALYSIS: What damage is visible? Rate severity 1-5.

2. CATEGORY: Pothole, Water leak, Streetlight, Waste management, or Other.

3. PRIORITY: URGENT (safety risk), HIGH (inconvenience), MEDIUM (noticeable), LOW (tracked).

4. DUPLICATE CHECK: Compare to recent reports (7 days, 50m radius).

5. REASONING: Explain priority, recommend action, estimate resolution time.

Output ONLY valid JSON:
{
  "category": "pothole|water_leak|streetlight|waste_management|other",
  "severity_score": 3,
  "priority": "urgent|high|medium|low",
  "reasoning": "...",
  "confidence_overall": 0.92
}
"""

def analyze_issue(image_base64: str, description: str, lat: float, lng: float, recent_reports: list) -> dict:
    """Analyze civic issue using Grok API (OpenAI-compatible)."""
    
    try:
        response = client.chat.completions.create(
            model=GROK_MODEL,
            max_tokens=1024,
            temperature=0.7,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        },
                        {
                            "type": "text",
                            "text": f"""Analyze this civic issue:
DESCRIPTION: {description}
LOCATION: {lat}, {lng}
RECENT_REPORTS: {recent_reports}

Return ONLY JSON."""
                        }
                    ]
                }
            ]
        )
        
        result_text = response.choices[0].message.content.strip()
        
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1].strip()
            if result_text.startswith("json"):
                result_text = result_text[4:].strip()
        
        return json.loads(result_text)
    
    except Exception as e:
        print(f"[ERROR] Grok API error: {str(e)}")
        return {
            "category": "unknown",
            "priority": "medium",
            "severity_score": 3,
            "reasoning": f"API error: {str(e)}",
            "confidence_overall": 0.0
        }
```

---

## ✅ Verification (Copy-Paste)

**Run in PowerShell**:
```powershell
cd "c:\Community Hero"

# Check Grok key
py -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Grok Key Loaded!' if os.getenv('XAI_API_KEY') else '❌ Key Missing!')"

# Install dependencies
cd backend
pip install -r requirements.txt

# Run app
py app.py
```

Should see: `Running on http://127.0.0.1:5000` ✅

---

## 🎯 That's It!

**Your Community Hero now uses**:
- ✅ Grok API (free $25 credits)
- ✅ OpenAI SDK (easier integration)
- ✅ Local SQLite database
- ✅ OpenStreetMap + Leaflet
- ✅ Zero hidden costs

---

## 🚀 Run Forever

```powershell
cd "c:\Community Hero\backend"
py app.py
```

Open: `c:\Community Hero\frontend\dashboard.html`

**Done!** 🏆

---

## 📋 What Changed

| Component | Before | After |
|-----------|--------|-------|
| API | Anthropic Claude | Grok (xAI) |
| SDK | `anthropic` | `openai` |
| Model | `claude-3-5-haiku` | `grok-3-fast` |
| Free Tier | 100K tokens | $25 credits |
| Speed | Medium | Fast ⚡ |

---

## ❓ FAQ

**Q: Is Grok really free?**  
A: Yes! $25 free credits. For hackathon (~1000 requests), completely free.

**Q: What if I run out of credits?**  
A: Add payment method (optional) or opt into data sharing program ($150/month free!).

**Q: Is Grok as good as Claude?**  
A: For this task (issue categorization), yes. Grok is fast and accurate enough.

**Q: Can I switch back to Anthropic?**  
A: Yes! Just change `XAI_API_KEY` to `ANTHROPIC_API_KEY` in `.env` and swap imports.

---

## 🔗 Direct Links

| Service | Link |
|---------|------|
| Grok API Console | https://console.x.ai |
| API Keys | https://console.x.ai/api-keys |
| API Docs | https://x.ai/api |
| Pricing | https://x.ai/api (see pricing tab) |

---

**Status**: ✅ Ready to implement (5 min setup)

