# HANDOFF — 雙 AI 接力交班檯

> **每次工作前**先讀本檔最上面的「目前狀態」。**每次工作結束前**更新「目前狀態」與「下一步」。
> 寫的時候假設下一個接手者是陌生人。

---

## 目前狀態（最新）
- **更新時間**：2026-05-10
- **最後操作者**：Claude Code（Opus 4.7）
- **進度**：第一支影片完成全流程
  - 影片：`你還在手動填課程計畫嗎 AI Agent 教師工作流實演`
  - 原始 14:00 → smart-cut（threshold 0.06、margin 0/0.1s）→ 1:42
  - audio-to-srt 完成清字（37 段、530 字）
  - 標題候選 10 個 → 使用者選 #7
  - 封面（gpt-image-2 low）+ metadata.md 全部產出
  - 全部素材在 `output/你還在手動填課程計畫嗎 AI Agent 教師工作流實演 [Claude]/`
- **環境驗證紀錄**：
  - ffmpeg ✅、Groq Key（`~/.groq_api_key`）✅
  - OpenAI Key 存放於 `~/.openai.env`，呼叫前用 `export $(cat ~/.openai.env | xargs)` 載入
  - auto-editor CLI 不在 PATH，smart_cut.py 已自動 fallback 到 `python -m auto_editor`
- **Codex 複測紀錄（2026-05-10）**：
  - ffmpeg ✅、Groq Key 檔 ✅、OpenAI env 檔 ✅、`scripts/sync-skills.ps1` dry-run ✅
  - Codex 目前使用 `C:\Python314\python.exe`；已安裝 `auto-editor 29.3.1` 到使用者 Python 套件目錄，`python -m auto_editor` ✅
  - smart-cut ✅（測試輸出：`working/codex-flow-test/sample.cut.mp4`）
  - 字幕後處理本機鏈路 ✅：抽音訊、resegment、apply_vocab、validate_srt、srt_to_txt
  - 已完成 Codex 版標題 #3：「老師必看：用 AI Agent 自動填好年度課程計畫」
  - Codex 版完整輸出在 `output/老師必看 AI Agent 自動填好年度課程計畫 [Codex]/`，含影片、SRT、txt、metadata.md、內建 Image2 產出的亮藍 Codex 版 `cover.png`
  - 封面已重新生成，要求人物重新參考 `assets/persona/三師爸人物形象照.png`；目前內建 Image2 若無 reference image 欄位，只能用 prompt 約束人物特徵，若臉不像本人需改用支援圖片參考/編輯的流程
  - 總控 Skill 已拆分：Codex 用 `skills/codex-youtube-video-workflow/`，Claude Code 用 `skills/claude-youtube-video-workflow/`；備份在 `skills-backup/`
  - 測試產物在 `working/codex-flow-test/`（被 `.gitignore` 忽略）

## 下一步（給下一個 AI）
- 第一支影片**還沒上架 YouTube**，使用者可能會回來確認封面、文案要不要再改
- 等下一支影片素材丟進 `raw/`

## 已知議題 / 待解問題
- 封面 png 是 1536x1024（3:2），YouTube 建議 1280x720（16:9）— 視覺上沒太大差，需要的話可以後處理裁切
- smart-cut 預設 threshold 0.04 對這位口播者太鬆，這支影片用 0.06 才剛好。下一支可以先試 0.05 找平衡。
- `auto-editor.exe` 安裝在 `C:\Users\mathr\AppData\Roaming\Python\Python314\Scripts`，該路徑不在 PATH；但 `smart_cut.py` 會走 `python -m auto_editor`，所以不影響 Codex 執行。
- `resegment.py` 不會自動建立輸出資料夾；新影片流程要先建立 `_subtitles/`，否則會 `FileNotFoundError`。
- PowerShell 操作含空白或 `[Claude]` / `[Codex]` 的路徑時要加引號；含中括號路徑建議用 `-LiteralPath`。

## 封面生成規範（2026-05-10 新增、傍晚 v3 補強）
**所有封面必須以 `assets/persona/三師爸人物形象照.png` 作為人物基準。**
呼叫 `cover-image` Skill 時帶 `--edit assets/persona/三師爸人物形象照.png`。
**每一次封面都必須重新讀取 / 參考這張人物形象照；不能從上一張已生成封面或任何衍生圖片延續人物。**

**生封面前 SOP**：
1. `Read assets/style/reference-thumbnails.png`（看頻道既有 12 張封面）
2. `Read assets/style/cover-style.md`（讀風格指南）
3. `Read assets/persona/三師爸人物形象照.png`（每次重新讀人物基準照，不可沿用舊封面）
4. 依影片主角決定主色：**Claude=橘 / Codex=藍 / 兩者並用=橘+藍**
5. 撰寫 prompt → 呼叫 cover-image Skill / Codex 內建 Image2

細節見 `CLAUDE.md` §「封面規範」與 `assets/style/cover-style.md`。

## 環境前置確認
| 項目 | 確認方式 | 備註 |
|------|---------|------|
| Groq API Key | `echo $GROQ_API_KEY` 或 `ls ~/.groq_api_key` | 給 audio-to-srt 用 |
| OpenAI API Key | `echo $OPENAI_API_KEY` | 給 cover-image 用 |
| ffmpeg | `ffmpeg -version` | 給音訊壓縮、剪輯用 |

---

## 交班歷史（新的寫在最上面）

### 2026-05-10（傍晚 v2）— 加入封面人物基準規範
- 使用者提供 `三師爸人物形象照.png`，搬到 `assets/persona/`
- 規範寫進 CLAUDE.md / AGENTS.md / skills/cover-image/SKILL.md：所有封面必帶 `--edit assets/persona/三師爸人物形象照.png`
- 第一支影片封面已重生，人物樣貌（眼鏡、黑外套、髮型）完美延續

### 2026-05-10（傍晚）— Claude Code 跑完第一支影片
- 全流程實證：smart-cut → audio-to-srt → 10 標題 → 使用者選 #7 → 封面 + metadata
- 學到：smart-cut 對停頓多的口播者要把 threshold 拉到 0.06；margin 用 `0sec,0.1sec` 開頭不留緩衝聽起來最俐落
- 學到：transcribe_groq.py 直接吃 mp4 沒問題（內部用 ffmpeg 處理）
- 交付路徑：`output/你還在手動填課程計畫嗎 AI Agent 教師工作流實演 [Claude]/`

### 2026-05-10（下午）— Claude Code 工作流定稿
- 新增第三個 Skill `smart-cut`（auto-editor 包裝）
- 改寫 CLAUDE.md / AGENTS.md 的「標準工作流」章節：剪口播 → 字幕 → 10 標題 → 選定後建資料夾 → 平行產封面/文案
- 確立 `output/<標題>/` 為單一交付資料夾的命名與打包規範

### 2026-05-10 — Claude Code 專案初始化
- 建立雙 AI 接力工作框架
- 複製兩個 Skill 進 `skills/`
- Git + GitHub + Obsidian 三處同步完成
