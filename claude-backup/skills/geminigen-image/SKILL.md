---
name: geminigen-image
description: Generate images directly via GeminiGen.ai API and save local files for downstream posting/creative workflows. Use when the user asks to create AI images, render variants from prompts, poll generation status, or produce downloadable image assets without using the full facebook-page-publisher flow.
---

# GeminiGen Image

Use this skill to generate image assets from GeminiGen.ai as a standalone workflow.

## Workflow

1. Ensure API key exists in `~/.meta-ads/.env` under `GEMINIGEN_API_KEY`.
2. Run `scripts/geminigen_image.py` with prompt and rendering parameters.
3. For async generation, use `--wait` to poll history until complete.
4. Use the returned local file path in later flows (Telegram send, Facebook post, slides, etc).

## Command

```bash
python3 skills/geminigen-image/scripts/geminigen_image.py \
  --prompt "<image prompt>" \
  --model nano-banana-pro \
  --aspect-ratio 16:9 \
  --style Photorealistic \
  --output-format jpeg \
  --resolution 2K \
  --wait
```

## Options

- `--prompt` (required): image prompt text.
- `--model`: default `nano-banana-pro`.
- `--aspect-ratio`: default `16:9`.
- `--style`: default `Photorealistic`.
- `--file-urls`: optional source images for image-to-image tasks.
- `--output-format`: `jpeg|jpg|png|webp` (API-dependent).
- `--resolution`: default `2K`.
- `--wait`: poll until completed.
- `--poll-interval`: seconds between polls (default 5).
- `--max-wait`: max polling seconds (default 180).

## Output

- Without `--wait`: prints raw API response JSON.
- With `--wait`: downloads image to `.openclaw/generated-images/` and prints:
  - `saved`: local file path
  - `history`: final GeminiGen history payload

## References

- `references/env.md`: required env vars and notes.
- `scripts/geminigen_image.py`: executable implementation.
