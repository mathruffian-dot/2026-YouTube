# 2026Youtube — YouTube 影片自動化生產線

> 把原始影片素材丟進來，AI 接力產出剪好的影片、SRT 字幕、純文字稿、封面圖、YouTube 描述、社群貼文、SEO 關鍵字。
> 整套工作流由 **Claude Code** 與 **OpenAI Codex** 透過 `HANDOFF.md` 接力完成。

---

## 🚀 第一次拿到這個 repo？

**請先看 [`SETUP.md`](./SETUP.md)** — 完整的安裝、API key、個人化清單、第一次跑流程。

---

## 📂 工作流概覽

```
raw/<影片代號>/原始.mp4
    │
    ├─ smart-cut          → 去靜音（auto-editor）
    ├─ audio-to-srt       → SRT + 純文字（Groq Whisper）
    ├─ AI 生 10 個標題    → 等使用者挑
    │
    └─ 使用者挑完 ──→ output/<YouTube 標題>/
                          ├── <標題>.mp4
                          ├── <標題>.srt
                          ├── <標題>.txt
                          ├── cover.png         ← gpt-image-2 + 你的人物照
                          └── metadata.md       ← 描述 / 社群 / SEO
```

## 對 AI Agent 的入口
- **Claude Code** → 讀 [`CLAUDE.md`](./CLAUDE.md)
- **OpenAI Codex** → 讀 [`AGENTS.md`](./AGENTS.md)
- **接班交接** → 讀寫 [`HANDOFF.md`](./HANDOFF.md)

## 三個 Skill
- [`skills/smart-cut/`](./skills/smart-cut/SKILL.md) — 智能剪口播（auto-editor）
- [`skills/audio-to-srt/`](./skills/audio-to-srt/SKILL.md) — 語音轉字幕（Groq Whisper）
- [`skills/cover-image/`](./skills/cover-image/SKILL.md) — 封面圖生成（gpt-image-2）

## 個人化資產
- [`assets/persona/`](./assets/persona/README.md) — 你的人物形象照
- [`assets/style/`](./assets/style/README.md) — 你的頻道封面風格指南

## 同步全域 Skill 到專案副本
```powershell
./scripts/sync-skills.ps1            # dry-run
./scripts/sync-skills.ps1 -Apply     # 真的同步
```

---

## 對人的快速操作
1. 把影片素材丟進 `raw/<影片代號>/`
2. 跟 AI Agent 說：「處理 `<影片代號>`，主角是 Claude（或 Codex）」
3. AI 跑完整流程，在 step 6 暫停讓你挑標題
4. 挑完後 AI 繼續產封面與文案
5. 完成品在 `output/<標題>/`

完整細節見 [`SETUP.md`](./SETUP.md)。
