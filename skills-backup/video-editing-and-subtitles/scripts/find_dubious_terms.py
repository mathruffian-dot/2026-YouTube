#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find_dubious_terms.py - 掃描 SRT 字幕中可能存在的專有名詞及音譯疑慮段落。
"""
import argparse
import re
from pathlib import Path

DEFAULT_TERMS = [
    "antigravity", "claude", "gemini", "typeless", "gem", "voicetype", "notype",
    "克勞德", "傑米奈", "泰普勒斯", "威士帕", "三師爸", "cloud", "jens", "cortex",
    "ntegreti", "banana", "nano", "classroom", "clasp", "gas", "agent"
]

def scan_srt(srt_path: Path, out_path: Path, terms: list[str]) -> None:
    if not srt_path.exists():
        print(f"[ERR] 找不到輸入字幕檔：{srt_path}")
        return

    content = srt_path.read_text(encoding="utf-8")
    blocks = re.split(r'\n\s*\n', content)
    
    # 建立正則表達式，忽略大小寫且符合任何一個關鍵字
    pattern_str = r'(' + '|'.join(re.escape(t) for t in terms) + r')'
    pattern = re.compile(pattern_str, re.IGNORECASE)
    
    found_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        if len(lines) >= 3:
            num = lines[0].strip()
            time_str = lines[1].strip()
            text = " ".join(lines[2:]).strip()
            
            matches = pattern.findall(text)
            if matches:
                # 取得不重複的匹配項並保留原字大小寫
                found_blocks.append({
                    "num": num,
                    "time": time_str,
                    "text": text,
                    "matches": list(set(matches))
                })

    md_lines = []
    md_lines.append("# 術語與疑慮片段提取結果\n")
    md_lines.append(f"共找到 {len(found_blocks)} 個含有關鍵術語的段落。\n")
    
    for b in found_blocks:
        highlighted_text = b["text"]
        # 長詞先替換避免被子字串重複影響
        sorted_matches = sorted(b["matches"], key=len, reverse=True)
        for match in sorted_matches:
            reg = re.compile(re.escape(match), re.IGNORECASE)
            highlighted_text = reg.sub(lambda m: f"**{m.group(0)}**", highlighted_text)
            
        md_lines.append(f"### 段落 {b['num']} ({b['time']})")
        md_lines.append(f"- **偵測術語**: {', '.join(b['matches'])}")
        md_lines.append(f"- **內容**: {highlighted_text}\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"[OK] 已輸出疑慮對照表：{out_path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="尋找 SRT 中的疑慮術語段落")
    ap.add_argument("src", type=Path, help="輸入的 SRT 字幕路徑")
    ap.add_argument("--out", type=Path, required=True, help="輸出的 Markdown 檔案路徑")
    ap.add_argument("--terms", default=None, help="自訂關鍵字，多個以逗號分隔")
    args = ap.parse_args()

    terms = DEFAULT_TERMS
    if args.terms:
        terms = [t.strip() for t in args.terms.split(",") if t.strip()]

    scan_srt(args.src, args.out, terms)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
