---
name: claude-youtube-video-workflow
description: Claude Code 專用的 2026Youtube 總控工作流 Skill。當使用者要求 Claude Code 處理 raw 裡的新影片、一次跑完整 YouTube 生產線、剪口播、轉字幕、產標題、用 cover-image/draw.py 產封面、寫 metadata、打包 output，或說「使用 claude-youtube-video-workflow」時使用。此 Skill 明確走 Claude Code / OpenAI API Key 封面路線，不使用 Codex 內建 Image2。
---

# claude-youtube-video-workflow：Claude Code 版 YouTube 生產總控

## 先讀

- `HANDOFF.md`
- `CLAUDE.md`
- `assets/style/reference-thumbnails.png`
- `assets/style/cover-style.md`
- `assets/persona/三師爸人物形象照.png`

## Claude Code 專用規則

- 封面使用 `skills/cover-image/draw.py` 或 Claude 全域 `~/.claude/skills/draw/draw.py`。
- 需要 OpenAI API Key：`OPENAI_API_KEY` 或 `~/.openai.env`。
- 產封面必帶 `--edit assets/persona/三師爸人物形象照.png`。
- 每次封面都必須重新使用人物基準照，不得從上一張封面或衍生圖延續人物。
- Claude 版代表色是橘色：`#FF8C42`、`#FFA500`、`#FF6B35`。
- Claude 輸出資料夾固定加 `[Claude]` 後綴。

## 流程

1. **收件**
   - 找 `raw/` 的新影片。
   - 建立 `working/<video-id>/`。

2. **剪口播**
   - 讀 `skills/smart-cut/SKILL.md`。
   - 執行 `skills/smart-cut/scripts/smart_cut.py`。
   - 建議起始參數：`--threshold 0.05`；停頓多可用 `0.06`；短實演片可用 `--margin "0sec,0.1sec"`。
   - 輸出 `working/<video-id>/<video-id>.cut.mp4`。

3. **轉字幕**
   - 先用 ffmpeg 從剪好影片抽 16kHz mono 音訊。
   - 讀 `skills/audio-to-srt/SKILL.md`。
   - 執行 Groq transcription、resegment、apply_vocab、清字、validate、srt_to_txt。
   - 輸出 `working/<video-id>/<video-id>.srt` 與 `.txt`。

4. **產標題並暫停**
   - 讀清字後 `.txt`。
   - 產生 10 個標題候選到 `working/<video-id>/titles.md`。
   - 回報標題清單，停下等使用者選編號。

5. **建立 Claude 輸出資料夾**
   - 清洗標題中的 Windows 不合法字元：`？！：／＼?!:/\\<>|"*`。
   - 建立 `output/<清洗後標題> [Claude]/`。
   - 檔案本身不要加 `[Claude]`。

6. **產封面**
   - 重新讀人物基準照與風格指南，不沿用舊封面。
   - Prompt 必含：
     - 人物特徵：短黑髮帶少量灰白、黑框矩形眼鏡、黑色長版防風連帽外套、黑色上衣、自然微笑、教師氣質。
     - Claude 主色：橘色 / 橘黃光，不要 Codex 亮藍作主光。
     - 科技教學風格：深海軍藍背景、資料流、AI Agent、課程計畫表格。
   - 標準呼叫：
     ```powershell
     python skills\cover-image\draw.py "<prompt>" --edit "assets\persona\三師爸人物形象照.png" --size 1536x1024 --quality low --name cover --outdir "output\<標題> [Claude]"
     ```
   - 若輸出有時間戳檔名，整理為 `cover.png`。

7. **寫 metadata**
   - `metadata.md` 必含：
     - YouTube 描述
     - 章節建議
     - Facebook / Instagram / Threads 貼文
     - SEO 主關鍵字、次關鍵字、長尾關鍵字、競品搜尋詞
     - 「YouTube 標籤欄位（直接複製）」：半形逗號分隔，含「全部一次貼」
     - 上架前 checklist

8. **打包與檢查**
   - 輸出資料夾應包含：
     - `<標題>.mp4`
     - `<標題>.srt`
     - `<標題>.txt`
     - `cover.png`
     - `metadata.md`
   - PowerShell 檢查含 `[Claude]` 的路徑時用 `-LiteralPath`。

9. **更新交班**
   - 更新 `HANDOFF.md`：完成項目、輸出位置、封面狀態、待審事項、下一步。

## 踩坑

- `OPENAI_API_KEY` 不存在或帳號未驗證時，封面會失敗。
- `skills/cover-image/draw.py` 需要 `openai` Python 套件。
- Groq transcription 會上傳音訊到第三方服務；若需要明確授權，先停下。
- 中文檔名、空白、`[Claude]` 路徑要用引號與 `-LiteralPath`。
