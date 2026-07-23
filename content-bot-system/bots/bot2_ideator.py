"""Bot 2 - Ideator

Reads unprocessed trending items from Bot 1, asks the LLM to pick distinct,
"easy to go viral" angles out of the raw noise, and writes them to
data/ideas.jsonl for Bot 3 to draft. Keeps a rolling list of recently-used
angles (data/used_topics.json) and feeds it back into the prompt so the same
topic doesn't get rewritten every run.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import hashlib
import logging

import config
import llm
from utils import append_jsonl, now_iso, read_json, read_jsonl, rewrite_jsonl, write_json

log = logging.getLogger("bot2_ideator")

BATCH_SIZE = 15
IDEAS_PER_RUN = 5
USED_TOPICS_KEEP = 50

SYSTEM_PROMPT = """Bạn là một content strategist chuyên tìm góc độ (angle) độc lạ, dễ viral \
từ tin tức/chủ đề đang trending. Với danh sách tin thô được cung cấp, hãy chọn ra những góc \
độ khác biệt nhau, tránh trùng lặp với các chủ đề đã dùng gần đây.

QUY TẮC: KHÔNG đề xuất góc độ chứa cam kết/số tiền thu nhập cụ thể (vd "kiếm $3000/tháng",
"thu nhập X triệu") vì đây là điều không thể đảm bảo và dễ gây hiểu lầm. Góc độ nên tập trung
vào giá trị thật (giải thích, hướng dẫn, so sánh...), không phải lời hứa hẹn kiếm tiền.

Trả lời CHỈ bằng JSON hợp lệ, không thêm giải thích, đúng theo schema:
[
  {
    "angle": "góc độ/tiêu đề đề xuất, ngắn gọn, gây tò mò",
    "hook": "câu mở đầu (hook) để thu hút người đọc/xem trong 3 giây đầu",
    "format": "blog" hoặc "social",
    "why_viral": "1 câu giải thích tại sao góc này dễ viral",
    "source_title": "tiêu đề tin gốc được dùng làm cảm hứng",
    "source_url": "url tin gốc"
  }
]"""


def _idea_id(angle: str) -> str:
    return hashlib.sha1(angle.encode("utf-8")).hexdigest()[:16]


def run() -> int:
    trending = read_jsonl(config.TRENDING_FILE)
    pending = [item for item in trending if item.get("status") == "new"][:BATCH_SIZE]

    if not pending:
        log.info("Bot2 ideator: no new trending items to process")
        return 0

    used_topics = read_json(config.USED_TOPICS_FILE, default=[])
    recent_angles = [t["angle"] for t in used_topics[-USED_TOPICS_KEEP:]]

    raw_list = "\n".join(
        f"- [{item['source']}] {item['title']} — {item['summary']} ({item['url']})"
        for item in pending
    )
    avoid_list = "\n".join(f"- {a}" for a in recent_angles) or "(chưa có)"

    user_prompt = (
        f"Danh sách tin trending:\n{raw_list}\n\n"
        f"Các góc độ đã dùng gần đây, TRÁNH lặp lại ý tưởng tương tự:\n{avoid_list}\n\n"
        f"Hãy chọn ra tối đa {IDEAS_PER_RUN} góc độ tốt nhất, khác biệt nhau."
    )

    ideas = llm.generate_json(SYSTEM_PROMPT, user_prompt, max_tokens=2000)
    if not isinstance(ideas, list):
        raise ValueError(f"Expected a JSON array of ideas, got: {type(ideas)}")

    added = 0
    for idea in ideas[:IDEAS_PER_RUN]:
        angle = idea.get("angle", "").strip()
        if not angle:
            continue
        record = {
            "id": _idea_id(angle),
            "angle": angle,
            "hook": idea.get("hook", ""),
            "format": idea.get("format", "blog"),
            "why_viral": idea.get("why_viral", ""),
            "source_title": idea.get("source_title", ""),
            "source_url": idea.get("source_url", ""),
            "created_at": now_iso(),
            "status": "new",
        }
        append_jsonl(config.IDEAS_FILE, record)
        used_topics.append({"angle": angle, "created_at": record["created_at"]})
        added += 1

    write_json(config.USED_TOPICS_FILE, used_topics[-USED_TOPICS_KEEP:])

    # Mark the trending items we just consumed so future runs don't reuse them.
    pending_ids = {item["id"] for item in pending}
    for item in trending:
        if item["id"] in pending_ids:
            item["status"] = "processed"
    rewrite_jsonl(config.TRENDING_FILE, trending)

    log.info("Bot2 ideator: generated %d new ideas from %d trending items", added, len(pending))
    return added


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    run()
