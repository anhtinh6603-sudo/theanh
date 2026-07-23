"""Bot 1 - Web Scraper

Pulls trending items from RSS news feeds plus Hacker News and Reddit's public
JSON endpoints. We deliberately don't scrape Facebook/TikTok pages directly:
those sites block automated scraping at the network/ToS level (confirmed to
be unreachable through this environment's own proxy), and scraping them
without their official APIs is against their terms of service. RSS + public
JSON trending endpoints give the same "what's hot right now" signal legally
and reliably.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import hashlib
import logging

import feedparser
import requests

import config
from utils import append_jsonl, now_iso, read_jsonl

log = logging.getLogger("bot1_scraper")

USER_AGENT = "Mozilla/5.0 (compatible; ContentBotSystem/1.0)"
HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
REDDIT_HOT = "https://www.reddit.com/r/all/hot.json?limit=25"


def _item_id(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def fetch_rss(feed_urls: list[str]) -> list[dict]:
    items = []
    for feed_url in feed_urls:
        try:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[:20]:
                url = entry.get("link", "")
                if not url:
                    continue
                items.append(
                    {
                        "title": entry.get("title", "").strip(),
                        "url": url,
                        "source": f"rss:{parsed.feed.get('title', feed_url)}",
                        "summary": entry.get("summary", "")[:500],
                    }
                )
        except Exception as exc:
            log.warning("RSS feed failed (%s): %s", feed_url, exc)
    return items


def fetch_hackernews(limit: int = 20) -> list[dict]:
    items = []
    try:
        ids = requests.get(HN_TOP_STORIES, timeout=10).json()[:limit]
        for story_id in ids:
            story = requests.get(HN_ITEM.format(story_id), timeout=10).json()
            if not story or "title" not in story:
                continue
            items.append(
                {
                    "title": story["title"],
                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "source": "hackernews",
                    "summary": f"{story.get('score', 0)} points, {story.get('descendants', 0)} comments",
                }
            )
    except Exception as exc:
        log.warning("Hacker News fetch failed: %s", exc)
    return items


def fetch_reddit(limit: int = 20) -> list[dict]:
    items = []
    try:
        resp = requests.get(REDDIT_HOT, headers={"User-Agent": USER_AGENT}, timeout=10)
        resp.raise_for_status()
        for child in resp.json()["data"]["children"][:limit]:
            post = child["data"]
            items.append(
                {
                    "title": post.get("title", ""),
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "source": f"reddit:r/{post.get('subreddit', 'all')}",
                    "summary": f"{post.get('ups', 0)} upvotes",
                }
            )
    except Exception as exc:
        log.warning("Reddit fetch failed: %s", exc)
    return items


def run() -> int:
    """Fetch trending items from all sources, dedupe against what's already
    stored, append only new ones with status="new". Returns the count added.
    """
    existing = read_jsonl(config.TRENDING_FILE)
    seen_urls = {item["url"] for item in existing}

    raw_items = fetch_rss(config.RSS_FEEDS) + fetch_hackernews() + fetch_reddit()

    added = 0
    for raw in raw_items:
        if not raw.get("title") or not raw.get("url") or raw["url"] in seen_urls:
            continue
        seen_urls.add(raw["url"])
        record = {
            "id": _item_id(raw["url"]),
            "title": raw["title"],
            "url": raw["url"],
            "source": raw["source"],
            "summary": raw.get("summary", ""),
            "scraped_at": now_iso(),
            "status": "new",
        }
        append_jsonl(config.TRENDING_FILE, record)
        added += 1

    log.info("Bot1 scraper: added %d new trending items (%d fetched total)", added, len(raw_items))
    return added


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    run()
