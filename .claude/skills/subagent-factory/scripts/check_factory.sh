#!/usr/bin/env bash
# Lệnh kiểm tra toàn hệ thống Công xưởng Subagent.
set -u
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
FACTORY="$ROOT/.claude/skills/subagent-factory/factory"
fail=0

ok()   { printf '  ✅ %s\n' "$1"; }
warn() { printf '  ⚠️  %s\n' "$1"; }
bad()  { printf '  ❌ %s\n' "$1"; fail=1; }

echo "== Môi trường"
for c in node python3 ffmpeg ffprobe git; do
  if command -v "$c" >/dev/null 2>&1; then ok "$c"; else bad "$c thiếu"; fi
done
if command -v chromium >/dev/null 2>&1 || [ -d "${PLAYWRIGHT_BROWSERS_PATH:-/nonexistent}" ]; then
  ok "trình duyệt (chromium/playwright)"
else
  warn "không thấy chromium"
fi
avail_kb=$(df -Pk "$ROOT" | awk 'NR==2{print $4}')
if [ "${avail_kb:-0}" -gt 2097152 ]; then ok "đĩa trống > 2GB"; else warn "đĩa trống thấp"; fi

echo "== Thành phần công xưởng"
for f in registry.yaml permissions.yaml sources.yaml queue.yaml triggers.yaml quality-gate.md memory/profile.md; do
  if [ -f "$FACTORY/$f" ]; then ok "$f"; else bad "$f thiếu"; fi
done

echo "== Registry"
python3 - "$ROOT" "$FACTORY/registry.yaml" <<'PY' || fail=1
import os, sys
root, path = sys.argv[1], sys.argv[2]
try:
    import yaml
except ImportError:
    print("  ⚠️  thiếu PyYAML, bỏ qua kiểm registry (pip install pyyaml)")
    sys.exit(0)
data = yaml.safe_load(open(path, encoding="utf-8"))
bad = False
ids = set()
for a in data.get("agents", []):
    aid, st = a.get("id"), a.get("status")
    if aid in ids:
        print(f"  ❌ trùng id {aid}"); bad = True
    ids.add(aid)
    if st not in {"proposed", "active", "locked", "retired"}:
        print(f"  ❌ {aid}: status không hợp lệ ({st})"); bad = True
    elif st == "active" and not (a.get("file") and os.path.isfile(os.path.join(root, a["file"]))):
        print(f"  ❌ {aid}: active nhưng thiếu file agent"); bad = True
    else:
        print(f"  ✅ {aid} [{st}]")
sys.exit(1 if bad else 0)
PY

echo "== Bí mật"
if git -C "$ROOT" ls-files | grep -E '(^|/)\.env$' >/dev/null; then bad ".env đang bị git theo dõi"; else ok "không có .env trong git"; fi

[ "$fail" -eq 0 ] && echo "KẾT QUẢ: SẴN SÀNG" || echo "KẾT QUẢ: CÓ LỖI"
exit "$fail"
