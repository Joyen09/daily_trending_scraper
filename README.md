# Daily GitHub Trending Fetcher

This project automatically fetches GitHub Trending repositories every day and outputs them to a markdown file (`trending.md`).

## 🔧 Features
- Scrapes GitHub Trending page (daily)
- Parses top repositories: name, description, link
- Outputs as clean Markdown file
- Can be automated using GitHub Actions

## 📁 Output Example
```
# GitHub Trending Repos - 2025-03-17

1. [octocat/Hello-World](https://github.com/octocat/Hello-World)
   - My first repository on GitHub!

2. [torvalds/linux](https://github.com/torvalds/linux)
   - Linux kernel source tree
```

## ▶ How to Run Locally
```bash
pip install -r requirements.txt
python daily_trending_scraper.py
```

## ⚙ GitHub Actions Setup
To automate the fetch daily, add the following workflow file at `.github/workflows/daily.yml`:
```yaml
name: Daily Trending Fetcher

on:
  schedule:
    - cron: '0 2 * * *' # Every day at 10:00 AM Taiwan time
  workflow_dispatch:

jobs:
  fetch-trending:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install beautifulsoup4 requests

      - name: Run trending fetch script
        run: python daily_trending_scraper.py

      - name: Commit & push result
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add trending.md
          git commit -m "Update trending.md $(date '+%Y-%m-%d')" || echo "Nothing to commit"
          git push
```

## 📦 Requirements
See `requirements.txt`:
```
requests
beautifulsoup4
```

---

Feel free to star 🌟 this project if you find it useful!

