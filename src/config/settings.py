import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================
# API KEYS
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "CricketNewsBot/1.0")

# =========================
# EMAIL
# =========================
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# =========================
# TELEGRAM
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# =========================
# DATABASE
# =========================
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/cricket_news.db")
VECTORDB_PATH = os.getenv("VECTORDB_PATH", "data/vectordb")

# =========================
# APP CONFIG
# =========================
VERIFICATION_ENABLED = os.getenv("VERIFICATION_ENABLED", "false").lower() == "true"
SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")
SCHEDULER_HOUR = int(os.getenv("SCHEDULER_HOUR", 8))
SCHEDULER_MINUTE = int(os.getenv("SCHEDULER_MINUTE", 0))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")