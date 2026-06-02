#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_end_card.py — 為短片結尾添加一個 3 秒字卡「完整影片請看留言」

用法：
  python add_end_card.py \
    --input-mp4 working/antigravity-ep03/short-tmp/short.mp4 \
    --output-mp4 working/antigravity-ep03/short-tmp/short_with_card.mp4
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def get_stream_info(mp4_path: Path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=codec_type,sample_rate,channels,r_frame_rate,pix_fmt',
        '-of', 'json', str(mp4_path)
    ]
    try:
        out = subprocess.check_output(cmd, text=True)
        data = json.loads(out)
        v_info = {}
        a_info = {}
        for stream in data.get('streams', []):
            if stream['codec_type'] == 'video':
                v_info = stream
            elif stream['codec_type'] == 'audio':
                a_info = stream
        return v_info, a_info
    except Exception as e:
        print(f"[ERR] ffprobe 讀取失敗: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description='為短片結尾添加 3 秒字卡「完整影片請看留言」')
    ap.add_argument('--input-mp4', type=Path, required=True)
    ap.add_argument('--output-mp4', type=Path, required=True)
    ap.add_argument('--duration', type=float, default=3.0, help='字卡停留秒數')
    args = ap.parse_args()

    if not args.input_mp4.exists():
        print(f"[ERR] 找不到輸入影片: {args.input_mp4}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] 正在讀取影片資訊: {args.input_mp4}")
    v_info, a_info = get_stream_info(args.input_mp4)

    # 取得原始視訊參數，若無則設為預設值
    fps = v_info.get('r_frame_rate', '30')
    pix_fmt = v_info.get('pix_fmt', 'yuv420p')
    
    # 取得原始音訊參數，若無則設為預設值
    sample_rate = a_info.get('sample_rate', '44100')
    channels = a_info.get('channels', 2)
    layout = 'stereo' if channels == 2 else 'mono'

    tmp_dir = args.input_mp4.parent / 'end-card-tmp'
    tmp_dir.mkdir(parents=True, exist_ok=True)
    card_mp4 = tmp_dir / 'card.mp4'

    # 設定字卡背景顏色為深海軍藍 `#0A192F`，文字為白色，加亮藍色陰影/霓虹邊緣
    # 在 Windows 環境中使用微軟正黑體 msjh.ttc
    font_path = "C\:\\\\Windows\\\\Fonts\\\\msjh.ttc"
    text = "完整影片請看留言"
    
    # ffmpeg drawtext filter 字幕繪製
    drawtext_filter = (
        f"drawtext=fontfile='{font_path}':"
        f"text='{text}':"
        f"fontsize=72:"
        f"fontcolor=0x00D4FF:"  # 霓虹亮藍色
        f"bordercolor=0xFFFFFF:" # 白色描邊
        f"borderw=3:"
        f"x=(w-text_w)/2:"
        f"y=(h-text_h)/2"
    )

    print(f"[INFO] 正在生成結尾字卡影片 (時長: {args.duration}s)...")
    # 生成字卡 (含無聲音軌以匹配 concat)
    cmd_gen_card = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f"color=c=0x0A192F:s=1920x1080:d={args.duration}:r={fps}",
        '-f', 'lavfi', '-i', f"anullsrc=r={sample_rate}:cl={layout}",
        '-vf', drawtext_filter,
        '-c:v', 'libx264', '-pix_fmt', pix_fmt,
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest',
        str(card_mp4)
    ]
    
    rc = subprocess.call(cmd_gen_card)
    if rc != 0:
        print(f"[ERR] 生成字卡失敗, rc={rc}", file=sys.stderr)
        sys.exit(rc)

    print(f"[INFO] 正在拼接影片與字卡...")
    # 使用 ffmpeg filter_complex concat 拼接影片
    # 確保兩段影片以完全相同的參數做重新編碼/拼接，避免播放器相容性問題
    concat_filter = (
        "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]"
    )
    
    cmd_concat = [
        'ffmpeg', '-y',
        '-i', str(args.input_mp4),
        '-i', str(card_mp4),
        '-filter_complex', concat_filter,
        '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
        '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart',
        str(args.output_mp4)
    ]
    
    rc = subprocess.call(cmd_concat)
    if rc != 0:
        print(f"[ERR] 拼接失敗, rc={rc}", file=sys.stderr)
        sys.exit(rc)

    # 清除暫存目錄
    try:
        card_mp4.unlink()
        tmp_dir.rmdir()
    except Exception as e:
        print(f"[WARN] 清除暫存檔失敗: {e}")

    print(f"[DONE] 成功將字卡添加至短片結尾！")
    print(f"  - 輸出檔案: {args.output_mp4}")


if __name__ == '__main__':
    main()
