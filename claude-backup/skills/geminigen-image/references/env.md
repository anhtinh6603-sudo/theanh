# GeminiGen Environment

This skill reads API credentials from:

- `~/.meta-ads/.env`

Required key:

- `GEMINIGEN_API_KEY=<your_api_key>`

Notes:

- Output images are saved to:
  - `/home/openclaw/.openclaw/workspace/.openclaw/generated-images`
- Keep API keys local; do not commit to git or memory logs.
- If the API returns async UUID only, run with `--wait` so script polls history and downloads final asset automatically.
