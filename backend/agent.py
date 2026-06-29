# backend/agent.py
from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

# Initialize Groq client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY', os.getenv('XAI_API_KEY')),
    base_url="https://api.groq.com/openai/v1"
)

GROQ_MODEL = os.getenv('GROQ_MODEL', 'qwen/qwen3.6-27b')

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
    """Analyze civic issue using Groq API (OpenAI-compatible)."""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=1024,
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
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

        # Robust JSON extraction
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        else:
            start = result_text.find('{')
            end = result_text.rfind('}')
            if start != -1 and end != -1:
                result_text = result_text[start:end+1]

        return json.loads(result_text)

    except Exception as e:
        print(f"[ERROR] Groq API error: {str(e)}")
        return {
            "category": "unknown",
            "priority": "medium",
            "severity_score": 3,
            "reasoning": f"API error: {str(e)}",
            "confidence_overall": 0.0
        }


def predict_future_issues(hotspots: list) -> dict:
    """Use Grok to predict future high-risk areas."""
    from datetime import datetime
    if not hotspots:
        return {"high_risk_locations": [], "timestamp": datetime.now().isoformat()}

    prompt = f"""
Based on these reported hotspots in Ghaziabad, predict which OTHER areas are at HIGH risk
for similar issues in the next 7 days.

Current hotspots:
{json.dumps(hotspots, indent=2)}

Consider monsoon season, old infrastructure in Sector 7-11, and NH-119 traffic load.

Return ONLY valid JSON:
{{
  "high_risk_locations": [
    {{
      "latitude": 28.6xxx,
      "longitude": 77.0xxx,
      "category": "pothole|water_leak|streetlight|waste_management|other",
      "confidence": 0.75,
      "reason": "explanation"
    }}
  ],
  "timestamp": "{datetime.now().isoformat()}"
}}
"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=1024,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        result_text = response.choices[0].message.content.strip()

        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        else:
            start = result_text.find('{')
            end = result_text.rfind('}')
            if start != -1 and end != -1:
                result_text = result_text[start:end+1]

        return json.loads(result_text)
    except Exception as e:
        print(f"[ERROR] Prediction agent failed: {e}")
        return {"high_risk_locations": [], "timestamp": datetime.now().isoformat(), "error": str(e)}
