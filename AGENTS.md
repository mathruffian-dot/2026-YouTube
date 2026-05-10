# AGENTS.md — 給 Codex 的工作指南

> 這份檔案是 **OpenAI Codex** 在本專案的入口。Claude Code 讀的是 `CLAUDE.md`，內容與本檔對齊。
>
> **⚠️ 拿到此 repo 的新使用者**：先讀 `SETUP.md`，依「個人化清單」改完該改的（人物照、API key、頻道風格、HANDOFF.md），再開始用。

## 你是誰
你是 **OpenAI Codex**，與 **Claude Code** 在本專案接力完成 YouTube 影片自動化生產線。

## 開工前必讀
1. **`HANDOFF.md`** — 上一個 AI（可能是你自己上次、也可能是 Claude）留下的交班紀錄。**先讀這個**。
2. **`CLAUDE.md`** — 完整專案脈絡（與本檔對齊，但更詳細）。
3. **`README.md`** — 對人的快速說明。

## 專案目標
使用者把原始影片丟進 `raw/`，AI 接力完成：
1. **智能剪口播** → 去靜音
2. **語音轉字幕** → SRT + 純文字稿
3. **生 10 個吸引人的標題候選**，等使用者挑一個
4. 使用者選定後 → **以標題建資料夾**，平行產出封面、描述、社群貼文、SEO

最終交付到 `output/<YouTube 標題>/`：剪好的影片、SRT、txt、封面、metadata.md。

## 你可以使用的 Skills
本專案 `skills/` 目錄存放共用 Skill，讀 `SKILL.md` 即可使用。
這些 Skill 由 `scripts/sync-skills.ps1` 從全域同步而來；專案特殊規範（如封面人物基準）只寫在本檔與 CLAUDE.md，不會在 SKILL.md 裡。

| Skill | 路徑 | 用途 |
|-------|------|------|
| Codex 總控工作流 | `skills/codex-youtube-video-workflow/SKILL.md` | Codex 專用，串接剪片、字幕、標題、內建 Image2 封面、metadata、打包 |
| 智能剪口播 | `skills/smart-cut/SKILL.md` | auto-editor 去靜音 |
| 語音轉字幕 | `skills/audio-to-srt/SKILL.md` | 音訊 → SRT（先剪片再轉字幕，時間碼才對齊） |
| 封面圖生成 | （見下方備註）| **使用你內建的 image 2 生圖工具**，不要呼叫 `skills/cover-image/draw.py`（那是給 Claude Code 用的）|

Codex 總控 Skill 另有備份副本：`skills-backup/codex-youtube-video-workflow/`。Claude Code 的總控 Skill 另在 `skills/claude-youtube-video-workflow/`，不要混用。

### 封面生成（Codex 專用方式）
你內建 image 2 生圖功能，**直接用內建工具產封面**，不需要 OpenAI API Key、不要跑 draw.py。
但風格規範與人物基準照仍須遵守：
- 把 `assets/persona/三師爸人物形象照.png` 當作人物基準傳給內建工具（如果內建工具支援 reference image）
- **每一次封面都必須重新參考 `assets/persona/三師爸人物形象照.png`；不得從上一張已生成封面或任何衍生圖片延續人物。**
- prompt 依 `assets/style/cover-style.md` 風格指南撰寫
- 主色依影片主角決定（Claude=橘 / Codex=藍 / 兩者並用=橘+藍）
- 輸出存到 `output/<標題>/cover.png`

## 標準工作流
1. `raw/<影片代號>/原始.mp4` 進來
2. 在 `working/<影片代號>/` 開工作空間
3. 跑 `smart-cut` → `<影片代號>.cut.mp4`
4. ffmpeg 抽音訊 → 跑 `audio-to-srt` → `.srt` + `.txt`
5. 讀字幕生 10 個標題 → `working/<影片代號>/titles.md`，**停下等使用者挑**
6. 使用者挑完 → 把標題清洗成合法資料夾名（去除 `？！：／＼?!:/\\<>|"*`）→ 建 `output/<標題> [Codex]/`（你是 Codex，必加 `[Codex]` 後綴；資料夾內檔案不加後綴）
7. 平行：
   - **封面 SOP**（缺一不可）：
     a. `Read assets/style/reference-thumbnails.png`（看頻道既有封面）
     b. `Read assets/style/cover-style.md`（讀完整風格指南）
     c. `Read assets/persona/三師爸人物形象照.png`（每次重新讀人物基準照；不可沿用舊封面）
     d. 依影片主角決定主色：Claude=橘 / Codex=藍 / 兩者並用=橘+藍
     e. 撰寫 prompt → **用你內建的 image 2 生圖工具**產封面（人物基準照當 reference image），存到 `output/<標題> [Codex]/cover.png`
   - AI 寫 metadata.md（描述 / 社群 / SEO，**SEO 區塊必含「YouTube 標籤欄位（直接複製）」逗號分隔版**）
8. 把 .cut.mp4、.srt、.txt、封面、metadata 全搬進 `output/<標題> [Codex]/`，影片改名為 `<標題>.mp4`
9. 更新 `HANDOFF.md`

## 資料夾結構
```
raw/         # 使用者素材
working/     # 中間產物
output/
  thumbnails/  # 封面
  metadata/    # 文案
  final/       # 成品影片
projects/<影片代號>/  # 每支影片的工作空間
skills/      # 共用 Skill
```

## 工作風格
- 繁體中文回應、繁體中文 commit 訊息
- 修改前先確認計畫
- **大檔案不要進 git**（影片、模型權重）
- API Key 從使用者家目錄讀（`~/.groq_api_key`、`OPENAI_API_KEY`），不准寫進 repo

## 收工前必做
更新 `HANDOFF.md`：
- 我做了什麼
- 目前在哪一步
- 下一個 AI 接手時要做什麼
- 有沒有踩到坑、有沒有待解問題

## 同步機制
- Google Drive 自動同步檔案
- GitHub 是版本備份：`mathruffian-dot/2026-YouTube`
- Obsidian 對應筆記：`2026Youtube/工作筆記.md`（給人讀的）
