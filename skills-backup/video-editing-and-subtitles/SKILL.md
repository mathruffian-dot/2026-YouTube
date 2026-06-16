---
name: video-editing-and-subtitles
description: 影片去靜音剪輯與字幕精修工作流。當使用者要求「剪影片」「上字幕」「剪去沒聲音片段」「做 SRT 字幕與純文字稿」但不需要生成完整 YouTube 描述/封面/標題候選時，請使用此技能。此技能提供了標準的去靜音、語音轉錄、詞彙自動替換、提取疑慮術語供確認、以及最終輸出打包的標準化流程。
---

# 影片去靜音剪輯與字幕精修工作流

本技能適用於精簡版的影片處理需求，旨在快速剪去靜音片段、轉錄精準字幕，並透過人工確認關鍵術語以交付最高品質的影片、SRT 字幕及純文字稿。

## 前置工具與環境
- **ffmpeg**：在 PATH 中。
- **auto-editor**：可執行 `python -m auto_editor`（版本 29+）。
- **Groq API Key**：設定於環境變數 `GROQ_API_KEY` 或存在於 `~/.groq_api_key`。
- **自訂 Python 腳本**（均位於 `skills/`）：
  - `skills/smart-cut/scripts/smart_cut.py`
  - `skills/audio-to-srt/scripts/transcribe_groq.py`
  - `skills/audio-to-srt/scripts/resegment.py`
  - `skills/audio-to-srt/scripts/apply_vocab.py`
  - `skills/audio-to-srt/scripts/validate_srt.py`
  - `skills/audio-to-srt/scripts/srt_to_txt.py`
  - `skills/video-editing-and-subtitles/scripts/find_dubious_terms.py`
  - `skills/video-editing-and-subtitles/scripts/finalize_subtitles.py`

---

## 標準化工作流程

### Step 1：建立工作區與複製影片
1. 決定內部影片代號，例如 `<video-id>` (如 `antigravity-ep06`)。
2. 建立目錄 `raw/<video-id>/` 及 `working/<video-id>/`。
3. 將原始影片複製為 `raw/<video-id>/原始.mp4`。

### Step 2：智慧去靜音剪口播 (smart-cut)
執行 auto-editor 進行無聲剪除：
```bash
python "skills/smart-cut/scripts/smart_cut.py" \
  "raw/<video-id>/原始.mp4" \
  --out "working/<video-id>/<video-id>.cut.mp4" \
  --threshold 0.05
```
*(可根據口播人聲停頓調整 threshold 門檻在 0.04 ~ 0.06 之間，margin 預設 0.2s)*

### Step 3：音訊擷取與語音轉錄 (audio-to-srt)
1. 從 cut 後的影片擷取 16kHz mono wav 音訊：
   ```bash
   ffmpeg -i "working/<video-id>/<video-id>.cut.mp4" -vn -ar 16000 "working/<video-id>/<video-id>.cut.wav" -y
   ```
2. 上傳 Groq Whisper 進行 STT（大檔會自動以低位元率壓縮上傳）：
   ```bash
   python "skills/audio-to-srt/scripts/transcribe_groq.py" \
     "working/<video-id>/<video-id>.cut.wav" \
     --out "working/<video-id>/_subtitles/<video-id>.groq.json"
   ```
3. 依 word-level 時間戳重新精細斷句：
   ```bash
   python "skills/audio-to-srt/scripts/resegment.py" \
     "working/<video-id>/_subtitles/<video-id>.groq.json" \
     --out "working/<video-id>/_subtitles/<video-id>.raw.srt"
   ```
4. 機械式套用基礎詞彙替換：
   ```bash
   python "skills/audio-to-srt/scripts/apply_vocab.py" \
     "working/<video-id>/_subtitles/<video-id>.raw.srt" \
     --out "working/<video-id>/_subtitles/<video-id>.vocab.srt"
   ```

### Step 4：疑慮術語擷取與人工勘誤 (核心要求)
1. 執行篩選腳本，提取關鍵字（如 `Antigravity`、`Claude`、`Gemini`、`Gems`、`clasp` 等）以及常見音譯錯字的片段：
   ```bash
   python "skills/video-editing-and-subtitles/scripts/find_dubious_terms.py" \
     "working/<video-id>/_subtitles/<video-id>.vocab.srt" \
     --out "working/<video-id>/_subtitles/dubious_terms.md"
   ```
2. **與使用者核對**：讀取生成的 `dubious_terms.md`，將有疑慮的段落列在對話中，詢問使用者如何修正。
3. **套用使用者更正**：執行 `finalize_subtitles.py` 套用自訂更正規則（多個更正可多次指定 `--replace` 參數，亦支援特定段落更正如 `390:AGE->Agent`）：
   ```bash
   python "skills/video-editing-and-subtitles/scripts/finalize_subtitles.py" \
     "working/<video-id>/_subtitles/<video-id>.vocab.srt" \
     --out "working/<video-id>/_subtitles/<video-id>.clean.srt" \
     --replace "舊字->新字" \
     --replace "段號:特定舊字->新字"
   ```

### Step 5：驗證與打包輸出
1. 執行時間碼格式驗證：
   ```bash
   python "skills/audio-to-srt/scripts/validate_srt.py" \
     --raw "working/<video-id>/_subtitles/<video-id>.vocab.srt" \
     --clean "working/<video-id>/_subtitles/<video-id>.clean.srt"
   ```
2. 產生字幕純文字稿：
   ```bash
   python "skills/audio-to-srt/scripts/srt_to_txt.py" \
     "working/<video-id>/_subtitles/<video-id>.clean.srt" \
     --out "working/<video-id>/<video-id>.txt"
   ```
3. 建立輸出目錄：`output/<影片標題> [<AgentName>]/` (AgentName 可為 `Codex` 或 `Claude`)。
4. 將成品複製更名至輸出目錄：
   - 影片：`output/<標題> [<AgentName>]/<標題>.mp4`
   - 字幕：`output/<標題> [<AgentName>]/<標題>.srt`
   - 文字：`output/<標題> [<AgentName>]/<標題>.txt`

---

## 踩坑與注意事項
- **路徑中括號處理**：PowerShell 對於包含中括號（如 `[Codex]`）的路徑很敏感，執行檔案操作指令時，建議一律加上引號並使用 `-LiteralPath` 參數。
- **特定段落更正**：如果某個詞彙（如 `Gem` ➡️ `Gems`）在大部分情況需要修正，但在某些特定上下文（如 `Gemini`）不可動，請使用段落前綴限定替換範圍，例如 `390:AGE->Agent`。
