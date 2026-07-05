# Community Hero - Environment Configuration Template
# Copy this file to .env and fill in your actual values
# IMPORTANT: Never commit .env to git (add to .gitignore)

###############################################
# GROK API CONFIGURATION (REQUIRED)
###############################################
# Get your free Grok API key from: https://console.x.ai
# Free tier: $25 credits (enough for ~1000+ requests)
# Optional: Data Sharing Program gives $150/month credits
XAI_API_KEY=xai-YOUR-GROK-API-KEY-HERE

###############################################
# OPTIONAL: BACKUP API KEYS
###############################################
# If you want to keep Anthropic as backup (optional):
# ANTHROPIC_API_KEY=sk-ant-v0-YOUR-KEY-HERE

# If you have Gemini API key (optional, for future enhancements):
# GEMINI_API_KEY=AIza-YOUR-KEY-HERE

###############################################
# LOCAL STORAGE CONFIGURATION
###############################################
# Where uploaded images are stored locally
UPLOAD_FOLDER=./uploads

# Where the SQLite database is stored
DATABASE_PATH=./issues.db

# Where application logs are saved
LOG_FOLDER=./logs

###############################################
# FLASK CONFIGURATION
###############################################
# Environment: development, staging, production
FLASK_ENV=development

# Enable debug mode (reload on code changes, detailed errors)
FLASK_DEBUG=1

# Port to run Flask on
FLASK_PORT=5000

# Secret key for session management (generate: python -c "import os; print(os.urandom(24).hex())")
FLASK_SECRET_KEY=your-secret-key-here-change-in-production

###############################################
# GROK MODEL SELECTION
###############################################
# Available models:
# - grok-4.3: Best quality, slower, more tokens ($1.25/1M)
# - grok-3-fast: Fastest, cheapest, good quality ($0.50/1M)
# - grok-build-0.1: Balanced speed/quality ($1.00/1M)
GROK_MODEL=grok-3-fast

###############################################
# DATABASE CONFIGURATION
###############################################
# Database type (sqlite for local, postgresql for production)
DB_TYPE=sqlite

# Database name (for SQLite, this is the filename)
DB_NAME=issues

###############################################
# LOGGING CONFIGURATION
###############################################
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log file path (leave blank to only log to console)
LOG_FILE=./logs/community-hero.log

# Log to console as well as file
LOG_TO_CONSOLE=true

###############################################
# API RATE LIMITING
###############################################
# Max requests per minute (to prevent abuse)
RATE_LIMIT_PER_MINUTE=60

# Max file upload size in MB
MAX_UPLOAD_SIZE_MB=10

###############################################
# CORS CONFIGURATION
###############################################
# Allowed origins (comma-separated)
# For development: localhost only
# For production: add your domain
CORS_ORIGINS=http://localhost:8000,http://localhost:5000

###############################################
# GHAZIABAD LOCATION DEFAULTS
###############################################
# Default map center (Ghaziabad, India)
DEFAULT_LATITUDE=28.6692
DEFAULT_LONGITUDE=77.0669
DEFAULT_ZOOM=13

# Duplicate detection radius (meters)
DUPLICATE_RADIUS_METERS=50

# Duplicate detection time window (days)
DUPLICATE_TIME_WINDOW_DAYS=7

###############################################
# ISSUE CATEGORY CONFIGURATION
###############################################
# Comma-separated list of allowed categories
ISSUE_CATEGORIES=pothole,water_leak,streetlight,waste_management,other

# Priority levels
PRIORITY_LEVELS=urgent,high,medium,low

###############################################
# FEATURE FLAGS
###############################################
# Enable/disable features
ENABLE_VOICE_INPUT=true
ENABLE_PREDICTIONS=true
ENABLE_DUPLICATE_DETECTION=true
ENABLE_IMPACT_ANALYTICS=true

###############################################
# OPTIONAL: CLOUD INTEGRATIONS
###############################################
# If you want to sync to cloud later:
# GOOGLE_DRIVE_FOLDER_ID=your-folder-id
# GOOGLE_SHEETS_ID=your-sheet-id
# SENDGRID_API_KEY=your-sendgrid-key
# TWILIO_ACCOUNT_SID=your-twilio-sid
# TWILIO_AUTH_TOKEN=your-twilio-token

###############################################
# OPTIONAL: ANALYTICS
###############################################
# Google Analytics (if you want to track usage)
# GOOGLE_ANALYTICS_ID=G-XXXXX

# Sentry (error tracking)
# SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

###############################################
# NOTES & INSTRUCTIONS
###############################################
# 1. REQUIRED:
#    - XAI_API_KEY must be set to use Grok API
#
# 2. OPTIONAL:
#    - All other variables have sensible defaults
#    - You only need to set them if you want to override defaults
#
# 3. SECURITY:
#    - NEVER commit this file to git
#    - Add .env to .gitignore
#    - Keep your API keys private
#    - Rotate keys periodically
#
# 4. GETTING API KEYS:
#    - Grok: https://console.x.ai (free $25 credits)
#    - Anthropic: https://console.anthropic.com (backup option)
#    - Gemini: https://ai.google.dev (optional)
#
# 5. FOR PRODUCTION:
#    - Set FLASK_ENV=production
#    - Set FLASK_DEBUG=0
#    - Use strong FLASK_SECRET_KEY
#    - Set up proper CORS_ORIGINS
#    - Use environment secrets manager
#    - Set up proper logging
#    - Enable HTTPS
#
# 6. FOR DEVELOPMENT:
#    - Use FLASK_ENV=development
#    - Set FLASK_DEBUG=1
#    - Use localhost for CORS
#    - Set LOG_LEVEL=DEBUG
#
# 7. TROUBLESHOOTING:
#    - "API key invalid" → Check XAI_API_KEY is correct
#    - "File not found" → Check UPLOAD_FOLDER path
#    - "Database error" → Check DATABASE_PATH is writable
#    - "CORS error" → Check CORS_ORIGINS includes your domain
###############################################
