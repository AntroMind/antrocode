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
        /* --- 基礎設定與顏色 --- */
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

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-color-main); }
        ::-webkit-scrollbar-thumb { background: #555555; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #777777; }

        /* --- 側邊欄 --- */
        .sidebar { width: 250px; background-color: var(--bg-color-sidebar); padding: 20px; border-right: 1px solid var(--border-color); overflow-y: auto; display: flex; flex-direction: column; }
        .menu-icon { font-size: 24px; cursor: pointer; color: var(--text-muted); transition: color 0.2s; margin-bottom: 20px; }
        .menu-icon:hover { color: var(--text-color); }
        .sidebar-section { margin-top: 20px; }
        .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .section-header h3 { color: var(--text-muted); font-size: 14px; text-transform: uppercase; margin: 0; }
        .add-btn { background: transparent; border: none; color: var(--tech-green); font-size: 20px; cursor: pointer; transition: transform 0.2s; }
        .add-btn:hover { transform: scale(1.2); }
        .sidebar-section ul { list-style: none; }
        
        .sidebar-section li { 
            padding: 8px 12px; 
            border: 1px solid var(--border-color); 
            margin: 8px 0; 
            border-radius: 8px; 
            text-align: center; 
            background: var(--bg-color-element); 
            cursor: pointer; 
            transition: all 0.2s; 
            border-left: 4px solid transparent; 
            position: relative;
        }
        .sidebar-section li:hover { background: #3a3a3a; }
        .sidebar-section li.active-tab { border-left-color: var(--tech-green); background: #333; }
        .edit-input { width: 100%; background: transparent; border: none; color: var(--text-color); text-align: center; outline: none; font-size: 16px; border-bottom: 1px solid var(--tech-green); }

        /* --- 右鍵選單 --- */
        .context-menu { display: none; position: absolute; background-color: var(--bg-color-sidebar); border: 1px solid var(--border-color); border-radius: 8px; padding: 5px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.7); z-index: 1000; min-width: 120px; }
        .context-menu-item { padding: 10px 20px; cursor: pointer; color: var(--text-color); font-size: 14px; transition: background 0.2s; }
        .context-menu-item:hover { background-color: var(--bg-color-element); }
        .context-menu-item.danger { color: var(--danger-color); }

        /* --- 主要內容與標頭 --- */
        .main-content { flex: 1; display: flex; flex-direction: column; position: relative; min-width: 0; }
        .header { display: flex; justify-content: center; align-items: center; padding: 20px; border-bottom: 1px solid var(--border-color); position: relative; }
        #openSidebar { position: absolute; left: 20px; display: none; }
        .header h2 { font-weight: 500; letter-spacing: 1px; }
        .logo-container { position: absolute; right: 20px; display: flex; align-items: center; }

        /* --- 對話區 --- */
        .chat-display { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .chat-message { padding: 12px 16px; border-radius: 12px; line-height: 1.5; word-wrap: break-word; min-width: 0; }
        .user-message { align-self: flex-end; background-color: var(--tech-green); color: #000; border-bottom-right-radius: 2px; white-space: pre-wrap; max-width: 70%; }
        .ai-message { align-self: flex-start; background-color: var(--bg-color-element); color: var(--text-color); border-bottom-left-radius: 2px; width: 100%; max-width: 85%; }
        .error-message { border-left: 4px solid var(--danger-color); background-color: rgba(255, 68, 68, 0.1); }
        
        .ai-message p { margin-bottom: 10px; word-break: break-word; }
        .ai-message p:last-child { margin-bottom: 0; }
        .ai-message pre { background-color: #0d1117; padding: 12px; border-radius: 8px; overflow-x: auto; max-width: 100%; margin: 10px 0; border: 1px solid #30363d; }
        .ai-message code { font-family: 'Consolas', 'Courier New', monospace; background-color: rgba(0, 0, 0, 0.3); color: var(--tech-green); padding: 2px 4px; border-radius: 4px; word-break: break-word; }
        .ai-message pre code { background-color: transparent; padding: 0; color: inherit; word-break: normal; }

        /* --- 輸入區 --- */
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
        
        .empty-state { text-align: center; color: var(--text-muted); margin-top: 50px; font-style: italic; }
    </style>
</head>
<body>
    <div class="app-container">
        <aside class="sidebar" id="sidebar">
            <div class="menu-icon" id="closeSidebar">☰</div>
            <div class="sidebar-section">
                <div class="section-header"><h3>Agent</h3><button class="add-btn" onclick="createNewItem('agent')">+</button></div>
                <ul id="agentList"></ul>
            </div>
            <div class="sidebar-section">
                <div class="section-header"><h3>Project</h3><button class="add-btn" onclick="createNewItem('project')">+</button></div>
                <ul id="projectList"></ul>
            </div>
        </aside>

        <main class="main-content">
            <header class="header">
                <div class="menu-icon" id="openSidebar">☰</div>
                <h2 id="mainHeaderTitle">AntroCode</h2>
                <div class="logo-container">
                    <svg width="40" height="40" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <path d="M50 5 C50 40 60 50 95 50 C60 50 50 60 50 95 C50 60 40 50 5 50 C40 50 50 40 50 5 Z" fill="var(--tech-green)" />
                    </svg>
                </div>
            </header>
            
            <div class="chat-display" id="chatDisplay">
                </div>
            
            <div class="input-area">
                <div class="input-box">
                    <textarea id="chatInput" placeholder="Ask me anything..." rows="1"></textarea>
                    <div class="input-controls">
                        <div class="mode-wrapper">
                            <button class="mode-btn" id="modeBtn">Mode: Think</button>
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
        <div class="context-menu-item" id="renameOption">✏️ Rename</div>
        <div class="context-menu-item danger" id="deleteOption">🗑️ Delete</div>
    </div>

    <script>
        // ==========================================
        // API 設定 (請填入真實 Key)
        // ==========================================
        const ENVIRONMENT_CONFIG = {
            API_URL: 'https://api.deepseek.com/chat/completions', 
            API_KEY: 'sk-請在這裡貼上你的_真實_DEEPSEEK_API_KEY', 
            CURRENT_MODE: 'deepseek-reasoner' 
        };

        // ==========================================
        // 💾 Local Storage 狀態管理系統
        // ==========================================
        const STORAGE_KEY = 'antrocode_local_state';
        
        // 預設資料 (如果第一次開啟)
        const defaultState = {
            items: [
                { id: 'agent-1', type: 'agent', name: 'Agent 1' },
                { id: 'proj-1', type: 'project', name: 'Project 1' }
            ],
            chats: {
                'agent-1': [{ role: 'ai', content: 'System Ready. Switched to workspace **Agent 1**.' }],
                'proj-1': [{ role: 'ai', content: 'System Ready. Switched to workspace **Project 1**.' }]
            },
            activeId: 'agent-1'
        };

        // 讀取資料或使用預設值
        let appState = JSON.parse(localStorage.getItem(STORAGE_KEY)) || defaultState;

        function saveState() {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
        }

        function generateId(prefix) {
            return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).substr(2, 5)}`;
        }

        // ==========================================
        // 🎨 UI 渲染與互動邏輯
        // ==========================================
        const agentList = document.getElementById('agentList');
        const projectList = document.getElementById('projectList');
        const chatDisplay = document.getElementById('chatDisplay');
        const headerTitle = document.getElementById('mainHeaderTitle');
        const contextMenu = document.getElementById('customContextMenu');
        
        let targetIdToModify = null;

        // 1. 渲染側邊欄清單
        function renderSidebar() {
            agentList.innerHTML = '';
            projectList.innerHTML = '';

            appState.items.forEach(item => {
                const li = document.createElement('li');
                li.innerText = item.name;
                li.dataset.id = item.id;
                
                if (item.id === appState.activeId) {
                    li.classList.add('active-tab');
                }

                // 左鍵：切換分頁
                li.addEventListener('click', (e) => {
                    if (e.target.tagName === 'INPUT') return;
                    appState.activeId = item.id;
                    saveState();
                    renderSidebar(); 
                    renderChat();    
                });

                // 右鍵：開啟選單
                li.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    targetIdToModify = item.id;
                    contextMenu.style.display = 'block';
                    contextMenu.style.left = `${e.pageX}px`;
                    contextMenu.style.top = `${e.pageY}px`;
                });

                if (item.type === 'agent') agentList.appendChild(li);
                else projectList.appendChild(li);
            });
        }

        // 2. 渲染對話區
        function renderChat() {
            chatDisplay.innerHTML = '';
            
            if (!appState.activeId) {
                headerTitle.innerText = 'AntroCode';
                chatDisplay.innerHTML = '<div class="empty-state">No workspace selected. Create an Agent or Project to start.</div>';
                return;
            }

            const activeItem = appState.items.find(i => i.id === appState.activeId);
            if(activeItem) headerTitle.innerText = `AntroCode - ${activeItem.name}`;

            const history = appState.chats[appState.activeId] || [];
            history.forEach(msg => {
                const msgDiv = document.createElement('div');
                msgDiv.className = `chat-message ${msg.role === 'user' ? 'user' : 'ai'}-message`;
                
                // 標記錯誤訊息的樣式
                if (msg.role === 'error') {
                    msgDiv.className = 'chat-message ai-message error-message';
                    msgDiv.innerText = msg.content;
                } else if (msg.role === 'user') {
                    msgDiv.innerText = msg.content;
                } else {
                    msgDiv.innerHTML = marked.parse(msg.content);
                    msgDiv.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
                }
                chatDisplay.appendChild(msgDiv);
            });
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
        }

        // 3. 新增項目
        window.createNewItem = function(type) {
            const newId = generateId(type);
            const newItem = { id: newId, type: type, name: `untitled ${type}` };
            
            appState.items.push(newItem);
            appState.chats[newId] = [{ role: 'ai', content: `Workspace created. Start typing to interact.` }];
            appState.activeId = newId; 
            
            saveState();
            renderSidebar();
            renderChat();
        };

        // ==========================================
        // 右鍵選單操作 (改名 / 刪除)
        // ==========================================
        document.addEventListener('click', (event) => {
            if (event.target !== contextMenu) contextMenu.style.display = 'none';
        });

        document.getElementById('renameOption').addEventListener('click', () => {
            if (!targetIdToModify) return;
            const li = document.querySelector(`li[data-id="${targetIdToModify}"]`);
            if (!li) return;

            const item = appState.items.find(i => i.id === targetIdToModify);
            li.innerHTML = `<input type="text" class="edit-input" value="${item.name}">`;
            const input = li.querySelector('input');
            input.select();

            const saveNewName = () => {
                let newName = input.value.trim() || `untitled ${item.type}`;
                item.name = newName;
                saveState();
                renderSidebar();
                if (appState.activeId === targetIdToModify) renderChat(); 
            };

            input.addEventListener('blur', saveNewName);
            input.addEventListener('keypress', e => { if (e.key === 'Enter') input.blur(); });
            contextMenu.style.display = 'none';
        });

        document.getElementById('deleteOption').addEventListener('click', () => {
            if (!targetIdToModify) return;
            
            appState.items = appState.items.filter(i => i.id !== targetIdToModify);
            delete appState.chats[targetIdToModify];

            if (appState.activeId === targetIdToModify) {
                appState.activeId = appState.items.length > 0 ? appState.items[0].id : null;
            }

            saveState();
            renderSidebar();
            renderChat();
            contextMenu.style.display = 'none';
        });

        // ==========================================
        // 💬 非同步聊天與 API 串接邏輯 (已修復切換分頁問題)
        // ==========================================
        const chatInput = document.getElementById('chatInput');

        async function callAPI(userMessage) {
            if (!appState.activeId) return;

            // 死死記住是哪一個分頁發起的請求
            const requestTabId = appState.activeId;

            // 將使用者訊息存入該分頁的狀態並重新渲染
            appState.chats[requestTabId].push({ role: 'user', content: userMessage });
            saveState();

            // 如果目前還停留在發問的分頁，立刻更新畫面並顯示 Loading
            if (appState.activeId === requestTabId) {
                renderChat();
                const thinkingDiv = document.createElement('div');
                thinkingDiv.id = 'thinking-indicator';
                thinkingDiv.className = 'chat-message ai-message';
                thinkingDiv.innerText = 'DeepSeek is thinking...';
                chatDisplay.appendChild(thinkingDiv);
                chatDisplay.scrollTop = chatDisplay.scrollHeight;
            }

            try {
                if(ENVIRONMENT_CONFIG.API_KEY.includes('請在這裡貼上')) throw new Error('請先填寫 DeepSeek API Key！');

                // 組合歷史訊息 (過濾掉系統錯誤提示，只送乾淨的對話)
                const apiMessages = [
                    { role: 'system', content: 'You are a helpful coding assistant.' },
                    ...appState.chats[requestTabId]
                        .filter(m => m.role === 'user' || m.role === 'ai')
                        .map(m => ({ role: m.role === 'ai' ? 'assistant' : 'user', content: m.content }))
                ];

                const response = await fetch(ENVIRONMENT_CONFIG.API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${ENVIRONMENT_CONFIG.API_KEY}` },
                    body: JSON.stringify({ model: ENVIRONMENT_CONFIG.CURRENT_MODE, messages: apiMessages })
                });

                if (!response.ok) throw new Error(`API 錯誤: ${response.statusText}`);
                
                const data = await response.json();
                const aiResponseText = data.choices[0].message.content;

                // 🌟 把回覆精準存回「當初發問的分頁」歷史紀錄中
                appState.chats[requestTabId].push({ role: 'ai', content: aiResponseText });
                saveState();

                // 🌟 如果你剛好還停留在該分頁，才重新渲染畫面；如果切走了，就在背景默默存好
                if (appState.activeId === requestTabId) {
                    renderChat();
                }

            } catch (error) {
                // 如果發生錯誤，一樣存進當初的分頁
                appState.chats[requestTabId].push({ role: 'error', content: `[系統錯誤] ${error.message}` });
                saveState();
                
                if (appState.activeId === requestTabId) {
                    renderChat();
                }
            }
        }

        chatInput.addEventListener('input', function() { this.style.height = 'auto'; this.style.height = (this.scrollHeight) + 'px'; });
        chatInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault(); 
                const messageText = this.value.trim(); 
                if (messageText !== '' && appState.activeId) { 
                    this.value = ''; 
                    this.style.height = 'auto'; 
                    callAPI(messageText); 
                }
            }
        });

        // UI 雜項控制 (側邊欄開關、Mode 切換)
        document.getElementById('closeSidebar').addEventListener('click', () => { document.getElementById('sidebar').style.display = 'none'; document.getElementById('openSidebar').style.display = 'block'; });
        document.getElementById('openSidebar').addEventListener('click', () => { document.getElementById('sidebar').style.display = 'flex'; document.getElementById('openSidebar').style.display = 'none'; });
        
        const modeBtn = document.getElementById('modeBtn');
        const modeDropdown = document.getElementById('modeDropdown');
        modeBtn.addEventListener('click', (e) => { modeDropdown.classList.toggle('show'); e.stopPropagation(); });
        document.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', (e) => { 
                const selected = e.target.innerText.trim();
                modeBtn.innerHTML = `Mode: ${selected}`; 
                ENVIRONMENT_CONFIG.CURRENT_MODE = selected === 'Think' ? 'deepseek-reasoner' : 'deepseek-chat';
                modeDropdown.classList.remove('show'); 
            });
        });

        // 啟動應用程式
        renderSidebar();
        renderChat();

    </script>
</body>
</html>"""

# ==========================================
# 檔案產出與執行邏輯
# ==========================================
def main():
    output_filename = "antrocode_ui.html"
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(HTML_TEMPLATE)
    print(f"✅ 成功！已經將 HTML 程式碼寫入到 {output_filename} 中。")
    file_path = 'file://' + os.path.realpath(output_filename)
    webbrowser.open(file_path)
    print("🌐 正在為您開啟瀏覽器...")

if __name__ == "__main__":
    main()
