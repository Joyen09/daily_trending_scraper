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
        h1_tag = repo_item.find("h1")
        if not h1_tag:
            continue  # Skip if no h1 found (unexpected format)

        title = h1_tag.text.strip().replace("\n", " ").replace("  ", " ")
        description_tag = repo_item.select_one("p")
        description = description_tag.text.strip() if description_tag else "No description"
        link = "https://github.com/" + h1_tag.a['href'].strip()
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
