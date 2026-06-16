# HANDOFF — 雙 AI 接力交班檯

> **每次工作前**先讀本檔最上面的「目前狀態」。**每次工作結束前**更新「目前狀態」與「下一步」。
> 寫的時候假設下一個接手者是陌生人。

---

## 目前狀態（最新）
- **更新時間**：2026-06-15（深夜）
- **最後操作者**：Claude Code（Opus 4.8）
- **進度**：**AI Agent 基本功 EP01（用 Agent 學 Agent）長片＋短片全流程交付完成** ✅
  - 來源：`raw/aiagent-ep01/aiagent-ep01.mp4`（原長 75:20 / 2.44GB，來自使用者 Downloads；**VFR**）
  - **預防 VFR 黑畫面**：剪前先 ffprobe 確認 avg_frame_rate 非整數比 → 先轉 CFR（`-fps_mode cfr -r 30 -crf 18 -c:a copy`）再剪，全程驗證亮度正常
  - **GDrive 寫入坑（新）**：auto-editor 直接輸出到 GDrive 路徑時，檔案會在 smart_cut 報 OK 後消失（疑似 GDrive 同步脫水）。解法：輸出到本機 `C:\temp\`，再 `cp` 搬回專案。建議日後長片 smart-cut 一律輸出本機再搬回。
  - smart-cut（threshold 0.06、margin `0sec,0.1sec`）→ 48:48（剪 35.2%）
  - 轉字幕：Groq 11992 字 → resegment 1154 段 → apply_vocab → STOP1 使用者確認 8 處 → 套全部更正 → validate 硬關卡通過（1154 段全吻合）→ 刪 11 段抖內/喊名段重編號 → 最終 1143 段
  - **本集詞彙更正重點**（AI Agent 系列日後可沿用）：
    - Agent 家族：`A-GEN/Agin/Aging/AI Aging/AIH/AIA群/A群/agy/AIGEN` → **Agent / AI Agent**
    - 生成式：`生程式/真程式/真誠式/聖誠士/聖德斯/深層式/生存式/Sense4/CN4` → **生成式**
    - `Antigravity/Antigrity/Ntegraf2/MTGRAVIT2/agy/HGY` → **AntiGravity**；`Podex`→Codex、`Deepthic`→DeepSeek
    - 使用者拍板：GPT5.5/Gemini3.5/Fable **保留原文**；`充WL的服務員員`→充值；`破搓`→裹足不前；**抖內/觀眾名段落全刪**
  - 長片標題使用者選 #10：「一個 GitHub repo，複製我的整套 AI 工作流到你的 Agent」
  - 長片交付：`output/一個 GitHub repo，複製我的整套 AI 工作流到你的 Agent [Claude]/`（5 檔齊全；封面橘色、GitHub repo 複製 Agent 大軍主視覺）
  - **短片也已交付** ✅（A 痛點型，67.5s＋3s 字卡＝70.5s）：
    - 標題：「AI Agent 就是你的第二大腦」
    - 精華組合（3 段）：00:13:27.9-00:14:04.9 切換工具痛點 → 00:14:40.9-00:15:00.8 Agent 解放勞務 → 00:16:17.3-00:16:27.7 第二大腦收尾
    - 交付：`output/AI Agent 就是你的第二大腦 [Claude] (Short)/`（6 檔齊全）
  - **短片 C 版也已加剪交付** ✅（C 承諾型，49.9s＋3s 字卡＝52.9s，<60s 進 Shorts feed）：
    - 標題使用者選：「AI 時代，工作流可以一鍵複製給別人的 Agent」
    - 精華組合（3 段）：00:46:35.5-00:46:51.5 一個 repo＝複製一整個部隊 → 00:46:54.1-00:47:09.2 丟網址全自動跑一遍 → 00:47:16.2-00:47:34.8 複製任何人工作流、寫給 Agent 看
    - 交付：`output/AI 時代，工作流可以一鍵複製給別人的 Agent [Claude] (Short)/`（6 檔齊全；封面橘色、GitHub 一鍵複製 Agent 大軍）
  - 注意：影片中承諾「用 Agent 學 Agent 知識庫 repo 連結放說明欄」，上架時務必補上
- **前一支**：**AntiGravity EP07（Padlet MCP）長片＋短片全流程交付完成** ✅
  - 來源：`raw/antigravity-ep07/antigravity-ep07.mp4`（原長 48:18 / 1.56GB，來自使用者 Downloads）
  - smart-cut（threshold 0.06、margin `0sec,0.1sec`）→ 28:44（剪 40.5%）
  - 轉字幕：Groq 7288 字 → resegment 741 段（平均 2.33s）→ apply_vocab → STOP1 使用者確認 8 處疑慮 → finalize 套 155 段修正 → validate 硬關卡通過（741 段全吻合）→ 依使用者指示刪除段 740（觀眾暱稱）重編號 → 最終 740 段 / 10925 字
  - **本集詞彙更正重點**（Padlet 系列日後可沿用）：
    - `Pellet/Pallet/Paylet/Pelet/Petlet/Headlet/Panelad/Pairline/Panelette/Panet/配列` → **Padlet**
    - `Agin/A群/AIA群/A集員/Edging/AI Aging/AIAG/AIG/AGE` → **Agent / AI Agent**
    - 使用者拍板：`RuneIt`→ZoomIt、`提消`→提交、`先路`→嵌入、`未教育真人`→為教育增能、`資源供應`→支援供應、`圈的留言`→全部的留言
  - 長片標題使用者選 #9：「一句話生成 Padlet 課程牆：分區、投票、AI 插圖全自動完成」
  - 長片交付：`output/一句話生成 Padlet 課程牆_分區、投票、AI 插圖全自動完成 [Claude]/`（5 檔齊全；封面橘色主題、Padlet 牆主視覺）
  - **短片也已交付** ✅（A 痛點型，105.9s＋3s 字卡＝108.9s）：
    - 標題：「一句話，AI 幫你開好整面 Padlet」
    - 精華組合（4 段，對齊字幕邊界）：00:10:12.5-00:10:56.7 手動建牆痛點→Agent 開好 → 00:11:28.1-00:11:44.0 自動分區 → 00:12:19.8-00:12:40.4 投票實證 → 00:18:44.1-00:19:09.4 無限電子佈告欄金句
    - 交付：`output/一句話，AI 幫你開好整面 Padlet [Claude] (Short)/`（6 檔：乾淨版 mp4／字幕版 mp4／srt／txt／cover／metadata）
  - 注意：影片中多次承諾「repo 連結放說明欄」，**上架時務必放 Padlet MCP 的 GitHub repo 連結**（metadata checklist 已標註）
  - **黑畫面事故與修復（2026-06-12）**：第一版 cut.mp4 從 2:37 起全黑（僅有聲音）。原因：原始螢幕錄影是 **VFR（可變幀率）**，auto-editor 重編碼中途輸出黑幀。修復：先 `ffmpeg -fps_mode cfr -r 30 -c:v libx264 -crf 18 -c:a copy` 轉 CFR，再重跑 auto-editor——因音訊未動，新剪輯版時長與舊版毫秒級一致（1724.466s），字幕無需重做。長片與短片交付檔皆已用修復版覆蓋並逐點驗證亮度。
- **之前進度**：OpenCode EP04 長片＋短片交付（2026-06-08，詳見交班歷史）。
  - 影片：`Open Code 基本功EP04_ 免費 Agent組裝你的 Agent 大軍_無限解放token.mp4`（原長 93:54 / 3.27GB）
  - smart-cut（threshold 0.06、margin `0sec,0.1sec`）→ 52:43（剪 43.9%，這位口播者較連續、剪除率比實演片低屬正常）
  - 轉字幕：Groq 13947 字 → resegment 1387 段（平均 2.28s，防斷字 OK）→ apply_vocab → STOP1 疑慮確認 → 23 段套用更正
  - **本集詞彙更正重點**（之後若再剪三師爸 OpenCode 系列可沿用）：
    - 模型名統一：`Gemma412B` / `Gemma 412B` → **Gemma 4 12B**（使用者確認）
    - `CLA` → **CLI**；`Claude Go`→Claude Code；`Opensure`→OpenCode
  - validate 時間碼硬關卡通過（1387 段全吻合）
  - 標題候選 10 個 → 使用者選 **#3**「OpenCode 基本功 EP04：免費組裝你的 Agent 大軍，無限解放 Token」
  - 封面（gpt-image-2 low、橘色 Claude 主題、指揮官+士兵大軍構圖）+ metadata.md（兩套合併規格）全部產出
  - 交付路徑：`output/OpenCode 基本功 EP04_免費組裝你的 Agent 大軍，無限解放 Token [Claude]/`（5 檔齊全）
- **這次用的是擴充後總控**：`claude-youtube-video-workflow` 已縫入 3 個 STOP 關卡 + 時間碼硬關卡 + marketing-spec.md；本支即按新流程跑完。
- **之前進度**：Antigravity(Codex) 封裝 `video-editing-and-subtitles` 技能；EP05/EP06 短長片交付（詳見下方歷史）。

- **短片也已交付** ✅（B 好奇型，93s）：
  - 標題：「聰明人都這樣用 AI：軍師指揮、大軍出工」
  - 精華組合（4 段）：00:26:05-13 派工概念 hook → 00:27:52-00:28:23 軍師/士兵分工 → 00:45:28-50 Token 經濟學 → 00:47:49-00:48:17 收尾 CTA
  - 交付路徑：`output/聰明人都這樣用 AI_軍師指揮、大軍出工 [Claude] (Short)/`（6 檔：乾淨版 mp4／字幕版 mp4／srt／txt／cover／metadata）
  - 修正：結尾「AA君大君」→「AI 大軍」（長片字幕也一併修正回寫）；段 158「Gemma 4設備」→「Gemma 4 12B」

## 下一步（給下一個 AI）
- AntiGravity EP07 長片＋短片**皆已交付**，等待使用者下一步指令。
- 長片章節時間碼為建議值（metadata.md §5），上傳後請對照成片微調。
- 上架時記得在說明欄與短片留言區放 Padlet MCP repo 連結（影片中承諾）。
- 檢查 `raw/` 下尚有：`用 AI Agent 來幫忙寫年度領域課程計畫.mp4`、`AI_agents的基本認識.mp4`、`使用 AI Agent 來自動剪輯教學影片...mp4` 可依需要處理。

---

## 上一次狀態（2026-05-10 上午）
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

## 2026-05-11 短片三版實測（livestream-skills-pack）
- 來源直播：`raw/使用 AI Agent 來自動剪輯教學影片_Skills 技能懶人包福利大放送_.mp4`（3.3GB / 1h41m）
- 走「最短路徑」：跳過 smart-cut、跳過逐段清字（直播太長、短片用不到）
- ffmpeg 抽 16kHz mono 32kbps 音訊 24MB → 剛好擠進 Groq 25MB 上限
- Groq 轉錄：1937 段 / 17556 字
- 三個短片版本全成品（每版 5 檔齊全：mp4/srt/txt/cover.png/metadata.md）：
  - `output/沒有人比這個更簡單 AI Agent 自動剪片 [Claude] (Short)/`（A 痛點型，1:50）
  - `output/別再寫剪片程式 AI Skill 一鍵搞定 [Claude] (Short)/`（B 反直覺型，1:40）
  - `output/3 個秘訣 AI Agent 自動剪好教學影片 [Claude] (Short)/`（C 教學型，1:49）
- 封面均 Claude 橘色主題、SHORT 角標、人物樣貌延續基準照
- 中途事件：人物基準照因 git 歷史清理被連帶清掉本機，使用者從 `C:/2025三師爸/viewsonic專業形像照/` 重新放回；該檔已 .gitignore，本機需保留

## 已知議題 / 待解問題
- **VFR 原始檔會讓 auto-editor 輸出黑幀**（EP07 實際踩到：2:37 後全黑、僅剩聲音）。預防：smart-cut 前先 `ffprobe` 看 `avg_frame_rate` 是否為非整數比（如 `260793000/8693101`），是 VFR 就先轉 CFR（`ffmpeg -fps_mode cfr -r 30 -c:v libx264 -crf 18 -c:a copy`）再剪；音訊 copy 不動，剪輯點與時間軸不變。**已修復（2026-06-12）**：`smart_cut.py` 現會自動偵測 VFR 並先轉 CFR 暫存檔再剪、完成後刪暫存檔；SKILL.md 踩坑段亦已補充。
- 封面 png 是 1536x1024（3:2），YouTube 建議 1280x720（16:9）— 視覺上沒太大差，需要的話可以後處理裁切
- smart-cut 預設 threshold 0.04 對這位口播者太鬆，這支影片用 0.06 才剛好。下一支可以先試 0.05 找平衡。
- `auto-editor.exe` 安裝在 `C:\Users\mathr\AppData\Roaming\Python\Python314\Scripts`，該路徑不在 PATH；但 `smart_cut.py` 會走 `python -m auto_editor`，所以不影響 Codex 執行。
- `resegment.py` 不會自動建立輸出資料夾；新影片流程要先建立 `_subtitles/`，否則會 `FileNotFoundError`。
- PowerShell 操作含空白或 `[Claude]` / `[Codex]` 的路徑時要加引號；含中括號路徑建議用 `-LiteralPath`。
- `clip_cut.py` 會把 `--segments` 自動依時間排序（避免重疊偵測），所以**無法做倒敘剪輯**。版本 B 原想先放結論再回開場，被排序成順敘，效果略弱於設計。下次要做倒敘需加 `--keep-order` 選項並改寫重疊驗證。

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
