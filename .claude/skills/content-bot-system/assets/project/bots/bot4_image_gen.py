"""Bot 4 - Image Gen

For every drafted post, asks the LLM for a short English image prompt (image
models understand English prompts far better than Vietnamese), then calls
whichever image provider is configured (OpenAI images API or Leonardo AI —
Midjourney has no official API, so it isn't offered as an option here).
Saves the image next to the draft and updates its frontmatter.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import base64
import logging

import requests

import config
import llm
from utils import iter_drafts, write_draft

log = logging.getLogger("bot4_image_gen")

IMAGE_PROMPT_SYSTEM = """Bạn là chuyên gia viết prompt cho AI tạo ảnh (Midjourney/DALL-E/Leonardo). \
Dựa vào tiêu đề và nội dung bài viết, hãy viết 1 prompt tiếng Anh, mô tả cảnh cụ thể, phong cách \
ảnh (photo-realistic, editorial, flat illustration...), không chứa chữ/logo. Trả lời CHỈ prompt, \
không giải thích thêm, dưới 60 từ."""


def _image_prompt(title: str, body: str) -> str:
    excerpt = body[:800]
    return llm.generate_text(
        IMAGE_PROMPT_SYSTEM,
        f"Tiêu đề: {title}\n\nNội dung (trích):\n{excerpt}",
        max_tokens=150,
    ).strip()


def _generate_openai(prompt: str, out_path: Path) -> bool:
    from openai import OpenAI

    client = OpenAI(api_key=config.OPENAI_API_KEY)
    result = client.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1024")
    image_bytes = base64.b64decode(result.data[0].b64_json)
    out_path.write_bytes(image_bytes)
    return True


def _generate_leonardo(prompt: str, out_path: Path, timeout: int = 90) -> bool:
    headers = {"Authorization": f"Bearer {config.LEONARDO_API_KEY}", "Content-Type": "application/json"}
    create = requests.post(
        "https://cloud.leonardo.ai/api/rest/v1/generations",
        headers=headers,
        json={"prompt": prompt, "num_images": 1, "width": 1024, "height": 1024},
        timeout=30,
    )
    create.raise_for_status()
    generation_id = create.json()["sdGenerationJob"]["generationId"]

    deadline = time.time() + timeout
    while time.time() < deadline:
        status = requests.get(
            f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
            headers=headers,
            timeout=30,
        ).json()["generations_by_pk"]
        if status["status"] == "COMPLETE":
            image_url = status["generated_images"][0]["url"]
            out_path.write_bytes(requests.get(image_url, timeout=30).content)
            return True
        if status["status"] == "FAILED":
            return False
        time.sleep(3)
    log.warning("Leonardo generation %s timed out", generation_id)
    return False


def generate_image(prompt: str, out_path: Path) -> bool:
    if config.IMAGE_PROVIDER == "openai":
        return _generate_openai(prompt, out_path)
    if config.IMAGE_PROVIDER == "leonardo":
        return _generate_leonardo(prompt, out_path)
    log.info("IMAGE_PROVIDER=none (or unrecognized) — skipping image generation")
    return False


def run() -> int:
    processed = 0
    for path, frontmatter, body in iter_drafts(config.DRAFTS_DIR):
        if frontmatter.get("status") != "drafted":
            continue
        try:
            prompt = _image_prompt(frontmatter["title"], body)
            image_path = config.IMAGES_DIR / f"{path.stem}.png"
            ok = generate_image(prompt, image_path)
            if ok:
                frontmatter["images"] = [str(image_path.relative_to(config.ROOT_DIR))]
                frontmatter["image_prompt"] = prompt
                frontmatter["status"] = "image_done"
                write_draft(path, frontmatter, body)
                processed += 1
                log.info("Generated image for: %s", path.name)
            else:
                log.warning("No image produced for %s (provider=%s)", path.name, config.IMAGE_PROVIDER)
        except Exception as exc:
            log.error("Image generation failed for %s: %s", path.name, exc)

    log.info("Bot4 image gen: processed %d drafts", processed)
    return processed


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    run()
