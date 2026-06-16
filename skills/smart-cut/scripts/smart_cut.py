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


def detect_vfr(path: Path) -> bool:
    """用 ffprobe 比對 avg_frame_rate 與 r_frame_rate，不一致即視為 VFR（可變幀率）。"""
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=avg_frame_rate,r_frame_rate",
            "-of", "default=noprint_wrappers=1",
            str(path),
        ], text=True)
    except Exception as e:
        print(f"[WARN] ffprobe 檢查幀率失敗，跳過 VFR 偵測：{e}")
        return False

    rates: dict[str, str] = {}
    for line in out.splitlines():
        if "=" in line:
            key, _, val = line.partition("=")
            rates[key.strip()] = val.strip()

    avg = rates.get("avg_frame_rate", "")
    r = rates.get("r_frame_rate", "")
    if not avg or not r or avg in ("0/0", "N/A") or r in ("0/0", "N/A"):
        return False

    def to_float(frac: str) -> float | None:
        try:
            if "/" in frac:
                num, den = frac.split("/", 1)
                return float(num) / float(den) if float(den) != 0 else None
            return float(frac)
        except Exception:
            return None

    f_avg, f_r = to_float(avg), to_float(r)
    if f_avg is None or f_r is None:
        return False
    # 兩者差超過 0.01 fps 即判定 VFR（螢幕錄影常見 avg 是奇怪的長分數）
    return abs(f_avg - f_r) > 0.01


def convert_to_cfr(src: Path, dst: Path) -> None:
    """VFR → CFR 30fps。音訊 copy 不重編碼，確保 auto-editor 剪輯點不變。"""
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-fps_mode", "cfr", "-r", "30",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "copy",
        str(dst),
    ]
    print(f"[CMD] {' '.join(cmd)}")
    rc = subprocess.call(cmd)
    if rc != 0:
        print(f"[ERR] VFR→CFR 轉檔失敗，退出碼 {rc}", file=sys.stderr)
        sys.exit(rc)


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

    # VFR（可變幀率）原始檔直接餵 auto-editor 會中途輸出黑幀（EP07 實測：2:37 後全黑）。
    # 先轉成 CFR 30fps 暫存檔再剪；音訊 copy 不動，剪輯點與時間軸不變。
    ae_input = args.input
    cfr_tmp: Path | None = None
    if detect_vfr(args.input):
        print("[INFO] 偵測到 VFR，已先轉 CFR 再剪輯")
        cfr_tmp = args.out.parent / f"{args.input.stem}.cfr.tmp.mp4"
        convert_to_cfr(args.input, cfr_tmp)
        ae_input = cfr_tmp

    cmd = [
        *ae,
        str(ae_input),
        "--margin", args.margin,
        "--edit", f"audio:threshold={args.threshold}",
        "-o", str(args.out),
    ]
    print(f"[CMD] {' '.join(cmd)}")
    try:
        rc = subprocess.call(cmd)
    finally:
        if cfr_tmp is not None and cfr_tmp.exists():
            cfr_tmp.unlink()
    if rc != 0:
        print(f"[ERR] auto-editor 失敗，退出碼 {rc}", file=sys.stderr)
        sys.exit(rc)
    if cfr_tmp is not None:
        print("[OK] 偵測到 VFR，已先轉 CFR（暫存檔已刪除）")

    try:
        dur_in = get_duration(args.input)
        dur_out = get_duration(args.out)
        cut_pct = (1 - dur_out / dur_in) * 100 if dur_in > 0 else 0
        print(f"[OK] 原長 {fmt(dur_in)} → 新長 {fmt(dur_out)}（剪掉 {cut_pct:.1f}%）")
    except Exception as e:
        print(f"[WARN] 統計時長失敗：{e}")


if __name__ == "__main__":
    main()
