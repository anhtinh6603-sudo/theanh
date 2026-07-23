"""Provider-agnostic text generation: uses Claude if ANTHROPIC_API_KEY is set,
otherwise falls back to OpenAI. Bots call `generate_text` / `generate_json` and
don't need to know which provider is behind it.
"""
import json
import re

import config

_anthropic_client = None
_openai_client = None


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic

        _anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _anthropic_client


def _get_openai():
    global _openai_client
    if _openai_client is None:
        import openai

        _openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    return _openai_client


def active_provider() -> str:
    if config.ANTHROPIC_API_KEY:
        return "anthropic"
    if config.OPENAI_API_KEY:
        return "openai"
    raise RuntimeError(
        "No LLM API key configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env"
    )


def generate_text(system: str, user: str, max_tokens: int = 2000) -> str:
    provider = active_provider()
    if provider == "anthropic":
        client = _get_anthropic()
        resp = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in resp.content if block.type == "text")
    else:
        client = _get_openai()
        resp = client.chat.completions.create(
            model=config.OPENAI_TEXT_MODEL,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content


def generate_json(system: str, user: str, max_tokens: int = 2000):
    """Same as generate_text but strips markdown fences and parses JSON.
    Raises ValueError with the raw text included if parsing fails, so callers
    can log/inspect what the model actually returned.
    """
    raw = generate_text(system, user, max_tokens=max_tokens)
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {exc}\n--- raw ---\n{raw}") from exc
