import argparse
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build 2–5 word ASS karaoke captions from word timing JSON."
    )
    parser.add_argument("--timing", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def ass_time(seconds):
    total_cs = max(0, round(seconds * 100))
    hours, rem = divmod(total_cs, 360000)
    minutes, rem = divmod(rem, 6000)
    secs, cs = divmod(rem, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def group_words(words):
    segments, current = [], []
    for word in words:
        if current:
            previous = current[-1]
            previous_end = float(previous["start"]) + float(previous["duration"])
            if float(word["start"]) - previous_end > 0.40:
                segments.append(current)
                current = []
        current.append(word)
    if current:
        segments.append(current)
    groups = []
    for segment in segments:
        cursor = 0
        while cursor < len(segment):
            remaining = len(segment) - cursor
            if remaining <= 5:
                take = remaining
            elif remaining == 6 or remaining - 4 == 1:
                take = 3
            else:
                take = 4
            groups.append(segment[cursor : cursor + take])
            cursor += take
    return groups


def main():
    args = parse_args()
    words = json.loads(Path(args.timing).read_text(encoding="utf-8"))
    groups = group_words(words)
    if any(len(group) < 2 or len(group) > 5 for group in groups):
        raise RuntimeError("Caption grouping produced a group outside 2–5 words.")
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Arial,58,&H00FFF9EE,&H003FB9E6,&H00242321,&H90000000,-1,0,0,0,100,100,0,0,1,3,1,2,80,80,245,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for index, group in enumerate(groups):
        start = float(group[0]["start"])
        if index + 1 < len(groups):
            end = max(start + 0.2, float(groups[index + 1][0]["start"]) - 0.02)
        else:
            last = group[-1]
            end = float(last["start"]) + float(last["duration"]) + 0.15
        parts = []
        for word_index, word in enumerate(group):
            word_start = float(word["start"])
            word_end = (
                float(group[word_index + 1]["start"])
                if word_index + 1 < len(group)
                else end
            )
            centiseconds = max(1, round((word_end - word_start) * 100))
            parts.append(r"{\kf" + str(centiseconds) + "}" + word["text"])
        events.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Karaoke,,0,0,0,,"
            + " ".join(parts)
        )
    Path(args.out).write_text(header + "\n".join(events) + "\n", encoding="utf-8")
    print(f"words={len(words)} groups={len(groups)} output={args.out}")


if __name__ == "__main__":
    main()
