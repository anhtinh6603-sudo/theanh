#!/usr/bin/env python3
"""Đầu não Subagent — bộ máy ghi nhận job, kiểm quyền, quality gate cho đội agent.

hq.py KHÔNG tự chạy agent. Nó là xương sống ghi nhận/ kiểm soát: agent con
(Claude skill/subagent thật) vẫn do chủ hoặc Claude gọi trực tiếp; hq.py chỉ
đứng giữa để mọi việc đi qua đăng ký, kiểm quyền và quality gate thay vì
làm tắt.

Lệnh:
  hq.py new <agent> <file_or_text> "<mô tả>"
  hq.py check <job_id> <hanh_dong>
  hq.py run <job_id>
  hq.py gate <job_id> <tieu_chi> <pass|fail> [bang_chung]
  hq.py retry <job_id> "<ly_do>"
  hq.py done <job_id>
  hq.py status [job_id]
  hq.py lock <agent>
  hq.py stop
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config"
JOBS_FILE = ROOT / "jobs" / "jobs.json"
LOG_FILE = ROOT / "logs" / "hq.log.jsonl"
HALT_FILE = ROOT / "jobs" / "HALT"

REQUIRED_GATE_CRITERIA = [
    "yeu_cau", "thuong_hieu", "ky_thuat", "quyen", "trai_nghiem", "bang_chung",
]


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log(event: str, **fields) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **fields}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_registry():
    return load_json(CONFIG / "registry.json", {"agents": [], "coordinators": []})


def load_permissions():
    return load_json(CONFIG / "permissions.json", {"tiers": {}, "action_tiers": {}})


def find_agent(registry, name):
    for a in registry.get("agents", []):
        if a["name"] == name:
            return a
    return None


def content_hash(agent: str, file_or_text: str) -> str:
    p = Path(file_or_text)
    if p.exists() and p.is_file():
        data = p.read_bytes()
    else:
        data = file_or_text.encode("utf-8")
    h = hashlib.sha256()
    h.update(agent.encode("utf-8"))
    h.update(b"\0")
    h.update(data)
    return h.hexdigest()


def cmd_new(args) -> int:
    if HALT_FILE.exists():
        print("DỪNG KHẨN đang bật (jobs/HALT tồn tại) — không tạo job mới.")
        return 3
    registry = load_registry()
    agent = find_agent(registry, args.agent)
    if agent is None:
        print(f"Không tìm thấy agent '{args.agent}' trong registry.json")
        return 1
    if agent.get("status") != "active":
        print(f"Agent '{args.agent}' đang ở trạng thái '{agent.get('status')}', không active.")
        return 1

    fh = content_hash(args.agent, args.file)
    dedup_key = f"{args.agent}:{fh}"
    jobs = load_json(JOBS_FILE, {})

    for jid, job in jobs.items():
        if job.get("dedup_key") == dedup_key and job.get("status") != "failed":
            print(f"Job đã tồn tại (chống trùng): {jid} — status={job['status']}")
            return 0

    job_id = fh[:12]
    jobs[job_id] = {
        "agent": args.agent,
        "input": args.file,
        "desc": args.desc,
        "dedup_key": dedup_key,
        "status": "pending",
        "retries": 0,
        "gate": [],
        "history": [{"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": "new"}],
    }
    save_json(JOBS_FILE, jobs)
    log("new", job_id=job_id, agent=args.agent, desc=args.desc)
    print(job_id)
    return 0


def cmd_check(args) -> int:
    registry = load_registry()
    perms = load_permissions()
    jobs = load_json(JOBS_FILE, {})

    job = jobs.get(args.job_id)
    if job is None:
        print(f"Không tìm thấy job '{args.job_id}'")
        return 1

    agent = find_agent(registry, job["agent"])
    if agent is None or agent.get("status") != "active":
        print(f"Agent '{job['agent']}' không active — dừng.")
        return 1

    if args.hanh_dong not in agent.get("actions", []):
        print(f"Agent '{job['agent']}' không được khai hành động '{args.hanh_dong}' trong registry.")
        return 1

    tier = perms.get("action_tiers", {}).get(args.hanh_dong)
    if tier is None:
        print(f"Hành động '{args.hanh_dong}' chưa có trong permissions.json")
        return 1

    tier_desc = perms.get("tiers", {}).get(str(tier), "")
    print(f"Tier {tier}: {tier_desc}")
    log("check", job_id=args.job_id, action=args.hanh_dong, tier=tier)

    if tier >= 4:
        print("=> DỪNG, chuyển chủ trực tiếp thao tác (đăng nhập/OTP/thanh toán).")
        return 3
    if tier == 3:
        print("=> Xin duyệt chủ trước bước cuối (đăng bài/gửi tin/trả phí/đổi quyền).")
        return 2
    if tier == 2:
        print("=> Agent được chạy, nhưng phải hiện tiến trình cho chủ xem.")
        return 1
    print("=> Agent được tự động hoàn toàn.")
    return 0


def cmd_run(args) -> int:
    jobs = load_json(JOBS_FILE, {})
    job = jobs.get(args.job_id)
    if job is None:
        print(f"Không tìm thấy job '{args.job_id}'")
        return 1
    job["status"] = "running"
    job["history"].append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": "run"})
    save_json(JOBS_FILE, jobs)
    log("run", job_id=args.job_id, agent=job["agent"])
    print(
        f"Job {args.job_id} -> running. hq.py không tự thực thi agent — "
        f"gọi agent '{job['agent']}' thật (Claude Skill/Agent tool) bên ngoài, "
        f"rồi ghi quality gate bằng 'hq.py gate' và đóng job bằng 'hq.py done'."
    )
    return 0


def cmd_gate(args) -> int:
    if args.tieu_chi not in REQUIRED_GATE_CRITERIA:
        print(f"Tiêu chí không hợp lệ. Dùng một trong: {', '.join(REQUIRED_GATE_CRITERIA)}")
        return 1
    jobs = load_json(JOBS_FILE, {})
    job = jobs.get(args.job_id)
    if job is None:
        print(f"Không tìm thấy job '{args.job_id}'")
        return 1
    job["gate"] = [g for g in job["gate"] if g["tieu_chi"] != args.tieu_chi]
    job["gate"].append({
        "tieu_chi": args.tieu_chi,
        "result": args.result,
        "evidence": args.evidence or "",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    save_json(JOBS_FILE, jobs)
    log("gate", job_id=args.job_id, tieu_chi=args.tieu_chi, result=args.result)
    print(f"Đã ghi gate '{args.tieu_chi}' = {args.result}")
    return 0


def cmd_retry(args) -> int:
    jobs = load_json(JOBS_FILE, {})
    job = jobs.get(args.job_id)
    if job is None:
        print(f"Không tìm thấy job '{args.job_id}'")
        return 1
    job["retries"] += 1
    job["history"].append({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": "retry",
        "reason": args.reason, "count": job["retries"],
    })
    if job["retries"] > 2:
        job["status"] = "blocked"
        print(f"Job {args.job_id} hết lượt retry (>2) — status=blocked. Báo chủ phần chưa đạt.")
    else:
        print(f"Job {args.job_id} retry lần {job['retries']}/2. Lý do: {args.reason}")
    save_json(JOBS_FILE, jobs)
    log("retry", job_id=args.job_id, count=job["retries"], reason=args.reason)
    return 0


def cmd_done(args) -> int:
    jobs = load_json(JOBS_FILE, {})
    job = jobs.get(args.job_id)
    if job is None:
        print(f"Không tìm thấy job '{args.job_id}'")
        return 1
    have = {g["tieu_chi"]: g["result"] for g in job.get("gate", [])}
    missing = [c for c in REQUIRED_GATE_CRITERIA if c not in have]
    failed = [c for c, r in have.items() if r == "fail"]
    if missing or failed:
        print("Chưa đủ điều kiện đóng job:")
        if missing:
            print(f"  - Thiếu gate: {', '.join(missing)}")
        if failed:
            print(f"  - Gate fail: {', '.join(failed)}")
        return 1
    job["status"] = "done"
    job["history"].append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": "done"})
    save_json(JOBS_FILE, jobs)
    log("done", job_id=args.job_id, agent=job["agent"])
    print(f"Job {args.job_id} hoàn thành — đủ 6 tiêu chí quality gate. Sẵn sàng bàn giao chủ.")
    return 0


def cmd_status(args) -> int:
    jobs = load_json(JOBS_FILE, {})
    if args.job_id:
        job = jobs.get(args.job_id)
        if job is None:
            print(f"Không tìm thấy job '{args.job_id}'")
            return 1
        print(json.dumps(job, ensure_ascii=False, indent=2))
        return 0
    if not jobs:
        print("Chưa có job nào.")
        return 0
    for jid, job in jobs.items():
        print(f"{jid}  [{job['status']:9}]  {job['agent']:35}  {job['desc'][:50]}")
    return 0


def cmd_add_agent(args) -> int:
    registry = load_registry()
    if find_agent(registry, args.name) is not None:
        print(f"Agent '{args.name}' đã tồn tại trong registry — dùng 'activate' nếu muốn mở lại.")
        return 1
    actions = [a.strip() for a in args.actions.split(",") if a.strip()]
    registry.setdefault("agents", []).append({
        "name": args.name,
        "group": args.group,
        "capability": args.capability,
        "actions": actions,
        "status": "draft",
    })
    save_json(CONFIG / "registry.json", registry)
    log("add_agent", agent=args.name, status="draft")
    print(
        f"Đã thêm agent '{args.name}' với status=draft. "
        f"Agent draft KHÔNG nhận job mới (hq.py new sẽ chặn). "
        f"Test ổn rồi chạy 'hq.py activate {args.name}' mới cho chạy thật."
    )
    return 0


def cmd_activate(args) -> int:
    registry = load_registry()
    agent = find_agent(registry, args.agent)
    if agent is None:
        print(f"Không tìm thấy agent '{args.agent}'")
        return 1
    if agent.get("status") == "active":
        print(f"Agent '{args.agent}' đã active.")
        return 0
    prev = agent.get("status")
    agent["status"] = "active"
    save_json(CONFIG / "registry.json", registry)
    log("activate", agent=args.agent, prev_status=prev)
    print(f"Agent '{args.agent}' chuyển {prev} -> active. Đảm bảo đã test (snapshot/selftest) trước khi làm việc này.")
    return 0


def cmd_lock(args) -> int:
    registry = load_registry()
    agent = find_agent(registry, args.agent)
    if agent is None:
        print(f"Không tìm thấy agent '{args.agent}'")
        return 1
    agent["status"] = "locked"
    save_json(CONFIG / "registry.json", registry)
    log("lock", agent=args.agent)
    print(f"Agent '{args.agent}' đã bị khóa (locked).")
    return 0


def cmd_stop(_args) -> int:
    HALT_FILE.parent.mkdir(parents=True, exist_ok=True)
    HALT_FILE.write_text(time.strftime("%Y-%m-%dT%H:%M:%S"), encoding="utf-8")
    log("stop")
    print("DỪNG KHẨN đã bật — mọi job mới bị chặn. Xoá file jobs/HALT để mở lại.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Đầu não Subagent HQ")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new")
    p.add_argument("agent")
    p.add_argument("file")
    p.add_argument("desc")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("check")
    p.add_argument("job_id")
    p.add_argument("hanh_dong")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("run")
    p.add_argument("job_id")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("gate")
    p.add_argument("job_id")
    p.add_argument("tieu_chi", choices=REQUIRED_GATE_CRITERIA)
    p.add_argument("result", choices=["pass", "fail"])
    p.add_argument("evidence", nargs="?", default="")
    p.set_defaults(func=cmd_gate)

    p = sub.add_parser("retry")
    p.add_argument("job_id")
    p.add_argument("reason")
    p.set_defaults(func=cmd_retry)

    p = sub.add_parser("done")
    p.add_argument("job_id")
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("status")
    p.add_argument("job_id", nargs="?")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("add-agent")
    p.add_argument("name")
    p.add_argument("group")
    p.add_argument("capability")
    p.add_argument("actions", help="Danh sách hành động, phân tách bởi dấu phẩy, vd: draft,post")
    p.set_defaults(func=cmd_add_agent)

    p = sub.add_parser("activate")
    p.add_argument("agent")
    p.set_defaults(func=cmd_activate)

    p = sub.add_parser("lock")
    p.add_argument("agent")
    p.set_defaults(func=cmd_lock)

    p = sub.add_parser("stop")
    p.set_defaults(func=cmd_stop)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
