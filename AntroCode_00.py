import os
import webbrowser

# ==========================================
# 網頁原始碼變數 (請保持 r""" 確保字串完整)
# ==========================================
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AntroCode - DeepSeek</title>
    
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

    <style>
        /* --- 1. 顏色變數與基礎設定 --- */
        :root {
            --bg-color-main: #121212;
            --bg-color-sidebar: #1e1e1e;
            --bg-color-element: #2a2a2a;
            --text-color: #ffffff;
            --text-muted: #aaaaaa;
            --border-color: #333333;
            --tech-green: #00FFAA;
            --danger-color: #ff4444;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        body { background-color: var(--bg-color-main); color: var(--text-color); }
        .app-container { display: flex; height: 100vh; }

        /* 自訂灰色捲軸樣式 */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-color-main); }
        ::-webkit-scrollbar-thumb { background: #555555; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #777777; }

        /* --- 2. 側邊欄 --- */
        .sidebar { width: 250px; background-color: var(--bg-color-sidebar); padding: 20px; border-right: 1px solid var(--border-color); overflow-y: auto; }
        .menu-icon { font-size: 24px; cursor: pointer; color: var(--text-muted); transition: color 0.2s; margin-bottom: 20px; }
        .menu-icon:hover { color: var(--text-color); }
        .sidebar-section { margin-top: 20px; }
        .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .section-header h3 { color: var(--text-muted); font-size: 14px; text-transform: uppercase; margin: 0; }
        .add-btn { background: transparent; border: none; color: var(--tech-green); font-size: 20px; cursor: pointer; transition: transform 0.2s; }
        .add-btn:hover { transform: scale(1.2); }
        .sidebar-section ul { list-style: none; }
        .sidebar-section li { padding: 8px 12px; border: 1px solid var(--border-color); margin: 8px 0; border-radius: 8px; text-align: center; background: var(--bg-color-element); cursor: pointer; transition: background 0.2s; }
        .sidebar-section li:hover { background: #3a3a3a; }
        .edit-input { width: 100%; background: transparent; border: none; color: var(--text-color); text-align: center; outline: none; font-size: 16px; }

        /* 右鍵選單 */
        .context-menu { display: none; position: absolute; background-color: var(--bg-color-sidebar); border: 1px solid var(--border-color); border-radius: 8px; padding: 5px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.5); z-index: 1000; }
        .context-menu-item { padding: 8px 20px; cursor: pointer; color: var(--danger-color); }
        .context-menu-item:hover { background-color: var(--bg-color-element); }

        /* --- 3. 主要內容與標頭 --- */
        .main-content { flex: 1; display: flex; flex-direction: column; position: relative; }
        .header { display: flex; justify-content: center; align-items: center; padding: 20px; border-bottom: 1px solid var(--border-color); position: relative; }
        #openSidebar { position: absolute; left: 20px; display: none; }
        .header h2 { font-weight: 500; letter-spacing: 2px; }
        .logo-container { position: absolute; right: 20px; display: flex; align-items: center; }

        /* --- 4. 對話區 --- */
        .chat-display { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        /* ✅ 修正了 white-space 以支援 Markdown */
        .chat-message { max-width: 70%; padding: 12px 16px; border-radius: 12px; line-height: 1.5; word-wrap: break-word; }
        .user-message { align-self: flex-end; background-color: var(--tech-green); color: #000; border-bottom-right-radius: 2px; white-space: pre-wrap; }
        .ai-message { align-self: flex-start; background-color: var(--bg-color-element); color: var(--text-color); border-bottom-left-radius: 2px; width: 100%; max-width: 85%; }

        /* ✅ Markdown 與 Highlight.js 專屬樣式 */
        .ai-message p { margin-bottom: 10px; }
        .ai-message p:last-child { margin-bottom: 0; }
        .ai-message pre {
            background-color: #0d1117; /* 深色代碼框背景 */
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
            border: 1px solid #30363d;
        }
        .ai-message code {
            font-family: 'Consolas', 'Courier New', monospace;
            background-color: rgba(0, 0, 0, 0.3);
            color: var(--tech-green); /* 行內代碼顏色 */
            padding: 2px 4px;
            border-radius: 4px;
        }
        .ai-message pre code {
            background-color: transparent; /* 獨立代碼框不需額外底色 */
            padding: 0;
            color: inherit; /* 讓 highlight.js 完全接管顏色 */
        }

        /* --- 5. 輸入區 --- */
        .input-area { padding: 20px; display: flex; justify-content: center; }
        .input-box { width: 80%; max-width: 800px; border: 1px solid var(--border-color); border-radius: 12px; display: flex; flex-direction: column; background: var(--bg-color-sidebar); padding: 12px; }
        .input-box textarea { width: 100%; border: none; background: transparent; color: var(--text-color); outline: none; font-size: 16px; padding: 10px; margin-bottom: 10px; resize: none; min-height: 44px; max-height: 150px; overflow-y: auto; }
        .input-box textarea::placeholder { color: var(--text-muted); }
        
        .input-controls { display: flex; align-items: center; }
        .mode-wrapper { position: relative; }
        button.mode-btn { padding: 8px 16px; border: 1px solid var(--border-color); border-radius: 20px; background: var(--bg-color-element); color: var(--text-color); cursor: pointer; font-size: 14px; transition: all 0.2s; }
        button.mode-btn:hover { background: #444; border-color: #666; }
        .mode-dropdown { display: none; position: absolute; bottom: 110%; left: 0; background-color: var(--bg-color-sidebar); border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; min-width: 150px; box-shadow: 0 -4px 10px rgba(0,0,0,0.5); }
        .mode-dropdown.show { display: block; }
        .dropdown-item { padding: 10px 15px; cursor: pointer; transition: background 0.2s; text-align: center; }
        .dropdown-item:hover { background-color: var(--bg-color-element); color: var(--tech-green); }
        .dropdown-item:active { background-color: var(--tech-green); color: #000; } /* 點擊時的視覺回饋 */
    </style>
</head>
<body>
    <div class="app-container">
        <aside class="sidebar" id="sidebar">
            <div class="menu-icon" id="closeSidebar">☰</div>
            <div class="sidebar-section">
                <div class="section-header"><h3>Agent</h3><button class="add-btn" id="addAgentBtn">+</button></div>
                <ul id="agentList"><li class="editable-item" data-type="agent">Agent 1</li></ul>
            </div>
            <div class="sidebar-section">
                <div class="section-header"><h3>Project</h3><button class="add-btn" id="addProjectBtn">+</button></div>
                <ul id="projectList"><li class="editable-item" data-type="project">Project 1</li></ul>
            </div>
        </aside>

        <main class="main-content">
            <header class="header">
                <div class="menu-icon" id="openSidebar">☰</div>
                <h2>AntroCode</h2>
                <div class="logo-container">
                    <svg width="40" height="40" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <path d="M50 5 C50 40 60 50 95 50 C60 50 50 60 50 95 C50 60 40 50 5 50 C40 50 50 40 50 5 Z" fill="var(--tech-green)" />
                    </svg>
                </div>
            </header>
            
            <div class="chat-display" id="chatDisplay">
                <div class="chat-message ai-message">System Ready. Connected to DeepSeek API. Please select your mode from the bottom menu.</div>
            </div>
            
            <div class="input-area">
                <div class="input-box">
                    <textarea id="chatInput" placeholder="Ask me anything..." rows="1"></textarea>
                    <div class="input-controls">
                        <div class="mode-wrapper">
                            <button class="mode-btn" id="modeBtn">Mode</button>
                            <div class="mode-dropdown" id="modeDropdown">
                                <div class="dropdown-item">Think</div>
                                <div class="dropdown-item">Fast</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <div class="context-menu" id="customContextMenu">
        <div class="context-menu-item" id="deleteOption">delete</div>
    </div>

    <script>
        // ==========================================
        // 🚀 API 環境設定區 (DeepSeek 配置)
        // ==========================================
        const ENVIRONMENT_CONFIG = {
            API_URL: 'https://api.deepseek.com/chat/completions', 
            API_KEY: 'sk-ce77d8e4d88b4cc79bf26889c0cf5229', // ⚠️ 替換時請一定要保留頭尾的單引號 ' '
            CURRENT_MODE: 'deepseek-reasoner'  // 預設對應的模型代號 (Think)
        };

        // ==========================================
        // 🎨 UI 互動邏輯
        // ==========================================
        const sidebar = document.getElementById('sidebar');
        const closeSidebarBtn = document.getElementById('closeSidebar');
        const openSidebarBtn = document.getElementById('openSidebar');
        const modeBtn = document.getElementById('modeBtn');
        const modeDropdown = document.getElementById('modeDropdown');

        closeSidebarBtn.addEventListener('click', () => { sidebar.style.display = 'none'; openSidebarBtn.style.display = 'block'; });
        openSidebarBtn.addEventListener('click', () => { sidebar.style.display = 'block'; openSidebarBtn.style.display = 'none'; });
        
        modeBtn.addEventListener('click', (event) => { modeDropdown.classList.toggle('show'); event.stopPropagation(); });
        
        // ✅ 💡 更新版的翻譯大腦：保留 Mode 文字並切換模型
        document.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', (event) => { 
                const selectedText = event.target.innerText.trim();
                
                // 讓按鈕顯示 "Mode: Think" 或 "Mode: Fast"
                modeBtn.innerHTML = `Mode: ${selectedText}`; 
                
                if (selectedText === 'Think') {
                    ENVIRONMENT_CONFIG.CURRENT_MODE = 'deepseek-reasoner';
                } else if (selectedText === 'Fast') {
                    ENVIRONMENT_CONFIG.CURRENT_MODE = 'deepseek-chat';
                }
                
                modeDropdown.classList.remove('show'); 
            });
        });

        const addAgentBtn = document.getElementById('addAgentBtn');
        const addProjectBtn = document.getElementById('addProjectBtn');
        const agentList = document.getElementById('agentList');
        const projectList = document.getElementById('projectList');
        const contextMenu = document.getElementById('customContextMenu');
        const deleteOption = document.getElementById('deleteOption');
        let targetLiToDelete = null; 

        function attachEventsToItem(liElement) {
            liElement.addEventListener('click', function() {
                if (this.querySelector('input')) return; 
                const currentText = this.innerText;
                const itemType = this.getAttribute('data-type'); 
                this.innerHTML = `<input type="text" class="edit-input" value="${currentText}">`;
                const input = this.querySelector('input');
                input.select(); 
                const saveText = () => {
                    let newText = input.value.trim();
                    if (newText === '') newText = `untitled ${itemType}`;
                    this.innerHTML = newText;
                };
                input.addEventListener('blur', saveText);
                input.addEventListener('keypress', function(e) { if (e.key === 'Enter') input.blur(); });
            });

            liElement.addEventListener('contextmenu', function(e) {
                e.preventDefault(); 
                targetLiToDelete = this; 
                contextMenu.style.display = 'block';
                contextMenu.style.left = `${e.pageX}px`;
                contextMenu.style.top = `${e.pageY}px`;
            });
        }

        function createNewItem(listElement, itemType) {
            const newLi = document.createElement('li');
            newLi.className = 'editable-item';
            newLi.setAttribute('data-type', itemType);
            newLi.innerText = `untitled ${itemType}`; 
            attachEventsToItem(newLi); 
            listElement.appendChild(newLi); 
        }

        addAgentBtn.addEventListener('click', () => createNewItem(agentList, 'agent'));
        addProjectBtn.addEventListener('click', () => createNewItem(projectList, 'project'));

        document.addEventListener('click', (event) => {
            if (!modeDropdown.contains(event.target) && !modeBtn.contains(event.target)) modeDropdown.classList.remove('show');
            if (event.target !== contextMenu) contextMenu.style.display = 'none';
        });

        deleteOption.addEventListener('click', () => {
            if (targetLiToDelete) { targetLiToDelete.remove(); targetLiToDelete = null; }
        });
        document.querySelectorAll('.editable-item').forEach(li => attachEventsToItem(li));

        // ==========================================
        // 💬 聊天與 DeepSeek API 串接邏輯
        // ==========================================
        const chatInput = document.getElementById('chatInput');
        const chatDisplay = document.getElementById('chatDisplay');

        function appendMessage(text, sender) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `chat-message ${sender}-message`;
            msgDiv.innerText = text;
            chatDisplay.appendChild(msgDiv);
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
            return msgDiv;
        }

        async function callAPI(userMessage) {
            const aiMessageDiv = appendMessage('DeepSeek is thinking...', 'ai');

            try {
                if(ENVIRONMENT_CONFIG.API_KEY.includes('請在這裡貼上')) {
                    throw new Error('請先在程式碼中填寫您的 DeepSeek API Key！');
                }

                const response = await fetch(ENVIRONMENT_CONFIG.API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${ENVIRONMENT_CONFIG.API_KEY}` 
                    },
                    body: JSON.stringify({
                        model: ENVIRONMENT_CONFIG.CURRENT_MODE, 
                        messages: [
                            { role: 'system', content: 'You are a helpful coding assistant.' },
                            { role: 'user', content: userMessage }
                        ]
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(`API 錯誤: ${errorData.error?.message || response.statusText}`);
                }
                
                const data = await response.json();
                const aiReply = data.choices[0].message.content;
                
                // ✅ 1. 使用 marked 解析 Markdown 為 HTML
                aiMessageDiv.innerHTML = marked.parse(aiReply);
                
                // ✅ 2. 針對所有 <pre><code> 區塊執行 Highlight 語法高亮
                aiMessageDiv.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });

            } catch (error) {
                console.error("API Error:", error);
                aiMessageDiv.innerText = `[系統提示] ${error.message}`;
                aiMessageDiv.style.backgroundColor = 'rgba(255, 68, 68, 0.2)'; 
                aiMessageDiv.style.borderLeft = '4px solid var(--danger-color)';
            }
        }

        chatInput.addEventListener('input', function() {
            this.style.height = 'auto'; 
            this.style.height = (this.scrollHeight) + 'px'; 
        });

        chatInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault(); 
                const messageText = this.value.trim(); 
                if (messageText !== '') {
                    appendMessage(messageText, 'user');
                    this.value = '';
                    this.style.height = 'auto';
                    callAPI(messageText);
                }
            }
        });
    </script>
</body>
</html>"""

# ==========================================
# 檔案產出與執行邏輯
# ==========================================
def main():
    # 1. 定義要產生的網頁檔案名稱
    output_filename = "antrocode_ui.html"
    
    # 2. 將變數寫入成實體的 HTML 檔案 (設定 utf-8 確保中文不會亂碼)
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(HTML_TEMPLATE)
        
    print(f"✅ 成功！已經將 HTML 程式碼寫入到 {output_filename} 中。")
    
    # 3. 取得該檔案的絕對路徑，並用預設瀏覽器自動開啟
    file_path = 'file://' + os.path.realpath(output_filename)
    webbrowser.open(file_path)
    print("🌐 正在為您開啟瀏覽器...")

if __name__ == "__main__":
    main()