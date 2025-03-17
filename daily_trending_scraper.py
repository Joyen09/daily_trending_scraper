# daily_trending_scraper.py
import requests
from datetime import datetime

GITHUB_TRENDING_URL = "https://github.com/trending?since=daily"

def fetch_trending_html():
    response = requests.get(GITHUB_TRENDING_URL)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch trending page")

def parse_trending(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    repos = []
    for repo_item in soup.select("article.Box-row"):
        title = repo_item.h1.text.strip().replace("\n", " ").replace("  ", " ")
        description_tag = repo_item.select_one("p")
        description = description_tag.text.strip() if description_tag else "No description"
        link = "https://github.com/" + repo_item.h1.a['href'].strip()
        repos.append((title, description, link))
    return repos

def generate_markdown(repos):
    today = datetime.now().strftime('%Y-%m-%d')
    output = f"# GitHub Trending Repos - {today}\n\n"
    for idx, (title, desc, link) in enumerate(repos, 1):
        output += f"{idx}. [{title}]({link})\n   - {desc}\n\n"
    return output

def save_to_file(markdown_text):
    with open("trending.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)

if __name__ == "__main__":
    html = fetch_trending_html()
    trending_repos = parse_trending(html)
    markdown = generate_markdown(trending_repos)
    save_to_file(markdown)
    print("Trending repos markdown generated.")

# README.md

# Daily GitHub Trending Fetcher

This project automatically fetches GitHub Trending repositories every day and outputs them to a markdown file.

- Scheduled with GitHub Actions (daily)
- Written in Python
- Output file: `trending.md`

## Features
- Scrapes GitHub Trending page
- Parses top repositories (name, description, link)
- Generates a clean Markdown file
- Automatically commits updates every day

## Output Example
```
# GitHub Trending Repos - 2025-03-17

1. [octocat/Hello-World](https://github.com/octocat/Hello-World)
   - My first repository on GitHub!

2. [torvalds/linux](https://github.com/torvalds/linux)
   - Linux kernel source tree
```

## How to Run Locally
```bash
pip install -r requirements.txt
python daily_trending_scraper.py
```

## GitHub Actions Workflow
Add this in `.github/workflows/daily.yml` to automate daily run:
```yaml
name: Daily Trending Fetcher

on:
  schedule:
    - cron: '0 2 * * *'  # 每天台灣時間上午10點執行（UTC+8）
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

---

## requirements.txt
```
requests
beautifulsoup4
```

---

Enjoy and star the repo if you find it useful!
