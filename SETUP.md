# SETUP — 給拿到這個 repo 的你

歡迎！這個 repo 是一條「**原始影片 → AI 接力 → 完整 YouTube 上架包**」的自動化生產線。
跟著這份 SETUP 跑一次，就能在你自己的 AI Agent（Claude Code 或 OpenAI Codex）裡重現整套工作流。

---

## 0. 這個 repo 在做什麼？
1. **smart-cut** — 用 auto-editor 自動剪掉沒講話的片段（去靜音）
2. **audio-to-srt** — 用 Groq Whisper 把語音轉成乾淨 SRT 字幕
3. **生 10 個 YouTube 標題候選** — 等你挑一個
4. **以選定標題建資料夾**，平行產出：
   - 封面圖（OpenAI gpt-image-2，自動套用你的人物與頻道風格）
   - YouTube 描述、社群貼文、SEO 關鍵字
5. **打包**：剪好的影片 + 字幕 + 純文字 + 封面 + metadata，全部放在 `output/<標題> [Claude]/` 或 `output/<標題> [Codex]/`（依執行的 AI Agent 標記，方便 A/B 比較）

整個流程由 **Claude Code** 與 **OpenAI Codex** 透過 `HANDOFF.md` 接力完成。
若要讓 AI 一次依序跑完整流程，依使用的 Agent 選擇總控 Skill：
- Codex：`skills/codex-youtube-video-workflow/SKILL.md`
- Claude Code：`skills/claude-youtube-video-workflow/SKILL.md`

---

## 1. 系統前置

需要這些工具：

| 工具 | 用途 | 安裝方式 |
|------|------|---------|
| Python 3.10+ | 跑 Skill 腳本 | python.org |
| ffmpeg | 影音處理 | `winget install Gyan.FFmpeg`（Win）/ `brew install ffmpeg`（Mac）|
| auto-editor | smart-cut 剪口播 | `pip install auto-editor` |
| groq (Python SDK) | audio-to-srt 呼叫 Groq Whisper | `pip install groq` |
| openai (Python SDK) | cover-image 呼叫 OpenAI | `pip install openai` |
| Git | 版本控制 | git-scm.com |
| Claude Code 或 OpenAI Codex CLI | AI Agent | 看你習慣哪一個 |

---

## 2. 取得 API Key

