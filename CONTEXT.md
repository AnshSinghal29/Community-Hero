# Community Hero - Agentic System Context

## Architecture
- Backend: Python Flask + Claude Anthropic API
- Frontend: HTML5 + Vanilla JS + Google Maps
- Data: Google Sheets + Google Drive
- Agents: Claude Opus 4.6 (analysis + predictions)

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

## Ghaziabad Context
- Population: ~1.7M
- Known hotspots: Sector 7-11 (infrastructure), NH-119 corridor (potholes)
- Monsoon (Jun-Sep): Water leaks peak, potholes increase
- Center coordinates: 28.6692, 77.0669
