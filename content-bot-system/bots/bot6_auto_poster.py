"""Bot 6 - Auto-poster

Publishes the next finished post (video from Bot 5, or the image from Bot 4
if no video was made) during the configured "golden hour" window, by driving
a real browser through your own already-logged-in session: upload media,
paste caption, click publish.

Important limits, on purpose:
  - This does NOT store or touch your password. It drives a Playwright
    *persistent* browser profile — you log in by hand once (`--setup`), the
    session cookies stay on disk, and every later run reuses that already
    authenticated session, same as a browser you never close.
  - Most platforms' Terms of Service prohibit automating their normal web UI,
    even against your own account. Prefer the official API for any platform
    that has one (Facebook Graph API, Instagram Graph API, TikTok Content
    Posting API, a blog's REST API, ...) — it's stable and ToS-compliant.
    Use this browser-automation path only where no API is available, and only
    against accounts you own, understanding the ToS/suspension risk.
  - Selectors for your target site are NOT included: DOM structure differs
    per platform/account/locale and changes constantly, so hardcoded guesses
    would silently break. Fill in platforms.yaml yourself (see
    platforms.example.yaml) after inspecting your own compose page.
"""
import sys
from datetime import datetime, time as dtime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import logging

import yaml

import config
from utils import append_jsonl, iter_drafts, now_iso, write_draft

log = logging.getLogger("bot6_auto_poster")

PLATFORMS_FILE = config.ROOT_DIR / "platforms.yaml"


def load_platform(name: str) -> dict:
    if not PLATFORMS_FILE.exists():
        raise FileNotFoundError(
            f"{PLATFORMS_FILE} not found. Copy platforms.example.yaml to platforms.yaml "
            "and fill in your own selectors first."
        )
    platforms = yaml.safe_load(PLATFORMS_FILE.read_text(encoding="utf-8")) or {}
    if name not in platforms:
        raise KeyError(f"Platform '{name}' not found in {PLATFORMS_FILE}")
    return platforms[name]


def _parse_hhmm(value: str) -> dtime:
    hour, minute = (int(part) for part in value.split(":"))
    return dtime(hour=hour, minute=minute)


def is_within_golden_hour(now: datetime | None = None) -> bool:
    now = now or datetime.now()
    start = _parse_hhmm(config.PUBLISH_WINDOW_START)
    end = _parse_hhmm(config.PUBLISH_WINDOW_END)
    current = now.time()
    if start <= end:
        return start <= current <= end
    return current >= start or current <= end  # window wraps past midnight


def login_setup(platform_name: str) -> None:
    """Opens a headed, persistent browser so you can log in by hand. Close
    the window (or Ctrl+C in the terminal) once you're logged in — the
    session is saved to BROWSER_PROFILE_DIR automatically.
    """
    from playwright.sync_api import sync_playwright

    platform = load_platform(platform_name)
    config.BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            str(config.BROWSER_PROFILE_DIR), headless=False
        )
        page = context.new_page()
        page.goto(platform["compose_url"])
        print(
            "\nLog in by hand in the opened browser window, navigate anywhere you like "
            "to confirm you're logged in, then press Enter here to save the session...\n"
        )
        input()
        context.close()
    log.info("Session saved to %s", config.BROWSER_PROFILE_DIR)


def publish_post(platform_name: str, media_path: Path, caption: str) -> None:
    from playwright.sync_api import sync_playwright

    platform = load_platform(platform_name)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            str(config.BROWSER_PROFILE_DIR), headless=True
        )
        page = context.new_page()
        page.goto(platform["compose_url"])
        page.set_input_files(platform["media_input_selector"], str(media_path))
        page.fill(platform["caption_selector"], caption)
        page.click(platform["publish_button_selector"])
        page.wait_for_timeout(platform.get("wait_after_publish_ms", 3000))
        context.close()


def _next_ready_draft():
    for path, frontmatter, body in iter_drafts(config.DRAFTS_DIR):
        if frontmatter.get("status") in ("video_done", "image_done"):
            yield path, frontmatter, body


def run(platform_name: str) -> int:
    if not is_within_golden_hour():
        log.info(
            "Outside golden-hour window (%s-%s), skipping this run",
            config.PUBLISH_WINDOW_START, config.PUBLISH_WINDOW_END,
        )
        return 0

    for path, frontmatter, body in _next_ready_draft():
        media_rel = frontmatter.get("video") or (frontmatter.get("images") or [None])[0]
        if not media_rel:
            log.warning("Skipping %s: no media to publish", path.name)
            continue
        media_path = config.ROOT_DIR / media_rel
        caption = frontmatter.get("social_caption", "") or frontmatter.get("title", "")
        hashtags = " ".join(frontmatter.get("hashtags", []))
        full_caption = f"{caption}\n\n{hashtags}".strip()

        try:
            publish_post(platform_name, media_path, full_caption)
            frontmatter["status"] = "published"
            write_draft(path, frontmatter, body)
            append_jsonl(
                config.PUBLISHED_FILE,
                {
                    "id": frontmatter.get("id"),
                    "title": frontmatter.get("title"),
                    "platform": platform_name,
                    "media": media_rel,
                    "published_at": now_iso(),
                },
            )
            log.info("Published: %s", path.name)
            return 1
        except Exception as exc:
            log.error("Failed to publish %s: %s", path.name, exc)
            return 0

    log.info("Bot6 auto-poster: nothing ready to publish")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", default="my_blog", help="Key from platforms.yaml")
    parser.add_argument("--setup", action="store_true", help="Open a browser to log in by hand once")
    args = parser.parse_args()

    if args.setup:
        login_setup(args.platform)
    else:
        run(args.platform)
