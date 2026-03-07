# 🚀 AntroCode_00/01 

AntroCode_00/01 是一個輕量級、純前端渲染的 AI 程式碼助手介面。透過 Python 腳本一鍵生成並啟動，完美串接 **DeepSeek API**，為開發者提供一個沉浸式的深色系（Dark Mode）駭客風工作空間。

不需要複雜的環境配置、不需要架設後端資料庫，只要填入你的 API Key，立刻擁有一個具備「本地記憶」與「多工處理」能力的專屬 AI 助手。

---

## ✨ 核心亮點功能 (Features)

- **💾 本地記憶守護 (Local Storage State Management)**
  - 聊天紀錄與工作區狀態自動保存在瀏覽器本地端。
  - 即使不小心按下 F5 重新整理或關閉分頁，心血也絕對不會消失！
- **🗂️ 獨立多工作區 (Multi-Workspace Support)**
  - 支援建立多個 `Agent` 與 `Project` 分頁。
  - 每個分頁擁有**獨立的上下文記憶**，跨專案開發不再精神錯亂。
- **⚡ 非同步背景思考 (Async Background Processing)**
  - 當 AI 正在生成超長程式碼時，你可以自由切換到其他分頁繼續工作。
  - AI 的回覆會精準存入當初發問的分頁中，絕不「跑錯棚」。
- **🎨 駭客風沉浸式 UI (Immersive Hacker UI)**
  - 採用 `#121212` 黑底配 `#00FFAA` 科技綠的極簡設計。
  - 內建 `marked.js` 與 `highlight.js`，完美渲染 Markdown 格式與程式碼語法高亮 (Syntax Highlighting)。
- **🔄 模型無縫切換 (Model Switching)**
  - 一鍵切換 `Think` (DeepSeek Reasoner) 與 `Fast` (DeepSeek Chat) 模式。

---

## 🛠️ 快速開始 (Getting Started)

### 1. 準備工作 (Prerequisites)
- 你的電腦需要安裝 [Python 3.x](https://www.python.org/)。
- 準備好一組有效的 [DeepSeek API Key](https://platform.deepseek.com/)。

### 2. 安裝與設定 (Installation & Setup)
下載本專案的 Python 腳本 `AntroCode_00/01.py`，並使用文字編輯器打開它。

找到程式碼中 `ENVIRONMENT_CONFIG` 的設定區塊，將你的 API Key 貼上去：

```javascript
const ENVIRONMENT_CONFIG = {
    API_URL: '[https://api.deepseek.com/chat/completions](https://api.deepseek.com/chat/completions)', 
    API_KEY: 'sk-請在這裡貼上你的_真實_DEEPSEEK_API_KEY', // <--- 替換成你的 Key
    CURRENT_MODE: 'deepseek-reasoner' 
};
