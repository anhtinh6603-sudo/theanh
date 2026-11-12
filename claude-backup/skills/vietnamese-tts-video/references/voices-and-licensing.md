# Voice options and what to tell the user about them

## Available free Vietnamese voices (via `edge-tts`)

Run `python -m edge_tts --list-voices` and filter for `vi-VN` to get the
current list; as of this writing there are two:

| Voice | Gender | Character |
|---|---|---|
| `vi-VN-NamMinhNeural` | Male | Friendly, positive |
| `vi-VN-HoaiMyNeural` | Female | Friendly, positive |

Pick the one matching the on-screen persona's gender unless the user says
otherwise.

## What `edge-tts` actually is — say this to the user

`edge-tts` is an open-source client that talks to the same free neural
TTS backend Microsoft Edge's built-in "Read aloud" feature uses. It:

- needs no API key and no signup,
- doesn't require solving a CAPTCHA (unlike some free TTS web pages),
- is **not** an official, licensed commercial TTS API — it's a reverse
  engineered client hitting a free consumer-facing endpoint. Microsoft
  could change or restrict it at any time, and its terms are not written
  with bulk commercial content production in mind the way a paid API
  (ElevenLabs, Azure Cognitive Services with a real subscription, Google
  Cloud TTS, etc.) is.

**Always tell the user explicitly, the first time you use this skill for
them, something like:** "Giọng đọc này dùng dịch vụ miễn phí không chính
thức (edge-tts / Microsoft Edge Read Aloud), phù hợp để làm bản nháp hoặc
thử nghiệm nhanh. Nếu bạn định phát hành hàng loạt / thương mại quy mô
lớn, nên cân nhắc nâng cấp sang một TTS có license thương mại rõ ràng
(ElevenLabs, Azure/Google Cloud TTS trả phí, v.v.) để chắc chắn về mặt
pháp lý và để giọng ổn định lâu dài."

This isn't a hard blocker — plenty of real creators use it for real
content — it's a disclosure so the user can make an informed call for
their own use case (a personal test video vs. a paid ad campaign are
different risk profiles).

## Never bypass a CAPTCHA to get a voice

If a TTS source (a web page, a different tool) requires solving a CAPTCHA,
stop and ask the user to complete that step themselves and hand you the
resulting audio file. Do not attempt to solve or automate past it. This
skill's whole reason for existing is to route around that limitation with
a source that doesn't require it (`edge-tts`) — if the user specifically
needs a *different* voice that's gated behind a CAPTCHA, that's a manual
step for them, not something to automate.

## Reusing a voice across a multi-part series

If earlier parts of a series (e.g. day 1 of a 7-day campaign) used some
other voice — a real recording, a paid TTS the user generated elsewhere —
you generally **cannot** make `edge-tts` reproduce that exact voice; it
has a fixed small set of neural voices, not voice cloning. Be upfront
about this: offer the closest matching free voice (same gender, similar
tone) as a *consistent stand-in* for the rest of the series, and note
that if voice continuity really matters for the final release, the user
should regenerate all parts through whichever paid/cloned voice tool
produced the original.
