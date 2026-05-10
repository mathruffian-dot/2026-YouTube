# 2026Youtube — YouTube 影片自動化工作流

> **⚠️ 拿到此 repo 的新使用者**：先讀 `SETUP.md`，依「個人化清單」改完該改的（人物照、API key、頻道風格、HANDOFF.md），再開始用。下面這份 CLAUDE.md 寫的是工作框架，個別內容（如「光武國中」「翰林版本」「三師爸」）是 mathruffian 的範例。

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
    ├── cover-image/    # 封面圖生成（OpenAI gpt-image-2）
    ├── codex-youtube-video-workflow/  # Codex 專用總控工作流
    └── claude-youtube-video-workflow/ # Claude Code 專用總控工作流
```

## 封面規範（兩條線必讀）

### 1. 人物基準照
**所有 YouTube 封面必須使用 `assets/persona/三師爸人物形象照.png` 作為人物基準。**
呼叫 `cover-image` Skill 時帶 `--edit assets/persona/三師爸人物形象照.png` 參數。
gpt-image-2 在 edit 模式下會延續人物的臉、髮型、體型、穿著（黑色連帽外套、眼鏡）。
**每一次封面都必須重新讀取並使用這張人物基準照；不得從上一張已生成封面或任何衍生圖片延續人物。**

### 2. 視覺風格指南
**生封面前的 SOP（缺一不可）：**
1. `Read assets/style/reference-thumbnails.png` — 用 Read 工具看頻道既有 12 張封面參考圖
2. `Read assets/style/cover-style.md` — 讀完整風格指南（色票、構圖、主題配色規則、prompt 範本）
3. `Read assets/persona/三師爸人物形象照.png` — 每次重新讀人物基準照，不可沿用舊封面
4. 依影片主角決定主色：**Claude=橘 / Codex=藍 / 兩者並用=橘+藍**
5. 撰寫 prompt 後再呼叫 `cover-image` Skill

> 規則衝突時的優先序：人物基準照 > 風格指南 > 個別影片 prompt 變化

## Skills 使用須知
`skills/` 內存放本專案專用 Skill。Codex 與 Claude Code 的總控 Skill 分開維護，因為封面生成方式、API Key、輸出標籤與人物參考限制不同。

| Skill | 路徑 | 觸發時機 |
|-------|------|---------|
| Claude 總控工作流 | `skills/claude-youtube-video-workflow/SKILL.md` | Claude Code 要一次跑完整 YouTube 生產線 |
| Codex 總控工作流 | `skills/codex-youtube-video-workflow/SKILL.md` | Codex 要一次跑完整 YouTube 生產線（不要給 Claude 混用） |
| 智能剪口播 | `skills/smart-cut/SKILL.md` | 原始影片 → 去靜音後的影片 |
| 語音轉字幕 | `skills/audio-to-srt/SKILL.md` | 剪好的影片/音訊 → SRT |
| 封面圖生成 | `skills/cover-image/SKILL.md` | 需要 YouTube 封面、社群圖 |

`skills-backup/` 另存 Codex / Claude 兩份總控 Skill，方便複製到其他專案或全域 skills。

> Claude Code 端：`audio-to-srt` 與 `cover-image` 仍以全域 `~/.claude/skills/` 為主，本資料夾的副本是給 Codex 讀的「離線版」。`smart-cut` 是專案原生 Skill。
>
> **同步全域 Skill → 專案副本**：跑 `./scripts/sync-skills.ps1`（dry-run）或加 `-Apply` 真的同步。
> **重要政策**：`skills/*/SKILL.md` 會被 sync 覆蓋。專案特殊規範（例如人物基準）只能寫在 `CLAUDE.md` / `AGENTS.md`，不要塞進 SKILL.md。

## 標準工作流（每支影片）

> **資料夾命名規則**：所有以 YouTube 標題命名的資料夾，需把 `？！：／＼?!:/\\<>|"*` 等不能當路徑名的字元去除或以全形等價字元替換。
>
> **AI Agent 標籤**：產出資料夾名稱結尾必須加 ` [Claude]` 或 ` [Codex]`（**Claude Code 用 `[Claude]`、OpenAI Codex 用 `[Codex]`**），方便 A/B 比較兩個 Agent 的差異。
> 範例：`output/你還在手動填課程計畫嗎 AI Agent 教師工作流實演 [Claude]/`

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
   - 把標題清洗成合法資料夾名 → 建 `output/<標題> [Claude]/`（你是 Claude Code，必加 `[Claude]` 後綴）
   - **平行**產出：
     - 觸發 `cover-image` Skill 生封面（**必帶 `--edit assets/persona/三師爸人物形象照.png`**，用標題當素材）→ `output/<標題>/cover.png`
       > Codex 端不走此路，改用 Codex 內建 image 2 工具直接產出（細節見 `AGENTS.md`）
     - AI 寫 YouTube 影片描述 → 寫進 `metadata.md`
     - AI 寫社群貼文（FB / IG / Threads 各一）→ 寫進 `metadata.md`
     - AI 列 SEO 關鍵字 → 寫進 `metadata.md`，**且必含「YouTube 標籤欄位（直接複製）」段落**：把主關鍵字、次關鍵字、長尾關鍵字、競品搜尋詞各做一份「半形逗號分隔」的純文字版本，外加一份「全部一次貼」版本，方便使用者直接複製到 YouTube 後台
8. **打包**：把以下檔案搬到 `output/<標題> [Claude]/`（內部檔案不加後綴，只有資料夾加）
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
