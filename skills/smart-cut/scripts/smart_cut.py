#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
smart_cut.py — auto-editor 包裝腳本
偵測音量低於閾值的片段並剪掉，輸出只有人聲的影片。
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def check_deps() -> list[str]:
    """回傳 auto-editor 的呼叫前綴（CLI 或 python -m auto_editor）。"""
    if shutil.which("ffmpeg") is None:
        print("[ERR] 找不到 ffmpeg。請先安裝 ffmpeg 並加入 PATH。", file=sys.stderr)
        sys.exit(1)
    if shutil.which("auto-editor") is not None:
        return ["auto-editor"]
    # 退而用 python -m auto_editor
    try:
        subprocess.check_output([sys.executable, "-m", "auto_editor", "--version"], stderr=subprocess.STDOUT)
        return [sys.executable, "-m", "auto_editor"]
    except Exception:
        print("[ERR] 找不到 auto-editor。請先安裝：pip install auto-editor", file=sys.stderr)
        sys.exit(1)


def get_duration(path: Path) -> float:
    """用 ffprobe 取得影片秒數。"""
    out = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ], text=True).strip()
    return float(out)


def fmt(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def main() -> None:
    ap = argparse.ArgumentParser(description="智能剪口播：去除靜音片段")
    ap.add_argument("input", type=Path, help="輸入影片檔")
    ap.add_argument("--out", type=Path, required=True, help="輸出影片檔")
    ap.add_argument("--margin", default="0.2s", help="每段語音前後保留秒數，預設 0.2s")
    ap.add_argument("--threshold", default="0.04", help="音量門檻，預設 0.04")
    args = ap.parse_args()

    ae = check_deps()

    if not args.input.exists():
        print(f"[ERR] 找不到輸入檔：{args.input}", file=sys.stderr)
        sys.exit(1)

    args.out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        *ae,
        str(args.input),
        "--margin", args.margin,
        "--edit", f"audio:threshold={args.threshold}",
        "-o", str(args.out),
    ]
    print(f"[CMD] {' '.join(cmd)}")
    rc = subprocess.call(cmd)
    if rc != 0:
        print(f"[ERR] auto-editor 失敗，退出碼 {rc}", file=sys.stderr)
        sys.exit(rc)

    try:
        dur_in = get_duration(args.input)
        dur_out = get_duration(args.out)
        cut_pct = (1 - dur_out / dur_in) * 100 if dur_in > 0 else 0
        print(f"[OK] 原長 {fmt(dur_in)} → 新長 {fmt(dur_out)}（剪掉 {cut_pct:.1f}%）")
    except Exception as e:
        print(f"[WARN] 統計時長失敗：{e}")


if __name__ == "__main__":
    main()
