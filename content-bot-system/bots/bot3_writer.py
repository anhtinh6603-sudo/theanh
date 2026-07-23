"""Bot 3 - Writer

Turns each idea from Bot 2 into a full draft: an SEO-friendly blog post or a
social caption, depending on the idea's format. Writes one Markdown file per
idea (YAML frontmatter + body) into data/drafts/, ready for Bot 4 (images)
and Bot 5 (video) to build on top of.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import logging

from slugify import slugify

import config
import llm
from utils import now_iso, read_jsonl, rewrite_jsonl, write_draft

log = logging.getLogger("bot3_writer")

SYSTEM_PROMPT = """Bạn là copywriter/content writer chuyên viết bài không sáo rỗng, đi thẳng \
vào giá trị cho người đọc, chuẩn SEO khi cần. Dựa vào góc độ (angle) và hook được cung cấp, \
hãy viết nội dung hoàn chỉnh. Trả lời CHỈ bằng JSON hợp lệ, đúng schema:
{
  "title": "tiêu đề chính thức, hấp dẫn, chứa từ khoá chính",
  "meta_description": "mô tả SEO 1-2 câu, dưới 160 ký tự",
  "body_markdown": "toàn bộ nội dung bài viết dạng markdown, có heading, đoạn ngắn, dễ đọc",
  "social_caption": "caption ngắn (dưới 300 ký tự) để đăng kèm ảnh/video lên mạng xã hội",
  "hashtags": ["#hashtag1", "#hashtag2"]
}"""


def _draft_prompt(idea: dict) -> str:
    return (
        f"Góc độ: {idea['angle']}\n"
        f"Hook: {idea['hook']}\n"
        f"Định dạng mong muốn: {idea['format']}\n"
        f"Lý do dễ viral: {idea['why_viral']}\n"
        f"Tin gốc tham khảo: {idea['source_title']} ({idea['source_url']})\n"
    )


def _write_draft_file(idea: dict, draft: dict) -> Path:
    slug = slugify(draft["title"])[:80] or idea["id"]
    path = config.DRAFTS_DIR / f"{slug}.md"

    frontmatter = {
        "id": idea["id"],
        "idea_id": idea["id"],
        "title": draft["title"],
        "meta_description": draft.get("meta_description", ""),
        "social_caption": draft.get("social_caption", ""),
        "hashtags": draft.get("hashtags", []),
        "format": idea["format"],
        "created_at": now_iso(),
        "status": "drafted",
        "images": [],
        "video": None,
    }

    write_draft(path, frontmatter, draft.get("body_markdown", ""))
    return path


def run() -> int:
    ideas = read_jsonl(config.IDEAS_FILE)
    pending = [idea for idea in ideas if idea.get("status") == "new"]

    if not pending:
        log.info("Bot3 writer: no new ideas to draft")
        return 0

    written = 0
    for idea in pending:
        try:
            draft = llm.generate_json(SYSTEM_PROMPT, _draft_prompt(idea), max_tokens=3000)
            path = _write_draft_file(idea, draft)
            idea["status"] = "drafted"
            written += 1
            log.info("Drafted: %s", path.name)
        except Exception as exc:
            log.error("Failed to draft idea %s: %s", idea["id"], exc)

    rewrite_jsonl(config.IDEAS_FILE, ideas)
    log.info("Bot3 writer: drafted %d/%d ideas", written, len(pending))
    return written


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    run()
