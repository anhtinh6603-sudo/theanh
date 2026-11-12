import argparse
import asyncio
import json
from pathlib import Path

import edge_tts


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Edge TTS audio and exact word-boundary timing."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--text-file")
    parser.add_argument("--voice", default="vi-VN-NamMinhNeural")
    parser.add_argument("--rate", default="+8%")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--timing", required=True)
    return parser.parse_args()


async def run(args):
    text = args.text
    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8").strip()
    communicate = edge_tts.Communicate(
        text, args.voice, rate=args.rate, boundary="WordBoundary"
    )
    words = []
    with Path(args.audio).open("wb") as audio:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append(
                    {
                        "text": chunk["text"],
                        "start": chunk["offset"] / 10_000_000,
                        "duration": chunk["duration"] / 10_000_000,
                    }
                )
    if not words:
        raise RuntimeError("No WordBoundary events were returned.")
    Path(args.timing).write_text(
        json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"audio={args.audio} words={len(words)} timing={args.timing}")


if __name__ == "__main__":
    asyncio.run(run(parse_args()))
