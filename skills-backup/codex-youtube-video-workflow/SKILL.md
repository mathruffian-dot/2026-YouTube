---
name: codex-youtube-video-workflow
description: Codex 專用的 2026Youtube 總控工作流 Skill。當使用者要求 Codex 處理 raw 裡的新影片、一次跑完整 YouTube 生產線、剪口播、轉字幕、產標題、用內建 Image2 產封面、寫 metadata、打包 output，或說「使用 codex-youtube-video-workflow」時使用。此 Skill 明確使用 Codex 內建生圖能力，不呼叫 Claude 的 cover-image/draw.py。
---

# codex-youtube-video-workflow：Codex 版 YouTube 生產總控

## 先讀

- `HANDOFF.md`
- `AGENTS.md`
- `assets/style/reference-thumbnails.png`
- `assets/style/cover-style.md`
- `assets/persona/三師爸人物形象照.png`

## Codex 專用規則

- 封面使用 Codex 內建 Image2 生圖，不需要 OpenAI API Key。
- 不要呼叫 `skills/cover-image/draw.py`；那是 Claude Code / API 路線。
- 每次封面都必須重新參考 `assets/persona/三師爸人物形象照.png`，不得從上一張封面或衍生圖延續人物。
- Codex 版代表色是亮藍 / 電子青：`#00D4FF`、`#0099FF`，可少量用紫光 `#9D4EDD`。
- Codex 輸出資料夾固定加 `[Codex]` 後綴。
- 若內建 Image2 不能實際傳 reference image，只能用 prompt 約束人物特徵；若人物不像本人，明確回報限制並重生或改用支援圖片參考的流程。

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
   - 若續跑中間檔，先建立 `_subtitles/`；`resegment.py` 不會自動建立輸出資料夾。
   - 輸出 `working/<video-id>/<video-id>.srt` 與 `.txt`。

4. **產標題並暫停**
   - 讀清字後 `.txt`。
   - 產生 10 個標題候選到 `working/<video-id>/titles.md`。
   - 回報標題清單，停下等使用者選編號。

5. **建立 Codex 輸出資料夾**
   - 清洗標題中的 Windows 不合法字元：`？！：／＼?!:/\\<>|"*`。
   - 建立 `output/<清洗後標題> [Codex]/`。
   - 檔案本身不要加 `[Codex]`。

6. **產封面**
   - 重新讀人物基準照與風格指南，不沿用舊封面。
   - Prompt 必含：
     - 人物特徵：短黑髮帶少量灰白、黑框矩形眼鏡、黑色長版防風連帽外套、黑色上衣、自然微笑、教師氣質。
     - Codex 主色：亮藍 / 電子青，不要 Claude 橘色主光。
     - 科技教學風格：深海軍藍背景、資料流、電路、AI Agent、課程計畫表格。
   - 將內建 Image2 產出的最新圖片複製到輸出資料夾，命名 `cover.png`。

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
   - PowerShell 檢查含 `[Codex]` 的路徑時用 `-LiteralPath`。

9. **更新交班**
   - 更新 `HANDOFF.md`：完成項目、輸出位置、封面狀態、待審事項、下一步。

## 踩坑

- Codex 使用的 Python 可能不同於 Claude Code；缺 `auto-editor` 或其他套件時，安裝到目前 `python`。
- `auto-editor.exe` 不在 PATH 沒關係，只要 `python -m auto_editor` 可用。
- Groq transcription 會上傳音訊到第三方服務；若需要明確授權，先停下。
- 中文檔名、空白、`[Codex]` 路徑要用引號與 `-LiteralPath`。
