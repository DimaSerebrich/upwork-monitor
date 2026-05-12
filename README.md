# Upwork Job Monitor 🔔

Monitors Upwork search queries for new job postings and sends real-time Telegram notifications with full job + client details.

## Features

- 🔍 **Any number of search URLs** — just add links to `settings.py`, timers adjust automatically
- 🤖 **Headless Chrome** via [nodriver](https://github.com/ultrafunkamsterdam/nodriver) — bypasses Cloudflare
- 📬 **Telegram notifications** with job details, client info, activity stats
- 🔁 **Global deduplication** — never sends the same job twice, even across different searches
- 🚫 **Smart filters** — skips low-budget fixed-price jobs and specific countries
- ⏱️ **Auto-scaled systemd timers** — timers are staggered evenly across 60 minutes based on URL count

## How it works

```
systemd timer (every 60min, staggered evenly across all URLs)
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
# Edit .env and fill in your Telegram bot token and channel ID
```

### 3. Add your search URLs

Open `settings.py` and edit `SEARCH_URLS`. You can paste any Upwork search page URL — as many as you want:

```python
SEARCH_URLS = [
    "https://www.upwork.com/nx/search/jobs/?q=Python+Backend&sort=recency&t=0,1",
    "https://www.upwork.com/nx/search/jobs/?q=React+Next.js&sort=recency&t=0,1",
    # add more...
]
```

> 💡 Tip: Set up your search on Upwork (skills, rate, job type, etc.), then just copy the URL from the browser.

### 4. Install systemd timers (as root)

```bash
sudo bash setup_timers.sh
```

The script reads `SEARCH_URLS` from `settings.py` and automatically creates the right number of timers, staggered evenly across 60 minutes.

**Examples:**
| URLs | Timer interval |
|------|---------------|
| 4    | every ~15 min |
| 8    | every ~7 min  |
| 12   | every ~5 min  |

Re-run `setup_timers.sh` any time you add or remove URLs.

### 5. Check logs

```bash
tail -f /tmp/upwork-monitor.log
```

## Configuration

All settings live in `settings.py`:

| Setting | Description |
|---|---|
| `SEARCH_URLS` | List of Upwork search page URLs to monitor |
| `SKIP_COUNTRIES` | Set of country names to skip (lowercase) |
| `MIN_FIXED_BUDGET` | Minimum fixed-price budget in USD (jobs below are skipped) |
| `COUNTRY_FLAGS` | Country → emoji flag mapping for notifications |

Secrets go in `.env`:

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (from @BotFather) |
| `TELEGRAM_CHANNEL` | Channel/chat ID to send jobs to |

## Manual run

```bash
# Run search index 0
python3 monitor.py 0

# Run all searches sequentially
for i in $(seq 0 $(($(python3 -c "from settings import SEARCH_URLS; print(len(SEARCH_URLS))")-1))); do
  python3 monitor.py $i
done
```

## Project structure

```
upwork-monitor/
├── monitor.py          # Main script
├── settings.py         # Search URLs, filters, all config
├── setup_timers.sh     # Install/update systemd timers
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your secrets (git-ignored)
└── state/
    └── seen_global.json  # Deduplication state (git-ignored)
```

## Telegram message format

Each notification includes:
- Title + direct link to the job
- Contract type, rate/budget, experience level, required skills
- Client: payment verified, rating, total spent, country flag
- Activity: proposals count, interviewing, last viewed by client
- Job description snippet
