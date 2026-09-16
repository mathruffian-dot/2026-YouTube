---
name: antigravity-youtube-video-workflow
description: YouTube 影片自動化生產線總控技能（Anti-Gravity 專屬最佳化版）。將原始口播影片一條龍處理成可直接上架之 YouTube 上架包：自動剪去靜音口播（smart-cut）、Groq Whisper 語音轉繁中字幕（audio-to-srt）、精細斷句與詞彙校正、10 組吸睛標題推薦、以選定標題建立交付包、原生調用 generate_image 依人物照與青藍科技風格產出 16:9 封面圖、撰寫 300 字 YouTube 描述與無 Emoji 社群貼文與 15-20 組 SEO 標籤（metadata.md），並支援選配 ≤2 分鐘亮點短片剪輯（short-video-workflow）。當使用者說「處理 YouTube 影片」「跑影片生產線」「YouTube 自動化剪輯」「剪 raw 影片」「跑 YouTube 一條龍」「製作 YouTube 上架包」或說出開工/收工指令時觸發。
---

# Anti-Gravity YouTube 影片自動化生產線工作流

本技能為 **Anti-Gravity (AI 編碼助理)** 量身打造的 YouTube 影音自動化生產線總控中心。整合去靜音、語音轉字幕、標題推薦、免 Key 原生生圖封面、行銷文案、SEO 標籤與短片剪輯。

---

## 核心亮點與優勢

1. **原生免 API Key 生圖**：封面圖直接調用 Anti-Gravity 原生 `generate_image` 工具（設定 `AspectRatio: '16:9'`），不需設定 OpenAI API Key，節省開銷且生成品質極高。
2. **三師爸人物基準與風格規範**：嚴格依循 `references/cover-style.md` 色彩與構圖指南，每次生成重新參考人物基準照（`assets/persona/`），主打青藍科技微光與亮黃高對比標題。
3. **無縫接軌各子技能**：
   - 剪口播：調用 `smart-cut`
   - 轉字幕：調用 `audio-to-srt`
   - 剪短片：調用 `short-video-workflow`
4. **標準交付目錄**：輸出統一規範為 `output/<YouTube 標題> [Antigravity]/`。

---

## 專案目錄與工作流契約

- **原始影片**：`raw/<video-id>/原始.mp4`
- **中間處理**：`working/<video-id>/`
- **最終交付**：`output/<YouTube 標題> [Antigravity]/`
  - `<標題>.mp4`（剪輯去靜音後影片）
  - `<標題>.srt`（繁體中文乾淨字幕）
  - `<標題>.txt`（純文字逐字稿）
  - `cover.png`（Anti-Gravity 原生生成 16:9 封面圖）
  - `metadata.md`（完整 YouTube 資訊、社群短文、SEO 標籤、一次貼整合區）
- **短片交付（選配）**：`output/<短片標題> [Antigravity] (Short)/`

---

## 一條龍標準執行步驟

### Step 1：環境依賴確認
確認以下核心工具：
1. `ffmpeg`：影音轉碼
2. `auto-editor`：智慧剪口播
3. `groq` (Python SDK) 與 `~/.groq_api_key`：Whisper 雲端轉字幕
4. 人物基準照：檢查專案 `assets/persona/` 目錄

### Step 2：智能剪口播（smart-cut）
執行 auto-editor 進行語音活動偵測並剪除靜音：
```powershell
python -m auto_editor "raw/<video-id>/原始.mp4" --threshold 0.04 --margin "0.25sec,0.25sec" --export default -o "working/<video-id>/<video-id>.cut.mp4"
```
*如影片為 VFR（可變幀率），先轉 CFR 再剪輯以避免黑畫面。*

### Step 3：音訊擷取與 Groq Whisper 轉字幕（audio-to-srt）
1. 擷取 16kHz mono wav 音訊：
   ```powershell
   ffmpeg -i "working/<video-id>/<video-id>.cut.mp4" -vn -ar 16000 "working/<video-id>/<video-id>.cut.wav" -y
   ```
