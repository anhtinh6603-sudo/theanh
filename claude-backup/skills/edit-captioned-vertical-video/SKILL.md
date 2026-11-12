---
name: "edit-captioned-vertical-video"
description: Edit existing footage into polished captioned vertical videos with fixed or adapted on-screen text, music, darkening or blur, slow motion, contextual logos, preview frames, and technical validation. Use when Codex should create, revise, or batch-render a 9:16 Reel, TikTok, or Short from user-supplied video, audio, text, and branding, including requests to slow footage, show all text at once, highlight keywords, reposition a logo, improve readability, replace music, or export an MP4. Do not use this skill to analyze social channels, write publishing strategy, or post content.
---

# Edit Captioned Vertical Video

Edit local media only. Receive an approved content specification and return a visually checked MP4 plus previews. Do not analyze channels or publish posts.

## Inputs

Accept either an existing workspace compatible with `render_reel.py` or create the minimum folders required by its schema:

- `01_VIDEO_GOC`: source footage
- `02_NHAC_NEN`: licensed music supplied by the user
- `03_LOGO`: optional transparent logos
- `04_NOI_DUNG`: content JSON
- `05_VIDEO_DA_XU_LY`: rendered MP4 and subtitle files
- `06_ANH_XEM_TRUOC`: preview frames
- `07_NHAT_KY`: media ledger
- `BRAND_CONFIG.json`: render defaults

Copy `assets/default-config.json` into the workspace when no config exists. Never modify source media.

## Edit workflow

1. Read the user's latest visual directions and the content JSON.
2. Determine whether text is `verbatim` or `adapted`. In verbatim mode, preserve every word and punctuation mark; change line breaks only.
3. Inspect source duration, orientation, subject location, movement, and safe text areas.
4. Select a fitting font installed on the machine. Preserve Vietnamese diacritics.
5. Set title/body hierarchy, line wrapping, safe margins, and keyword highlights.
6. Add a topical logo only when supplied or explicitly requested. Keep its aspect ratio and place it in a stable empty area.
7. Render with `python scripts/render_reel.py --workspace <folder> --content <content.json>`.
8. Validate with `python scripts/validate_output.py --video <output.mp4> --duration <seconds>`.
9. Inspect previews at 25%, 50%, and 75% using [references/VISUAL_QA.md](references/VISUAL_QA.md).
10. Correct overflow, weak contrast, awkward spacing, subject overlap, logo placement, or audio balance and rerender automatically.
11. Present the final video and preview. Keep publishing outside this skill.

## Default style

- Output 1080x1920 H.264/AAC MP4 at 30 fps with fast-start.
- Default to 20 seconds and 0.5x playback when a 10-second source should fill the full output.
- Crop to 9:16 while covering the canvas; do not stretch the source.
- Apply a mild blur and dark overlay while keeping the scene recognizable.
- Show the complete approved text as one fixed composition when requested.
- Use natural upper/lowercase, white primary text, and matte yellow-lime highlights without outline or glow.
- Make the title larger than supporting text and distribute sections evenly.
- Fade music during the last second. Do not include source audio unless requested.

## Revision behavior

- Treat an approved prior video as the visual standard when the user says to follow video 1 or another reference.
- Change only the requested element when revising: typography, spacing, logo, music, darkness, speed, crop, or content.
- Reinspect previews after every spatial change.
- If a centered logo covers the subject, keep it aligned with the content axis but move it to a stable empty zone or omit it.
- Never silently shorten approved text to solve layout problems.

## Quality gate

Require all technical validation checks to pass. Visually verify:

- text accuracy and readability at phone size
- balanced vertical spacing
- no text or logo over faces, eyes, hands, or key objects
- no clipping, black frames, frozen endings, or unintended source audio
- correct logo, music, duration, aspect ratio, and output file

If FFmpeg or FFprobe is unavailable, report the missing dependency and exact correction required. Keep all intermediate files recoverable.
