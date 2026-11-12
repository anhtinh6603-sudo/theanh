# Setup

## Purpose

This skill generates speech audio with Google Cloud Text-to-Speech using a service account.

## Required Google service-account fields

Export these two values from the downloaded service-account JSON:

- `client_email` -> `GOOGLE_TTS_CLIENT_EMAIL`
- `private_key` -> `GOOGLE_TTS_PRIVATE_KEY`

Example:

```bash
export GOOGLE_TTS_CLIENT_EMAIL='service-account@project-id.iam.gserviceaccount.com'
export GOOGLE_TTS_PRIVATE_KEY='-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n'
```

## Important formatting rule

If the private key is copied into a shell or config as escaped `\n`, the script normalizes it automatically.

## Test flow

1. Export the two variables.
2. Run the script:

```bash
node skills/google-tts-reply/scripts/google-tts.js --text "Xin chào" --out /tmp/test-google-tts.mp3
```

3. If the output file exists and has audio, the Google TTS side is working.

## OAuth flow used

The script:
1. builds a signed JWT using RS256
2. exchanges it at `https://oauth2.googleapis.com/token`
3. calls `https://texttospeech.googleapis.com/v1/text:synthesize`
4. writes the returned base64 audio to disk