2. 執行 Groq Whisper 轉錄並依 word-level 時間戳重新精細斷句：
   ```powershell
   $SkillDir = "C:\Users\User\.gemini\config\skills\audio-to-srt"
   python "$SkillDir\scripts\transcribe_groq.py" "working/<video-id>/<video-id>.cut.wav" --out "working/<video-id>/_subtitles/<video-id>.groq.json"
   python "$SkillDir\scripts\resegment.py" "working/<video-id>/_subtitles/<video-id>.groq.json" --audio "working/<video-id>/<video-id>.cut.wav" --out "working/<video-id>/_subtitles/<video-id>.raw.srt"
   python "$SkillDir\scripts\apply_vocab.py" "working/<video-id>/_subtitles/<video-id>.raw.srt" --out "working/<video-id>/_subtitles/<video-id>.vocab.srt"
   ```
3. 檢查專有名詞、產出 `working/<video-id>/<video-id>.clean.srt` 與純文字稿 `working/<video-id>/<video-id>.txt`。

### Step 4：AI 推薦 10 組吸睛標題（暫停等待挑選）
讀取純文字稿，依 `references/marketing-spec.md` 產出 10 組標題（好奇心驅動、價值導向、痛點解決穿插）。
**暫停並呈送給使用者挑選一個最中意的標題。**

### Step 5：建立交付資料夾並平行產出
使用者挑定 `<選定標題>` 後：
1. 建立 `output/<選定標題> [Antigravity]/`
2. 搬移/複製成片與字幕：
   - `output/<選定標題> [Antigravity]/<選定標題>.mp4`
   - `output/<選定標題> [Antigravity]/<選定標題>.srt`
   - `output/<選定標題> [Antigravity]/<選定標題>.txt`

### Step 6：原生生成 16:9 封面圖（generate_image）
依據 `references/cover-style.md` 規範：
- **比例**：`AspectRatio: '16:9'`
- **視覺重心**：
  - 左側：亮黃色（`#FFD700`）超粗黑體主題大標題、科技圖示、強烈放射光
  - 右側：三師爸人物形象（半身、沉穩指引手勢、深色夾克眼鏡、邊緣青藍科技輪廓光）
  - 背景：深海軍藍（`#0A1628`）、電子青粒子、微光網格
- 使用 `generate_image` 生成並儲存為 `output/<選定標題> [Antigravity]/cover.png`。

### Step 7：產出行銷與 SEO 文案（metadata.md）
依據 `references/marketing-spec.md` 撰寫：
1. **Hook 與內容描述**（≤ 300 字，含 3 個核心精華點與 CTA）
2. **社群分享短文**（FB/IG 專用，150-200 字，**嚴禁任何 Emoji**，真誠分享口吻，結尾互動提問）
3. **Threads 簡短共鳴金句**
4. **SEO 關鍵字清單**（15-20 組）
5. **YouTube 後台一次貼標籤**（半形逗號分隔）
6. **上架 Checklist**

### Step 8（選用）：短片模式（short-video-workflow）
若使用者需要短片：
- 從字幕中挑出 1-3 個 ≤2 分鐘精彩亮點片段
- 轉換為 9:16 直式畫面（`make_vertical.py`）
- 燒錄動態大字幕（`burn_subtitles.py`）
- 輸出至 `output/<短片標題> [Antigravity] (Short)/`

---

## 駕駛艙日常 SOP

### 🟢 說「開工」或「我來了」
1. 檢查目前工作目錄與 Git 狀態。
2. 讀取工作筆記或 `HANDOFF.md`，確認「上次做到哪」與「今日待辦」。
3. 回報開工摘要與第一步建議。

### 🔴 說「收工」或「下班了」
1. 檢查產出檔案完整度，防範影片等大檔被誤加入 Git。
2. 生成繁體中文 Commit 訊息並提交推送。
3. 輸出收工報告，祝下班愉快！