### Groq（給 audio-to-srt 用，**必填**）
1. 到 [console.groq.com](https://console.groq.com) 註冊
2. 建立 API Key
3. 存到 `~/.groq_api_key`（純文字，整檔就是 key 字串）

### OpenAI（給 cover-image 用，**只在 Claude Code 才需要**）
> ⚠️ **如果你只用 Codex 不用 Claude Code → 跳過這段、不需 OpenAI API Key**。Codex 內建 image 2 生圖功能，會直接用內建工具產封面，不會呼叫 `skills/cover-image/draw.py`。

1. 到 [platform.openai.com](https://platform.openai.com) 註冊
2. **要做 Individual 驗證**才能用 gpt-image-2（在 Settings → Organization → General）
3. 建立 API Key
4. 存到 `~/.openai.env`，格式：
   ```
   OPENAI_API_KEY=sk-...
   ```
5. 帳戶儲值（gpt-image-2 一張 low quality 約 NT$0.3）

> 不想另存環境檔的話，也可以直接 export 到 shell：`export OPENAI_API_KEY=sk-...`

### 兩個 AI Agent 的封面生成差異

| AI Agent | 封面生成方式 | 是否需要 OPENAI_API_KEY |
|---------|-------------|------------------------|
| **Claude Code** | 呼叫 `skills/cover-image/draw.py`（OpenAI Python SDK）| ✅ 需要 |
| **OpenAI Codex** | 用 Codex 內建的 image 2 生圖工具 | ❌ 不需要 |

兩邊都遵守同一份 `assets/style/cover-style.md` 規範與 `assets/persona/` 人物基準照，所以產出風格一致。

---

## 3. 個人化清單（**必改**）

下表是「每個拿到此 repo 的人都必須換成自己版本」的內容：

| 項目 | 檔案 / 位置 | 怎麼換 |
|------|------------|--------|
| **人物形象照** | `assets/persona/三師爸人物形象照.png` | 換成你自己的半身照（去背 PNG），檔名自取，**記得同步改 CLAUDE.md / AGENTS.md / cover-style.md 內所有引用此檔的地方** |
| **頻道封面風格** | `assets/style/cover-style.md` | 改成你自己頻道的色票、構圖、字體規則。你也可以整段重寫。 |
| **頻道封面參考圖**（選填）| `assets/style/reference-thumbnails.png` | 截圖你頻道現有的 9–12 張封面，貼成一張圖。AI 生封面前會 Read 這張學風格。沒有的話可以先不放，依靠 cover-style.md 即可。 |
| **字幕詞彙修正表** | `skills/audio-to-srt/references/vocabulary.md` | 預設含我這邊的常用詞（Claude、Codex、三師爸…）。換成你自己的專有名詞。 |
| **詞彙機械替換** | `skills/audio-to-srt/scripts/apply_vocab.py` | 內含 REPLACEMENTS dict，加你自己的「Whisper 常聽錯 → 正確」對照。 |
| **HANDOFF.md** | `HANDOFF.md` | 整個清空後重寫成「目前狀態：剛 fork repo、無進行中影片」。我留下的工作紀錄與你無關。 |
| **GitHub repo 連結** | `CLAUDE.md`、`AGENTS.md`、`README.md` | 把 `mathruffian-dot/2026-YouTube` 換成你的 |
| **頻道 / 學校名稱** | `CLAUDE.md`、`AGENTS.md` 內含「2026Youtube」「光武國中」等字眼 | 全文搜尋取代為你的 |

---

## 4. 你**可以調**的參數（每支影片可能不同）

### smart-cut（剪口播）

| 參數 | 我的設定 | 何時要改 |
|------|---------|---------|
| `--threshold` | `0.06`（嚴）| 你講話本來就很連貫 → 拉鬆到 `0.04`；你講話超多停頓/雜訊 → 拉嚴到 `0.08` |
| `--margin` | `"0sec,0.1sec"`（開頭不留、結尾留 0.1 秒）| 想要每段講話前後都自然餘音 → 改 `"0.2sec,0.2sec"` |

詳細說明見 `skills/smart-cut/SKILL.md`。

### cover-image（封面）

| 參數 | 預設 | 何時要改 |
|------|------|---------|
| `--quality` | `low`（NT$0.3，99% 場景夠用）| 要實體印刷或極致文字精度 → 升 `high`（NT$5.5）|
| `--size` | `1536x1024`（3:2，接近 16:9）| YouTube 嚴格 16:9 可後處理裁成 `1280x720` |

---

## 5. 第一次跑流程

### Step 1 — Clone & 設好環境
```bash
git clone https://github.com/<your>/<your-repo>.git
cd <your-repo>
pip install auto-editor groq openai
ffmpeg -version  # 確認有裝
```

### Step 1.5 — 環境驗證（逐條跑，全過才繼續）

```powershell
# 1. Python
python --version                  # 要 3.10+

# 2. ffmpeg
ffmpeg -version                   # 看到版本號即可

# 3. auto-editor（exit code 255 是正常的，看到版本號就對了）
python -m auto_editor --version

# 4. Python 套件
python -c "import groq; print('groq ok')"
python -c "import openai; print('openai ok')"

# 5. Groq API Key
python -c "
import os, pathlib
key_file = pathlib.Path('~/.groq_api_key').expanduser()
key = os.getenv('GROQ_API_KEY') or (key_file.read_text().strip() if key_file.exists() else '')
print('Groq key:', 'ok' if key else '缺 — 請照 Step 2 設定 ~/.groq_api_key')
"

# 6. OpenAI API Key（只在用 Claude Code 封面功能時需要）
python -c "
import os, pathlib
p = pathlib.Path('~/.openai.env').expanduser()
key = os.getenv('OPENAI_API_KEY', '')
if not key and p.exists():
    for line in p.read_text().splitlines():
        if line.startswith('OPENAI_API_KEY='):
            key = 'from file'
print('OpenAI key:', key if key else '未設定（只在 Claude Code 封面生成時需要）')
"
```

> **Windows 提醒**：含中文的路徑請用 **PowerShell**（不是 Git Bash）執行以上指令，避免編碼問題。

### Step 2 — 把 Step 3 的個人化清單跑一遍
特別注意：**人物照、HANDOFF.md、API keys** 三件事不弄好，後面跑不動。

### Step 3 — 同步 Skill（可選，但建議）
這個 repo 內 `skills/audio-to-srt/` 與 `skills/cover-image/` 是從 Claude 全域 Skill 複製過來的副本（Codex 看得到全域 Skill）。如果你**不是**用 Claude 全域 Skill，可以忽略；如果你是，跑：
```powershell
./scripts/sync-skills.ps1            # 看差異
./scripts/sync-skills.ps1 -Apply     # 真的同步
```

### Step 4 — 丟第一支影片試跑
```bash
# 把影片放進 raw/<隨意取個影片代號>/原始.mp4
# 然後在 Claude Code 或 Codex 裡說：
> 使用 codex-youtube-video-workflow 處理 raw/<影片代號>，主角是 Codex

# 或在 Claude Code 裡說：
> 使用 claude-youtube-video-workflow 處理 raw/<影片代號>，主角是 Claude
```

AI 會：
1. 讀 `HANDOFF.md`（看上次到哪 — 你應該看到「無進行中影片」）
2. 讀 `CLAUDE.md` 或 `AGENTS.md`（看工作流規範）
3. 跑 smart-cut → audio-to-srt
4. 生 10 個標題給你挑
5. 你挑完 → 建資料夾 → 平行產封面 + metadata
6. 收工前更新 `HANDOFF.md`

---

## 6. 兩個 AI Agent 接力

這個 repo 是雙 AI 接力設計：

| AI Agent | 入口檔 | 啟動 |
|---------|--------|------|
| Claude Code | `CLAUDE.md` | `claude` 在 repo 根目錄啟動 |
| OpenAI Codex | `AGENTS.md` | `codex` 在 repo 根目錄啟動 |

**接力規則：** 兩邊都會讀 `HANDOFF.md` 知道彼此做到哪、收工前必須更新。
**重要：** 兩邊不要同時動，會搶 commit 衝突。

---

## 7. 三處同步機制（選用）

我自己的工作流會把專案三處同步：
- **Google Drive** — 主要工作目錄
- **GitHub** — 版本備份
- **Obsidian** — 創意點子與工作筆記

如果你不需要 Obsidian，把 `CLAUDE.md` 內所有「Obsidian」段落刪掉即可。
GitHub 是強烈推薦保留（影片大檔已在 `.gitignore` 排除，repo 不會爆）。

---

## 8. 常見問題

**Q：生封面跳 `403 Organization must be verified`？**
A：去 platform.openai.com/settings/organization/general 做 Individual 驗證。

**Q：smart-cut 把我講話的句子剪掉了？**
A：threshold 太嚴，調鬆（0.06 → 0.04）；或把 margin 從 `0sec,0.1sec` 改成 `0.2sec,0.2sec`，每句話前後多留一點緩衝。

**Q：threshold 跟 margin 怎麼調？**
A：`--threshold` 是音量門檻（多小算靜音，0.06 = 6%，越大剪越多）；`--margin` 是每段語音前後保留的緩衝時間（格式 `前,後`，例如 `0sec,0.1sec` 表示開頭不留、結尾留 0.1 秒）。講話停頓多的口播者建議從 threshold 0.06 開始試。

**Q：字幕時間碼跟剪好的影片對不上？**
A：你應該是對「原始檔」轉字幕了。**先剪後轉**，順序顛倒會錯位。

**Q：`import groq` 出現 ModuleNotFoundError？**
A：`pip install groq` 裝一下，這個套件是字幕流程的必要依賴，早期版本的 SETUP.md 漏掉了。

**Q：`python -m auto_editor --version` 跑完 exit code 255？**
A：正常現象，auto-editor 的 `--version` 就是回傳 255，不是錯誤。只要看到版本號印出來就代表裝好了。

**Q：我用的是其他 AI（Gemini、本地 LLM），這個 repo 還能用嗎？**
A：核心 Skill（smart-cut / audio-to-srt / cover-image）跟 AI Agent 解耦，本身就能獨立呼叫。但「10 標題候選 / 描述撰寫」步驟需要 LLM 推理，要自己改成你用的 LLM。

---

## 9. 給回饋
這個 repo 是 [mathruffian-dot/2026-YouTube](https://github.com/mathruffian-dot/2026-YouTube) fork 出來的。
有 bug、改進建議歡迎開 issue。
