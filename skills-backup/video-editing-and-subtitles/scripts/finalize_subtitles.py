#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
finalize_subtitles.py - 通用字幕精修套用腳本。
支援多次指定 --replace "舊字->新字" 的參數，並執行內建的大小寫統一與常見錯字修正。
"""
import argparse
import re
from pathlib import Path

# 內建通用替換邏輯（機械替換）
BUILTIN_REPLACEMENTS = [
    ("Antigravity", "AntiGravity"),
    ("antigravity", "AntiGravity"),
    ("Anti-Gravity", "AntiGravity"),
    ("胡椒它的", "呼叫它的"),
]

def apply_replacements(text: str, custom_replaces: list[tuple[str, str]], seg_num: str) -> str:
    # 1. 先跑使用者自訂的更正 (自訂更正優先級最高)
    for old, new in custom_replaces:
        # 支援針對特定段落的規則，例如: "390:AGE->Agent"
        if ":" in old:
            parts = old.split(":", 1)
            target_seg = parts[0].strip()
            actual_old = parts[1]
            if target_seg == seg_num:
                text = text.replace(actual_old, new)
        else:
            # 全局替換 (忽略大小寫的全局取代可以使用 re.sub 或直接 replace)
            # 這裡為了簡單，使用不分大小寫的替換
            reg = re.compile(re.escape(old), re.IGNORECASE)
            text = reg.sub(new, text)
            
    # 2. 再跑內建的基礎大小寫與錯字統一
    for old, new in BUILTIN_REPLACEMENTS:
        text = text.replace(old, new)
        
    return text

def process_srt(src_path: Path, dst_path: Path, custom_replaces: list[tuple[str, str]]) -> None:
    if not src_path.exists():
        print(f"[ERR] 找不到輸入字幕檔：{src_path}")
        return

    content = src_path.read_text(encoding="utf-8")
    blocks = re.split(r'(\r?\n\r?\n)', content)
    
    out = []
    n_replaced = 0
    for seg in blocks:
        if not seg.strip() or seg.isspace() or "-->" not in seg:
            out.append(seg)
            continue
        
        lines = seg.splitlines(keepends=False)
        if len(lines) < 3:
            out.append(seg)
            continue
            
        header = "\n".join(lines[:2])
        body_before = "\n".join(lines[2:])
        seg_num = lines[0].strip()
        
        body_after = apply_replacements(body_before, custom_replaces, seg_num)
        if body_after != body_before:
            n_replaced += 1
            
        out.append(header + "\n" + body_after)
        
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text("".join(out), encoding="utf-8")
    print(f"[OK] 已輸出精修字幕：{dst_path}")
    print(f"     共 {n_replaced} 段字幕被修改。")

def main() -> int:
    ap = argparse.ArgumentParser(description="字幕套用修正與精修")
    ap.add_argument("src", type=Path, help="輸入的 SRT 字幕路徑 (如 .vocab.srt)")
    ap.add_argument("--out", type=Path, required=True, help="輸出的精修後 SRT 路徑")
    ap.add_argument("--replace", action="append", default=[], 
                    help="替換規則，格式為 '舊字->新字' (可多次指定)。支援特定段落，如 '390:AGE->Agent'")
    args = ap.parse_args()

    custom_replaces = []
    for r in args.replace:
        if "->" in r:
            old, new = r.split("->", 1)
            custom_replaces.append((old.strip(), new.strip()))
        else:
            print(f"[WARN] 忽略無效替換規則格式（應為 '舊字->新字'）：{r}")

    process_srt(args.src, args.out, custom_replaces)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
