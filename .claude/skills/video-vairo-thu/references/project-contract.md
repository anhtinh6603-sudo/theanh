# Cấu trúc dự án

```text
project/
|-- BRIEF.md
|-- SCRIPT.md
|-- STORYBOARD.md
|-- flow-prompts.md
|-- takes.json
|-- timeline.json
|-- images/
|   `-- scene-01.png ...
|-- flow/
|   `-- scene-01.mp4 ...
|-- audio/
|   `-- 01-wife.mp3 ...
|-- work/
|   `-- captions.ass
|-- qa/
`-- final.mp4
```

## `timeline.json`

```json
{
  "target_duration": 45,
  "scene_durations": [7, 8, 8, 8, 7, 7],
  "audio_tracks": [
    {"file": "audio/01-wife.mp3", "start_ms": 400, "volume": 1.0}
  ],
  "bgm": {"file": "audio/bgm.wav", "volume": 0.10}
}
```

- `scene_durations` phải có cùng số phần tử với `flow/scene-*.mp4`.
- Tổng `scene_durations` phải bằng `target_duration`.
- `audio_tracks` chứa cả thoại và SFX; thời gian tính từ đầu video.
- `bgm` là tùy chọn. Nếu có, renderer lặp nhạc tới hết video và fade hai đầu.

## `takes.json`

```json
[
  {
    "file": "01-wife",
    "voice_env": "VAIRO_WIFE_VOICE_ID",
    "text": "[curious] Câu thoại tiếng Việt."
  }
]
```

`voice_env` là tên biến môi trường chứa voice ID. Có thể dùng `voice_id` trực tiếp khi voice ID không nhạy cảm và được phép chia sẻ.

