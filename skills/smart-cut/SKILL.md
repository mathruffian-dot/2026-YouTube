---
name: smart-cut
description: 智能剪口播 Skill。當使用者提供影片原始檔並要求「剪掉沒講話的片段」「去靜音」「剪口播」「自動剪輯」「像剪映那樣自動去停頓」時請一定要使用此技能。底層走 auto-editor（開源），偵測音量低於閾值的片段並剪掉，輸出只有人聲的版本。給 Claude Code 與 OpenAI Codex 共用。
---

# smart-cut：智能剪口播

## 何時觸發
使用者提供 mp4/mov/mkv/webm 原始影片，並要求：
- 剪口播、去靜音、剪掉沒聲音的部分
- 自動剪輯、像剪映那樣自動去停頓
- 「先把廢話片段砍掉」

## 原理
偵測音訊中音量低於閾值的片段 → 剪掉 → 把剩下的片段 concat 回成一支影片。剪映「智能剪口播」就是這類演算法。本 Skill 用開源 [auto-editor](https://github.com/WyattBlue/auto-editor) 包裝。

## 前置需求
```bash
# 第一次使用要裝
pip install auto-editor
ffmpeg -version  # auto-editor 內部會呼叫 ffmpeg
```

## 預設參數（已調過的甜蜜點）
| 參數 | 值 | 為什麼 |
|------|----|--------|
| `--margin` | `0.2s` | 每段語音前後留 0.2 秒，避免截太死 |
| `--edit` | `audio:threshold=0.04` | 音量門檻 4%，一般口播合適 |
| `--export` | `default`（剪掉靜音）| 不是加速，是直接砍掉 |

口播者語速慢/停頓多 → 調 `--margin` 至 `0.3s`。
雜訊多 → 提高 `threshold` 到 `0.06`。

## 標準呼叫
```bash
python "skills/smart-cut/scripts/smart_cut.py" \
  "raw/<影片代號>/原始.mp4" \
  --out "working/<影片代號>/<影片代號>.cut.mp4"
```

腳本內部會：
1. 檢查 auto-editor 是否安裝；沒裝就提示
2. 跑 auto-editor 並把進度即時印出
3. 回報「剪掉幾秒 / 原長 / 新長 / 壓縮率」

## 輸出
- `<影片代號>.cut.mp4` — 去靜音後的影片
- 一行統計回報：例如 `原長 18:42 → 新長 12:15（剪掉 34.6%）`

## 與其他 Skill 的銜接
1. **smart-cut**（本 Skill）→ 產出剪好的影片
2. → 抽音訊（`ffmpeg -i x.cut.mp4 -vn -ar 16000 x.cut.wav`）
3. → **audio-to-srt** Skill：對 cut 後的音訊轉字幕（時間碼會對齊剪好的影片，不是原始檔）
4. → 後續封面、文案、標題

## 踩坑
- **VFR（可變幀率）原始檔會讓 auto-editor 輸出黑幀**（EP07 實測：2:37 後全黑、僅剩聲音，常見於螢幕錄影）。`smart_cut.py` 已內建防護：剪輯前用 ffprobe 比對 `avg_frame_rate` 與 `r_frame_rate`，不一致即判定 VFR，先用 `ffmpeg -fps_mode cfr -r 30 -c:v libx264 -preset veryfast -crf 18 -c:a copy` 轉成暫存 CFR 檔再餵 auto-editor（音訊 copy，剪輯點與時間軸不變），完成後自動刪暫存檔並印出「偵測到 VFR，已先轉 CFR」。
- **不要對「原始檔」轉字幕再剪片**：時間碼會錯位。**先剪後轉**才對齊。
- **太短的停頓也被剪掉聽起來會很急**：把 `--margin` 拉到 `0.3s` 或更高。
- **音樂段落會被誤判為靜音**：若影片含背景音樂段，要先標記區段，那段用 `--cut-out` 反向保護或事後手動補回。
- **輸出檔太大**：auto-editor 預設用無損 concat。若要壓縮，後處理用 `ffmpeg -c:v libx264 -crf 23`。

## 檔案結構
```
skills/smart-cut/
├── SKILL.md           # 本檔
└── scripts/
    └── smart_cut.py   # auto-editor 包裝腳本
```
