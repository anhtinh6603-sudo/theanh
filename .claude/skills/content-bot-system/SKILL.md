---
name: content-bot-system
description: Installs and runs a self-contained 6-bot content automation pipeline (web scraper, ideator, writer, image generator, video renderer, auto-poster, chained in that order) built for affiliate/content marketing. Use this skill whenever the user asks to set up, install, reinstall, or run "the content bot system", "the 6 bot pipeline", "hệ thống 6 bot", or an affiliate/content automation pipeline on a new machine — including phrases like "cài lại hệ thống bot", "lấy skill content bot ra dùng", or "set up my content pipeline on this server". Do NOT rebuild the bots from scratch by writing new code — this skill bundles the already-built, already-tested Python project; just install and configure it.
---

# Content Bot System (6-bot pipeline)

This skill bundles a complete, working Python project — not just instructions. The
code already exists in `assets/project/` and has been tested end-to-end (real
ffmpeg rendering, real Anthropic API calls). Your job when this skill triggers is
to **install and configure** it, not to regenerate the bots from a prompt.

## What it does

Six independent bots, chained by files (`data/*.jsonl` + markdown drafts), so any
subset can run standalone or on a cron schedule:

1. **Web Scraper** — pulls trending items from RSS feeds + Hacker News + Reddit's
   public JSON (not Facebook/TikTok directly — those block automated access at
   the ToS/network level).
2. **Ideator** — LLM (Claude or OpenAI) picks distinct, non-repeating content
   angles from the trending items.
3. **Writer** — drafts a full blog post or social caption per angle, saved as
   Markdown with YAML frontmatter.
4. **Image Gen** — generates one image per draft via OpenAI images or Leonardo AI
   (not Midjourney — no official API).
5. **Video Render** — turns the draft into a scene script, generates TTS
   narration (free `edge-tts` by default), and renders a vertical 1080x1920
   Shorts video with ffmpeg (Ken Burns pan/zoom + burned-in captions).
6. **Auto-poster** — publishes the finished post during a configured "golden
   hour" window, driving a Playwright browser that reuses a session you log
   into by hand once (no password handling, no bypassing login).

Full details on each bot, plus known limitations, are in
`assets/project/README.md` — read it once installed if you need specifics.

## Install steps

1. **Copy the bundled project to the target location** (ask the user where, or
   default to the current working directory):
   ```bash
   cp -r <skill-dir>/assets/project ./content-bot-system
   cd content-bot-system
   ```

2. **Create a virtualenv and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   `feedparser` pulls in `sgmllib3k`, which sometimes fails to build wheels on
   very new Python/setuptools combos — if `pip install` errors there, retry
   inside the venv (already-isolated environments resolve this most of the
   time) rather than fighting the system Python.

3. **Configure API keys:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set **at least one** of `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`
   (needed for bots 2, 3, and the image-prompt step of bot 4). Get keys at
   https://console.anthropic.com/settings/keys or
   https://platform.openai.com/api-keys — these need billing/credits set up on
   the provider's side, which is on the user, not something this skill can do.

   For Bot 4 (images), set `IMAGE_PROVIDER=openai` (uses the same OpenAI key) or
   `IMAGE_PROVIDER=leonardo` (needs `LEONARDO_API_KEY`), or leave `none` to skip
   image generation.

4. **Bot 5 (video) needs a real ffmpeg**, not ffmpeg.wasm — install one with
   libx264 + libfreetype + libfontconfig (the default for `apt install ffmpeg`
   or `brew install ffmpeg`). Verify with:
   ```bash
   ffmpeg -filters 2>/dev/null | grep -E "zoompan|drawtext"
   ```
   Both should be listed. If not, the system ffmpeg build is missing filters
   this bot depends on.

5. **Bot 6 (auto-poster) is optional and needs manual setup per platform** —
   don't attempt to run it automatically:
   ```bash
   cp platforms.example.yaml platforms.yaml
   ```
   Have the user open devtools on their actual "compose post" page and fill in
   the real CSS selectors themselves (they differ per platform/account/locale
   and go stale — don't guess or hardcode them). Then run
   `python bots/bot6_auto_poster.py --setup --platform <name>` so they can log
   in by hand once in a headed browser; the session persists to
   `BROWSER_PROFILE_DIR` for later automated runs. This step requires an
   interactive display — skip it entirely in headless/remote sandboxes and
   tell the user it needs to happen on a machine where they can see a browser
   window.

## Running it

```bash
python pipeline.py --all           # run bots 1-6 once, in order
python pipeline.py --only 2,3      # run just Bot 2 then Bot 3
python pipeline.py --only 6 --platform my_blog
```

Each bot logs what it did (or why it skipped) rather than failing silently —
"no new ideas to draft" or "outside golden-hour window" are normal, expected
log lines, not bugs.

For recurring use, `scripts/crontab.example` has ready-to-adapt cron lines:
bots 1-5 every few hours, bot 6 checked every 15 minutes (it no-ops outside its
configured posting window on its own).

## Content honesty guardrails — do not remove

`bots/bot2_ideator.py` and `bots/bot3_writer.py` contain explicit instructions
telling the LLM not to fabricate statistics, invent fake case studies/testimonials,
or promise specific income figures ("kiếm $3000/tháng"). This was added after
real testing showed the model would otherwise invent a fake named person with a
specific fabricated income story, and unverified numbers (e.g. a made-up
commission percentage) when describing a real affiliate product. If asked to
adapt these prompts for a different product/niche, keep these guardrails intact
— strip only the product-specific parts, not the anti-fabrication rules.

## Known environment limits (not bugs)

- Bot 1's sources (RSS/HN/Reddit) and Bot 4/5's providers (OpenAI, Microsoft's
  edge-tts) all need real outbound internet access. Restricted sandboxes that
  only allowlist `api.anthropic.com` will make bots 1, 4 (OpenAI path), and 5
  (edge-tts) fail or no-op — this is a network policy issue, not a code bug.
  Bots 2/3 (Anthropic) still work in that case.
- Bot 3 calls the LLM with `max_tokens=8000` — long/detailed articles can still
  hit this ceiling and produce truncated JSON. If that happens, either raise
  the limit further or ask for shorter `body_markdown` in the prompt.
- Bot 6 cannot run unattended in a headless/remote environment — the one-time
  `--setup` login needs an actual display.
