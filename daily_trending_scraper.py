from loguru import logger
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger.add("log.txt", rotation="1 week", encoding="utf-8", enqueue=True)

def fetch_trending():
    url = "https://github.com/trending"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info("Fetched trending page successfully.")
        return response.text
    except Exception as e:
        logger.error(f"Failed to fetch trending page: {e}")
        return None

def parse_trending(html):
    soup = BeautifulSoup(html, "html.parser")
    repo_items = soup.find_all("article", class_="Box-row")
    logger.info(f"Found {len(repo_items)} repositories.")
    repos = []

    if not repo_items:
        logger.warning("No repositories found. GitHub page structure may have changed.")
        return repos

    for repo_item in repo_items:
        try:
            h1_tag = repo_item.h1
            if not h1_tag:
                continue
            title = h1_tag.text.strip().replace("\n", " ").replace("  ", " ")
            link = "https://github.com" + h1_tag.a["href"]
            description_tag = repo_item.find("p", class_="col-9 color-fg-muted my-1 pr-4")
            description = description_tag.text.strip() if description_tag else "No description"
            repos.append((title, link, description))
        except Exception as e:
            logger.error(f"Error parsing a repository block: {e}")
    return repos

def write_to_markdown(repos):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = "trending.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# GitHub Trending Repos - {today}\n\n")
        if repos:
            for idx, (title, link, description) in enumerate(repos, 1):
                f.write(f"{idx}. [{title}]({link})\n   - {description}\n\n")
        else:
            f.write("_No trending repositories found today. This may be due to a GitHub page update._\n")
    logger.info(f"Wrote results to {filename}")

if __name__ == "__main__":
    html = fetch_trending()
    if html:
        trending_repos = parse_trending(html)
        write_to_markdown(trending_repos)
    else:
        logger.error("No HTML content retrieved. Skipping markdown output.")
