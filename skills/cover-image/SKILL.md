---
name: draw
description: OpenAI gpt-image-2 生圖技能（全域可用）。當使用者要求「畫一張」、「生一張圖」、「做一張圖」、「產生圖片」、「畫個封面」、「畫插圖」、「畫示意圖」、「畫分鏡」等任何需要 AI 生成圖像的情境時，請一定要使用此技能。此技能會呼叫本地腳本以 gpt-image-2 模型生圖，自動判斷 quality 等級（low/medium/high），存檔至當前專案的 slides/generated/ 目錄（若無則建於當下工作目錄），並主動回報使用的等級與預估台幣費用。適用於演講素材、教學插圖、簡報封面、社群圖、分鏡草稿等各種場景。
---

# 小克生圖技能（gpt-image-2）

## 用途
以 OpenAI 最新 gpt-image-2 模型生成圖片，支援 2.0 的新能力：正確文字渲染、多圖一致性（最高 8 張）、推理式構圖。

## 在本專案（2026Youtube）的特別規範
**所有 YouTube 封面必須以 `assets/persona/三師爸人物形象照.png` 作為人物基準。**
標準呼叫：
```bash
python skills/cover-image/draw.py "封面 prompt..." \
  --edit "assets/persona/三師爸人物形象照.png" \
  --size 1536x1024 --quality low \
  --name cover --outdir "output/<標題>/"
```
gpt-image-2 在 edit 模式下會延續人物的臉、髮型、體型、穿著（黑外套、眼鏡）。
prompt 中可描述人物位置與場景，但**不要**指定矛盾的五官、外套顏色、眼鏡屬性。

## 觸發情境
使用者說出：
- 「畫一張 XX」「生一張圖」「做一張圖」
- 「畫個封面／插圖／示意圖／分鏡」
- 「產生圖片」「幫我生圖」
- 「用 gpt-image 畫」
- 「改這張圖」「修改圖片」「把背景換成 XX」「幫我改圖」（→ 改圖模式，需提供圖片路徑）

## 前置需求
- 環境變數 `OPENAI_API_KEY` 已設定（或當前專案根目錄有 `.env` 檔含此變數）
- OpenAI 組織已完成 Individual 驗證（gpt-image-2 需要）
- 已安裝 `openai` Python 套件

## 腳本位置
`C:/Users/mathr/.claude/skills/draw/draw.py`

## 使用方式

### 基本呼叫
```bash
python C:/Users/mathr/.claude/skills/draw/draw.py "要畫的內容" --name 檔名前綴
```

### 參數
- `prompt`（必填）：要畫什麼，自然語言描述
- `--size`：`1024x1024`（方，預設）/ `1536x1024`（橫）/ `1024x1536`（直）/ `auto`
- `--quality`：`low` / `medium` / `high` / `auto`
- `--n`：生成張數 1–8（2.0 支援多圖一致性）
- `--name`：輸出檔名前綴
- `--outdir`：輸出目錄（預設：當前工作目錄的 `slides/generated/`，沒有就建在 `./generated/`）

## 判斷 quality 等級的原則
**預設永遠用 `low`**（使用者明確要求：省錢+速度優先）

- **low**（約 NT$0.3）：**99% 情境的正確選擇**。演講簡報、教學插圖、概念圖、封面、過場、demo、螢幕投影用途，甚至帶中文標題的簡報頁都能勝任。速度也快 4–5 倍。
- **medium**（約 NT$1.3）：通常不用，除非 low 明顯不夠。
- **high**（約 NT$5.5）：**僅限以下情境**：
  1. 使用者明確說「要最好的品質」「要 high」「要印出來」
  2. 實體印刷品（海報、書籍封面、名片）
  3. 密集跨語言文字完全零錯（餐單、多國標籤）

不確定就 **low**。不要自作主張升級。

尺寸影響：`1536x1024` 約乘 1.5 倍；多張 `n>1` 乘以張數。

## 執行後不需要報告等級或費用
使用者已熟悉規格，**不要**再附「用的是 low（約 NT$0.3）」這種行。
直接呈現結果即可，保持精簡。

若判斷需要升級到 medium 或 high，**先停下來問使用者**，不要自作主張。

## 錯誤處理
- 若出現 `403 Organization must be verified` → 提示使用者去 platform.openai.com/settings/organization/general 做 Individual 驗證
- 若出現 `401 Invalid API key` → 檢查 `.env` 或環境變數
- 若出現 `429 Rate limit` → 可能是 OpenAI 額度用完，提示使用者去 Billing 儲值

## 輸出
PNG 檔，檔名格式：`<name>_<YYYYMMDD_HHMMSS>.png`，多張時加 `_1` `_2` 後綴。
