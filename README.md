# Upwork Job Monitor 🔔

Monitors multiple Upwork search queries for new job postings and sends real-time Telegram notifications with full job + client details.

## Features

- 🔍 **8 search queries** — Python/FastAPI, Scrapy, React, AI/LLM, ETL and more
- 🤖 **Headless Chrome** via [nodriver](https://github.com/ultrafunkamsterdam/nodriver) — bypasses Cloudflare
- 📬 **Telegram notifications** with job details, client info, activity stats
- 🔁 **Global deduplication** — never sends the same job twice, even across different searches
- 🚫 **Smart filters** — skips low-budget fixed-price jobs and specific countries
- ⏱️ **systemd timers** — 8 staggered timers = effectively checks every ~7 minutes

## How it works

```
systemd timer (every 60min, offset by 7min each)
    └── monitor.py <index>
            ├── Open search URL in headless Chrome
            ├── Wait for Cloudflare to pass
            ├── Parse job tiles from HTML
            ├── For each new job: open job page → extract client info
            ├── Apply filters (country, budget)
            └── Send to Telegram → save to state/seen_global.json
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your values
```

### 3. Install systemd timers (as root)

```bash
sudo bash setup_timers.sh
```

This installs 8 timers (`upwork-monitor-0` … `upwork-monitor-7`) that run every 60 minutes, staggered 7 minutes apart.

### 4. Check logs

```bash
tail -f /tmp/upwork-monitor.log
```

## Configuration

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHANNEL` | Channel/chat ID to send jobs to |

Edit `SEARCH_URLS` in `monitor.py` to customize which queries to monitor.

Edit `SKIP_COUNTRIES` and `MIN_FIXED_BUDGET` to adjust filters.

## Manual run

```bash
# Run search index 0 (Python Backend)
python3 monitor.py 0

# Run all searches sequentially
for i in {0..7}; do python3 monitor.py $i; done
```

## Project structure

```
upwork-monitor/
├── monitor.py          # Main script
├── setup_timers.sh     # Install systemd timers
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your secrets (git-ignored)
└── state/
    └── seen_global.json  # Deduplication state (git-ignored)
```

## Telegram message format

Each job notification includes:
- Title + direct link
- Contract type, rate/budget, experience level, skills
- Client: payment verified, rating, total spent, country
- Activity: proposals count, interviewing, last viewed
- Job description snippet
