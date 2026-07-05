# -*- coding: utf-8 -*-
# Community Hero -- Quick Start Script
# Run this from the project root: py start.py

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
BACKEND = ROOT / "backend"
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"

print("=" * 55)
print("  🏛️  Community Hero — Quick Start")
print("=" * 55)
print()

# ── Check .env exists ──
if not ENV_FILE.exists():
    print("⚠️  .env file not found!")
    print(f"   Copy .env.example → .env and fill in your API keys.")
    print(f"   Then re-run: py start.py")
    print()
    sys.exit(1)

# ── Check for service account ──
sa_path = BACKEND / "service_account.json"
if not sa_path.exists():
    print("⚠️  service_account.json not found in backend/")
    print("   Download it from Google Cloud Console.")
    print("   Google Sheets integration will fail without it.")
    print()

# ── Load and show key env vars ──
from dotenv import dotenv_values
env = dotenv_values(ENV_FILE)

def masked(val):
    if not val: return "NOT SET ❌"
    if len(val) > 8: return val[:6] + "..." + val[-4:] + " ✅"
    return "SET ✅"

print("Configuration:")
print(f"  ANTHROPIC_API_KEY     : {masked(env.get('ANTHROPIC_API_KEY'))}")
print(f"  GOOGLE_SHEETS_ID      : {masked(env.get('GOOGLE_SHEETS_ID'))}")
print(f"  GOOGLE_MAPS_API_KEY   : {masked(env.get('GOOGLE_MAPS_API_KEY'))}")
print()

# ── Start Flask ──
port = env.get("FLASK_PORT", "5000")
print(f"Starting Flask on http://localhost:{port} ...")
print(f"Open frontend/dashboard.html in your browser.")
print(f"Press Ctrl+C to stop.\n")

os.chdir(BACKEND)
subprocess.run([sys.executable, "app.py"])
