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
   - **這位口播者實測甜蜜點**：`--threshold 0.06 --margin "0sec,0.1sec"`（剪掉約 80%、節奏俐落、開頭不留靜音）。
   - 起始建議：先用實測甜蜜點跑一次，給使用者看 `cut.mp4` 確認節奏；太狠 → threshold 0.05、margin "0.2sec,0.2sec"；太鬆 → threshold 0.07。
   - 輸出 `working/<video-id>/<video-id>.cut.mp4`。
   - 跑完回報「原長 X:XX → 新長 X:XX（剪掉 X%）」。

3. **轉字幕**
   - **可直接餵 cut.mp4 給 `transcribe_groq.py`**（內部自動用 ffmpeg 處理），不需先抽音訊。檔案 < 25MB Groq 直接吃；> 25MB 會自動降取樣。
   - 讀 `skills/audio-to-srt/SKILL.md`。
   - 流程：transcribe_groq.py → resegment.py → apply_vocab.py → **Claude 親自逐段清字**（讀 vocab.srt，依規則修錯字、加標點、不動時間碼、段數不變）→ validate_srt.py → srt_to_txt.py。
   - **先建立 `_subtitles/` 子資料夾**，否則 `resegment.py` 會 `FileNotFoundError`。
   - **常見 Whisper 誤判**（清字時記得修）：
     - 「燭光國中 / 竹光國中」→「光武國中」
     - 「稅教材」→「數學教材」
     - 「AI-Aging / AI 阿真 / AI 安進」→「AI Agent」
     - 「租寫的範本」→「填寫的範本」
     - 「微填」→「微調」
     - 「半年段另存心」→「按年段另存新檔」
     - Cloud / Claude / Codex 易混（apply_vocab 已處理大部分）
   - 輸出 `working/<video-id>/<video-id>.srt` 與 `.txt`，並把 .srt 也複製出來方便 step 8 使用。

4. **產標題並暫停**
   - 讀清字後 `.txt`。
   - 產生 **10 個** 標題候選到 `working/<video-id>/titles.md`。
   - 標題策略要分組（讓使用者方便比較）：痛點/解放型、教學/Know-how 型、對比/反問型、具體/案例型 各 2–3 個。
   - 回報標題清單給使用者，**停下等使用者選編號**。不要自己挑、不要往下跑。

5. **建立 Claude 輸出資料夾**
   - 清洗標題中的 Windows 不合法字元：`？！：／＼?!:/\\<>|"*`。
   - 建立 `output/<清洗後標題> [Claude]/`。
   - 檔案本身不要加 `[Claude]`。

6. **產封面**
   - **生封面前 SOP（缺一不可、每次都要做）**：
     a. `Read assets/style/reference-thumbnails.png`（看頻道既有 12 張封面）
     b. `Read assets/style/cover-style.md`（讀完整風格指南）
     c. `Read assets/persona/三師爸人物形象照.png`（每次重新讀人物基準照；不可沿用舊封面）
     d. 依影片主角決定主色：Claude=橘 / Codex=藍 / 兩者並用=橘+藍
   - Claude 版主色固定：`#FF8C42`、`#FFA500`、`#FF6B35`
   - **Prompt 範本**（已實測有效，依影片內容微調）：
     ```
     YouTube 封面 16:9，三師爸頻道科技教學風格。本支影片主角為 {AI_NAME}，採用{COLOR}主題配色。

     背景：深海軍藍 (#0A1628) 漸層底，左下與右上有 {THEME_LIGHT_COLOR} 放射光線與粒子特效，細微網格紋理，整體科技未來感、強烈呼喚點擊感。

     人物：畫面右側放置這位男性教師（戴眼鏡、黑色連帽外套），姿勢為{POSE}，臉部表情自信微笑，看向鏡頭。{COLOR} rim light 打在邊緣輪廓。人物樣貌、五官、髮型、外套、眼鏡全部延續輸入的人物基準照，不要更動。

     主視覺（左側中下方）：{TOPIC_VISUAL}。電腦周圍有發光暈。

     文字（左半邊）：
     - 集數標籤（左上）：『{SERIES_LABEL}』白色細字
     - 主標題（左中央）：『{TITLE_LINE_1}\\n{TITLE_LINE_2}』兩行排列，亮黃色 (#FFD700) 超粗黑體中文字，粗黑色描邊 5px，佔畫面寬度約 45%
     - 副標題（主標下方）：『{SUBTITLE}』白色細字，搭配兩側裝飾橫線

     整體：高對比、教學頻道氣口、適合教師受眾。
     不要：純白底、自然風景、寫實生活感、3D 浮雕字。
     ```
   - 標準呼叫：
     ```powershell
     python skills\cover-image\draw.py "<prompt>" --edit "assets\persona\三師爸人物形象照.png" --size 1536x1024 --quality low --name cover --outdir "output\<標題> [Claude]"
     ```
   - 跑完整理：刪掉時間戳檔名版本，留 `cover.png` 一份；用 Read 工具看一眼封面確認人物樣貌正確。

