# ANTIGRAVITY.md — 專案駕駛艙與自動化規範

本檔案是 **Anti-Gravity (AI 編碼助理)** 在 `2026Youtube` 專案的駕駛艙。透過本檔案，您可以規範 AI 代理的操作準則、自訂自動化工作流程（開工/收工 SOP），以及連結您的第二大腦（Obsidian）。

---

## 專案基本資訊

- **專案名稱**：2026Youtube
- **專案簡介**：雙 AI 接力之 YouTube 影片生產自動化工作流（去靜音、轉字幕、標題推薦、封面生成、metadata 產出、短片剪輯）。
- **當前版本**：v1.2.0 (Anti-Gravity 專屬最佳化版)

---

## Obsidian 第二大腦同步設定

- **Obsidian Vault 根目錄**：`C:\Users\mathr\OneDrive\文件\Secondbrain`
- **專案工作筆記**：`專案/2026Youtube/工作筆記.md`

---

## Anti-Gravity 專屬自動化常規流程 (SOP)

當我（使用者）在對話中說出對應關鍵字時，請 Anti-Gravity 自動執行以下 SOP：

### 🟢 1. 說「開工」或「我來了」時
1. **目錄確認**：確認當前工作目錄位於 Git 儲存庫 `g:\我的雲端硬碟\2026Youtube` 中。
2. **第二大腦同步**：讀取 Obsidian `專案/2026Youtube/工作筆記.md` 中關於本專案的「上次做到哪」與「下一步計畫」。
3. **Git 狀態確認**：執行 `git status` 與 `git log -n 5`，檢查本地與遠端分支狀態。
4. **回報**：提供精簡的開工摘要，並給出建議的今日第一步行動。

### 🔴 2. 說「收工」或「下班了」時
1. **工作成果提交**：
   - 執行 `git add <相關檔案>`（防範大檔案與影片）。
   - 詢問我並自動生成合適的繁體中文 commit message，執行 `git commit` 與 `git push`。
2. **第二大腦更新**：自動在 Obsidian `專案/2026Youtube/工作筆記.md` 中更新今日的「已完成工作」與「留待下次待辦事項」。
3. **防呆檢查**：掃描專案中是否有意外提交的 API Key、`.env` 敏感檔案。
4. **結束語**：給出收工報告，祝您下班愉快！

---

## Anti-Gravity 原生功能指南

- **生圖**：我原生擁有強大的 `generate_image` 工具。生圖不需設定任何 OpenAI API Key，只要直接對我說「畫一張封面圖」，我就能為您生成高畫質的圖像。
- **人物基準照與風格規範**：
  - **每一次封面都必須重新參考 `assets/persona/三師爸人物形象照.png`**（不可沿用舊封面或衍生圖）。
  - 風格與配色請依據 `assets/style/cover-style.md`。
  - Codex/Antigravity 版的主代表色為：亮藍 / 電子青 (`#00D4FF`、`#0099FF`)。
