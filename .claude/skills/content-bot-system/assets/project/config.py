import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DRAFTS_DIR = DATA_DIR / "drafts"
IMAGES_DIR = DATA_DIR / "images"
VIDEOS_DIR = DATA_DIR / "videos"
REPORTS_DIR = DATA_DIR / "reports"
OUTPUT_DIR = ROOT_DIR / "output"
READY_DIR = OUTPUT_DIR / "ready_to_publish"

TRENDING_FILE = DATA_DIR / "trending.jsonl"
IDEAS_FILE = DATA_DIR / "ideas.jsonl"
PUBLISHED_FILE = DATA_DIR / "published.jsonl"
USED_TOPICS_FILE = DATA_DIR / "used_topics.json"

for d in (DATA_DIR, DRAFTS_DIR, IMAGES_DIR, VIDEOS_DIR, REPORTS_DIR, OUTPUT_DIR, READY_DIR):
    d.mkdir(parents=True, exist_ok=True)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "openai").lower()
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY", "")

DEFAULT_RSS_FEEDS = [
    "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "https://hnrss.org/frontpage",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
]
RSS_FEEDS = [f.strip() for f in os.getenv("RSS_FEEDS", "").split(",") if f.strip()] or DEFAULT_RSS_FEEDS

TTS_PROVIDER = os.getenv("TTS_PROVIDER", "edge").lower()
TTS_VOICE = os.getenv("TTS_VOICE", "vi-VN-HoaiMyNeural")

BROWSER_PROFILE_DIR = ROOT_DIR / os.getenv("BROWSER_PROFILE_DIR", "./data/browser-profile")
PUBLISH_WINDOW_START = os.getenv("PUBLISH_WINDOW_START", "19:00")
PUBLISH_WINDOW_END = os.getenv("PUBLISH_WINDOW_END", "21:00")

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
OPENAI_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
