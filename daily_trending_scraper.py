# daily_trending_scraper.py
# 📊 GitHub Trending 自動爬蟲，每日備份與記錄

from loguru import logger
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import shutil
import os

# 加入日誌紀錄器
logger.add("log.txt", rotation="1 week", encoding="utf-8", enqueue=True)

def fetch_trending():
    """從 GitHub Trending 頁面抓取 HTML"""
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info("✅ 成功取得 GitHub Trending 頁面")
        return response.text
    except Exception as e:
        logger.error(f"❌ 無法取得 GitHub Trending 頁面: {e}")
        return None

def parse_trending(html):
    """解析 HTML 並擷取 trending 倉庫資料"""
    soup = BeautifulSoup(html, "html.parser")
    repo_items = soup.select("article.Box-row")
    logger.info(f"🔍 找到 {len(repo_items)} 個 trending 倉庫")
    repos = []

    if not repo_items:
        logger.warning("⚠️ 找不到 trending 倉庫，GitHub 頁面結構可能改變")
        return repos

    for repo_item in repo_items:
        try:
            h1_tag = repo_item.select_one("h2 a") or repo_item.h1
            if not h1_tag:
                continue
            title = h1_tag.text.strip().replace("\n", " ").replace("  ", " ")
            link = "https://github.com" + h1_tag.get("href", "")
            description_tag = repo_item.find("p")
            description = description_tag.text.strip() if description_tag else "No description"
            repos.append((title, link, description))
        except Exception as e:
            logger.error(f"❌ 解析倉庫資料失敗: {e}")
    return repos

def backup_previous_file():
    """備份前一天的 markdown 檔案"""
    today = datetime.now().strftime("%Y-%m-%d")
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    source_file = "trending.md"
    backup_file = os.path.join(backup_dir, f"trending_{today}.md")
    if os.path.exists(source_file):
        shutil.copy2(source_file, backup_file)
        logger.info(f"💾 備份 trending.md 到 {backup_file}")

def write_to_markdown(repos):
    """輸出 trending 資料到 markdown 檔"""
    backup_previous_file()
    today = datetime.now().strftime("%Y-%m-%d")
    filename = "trending.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# GitHub Trending Repos - {today}\n\n")
        if repos:
            for idx, (title, link, description) in enumerate(repos, 1):
                f.write(f"{idx}. [{title}]({link})\n   - {description}\n\n")
        else:
            f.write("*No trending repositories found today. This may be due to a GitHub page update.*\n")
    logger.info(f"✅ 已輸出 markdown 檔：{filename}")

if __name__ == "__main__":
    html = fetch_trending()
    if html:
        trending_repos = parse_trending(html)
        write_to_markdown(trending_repos)
    else:
        logger.error("⚠️ 未取得 HTML 資料，停止輸出")
