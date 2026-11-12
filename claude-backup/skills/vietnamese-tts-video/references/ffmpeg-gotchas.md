# ffmpeg gotchas this skill exists to avoid

These were discovered the hard way — by burning captions, looking at the
actual output frames, and finding giant text spilling off the top of the
screen and covering the subject's face. `scripts/render_video.py` already
does the right thing; this file explains *why*, so if you ever have to
touch the filter graph by hand you don't reintroduce the bug.

## 1. `subtitles=file.srt:original_size=WxH` does not reliably scale text

The intuitive fix for "captions are the wrong size" is to tell the
`subtitles` filter what resolution the subtitle file was authored for,
via `original_size=1080x1920`. In testing this did **not** produce
correctly-sized text when burning a plain `.srt` (no embedded resolution)
onto a 1080×1920 video — captions still rendered enormous, wrapped to one
word per line, and ran off the top of the frame.

**Fix that actually works:** convert the `.srt` to `.ass` first
(`ffmpeg -i file.srt file.ass`), then directly edit the `[Script Info]`
block:

```
PlayResX: 1080
PlayResY: 1920
```

and the `Style: Default,...` line in `[V4+ Styles]` to set the real
`Fontname`, `Fontsize`, colours, `Alignment`, and margins. Then burn the
**patched .ass file** with a plain `subtitles=file.ass` — no
`force_style`, no `original_size` needed, because the style is now
correct at the source.

Why: ffmpeg's default SRT→ASS conversion stamps `PlayResX: 384` /
`PlayResY: 288` (an old SSA-era default) with `Fontsize: 16`. `force_style`
only overrides individual style fields on top of that base — it doesn't
reliably fix the PlayRes mismatch that's actually causing the scale-up
libass applies when it renders onto a much larger real frame. Editing
PlayRes and Fontsize together, so they're mutually consistent for the
*actual output size*, is what fixes it.

## 2. Alignment: prefer bottom (`Alignment: 2`), not top

Vietnamese sentences are long, so a caption block is often 3+ lines.
Top alignment (`Alignment: 8`) grows a tall multi-line block *downward*
from a fixed top anchor and doesn't clip — but for `subtitles` with a
capped rendering area, and combined with the PlayRes mismatch above, tall
top-anchored blocks are the ones observed running off-frame and covering
the face. Bottom alignment (`Alignment: 2`) grows *upward* from the
bottom margin, staying clear of the subject's face which is usually in
the upper half of a portrait photo. Use bottom unless the specific photo
composition has empty space up top and a face/hands lower down.

## 3. Zoompan frame count must match the audio exactly

`zoompan` needs an explicit `d=<frame count>` to know how many output
frames to generate from the single looped input image. If you don't tie
`d` to `round(duration_seconds * fps)` (duration = the **narration
audio's** duration, from `ffprobe`), the rendered video's length drifts
from the audio — in testing this produced a video 3+ seconds longer than
the audio, i.e. several seconds of silent tail at the end. Always:

1. Measure real audio duration with ffprobe *after* TTS synthesis (don't
   estimate from character count).
2. Compute `frame_count = round(duration * fps)`.
3. Pass `d=<frame_count>` to zoompan and also pass `-t <duration>` on the
   final ffmpeg output as a belt-and-suspenders trim.

## 4. Give zoompan resolution headroom before it zooms

`zoompan` zooming into a source image at its final output resolution
causes visible upscaling artifacts as it pushes in. Scale the cropped
image up (e.g. 2x the target — `2160x3840` for a `1080x1920` target)
*before* the `zoompan` filter, then let `zoompan`'s own `s=1080x1920`
downscale it back on output. This gives it pixels to zoom into instead of
stretching what's already there.

## 5. Escaping the `.ass` path inside `-filter_complex`

Filter option values use `:` as a separator, so a Windows path's drive
letter (`C:`) breaks parsing. Either `cd` into the file's directory and
pass a bare filename (simplest — what the bundled script does by running
ffmpeg with `cwd` set to the ass file's directory), or escape colons and
backslashes explicitly (`C\:/Windows/Fonts`, forward slashes). Prefer the
`cwd` trick; it's much less error-prone than hand-escaping.

## 6. edge-tts occasionally fails one call for no real reason

`edge_tts.exceptions.NoAudioReceived` sometimes fires on the very first
call to Microsoft's free endpoint and then succeeds immediately on retry
with the identical arguments. It is not voice-specific and not a real
parameter problem — just retry 2-3 times with a short pause before
concluding the voice or network is actually down.