7. **寫 metadata**
   - `metadata.md` 必含**七個區塊**（缺一不可）：
     1. **YouTube 描述**：第一段 2–3 句講影片價值與目標受眾；列點寫影片重點（✅ 開頭）；補關鍵詞 hashtag。
     2. **章節時間碼**：建議性質，依字幕大致的段落切時間。
     3. **社群貼文**三種版本：Facebook（教師社群口吻、可長一點）、Instagram（短文+多 hashtag）、Threads（共鳴型短句）。
     4. **SEO 關鍵字**（markdown 列表版）：主關鍵字、次關鍵字、長尾關鍵字、競品搜尋詞。
     5. **YouTube 標籤欄位（直接複製）**：把 4 組關鍵字各做一份「半形逗號分隔」純文字版本，外加一份「**全部一次貼**」整合版（這是使用者實際會貼到 YouTube 後台的那一段）。
     6. **上架前 checklist**：標題、封面、字幕、描述前 100 字含主關鍵字、章節時間碼確認、標籤、播放清單、社群同步發佈。
   - 第一段描述要呼應使用者選定的標題情緒（痛點型 / 教學型 / 對比型）。

8. **打包與自我檢查**
   - 輸出資料夾應包含 **5 個檔案**（檔名不加 `[Claude]` 後綴）：
     - `<標題>.mp4`（從 working/ 複製過來改名）
     - `<標題>.srt`
     - `<標題>.txt`
     - `cover.png`
     - `metadata.md`
   - **自我檢查清單**（跑完後逐項確認）：
     - [ ] 資料夾名結尾有 ` [Claude]` 後綴
     - [ ] 資料夾內 5 個檔案齊全
     - [ ] 影片檔名等於 YouTube 標題（不含後綴）
     - [ ] cover.png 可開啟、人物樣貌延續基準照（用 Read 看一眼）
     - [ ] cover.png 主色為橘色（不是藍色）
     - [ ] metadata.md 含「全部一次貼」整合版標籤段
     - [ ] HANDOFF.md 已更新本支影片狀態
   - **PowerShell 提醒**：路徑含 `[Claude]` 時 PowerShell 會把中括號當 wildcard，用 `-LiteralPath` 或加單引號。Bash 沒這問題。

9. **更新交班**
   - 更新 `HANDOFF.md`：完成項目、輸出位置、封面狀態、待審事項、下一步。

## 踩坑

- `OPENAI_API_KEY` 不存在或帳號未驗證時，封面會失敗。檢查順序：環境變數 → `~/.openai.env`。Bash 載入：`export $(cat ~/.openai.env | xargs)`。
- `skills/cover-image/draw.py` 需要 `openai` Python 套件。
- gpt-image-2 需 OpenAI Individual 驗證；未驗證會吐 `403 Organization must be verified`。
- `auto-editor` 不在 PATH 沒關係，`smart_cut.py` 會自動 fallback 到 `python -m auto_editor`。
- Groq transcription 會上傳音訊到第三方服務；若內容敏感先停下問使用者。
- Groq 25MB 上限：`transcribe_groq.py` 內建 ffmpeg 自動降取樣到 16kHz mono 32kbps。
- `resegment.py` 不會自動建輸出資料夾，先 `mkdir _subtitles`。
- 中文檔名、空白、`[Claude]` 中括號路徑：PowerShell 用 `-LiteralPath` 或單引號；Bash 直接雙引號即可。
- 封面 prompt 矛盾（例如同時說人物穿藍色但基準照是黑色外套）→ gpt-image-2 會妥協；prompt 中只描述位置與場景，不要重新描述五官/穿著屬性。
- **每次封面都要重新讀基準照**，不能拿前一張封面當輸入；模型會放大誤差，越生越不像。

## 範例：本專案第一支影片的成果參數
讓你知道實測 OK 的參數長相：
- 影片：`你還在手動填課程計畫嗎 AI Agent 教師工作流實演`
- 原長 14:00 → smart-cut（threshold 0.06、margin "0sec,0.1sec"）→ 1:42（剪 88%）
- 字幕 37 段、530 字、總時長 1:41
- 標題候選 10 個，分四組策略，使用者選 #7
- 封面：橘色主題、左側 Claude AI 介面 + 紅 X 紙本、右側人物指向左方
- 完整成品：`output/你還在手動填課程計畫嗎 AI Agent 教師工作流實演 [Claude]/`
