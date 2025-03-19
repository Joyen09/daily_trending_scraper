# 📈 GitHub Daily Trending Scraper

This is an automated Python project that fetches GitHub Trending repositories every day and saves the result into a Markdown file (`trending.md`). It also keeps a daily backup of the trending data and logs all activities.

## 🔧 Features

- 📊 Scrapes [GitHub Trending](https://github.com/trending)
- 💾 Daily backup of trending.md into `/backups/`
- 📝 Outputs clear markdown format with title, URL, and description
- 🪵 Logging system with [loguru](https://github.com/Delgan/loguru)
- ⏰ Run daily via GitHub Actions (optional)

---

## 📂 Project Structure
```
├── daily_trending_scraper.py   # Main script
├── trending.md                 # Latest scraped trending repos
├── log.txt                     # Logs of scraping process
├── backups/                    # Historical markdown backup
├── requirements.txt            # Required dependencies
└── .github/workflows/
    └── daily.yml               # GitHub Actions scheduler
```

---

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
python daily_trending_scraper.py
```

---

## 💡 GitHub Actions Automation (Optional)
You can automate this job daily using GitHub Actions.
Make sure your repository has the correct permissions and `GITHUB_TOKEN` enabled for push access.

```yaml
# .github/workflows/daily.yml
name: Daily Trending Scraper

on:
  schedule:
    - cron: "0 0 * * *"  # runs every day at 00:00 UTC
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run scraper
        run: python daily_trending_scraper.py

      - name: Commit and push
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add .
          git commit -m "Update trending.md - $(date +'%Y-%m-%d')" || echo "Nothing to commit"
          git push
```

---

## 📦 Requirements
See `requirements.txt`:
```
requests
beautifulsoup4
loguru
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📬 Contact
Maintained by Joyen. Feel free to fork or raise an issue!

