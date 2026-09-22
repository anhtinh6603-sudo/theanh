# Cài đặt Video vairo thú — bản đa nền tảng

Giải nén ZIP, mở Terminal/PowerShell tại thư mục `video-vairo-thu`, rồi chạy một lệnh phù hợp. Cần Python 3.10+; quy trình xuất video cần thêm `ffmpeg` và `ffprobe` trong `PATH`.

## Claude Code / Claude Desktop có Claude Code

```text
python install.py --target claude
```

Skill được chép vào `~/.claude/skills/video-vairo-thu`. Khởi động lại phiên Claude Code, rồi gọi `/video-vairo-thu` hoặc yêu cầu tự nhiên “Dùng Video vairo thú…”. Claude phải chạy trên máy có quyền truy cập file, trình duyệt Flow và FFmpeg thì mới xuất được MP4.

## Codex

```text
python install.py --target codex
```

Skill được chép vào `%USERPROFILE%/.codex/skills/video-vairo-thu` (Windows) hoặc `~/.codex/skills/video-vairo-thu` (macOS/Linux). Gọi `$video-vairo-thu`.

## Gemini CLI

```text
python install.py --target gemini
```

Gói được cài như extension tại `~/.gemini/extensions/video-vairo-thu`; `GEMINI.md` là context chính.

## Cursor

```text
python install.py --target cursor --project "/duong/dan/toi/du-an"
```

Core skill được chép vào `.agent-skills/video-vairo-thu`, còn rule được chép vào `.cursor/rules/video-vairo-thu.mdc`.

## Claude web/mobile hoặc nền tảng chat không chạy được lệnh

Không thể “cài” script cục bộ vào app điện thoại. Hãy tải file `prompts/CLAUDE-WEB-MOBILE.md` lên Project Knowledge/Files hoặc dán nội dung vào Project Instructions. Chế độ này tạo đầy đủ bộ kịch bản và prompt; việc điều khiển Flow, tải clip và chạy FFmpeg phải được chuyển sang máy có công cụ tương ứng.

## Dùng như gói prompt chung

Các agent khác có thể đọc `AGENTS.md`, rồi `SKILL.md`. Không cần hỗ trợ định dạng Skill riêng miễn là agent đọc được file Markdown và chạy được Python/FFmpeg.

## Cấu hình ElevenLabs

Đặt khóa và voice ID bằng biến môi trường. Ví dụ PowerShell:

```powershell
$env:ELEVENLABS_API_KEY = "your-key"
$env:VAIRO_WIFE_VOICE_ID = "your-wife-voice-id"
$env:VAIRO_HUSBAND_VOICE_ID = "your-husband-voice-id"
```

Ví dụ macOS/Linux:

```bash
export ELEVENLABS_API_KEY="your-key"
export VAIRO_WIFE_VOICE_ID="your-wife-voice-id"
export VAIRO_HUSBAND_VOICE_ID="your-husband-voice-id"
```

Không ghi các giá trị này vào Skill, Git hoặc file chia sẻ.

## Tạo và xuất dự án

```text
python scripts/new_video_project.py --project "/Videos/tap-01" --title "Tên tập"
python scripts/generate_elevenlabs.py --project "/Videos/tap-01"
python scripts/render_video.py --project "/Videos/tap-01"
python scripts/qc_video.py --video "/Videos/tap-01/final.mp4"
```

Dùng `python install.py --help` hoặc thêm `--force` khi chủ động muốn thay thế bản cài cũ.
