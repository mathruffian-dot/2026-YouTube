---
name: codex-youtube-video-workflow
description: Codex 專用的 2026Youtube 總控工作流 Skill。當使用者要求 Codex 處理 raw 裡的新影片、一次跑完整 YouTube 生產線（剪口播→轉字幕→清字確認→長片打包→短片精華→雙格式行銷資訊）、剪口播、轉字幕、產標題、用內建 Image2 產封面、寫 metadata、剪 short、打包 output，或說「使用 codex-youtube-video-workflow」時使用。此 Skill 明確使用 Codex 內建生圖能力，不呼叫 Claude 的 cover-image/draw.py。
---

# codex-youtube-video-workflow：Codex 版 YouTube 生產總控

## 一條龍總覽（長片 → 短片 → 雙格式資訊）

本 Skill 一次完成三大階段，中間有 **3 個 STOP 關卡**，每關都必須**停下等使用者拍板，不准自動往下衝**：

```
階段 1 長片：剪口播 → 轉字幕 → 🛑STOP1 疑慮字幕確認 → 時間碼硬關卡 → 標題 → 封面 → 長片 metadata → 打包
階段 2 短片：讀完整字幕 → 亮點偵測 → 🛑STOP2 三候選確認 → 切片組片 → 短片 metadata → 打包
（標題候選為 🛑STOP3，已含在各階段內）
```

- **🛑 STOP 1**（階段 1 step 3）：疑慮術語列出來等使用者勘誤，套完才往下。
- **🛑 STOP 2**（階段 2）：短片 3 候選版本等使用者選編號。
- **🛑 STOP 3**（step 4 / 短片 step）：標題候選等使用者選。
- **硬關卡**：`validate_srt.py` 不通過（段數不一致 / 時間碼對不上）→ **中止交付並回報**，不得硬出。
- **防斷字**：字幕切句靠 `resegment.py` 切點優先序；短片切片一律對齊字幕段落邊界，**不准切到一句話中間**。

> 短片階段非必跑：使用者沒要短片就停在階段 1 收尾。要短片才接階段 2。

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
   - 流程：Groq transcription → resegment → apply_vocab → 親自逐段清字（不動時間碼、段數不變）→ **🛑 STOP 1 疑慮術語確認**（見下）→ validate_srt【硬關卡】→ srt_to_txt。
   - 若續跑中間檔，先建立 `_subtitles/`；`resegment.py` 不會自動建立輸出資料夾。
   - **🛑 STOP 1：疑慮術語確認（不准跳過）**
     1. 跑 `python skills/video-editing-and-subtitles/scripts/find_dubious_terms.py "working/<video-id>/_subtitles/<video-id>.vocab.srt" --out "working/<video-id>/_subtitles/dubious_terms.md"`，撈出專有名詞與常見音譯錯字段落。
     2. **讀 `dubious_terms.md`，把有疑慮的段落列在對話中，停下問使用者怎麼改**，不要自己猜了就往下。
     3. 使用者回覆後用 `python skills/video-editing-and-subtitles/scripts/finalize_subtitles.py "<vocab.srt>" --out "<clean.srt>" --replace "舊->新" --replace "段號:舊->新"` 套更正（特定段落限定用 `390:AGE->Agent` 格式）。
   - **時間碼硬關卡**：`validate_srt.py --raw <vocab.srt> --clean <clean.srt>` 若段數不一致或時間碼對不上 → **中止，回報差異，不得交付**。
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

7. **寫 metadata（依行銷規格）**
   - **先 Read `references/marketing-spec.md`**（txt v1.5 主規格 + 頻道補充欄位的兩套合併版），一律以它為準。
   - 吃**清字後 `.txt` 逐字稿**生成，素材要呼應字幕真實內容。長片 `metadata.md` 至少含：
     1. **10 個標題候選**（好奇/價值/痛點三風格穿插）
     2. **影片描述 ≤300 字**：Hook + 3 個關鍵知識點列點 + CTA；第一段情緒呼應使用者選定的標題類型。
     3. **社群貼文**（FB / IG / Threads）：**嚴禁 Emoji**、每段 ≤3 行、長片 150–200 字、誠摯老師口吻、結尾留互動問題。
     4. **SEO 關鍵字 15–20 個** + **「全部一次貼」整合版標籤**（半形逗號分隔）。
     5. **章節時間碼**（依字幕段落，建議性質）。
     6. **上架前 checklist**。
   - 細節格式與短片覆寫規則完全以 `references/marketing-spec.md` 為準。

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

## 階段 2：短片精華（要短片才跑）

長片跑完（已有 `cut.mp4` + `clean.srt`）後，若使用者要短片，**接手 `skills/short-video-workflow/SKILL.md` 完整流程**。重點關卡：

1. **強制完整讀 `working/<video-id>/<video-id>.srt`**：擷取精華前一定先看過整份字幕、理解時間碼，不准只看片段就抓。
2. **亮點偵測**：依痛點/反問/數字承諾/強斷言/轉折揭密等檢核表給每段 0–3 分。
3. **🛑 STOP 2：三候選版本確認**
   - 組 3 個版本（A 痛點型 / B 好奇型 / C 承諾型 hook），每版三幕結構、≤120s、寫進 `working/<video-id>/shorts-candidates.md`。
   - **列三版時間碼與三幕劇本給使用者，停下等使用者選 A/B/C**（或使用者自給時間碼）。不准自己挑。
4. **切片組片**：`clip_cut.py` 切片（**對齊字幕段落邊界，不切到一句話中間**）→ 確認 ≤120s → `add_end_card.py` 結尾字卡 → `burn_subtitles.py` 燒字幕。
5. **短片標題（🛑 STOP 3）**：出 3 個更短更聳動的候選等使用者選。
6. **短片 metadata**：同樣 **Read `references/marketing-spec.md`**，套用其中「C. 短片差異」覆寫（標題 3 個、描述 ≤150 字、`#Shorts` 必備、標籤結尾加 `Shorts,短影片`）。

規格：16:9、≤120s、主色 Codex 亮藍 / 電子青、輸出 `output/<短片標題> [Codex] (Short)/`，封面用 Codex 內建 Image2、不呼叫 draw.py。

## 踩坑

- Codex 使用的 Python 可能不同於 Claude Code；缺 `auto-editor` 或其他套件時，安裝到目前 `python`。
- `auto-editor.exe` 不在 PATH 沒關係，只要 `python -m auto_editor` 可用。
- Groq transcription 會上傳音訊到第三方服務；若需要明確授權，先停下。
- 中文檔名、空白、`[Codex]` 路徑要用引號與 `-LiteralPath`。
