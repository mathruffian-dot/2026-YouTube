# 2026Youtube — YouTube 影片自動化工作流

## 專案簡介
本專案是一條 **YouTube 影片自動化生產線**。使用者把原始影片素材丟進 `raw/`，AI 代理人接力完成：
1. **智能剪口播**（auto-editor 去靜音 → 純人聲版本）
2. **語音轉字幕**（Groq Whisper → SRT + 純文字稿）
3. **生 10 個吸引人的標題** → 使用者挑一個
4. **以選定標題建資料夾，平行產出**：封面圖（gpt-image-2）、YouTube 描述、社群貼文、SEO 關鍵字
5. **打包交付**：剪好的影片、字幕、純文字、封面、文案 一份齊全

最終交付：`output/<YouTube 標題>/` 內含完整素材包。

## 雙 AI 接力工作機制
本專案會由兩個 AI 代理人協作，**Claude Code** 與 **OpenAI Codex** 接力工作。

- **Claude Code** 讀 `CLAUDE.md`（本檔）
- **Codex** 讀 `AGENTS.md`（與本檔內容對齊，給 Codex 看的版本）
- **共同交班檯**：`HANDOFF.md` —— 每次工作結束前必須更新「目前狀態 / 下一步」，下一個 AI 接手時先讀此檔

> 規則：**不要假設另一個 AI 知道你做了什麼。** 寫得像給陌生人看。

## 關鍵時程
- 無固定截止日期，依實際素材到位節奏推進

## 語言與風格
- 所有回應、文件、commit 訊息皆使用**繁體中文**
- 修改前先確認計畫，優先保留原有資料結構

## 資料夾結構
```
2026Youtube/
├── CLAUDE.md           # 本檔（Claude Code 讀）
├── AGENTS.md           # Codex 讀（與本檔對齊）
├── HANDOFF.md          # 雙 AI 共同交班檯
├── README.md           # 對人的快速說明
├── .gitignore
├── raw/                # 使用者上傳的原始影片素材
├── working/            # 中間產物（SRT、剪輯草稿）
├── output/
│   ├── thumbnails/     # 封面圖
│   ├── metadata/       # 描述 / 社群貼文 / SEO / 標題候選
│   └── final/          # 最終交付的成品影片
├── projects/           # 一支影片開一個子資料夾，便於管理
├── assets/             # 跨影片共用素材
│   └── persona/        # 人物形象基準照（封面強制使用）
│       └── 三師爸人物形象照.png
└── skills/             # 共用 Skill（Claude / Codex 皆可讀取）
    ├── smart-cut/      # 智能剪口播（auto-editor）
    ├── audio-to-srt/   # 語音轉字幕（Groq Whisper-large-v3-turbo）
    └── cover-image/    # 封面圖生成（OpenAI gpt-image-2）
```

## 封面人物基準照（重要規範）
**所有 YouTube 封面必須使用 `assets/persona/三師爸人物形象照.png` 作為人物基準。**

實作方式：呼叫 `cover-image` Skill 時帶 `--edit assets/persona/三師爸人物形象照.png` 參數。gpt-image-2 在 edit 模式下會延續人物的臉、髮型、體型、穿著（黑色連帽外套、眼鏡）。

prompt 撰寫要點：
- 在描述中說明「畫面右側放置這位男性教師（戴眼鏡、黑色連帽外套）」之類的位置語意
- **不要**改變人物五官、外套顏色、眼鏡（gpt-image-2 在 edit 模式下會盡量保留，但 prompt 矛盾會破功）
- 場景、背景、配色、文字標題都可以自由設計

## Skills 使用須知
`skills/` 內的三個 Skill 是給本專案專用的副本（其中兩個複製自全域 Skill），目的是讓 Codex 也能在同一專案內讀到它們的 `SKILL.md` 與腳本。

