"""
settings.py — all configuration for Upwork Monitor.
Edit this file to add/remove search URLs, adjust filters, etc.
"""

# ── Telegram ──────────────────────────────────────────────────────────────────
# Loaded from .env — do not hardcode here.
# Required env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL

# ── Search URLs ───────────────────────────────────────────────────────────────
# Each URL gets its own systemd timer.
# Run `sudo bash setup_timers.sh` after adding/removing URLs.

SEARCH_URLS = [
    # Python backend
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=Python%20Backend%20Developer%20RestAPI%20Rest%20API&sort=recency&t=0,1",
    # FastAPI / Django / PostgreSQL
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=FastAPI%20Fast%20API%20Python%20PostgreSQL%20SQL%20Postgres%20Django&sort=recency&t=0,1",
    # Scraping
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=Scrapy%20Scraping%20Scrapping%20Data%20Extraction&sort=recency&t=0,1",
    # Automation / bots
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=Python%20Automation%20Bots%20Scripts&sort=recency&t=0,1",
    # React / Next.js
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=React.js%20ReactJS%20React%20Js%20Next.js%20NextJS%20Next%20Js%20Full%20Stack%20FullStack&sort=recency&t=0,1",
    # React Native / mobile
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=ReactNative%20React%20Native%20Mobile%20App&sort=recency&t=0,1",
    # LLM / RAG / AI agents
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=LLM%20RAG%20AI%20Agent%20LangChain%20LlamaIndex&sort=recency&t=0,1",
    # Data pipelines / ETL
    "https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2,3&hourly_rate=25-&job_type=hourly,fixed&q=Data%20Pipeline%20ETL%20PostgreSQL%20Scraping%20Data%20Engineering&sort=recency&t=0,1",
]

# ── Filters ───────────────────────────────────────────────────────────────────

# Skip jobs from these countries (lowercase)
SKIP_COUNTRIES = {"india", "bangladesh", "pakistan"}

# Skip fixed-price jobs below this budget (USD)
MIN_FIXED_BUDGET = 1000

# ── Country flags ─────────────────────────────────────────────────────────────

COUNTRY_FLAGS = {
    "United States": "🇺🇸", "Canada": "🇨🇦", "United Kingdom": "🇬🇧",
    "Australia": "🇦🇺", "Germany": "🇩🇪", "Netherlands": "🇳🇱",
    "France": "🇫🇷", "Sweden": "🇸🇪", "Norway": "🇳🇴",
    "Switzerland": "🇨🇭", "Israel": "🇮🇱", "UAE": "🇦🇪", "Singapore": "🇸🇬",
}
