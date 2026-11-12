---
name: google-tts-reply
description: Generate Vietnamese speech audio from text using Google Cloud Text-to-Speech and prepare it for outbound chat delivery. Use when building or testing voice replies, Telegram audio reply workflows, Google TTS JWT/OAuth flows, service-account based speech generation, or reusable text-to-audio automation.
---

# Google TTS Reply

Create speech audio with Google Cloud TTS without hardcoding secrets into the skill.

## Default workflow

1. Read `references/setup.md` before first use.
2. Put Google service-account credentials in environment variables, not in skill files.
3. Run `scripts/google-tts.js` to generate an audio file from text.
4. If needed, send the generated file with OpenClaw messaging or another delivery step.

## Environment variables

Required:
- `GOOGLE_TTS_CLIENT_EMAIL`
- `GOOGLE_TTS_PRIVATE_KEY`

Optional:
- `GOOGLE_TTS_VOICE` (default: `vi-VN-Chirp3-HD-Aoede`)
- `GOOGLE_TTS_LANGUAGE_CODE` (default: `vi-VN`)
- `GOOGLE_TTS_AUDIO_ENCODING` (default: `MP3`)

## Commands

Generate audio:

```bash
node skills/google-tts-reply/scripts/google-tts.js \
  --text "Xin chào anh Tuấn Anh" \
  --out /tmp/google-tts-reply.mp3
```

## Notes

- Keep replies short and natural for messaging.
- Prefer MP3 first for compatibility.
- Do not commit credentials.
- If Google returns auth errors, verify private key formatting first.
