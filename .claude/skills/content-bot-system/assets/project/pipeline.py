"""Orchestrator CLI for the 6-bot content pipeline.

Usage:
  python pipeline.py --all                 # run bots 1-6 in order, once
  python pipeline.py --only 2,3            # run only Bot 2 then Bot 3
  python pipeline.py --only 6 --platform my_blog

Each bot is independent and file-based (reads/writes data/*.jsonl and
data/drafts/*.md), so running a subset or on a schedule via cron is safe —
a bot with nothing new to do just logs that and exits.
"""
import argparse
import logging

from bots import (
    bot1_scraper,
    bot2_ideator,
    bot3_writer,
    bot4_image_gen,
    bot5_video_render,
    bot6_auto_poster,
)

log = logging.getLogger("pipeline")

BOTS = {
    1: ("Web Scraper", bot1_scraper.run),
    2: ("Ideator", bot2_ideator.run),
    3: ("Writer", bot3_writer.run),
    4: ("Image Gen", bot4_image_gen.run),
    5: ("Video Render", bot5_video_render.run),
}


def run_bots(bot_ids: list[int], platform: str) -> None:
    for bot_id in bot_ids:
        if bot_id == 6:
            log.info("--- Bot 6: Auto-poster ---")
            bot6_auto_poster.run(platform)
            continue
        name, fn = BOTS[bot_id]
        log.info("--- Bot %d: %s ---", bot_id, name)
        fn()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run bots 1-6 in order")
    group.add_argument("--only", help="Comma-separated bot numbers, e.g. 1,2,3")
    parser.add_argument("--platform", default="my_blog", help="Platform key for Bot 6 (platforms.yaml)")
    args = parser.parse_args()

    bot_ids = list(range(1, 7)) if args.all else [int(x) for x in args.only.split(",")]
    run_bots(bot_ids, args.platform)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main()