| Skill | 路徑 | 觸發時機 |
|-------|------|---------|
| 智能剪口播 | `skills/smart-cut/SKILL.md` | 原始影片 → 去靜音後的影片 |
| 語音轉字幕 | `skills/audio-to-srt/SKILL.md` | 剪好的影片/音訊 → SRT |
| 封面圖生成 | `skills/cover-image/SKILL.md` | 需要 YouTube 封面、社群圖 |

> Claude Code 端：`audio-to-srt` 與 `cover-image` 仍以全域 `~/.claude/skills/` 為主，本資料夾的副本是給 Codex 讀的「離線版」。`smart-cut` 是專案原生 Skill。若全域 Skill 有更新，請同步更新本資料夾的副本。

## 標準工作流（每支影片）

> **資料夾命名規則**：所有以 YouTube 標題命名的資料夾，需把 `？！：／＼?!:/\\<>|"*` 等不能當路徑名的字元去除或以全形等價字元替換。

1. **收件**：使用者把素材丟進 `raw/<影片代號>/`（影片代號是暫時的工作識別，可以隨便取，例如日期+主題）
2. **建工作空間**：在 `working/<影片代號>/` 建子資料夾
3. **智能剪口播** → 觸發 `smart-cut` Skill
   - 輸入：`raw/<影片代號>/原始.mp4`
   - 輸出：`working/<影片代號>/<影片代號>.cut.mp4`
4. **抽音訊**：`ffmpeg -i .cut.mp4 -vn -ar 16000 -ac 1 .cut.wav`
5. **語音轉字幕** → 觸發 `audio-to-srt` Skill
   - 輸入：剪好的音訊
   - 輸出：`working/<影片代號>/<影片代號>.srt` + `.txt`
6. **生 10 個標題候選** → AI 讀字幕、生 10 個吸引人的標題 → 寫到 `working/<影片代號>/titles.md`，**等使用者挑一個**
7. **使用者選定標題後**：
   - 把標題清洗成合法資料夾名 → 建 `output/<標題>/`
   - **平行**產出：
     - 觸發 `cover-image` Skill 生封面（**必帶 `--edit assets/persona/三師爸人物形象照.png`**，用標題當素材）→ `output/<標題>/cover.png`
     - AI 寫 YouTube 影片描述 → 寫進 `metadata.md`
     - AI 寫社群貼文（FB / IG / Threads 各一）→ 寫進 `metadata.md`
     - AI 列 SEO 關鍵字 → 寫進 `metadata.md`
8. **打包**：把以下檔案搬到 `output/<標題>/`
   - `<標題>.mp4`（剪好的影片，從 working 複製過來改名）
   - `<標題>.srt`（字幕）
   - `<標題>.txt`（純文字稿）
   - `cover.png`（封面）
   - `metadata.md`（描述 + 社群 + SEO）
   - 其他相關素材
9. **更新 `HANDOFF.md`**：標註本支影片狀態（草稿 / 待審 / 完成）

## Obsidian 關聯資料
- `2026Youtube/工作筆記.md` — 第二大腦中的對應筆記，存進度與點子

## 三處同步指引
| 平台 | 路徑 / 位置 | 用途 |
|------|-------------|------|
| Google Drive | `G:\我的雲端硬碟\2026Youtube\` | 主要工作目錄，Claude Code / Codex 直接讀寫 |
| Obsidian | `2026Youtube/` | 第二大腦，存創意點子與工作筆記 |
| GitHub | `mathruffian-dot/2026-YouTube` | 版本控制與備份（私有） |

## 工作注意事項
- 此資料夾位於 Google 雲端硬碟，跨裝置自動同步
- 影片原始檔可能很大，預設**不**進 git（見 `.gitignore`）
- 每次工作前後都要更新 `HANDOFF.md`
- API Key（Groq、OpenAI）放在使用者家目錄，**不**進 repo

## 最近更動紀錄
| 日期 | 變更摘要 | GDrive | Obsidian | GitHub |
|------|----------|--------|----------|--------|
| 2026-05-10 | 專案初始化、建立雙 AI 接力框架、複製兩個 Skill | ✅ | ✅ | ✅ |
