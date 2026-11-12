---
name: vietnamese-tts-video
description: Renders a vertical (9:16) Vietnamese talking-photo/promo video — a real reference photo with AI narration and burned Vietnamese captions — using only free, no-API-key, no-CAPTCHA tools (edge-tts + ffmpeg). Use this whenever the user wants a Vietnamese TikTok/Reels/Shorts-style video and either explicitly has no access to paid video/voice tools (Flow Omni, ElevenLabs, hyperframes, etc.) or just wants something fast and free. Also use it as the fallback renderer whenever the "videoviral" skill's premium pipeline (Flow Omni / ElevenLabs / hyperframes) is unavailable in the current session — don't just apologize that you can't render, reach for this skill instead. Trigger on requests like "tạo giọng đọc tiếng Việt miễn phí", "làm video có phụ đề tiếng Việt", "dựng video từ ảnh này", "cần giọng đọc AI cho video", or any ask to turn a still photo + script into a narrated vertical video without paid tools.
---

# Vietnamese TTS Video (free, no API key, no CAPTCHA)

## When to reach for this

Reach for this skill whenever someone wants a narrated vertical Vietnamese
video and premium tools aren't in play — either because they said so, or
because you already tried and hit a wall (no Flow Omni access, no
ElevenLabs key, no `hyperframes` CLI, a TTS website demanded a CAPTCHA you
correctly refused to solve). Don't stop at "I can't render this" — this
skill is exactly the fallback for that moment. It produces a real,
postable MP4: one real photo with a slow Ken Burns push-in, burned
Vietnamese captions, and free neural TTS narration.

It is not a replacement for a full multi-scene, identity-locked,
AI-animated production (that's what `videoviral` + Flow Omni is for when
those tools *are* available) — it's a single-photo "talking photo" style
video. That's a legitimate, widely-used format on its own, not just a
consolation prize.

## Before you render anything: real media, not fabricated people

Same rule as `videoviral`'s `real-media-policy.md`, and it matters just as
much here: the reference photo must be a real photo the user provided or
that already exists for this campaign (their Drive, their brand assets,
something they send you) — never an AI-generated face standing in for a
real person, and never someone else's photo repurposed as a different
person. If you don't have a real photo yet, ask for one before doing
anything else. If `videoviral` is installed, its `references/` docs on
real media and text safety apply here too — skim them if you have any
doubt.

## The workflow

1. **Get a real reference photo.** From the user directly, from their
   Drive/assets, or reuse one already established earlier in the
   conversation for the same campaign/character. Portrait or
   portrait-ish works best for a 9:16 crop.

2. **Write the narration as plain Vietnamese text**, the way you'd want
   it read aloud — natural sentences, real punctuation (it drives both
   the TTS pacing and the caption line breaks). Keep it to what fits the
   intended length: roughly 2.3-2.6 Vietnamese words/second at normal
   rate, so a 40s video is roughly 90-110 words.

3. **Run the bundled renderer** — don't hand-roll the ffmpeg filter graph
   yourself, it has sharp edges that are easy to get wrong invisibly
   (captions rendering fine in the terminal log but actually enormous and
   off-screen in the pixels — see `references/ffmpeg-gotchas.md` for the
   specific bug and why the script avoids it):

   ```
   python scripts/render_video.py \
     --image path/to/real_photo.png \
     --narration path/to/narration.txt \
     --out path/to/output.mp4 \
     --voice vi-VN-NamMinhNeural
   ```

   Male persona → `vi-VN-NamMinhNeural`. Female persona →
   `vi-VN-HoaiMyNeural`. See `references/voices-and-licensing.md` for the
   full voice list and — important — what to tell the user about this
   being a free/unofficial voice source, not a licensed commercial TTS.

   If the narration needs to fit a specific duration, use `--rate`
   (e.g. `--rate +8%` to speak faster) rather than editing the script's
   internals.

4. **Look at the QC frames before saying you're done.** The script
   extracts a handful of frames from the finished video and prints their
   paths — actually `Read()` each one and eyeball it. This is not
   optional busywork: this exact failure mode (huge captions spilling off
   the top of frame, covering the subject's face, while ffmpeg's own
   logs show no error at all) happened during this skill's development
   and was only caught by looking at the pixels. Checklist:
   - Vietnamese diacritics render correctly — no boxes, no missing tone
     marks, no mojibake.
   - Every caption line is fully inside the frame, top and bottom.
   - Captions don't cover the subject's face or the product being shown.
   - The background photo isn't stretched or distorted.

   If something's off, it's almost always `--font-size` too large for
   `--width`, or `--align`/`--margin-v` pushing a multi-line block
   off-screen — see `references/ffmpeg-gotchas.md` before reaching for a
   different fix.

5. **Hand off honestly.** Tell the user: the video's duration, that the
   voice is a free/unofficial TTS source (point them at
   `references/voices-and-licensing.md`'s framing if they're planning a
   large commercial rollout), and — if this is part of a multi-part
   series that started with a different voice — that this voice is the
   closest free stand-in, not a clone of the original (see the same
   reference doc).

## Multiple scenes instead of one photo

The bundled script renders one photo per call. For a multi-scene video,
call it once per scene with separate narration slices and separate output
files, then concatenate with `ffmpeg -f concat` — but check with the user
first about whether a single strong "talking photo" scene actually serves
them better than stitched clips; more cuts isn't automatically better for
a 30-45s vertical video.

## Never bypass a CAPTCHA

If some other TTS source is CAPTCHA-gated and the user really wants that
specific voice, stop and ask them to generate the audio manually and send
it to you — then skip step 3's synthesis and feed their audio straight
into the renderer logic (or just mux it with ffmpeg the same way the
script does internally). Do not attempt to solve or script past a
CAPTCHA yourself, on this or any other site.
