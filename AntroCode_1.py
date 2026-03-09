import os
import webbrowser

# ==========================================
# 網頁原始碼變數 (加入自訂上下文數量、本地 Token 估算與完善儲存機制) / Web page source code variables (added custom context limit, local Token estimation, and robust storage mechanism)
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
        /* --- 基礎設定與顏色 / Basic settings and colors --- */
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
        .app-container { display: flex; height: 100vh; overflow: hidden; }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-color-main); }
        ::-webkit-scrollbar-thumb { background: #555555; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #777777; }

        /* --- 側邊欄 / Sidebar --- */
        .sidebar { width: 250px; background-color: var(--bg-color-sidebar); padding: 20px; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }
        .sidebar-scroll-area { flex: 1; overflow-y: auto; }
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

        .sidebar-footer { margin-top: auto; padding-top: 15px; border-top: 1px solid var(--border-color); }
        .settings-btn-sidebar { width: 100%; padding: 10px; background: transparent; border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-muted); cursor: pointer; transition: 0.2s; text-align: center; }
        .settings-btn-sidebar:hover { background: var(--bg-color-element); color: var(--text-color); }

        /* --- 右鍵選單 / Context Menu --- */
        .context-menu { display: none; position: absolute; background-color: var(--bg-color-sidebar); border: 1px solid var(--border-color); border-radius: 8px; padding: 5px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.7); z-index: 1000; min-width: 120px; }
        .context-menu-item { padding: 10px 20px; cursor: pointer; color: var(--text-color); font-size: 14px; transition: background 0.2s; }
        .context-menu-item:hover { background-color: var(--bg-color-element); }
        .context-menu-item.danger { color: var(--danger-color); }

        /* --- 主要內容與標頭 / Main Content and Header --- */
        .main-content { flex: 1; display: flex; flex-direction: column; position: relative; min-width: 0; }
        .header { display: flex; justify-content: center; align-items: center; padding: 20px; border-bottom: 1px solid var(--border-color); position: relative; }
        #openSidebar { position: absolute; left: 20px; display: none; }
        .header h2 { font-weight: 500; letter-spacing: 1px; }
        .logo-container { position: absolute; right: 20px; display: flex; align-items: center; }

        /* --- 對話區 / Chat Display Area --- */
        .chat-display { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .chat-message { padding: 12px 16px; border-radius: 12px; line-height: 1.5; word-wrap: break-word; min-width: 0; }
        .user-message { align-self: flex-end; background-color: var(--tech-green); color: #000; border-bottom-right-radius: 2px; white-space: pre-wrap; max-width: 70%; }
        .ai-message { align-self: flex-start; background-color: var(--bg-color-element); color: var(--text-color); border-bottom-left-radius: 2px; width: 100%; max-width: 85%; }
        
        .error-message { border-left: 4px solid var(--danger-color); background-color: rgba(255, 68, 68, 0.1); color: #ffcccc; }
        .error-message p { margin-bottom: 8px; }
        .error-message p:last-child { margin-bottom: 0; }
        
        .ai-message p { margin-bottom: 10px; word-break: break-word; }
        .ai-message p:last-child { margin-bottom: 0; }
        
        .code-container { position: relative; margin: 10px 0; }
        .ai-message pre { background-color: #0d1117; padding: 35px 12px 12px 12px; border-radius: 8px; overflow-x: auto; border: 1px solid #30363d; margin: 0; }
        .ai-message code { font-family: 'Consolas', 'Courier New', monospace; background-color: rgba(0, 0, 0, 0.3); color: var(--tech-green); padding: 2px 4px; border-radius: 4px; word-break: break-word; }
        
        .ai-message pre code { 
            font-family: 'Consolas', 'Courier New', monospace; 
            background-color: transparent; 
            padding: 0; 
            color: #c9d1d9; 
            word-break: normal; 
            font-size: 14px;
        }

        .copy-btn { position: absolute; top: 8px; right: 8px; background: #30363d; border: 1px solid #555; color: #ccc; border-radius: 4px; padding: 4px 10px; font-size: 12px; cursor: pointer; transition: 0.2s; }
        .copy-btn:hover { background: #444; color: #fff; }
        
        .reasoning-block { border-left: 3px solid #555; padding-left: 12px; color: #888; font-style: italic; margin-bottom: 15px; background: rgba(0,0,0,0.15); padding: 10px 12px; border-radius: 0 8px 8px 0; }

        /* --- 輸入區 / Input Area --- */
        .input-area { padding: 20px; display: flex; justify-content: center; }
        .input-box { width: 80%; max-width: 800px; border: 1px solid var(--border-color); border-radius: 12px; display: flex; flex-direction: column; background: var(--bg-color-sidebar); padding: 12px; }
        .input-box textarea { width: 100%; border: none; background: transparent; color: var(--text-color); outline: none; font-size: 16px; padding: 10px; margin-bottom: 10px; resize: none; min-height: 44px; max-height: 150px; overflow-y: auto; }
        .input-box textarea::placeholder { color: var(--text-muted); }
        .input-controls { display: flex; align-items: center; justify-content: space-between; }
        .left-controls { display: flex; align-items: center; gap: 10px; }
        
        .mode-wrapper { position: relative; }
        button.mode-btn { padding: 8px 16px; border: 1px solid var(--border-color); border-radius: 20px; background: var(--bg-color-element); color: var(--text-color); cursor: pointer; font-size: 14px; transition: all 0.2s; }
        button.mode-btn:hover { background: #444; border-color: #666; }
        
        .stop-btn { border-color: var(--danger-color) !important; color: var(--danger-color) !important; display: none; }
        .stop-btn:hover { background: rgba(255, 68, 68, 0.1) !important; }

        .mode-dropdown { display: none; position: absolute; bottom: 110%; left: 0; background-color: var(--bg-color-sidebar); border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; min-width: 150px; box-shadow: 0 -4px 10px rgba(0,0,0,0.5); z-index: 10; }
        .mode-dropdown.show { display: block; }
        .dropdown-item { padding: 10px 15px; cursor: pointer; transition: background 0.2s; text-align: center; }
        .dropdown-item:hover { background-color: var(--bg-color-element); color: var(--tech-green); }
        
        .token-counter { font-size: 13px; color: var(--text-muted); background: var(--bg-color-element); padding: 6px 12px; border-radius: 15px; border: 1px solid var(--border-color); cursor: help; }
        .token-counter span { color: var(--tech-green); font-weight: bold; }

        .empty-state { text-align: center; color: var(--text-muted); margin-top: 50px; font-style: italic; }

        /* --- 設定彈窗 (Modal) / Settings Modal --- */
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 2000; justify-content: center; align-items: center; }
        .modal-content { background: var(--bg-color-sidebar); padding: 25px; border-radius: 12px; width: 420px; border: 1px solid var(--border-color); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .modal-content h3 { margin-bottom: 15px; color: var(--text-color); }
        .setting-group { margin-bottom: 15px; }
        .setting-group label { display: block; font-size: 13px; color: var(--text-muted); margin-bottom: 8px; }
        .modal-input { width: 100%; padding: 10px; background: var(--bg-color-element); border: 1px solid var(--border-color); color: var(--text-color); border-radius: 6px; outline: none; }
        .modal-input:focus { border-color: var(--tech-green); }
        
        /* 新增：資料管理區域樣式 / Added: Data management area styles */
        .data-management { margin-top: 20px; padding-top: 15px; border-top: 1px solid var(--border-color); display: flex; gap: 8px; flex-wrap: wrap; justify-content: space-between; }
        .data-btn { flex: 1; padding: 8px; background: var(--bg-color-element); border: 1px solid var(--border-color); color: var(--text-color); border-radius: 6px; cursor: pointer; font-size: 12px; transition: 0.2s; text-align: center; }
        .data-btn:hover { background: #444; }
        .data-btn.danger { color: var(--danger-color); border-color: rgba(255, 68, 68, 0.3); }
        .data-btn.danger:hover { background: rgba(255, 68, 68, 0.1); }

        .modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
        .modal-actions button { padding: 8px 15px; border: none; border-radius: 6px; cursor: pointer; }
        .btn-cancel { background: transparent; color: var(--text-muted); }
        .btn-cancel:hover { color: var(--text-color); }
        .btn-save { background: var(--tech-green); color: #000; font-weight: bold; }
        .btn-save:hover { opacity: 0.8; }
    </style>
</head>
<body>
    <div class="app-container">
        <aside class="sidebar" id="sidebar">
            <div class="menu-icon" id="closeSidebar">☰</div>
            <div class="sidebar-scroll-area">
                <div class="sidebar-section">
                    <div class="section-header"><h3>Agent</h3><button class="add-btn" onclick="createNewItem('agent')">+</button></div>
                    <ul id="agentList"></ul>
                </div>
                <div class="sidebar-section">
                    <div class="section-header"><h3>Project</h3><button class="add-btn" onclick="createNewItem('project')">+</button></div>
                    <ul id="projectList"></ul>
                </div>
            </div>
            <div class="sidebar-footer">
                <button class="settings-btn-sidebar" id="openSettingsBtn">⚙️ Settings</button>
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
            
            <div class="chat-display" id="chatDisplay"></div>
            
            <div class="input-area">
                <div class="input-box">
                    <textarea id="chatInput" placeholder="Ask me anything..." rows="1"></textarea>
                    <div class="input-controls">
                        <div class="left-controls">
                            <div class="mode-wrapper">
                                <button class="mode-btn" id="modeBtn">Mode: Think</button>
                                <div class="mode-dropdown" id="modeDropdown">
                                    <div class="dropdown-item">Think</div>
                                    <div class="dropdown-item">Fast</div>
                                </div>
                            </div>
                            <button class="mode-btn stop-btn" id="stopBtn">⏹️ Stop</button>
                            <div class="token-counter" id="tokenCounter" title="Total tokens used in this workspace">
                                🪙 Tokens: <span id="tokenValue">0</span>
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

    <div class="modal-overlay" id="settingsModal">
        <div class="modal-content">
            <h3>⚙️ Settings & Data</h3>
            <div class="setting-group">
                <label>DeepSeek API Key (Stored Locally):</label>
                <input type="password" id="apiKeyInput" class="modal-input" placeholder="sk-...">
            </div>
            <div class="setting-group">
                <label>Context History Limit (Messages to send):</label>
                <input type="number" id="contextLimitInput" class="modal-input" placeholder="15" min="1" max="100">
            </div>
            
            <div class="data-management">
                <button class="data-btn" id="exportDataBtn">📥 導出備份 / Export</button>
                <button class="data-btn" onclick="document.getElementById('importFileInput').click()">📤 導入還原 / Import</button>
                <input type="file" id="importFileInput" style="display: none;" accept=".json">
                <button class="data-btn danger" id="clearDataBtn">🗑️ 清除全部 / Clear All</button>
            </div>

            <div class="modal-actions">
                <button class="btn-cancel" id="closeModalBtn">Cancel</button>
                <button class="btn-save" id="saveKeyBtn">Save</button>
            </div>
        </div>
    </div>

    <script>
        const ENVIRONMENT_CONFIG = {
            API_URL: 'https://api.deepseek.com/chat/completions', 
            CURRENT_MODE: 'deepseek-reasoner'
        };

        function getSettings() {
            return {
                apiKey: localStorage.getItem('antrocode_api_key') || '',
                contextLimit: parseInt(localStorage.getItem('antrocode_context_limit')) || 15
            };
        }
        function saveSettings(key, limit) {
            localStorage.setItem('antrocode_api_key', key.trim());
            localStorage.setItem('antrocode_context_limit', limit);
        }

        // ==========================================
        // 💾 狀態管理防呆與資料保護修復 / State management fallback and data protection fixes
        // ==========================================
        const STORAGE_KEY = 'antrocode_local_state_v3'; // 更新版本號確保乾淨狀態 / Update version number to ensure clean state
        
        const defaultState = {
            items: [
                { id: 'agent-1', type: 'agent', name: 'Agent 1' },
                { id: 'proj-1', type: 'project', name: 'Project 1' }
            ],
            chats: {
                'agent-1': [{ role: 'ai', content: 'System Ready. Switched to workspace **Agent 1**.' }],
                'proj-1': [{ role: 'ai', content: 'System Ready. Switched to workspace **Project 1**.' }]
            },
            tokens: { 'agent-1': 0, 'proj-1': 0 },
            activeId: 'agent-1'
        };

        let appState;

        // 修復 1: 防止 JSON 解析損壞導致白畫面 / Fix 1: Prevent white screen caused by corrupted JSON parsing
        try {
            const savedData = localStorage.getItem(STORAGE_KEY);
            appState = savedData ? JSON.parse(savedData) : defaultState;
            
            // 防呆驗證資料結構 / Fallback validation of data structure
            if (!appState || typeof appState !== 'object') throw new Error("Invalid state structure");
            if (!appState.tokens) appState.tokens = {};
            if (!appState.chats) appState.chats = {};
            if (!Array.isArray(appState.items)) appState.items = [];
        } catch (error) {
            console.error("讀取歷史紀錄失敗，已重置狀態 / Failed to read history, state reset:", error);
            appState = JSON.parse(JSON.stringify(defaultState)); // 深度拷貝預設狀態 / Deep copy default state
        }

        // 修復 2: 攔截儲存空間不足 (QuotaExceededError) 的崩潰 / Fix 2: Intercept storage space full crash
        function saveState() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
            } catch (error) {
                if (error.name === 'QuotaExceededError' || error.name === 'NS_ERROR_DOM_QUOTA_REACHED') {
                    alert('⚠️ 系統提示：您的本地儲存空間已滿！請刪除一些舊的專案或對話，或導出備份後清除空間。\nSystem Notice: Local storage is full! Please delete some items or export backup and clear space.');
                } else {
                    console.error('儲存狀態時發生未知錯誤 / Unknown error while saving state:', error);
                }
            }
        }

        function generateId(prefix) {
            return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).substr(2, 5)}`;
        }

        function estimateTokensLocally(messagesArray, generatedText) {
            let totalText = messagesArray.map(m => m.content).join(" ") + generatedText;
            return Math.ceil(totalText.length * 1.5);
        }

        // ==========================================
        // 🎨 UI 渲染與 API 邏輯維持不變... / UI rendering and API logic remain unchanged...
        // ==========================================
        const agentList = document.getElementById('agentList');
        const projectList = document.getElementById('projectList');
        const chatDisplay = document.getElementById('chatDisplay');
        const headerTitle = document.getElementById('mainHeaderTitle');
        const contextMenu = document.getElementById('customContextMenu');
        const tokenValueDisplay = document.getElementById('tokenValue');
        const tokenCounterDiv = document.getElementById('tokenCounter');
        const stopBtn = document.getElementById('stopBtn');
        const chatInput = document.getElementById('chatInput');
        
        let targetIdToModify = null;
        let currentAbortController = null;

        function renderSidebar() {
            agentList.innerHTML = '';
            projectList.innerHTML = '';

            appState.items.forEach(item => {
                const li = document.createElement('li');
                li.innerText = item.name; // 這裡使用 innerText 防範 XSS 攻擊 / Uses innerText to prevent XSS attacks
                li.dataset.id = item.id;
                
                if (item.id === appState.activeId) li.classList.add('active-tab');

                li.addEventListener('click', (e) => {
                    if (e.target.tagName === 'INPUT') return;
                    appState.activeId = item.id;
                    saveState();
                    renderSidebar(); 
                    renderChat();    
                });

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

        function attachCopyButtons(container) {
            container.querySelectorAll('pre').forEach(pre => {
                if(pre.querySelector('.copy-btn')) return; 
                const wrapper = document.createElement('div');
                wrapper.className = 'code-container';
                pre.parentNode.insertBefore(wrapper, pre);
                wrapper.appendChild(pre);

                const btn = document.createElement('button');
                btn.className = 'copy-btn';
                btn.innerText = 'Copy';
                btn.onclick = () => {
                    const code = pre.querySelector('code');
                    if(code) {
                        navigator.clipboard.writeText(code.innerText).then(() => {
                            btn.innerText = 'Copied!';
                            btn.style.color = 'var(--tech-green)';
                            setTimeout(() => { btn.innerText = 'Copy'; btn.style.color = '#ccc'; }, 2000);
                        });
                    }
                };
                wrapper.appendChild(btn);
            });
        }

        function renderChat() {
            chatDisplay.innerHTML = '';
            
            if (!appState.activeId) {
                headerTitle.innerText = 'AntroCode';
                chatDisplay.innerHTML = '<div class="empty-state">No workspace selected.</div>';
                tokenValueDisplay.innerText = "0";
                return;
            }

            const activeItem = appState.items.find(i => i.id === appState.activeId);
            if(activeItem) headerTitle.innerText = `AntroCode - ${activeItem.name}`;
            
            tokenValueDisplay.innerText = (appState.tokens[appState.activeId] || 0).toLocaleString();

            const history = appState.chats[appState.activeId] || [];

            history.forEach(msg => {
                const msgDiv = document.createElement('div');
                msgDiv.className = `chat-message ${msg.role === 'user' ? 'user' : 'ai'}-message`;
                
                if (msg.role === 'error') {
                    msgDiv.className = 'chat-message ai-message error-message';
                    msgDiv.innerHTML = marked.parse(msg.content);
                } else if (msg.role === 'user') {
                    msgDiv.innerText = msg.content;
                } else {
                    let finalHTML = "";
                    if (msg.reasoning) {
                        finalHTML += `<div class="reasoning-block">${marked.parse(msg.reasoning)}</div>`;
                    }
                    finalHTML += marked.parse(msg.content);
                    msgDiv.innerHTML = finalHTML;
                    msgDiv.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
                    attachCopyButtons(msgDiv);
                }
                chatDisplay.appendChild(msgDiv);
            });
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
        }

        async function callAPI(userMessage) {
            const userSettings = getSettings();
            if (!userSettings.apiKey) {
                openSettingsModal();
                return;
            }
            if (!appState.activeId) return;

            const requestTabId = appState.activeId;
            if (!appState.chats[requestTabId]) appState.chats[requestTabId] = [];
            
            appState.chats[requestTabId].push({ role: 'user', content: userMessage });
            saveState();

            let currentAiMessage = { role: 'ai', content: '', reasoning: '' };
            let msgDiv = null;

            if (appState.activeId === requestTabId) {
                renderChat(); 
                msgDiv = document.createElement('div');
                msgDiv.className = 'chat-message ai-message';
                msgDiv.innerHTML = '<span style="color:var(--text-muted); font-style:italic;">DeepSeek is thinking...</span>';
                chatDisplay.appendChild(msgDiv);
                chatDisplay.scrollTop = chatDisplay.scrollHeight;
            }

            currentAbortController = new AbortController();
            stopBtn.style.display = 'block';

            const rawHistory = appState.chats[requestTabId].filter(m => m.role === 'user' || m.role === 'ai');
            const recentHistory = rawHistory.slice(-userSettings.contextLimit);

            const apiMessages = [
                { role: 'system', content: 'You are a helpful coding assistant.' },
                ...recentHistory.map(m => ({ role: m.role === 'ai' ? 'assistant' : 'user', content: m.content }))
            ];

            try {
                const response = await fetch(ENVIRONMENT_CONFIG.API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${userSettings.apiKey}` },
                    body: JSON.stringify({ 
                        model: ENVIRONMENT_CONFIG.CURRENT_MODE, 
                        messages: apiMessages,
                        stream: true, 
                        stream_options: { include_usage: true } 
                    }),
                    signal: currentAbortController.signal 
                });

                if (!response.ok) {
                    throw new Error(`伺服器拒絕了請求 (狀態碼：${response.status}) / Server rejected the request (Status Code: ${response.status}) - ${response.statusText}`);
                }
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let done = false;
                let buffer = ""; 

                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    done = readerDone;
                    if (value) {
                        buffer += decoder.decode(value, { stream: true });
                        let lines = buffer.split('\n');
                        buffer = lines.pop();

                        for (let line of lines) {
                            if (line.trim() === '') continue;
                            if (line.startsWith('data: ')) {
                                const dataStr = line.slice(6);
                                if (dataStr === '[DONE]') break;
                                
                                try {
                                    const data = JSON.parse(dataStr);
                                    
                                    if (data.usage) {
                                        appState.tokens[requestTabId] = (appState.tokens[requestTabId] || 0) + data.usage.total_tokens;
                                        if (appState.activeId === requestTabId) {
                                            tokenValueDisplay.innerText = appState.tokens[requestTabId].toLocaleString();
                                        }
                                        continue;
                                    }

                                    const delta = data.choices[0].delta;
                                    if (delta.reasoning_content) currentAiMessage.reasoning += delta.reasoning_content;
                                    if (delta.content) currentAiMessage.content += delta.content;

                                    if (appState.activeId === requestTabId && msgDiv) {
                                        let tempHTML = "";
                                        if (currentAiMessage.reasoning) tempHTML += `<div class="reasoning-block">${marked.parse(currentAiMessage.reasoning)}</div>`;
                                        tempHTML += marked.parse(currentAiMessage.content || "...");
                                        msgDiv.innerHTML = tempHTML;
                                        chatDisplay.scrollTop = chatDisplay.scrollHeight;
                                    }
                                } catch (e) { console.warn("Parse warn:", e); }
                            }
                        }
                    }
                }

                if (appState.activeId === requestTabId && msgDiv) {
                    msgDiv.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
                    attachCopyButtons(msgDiv);
                }

                appState.chats[requestTabId].push(currentAiMessage);
                saveState();

            } catch (error) {
                if (error.name === 'AbortError') {
                    currentAiMessage.content += "\n\n*(生成已由使用者中斷 / Generation aborted by user)*";
                    appState.chats[requestTabId].push(currentAiMessage);
                    
                    let estimatedCost = estimateTokensLocally(apiMessages, currentAiMessage.reasoning + currentAiMessage.content);
                    appState.tokens[requestTabId] = (appState.tokens[requestTabId] || 0) + estimatedCost;
                    
                    if (appState.activeId === requestTabId && msgDiv) {
                        let finalHTML = currentAiMessage.reasoning ? `<div class="reasoning-block">${marked.parse(currentAiMessage.reasoning)}</div>` : "";
                        finalHTML += marked.parse(currentAiMessage.content);
                        msgDiv.innerHTML = finalHTML;
                        msgDiv.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
                        attachCopyButtons(msgDiv);
                        chatDisplay.scrollTop = chatDisplay.scrollHeight;
                        tokenValueDisplay.innerText = appState.tokens[requestTabId].toLocaleString() + " (Est.)";
                    }
                    saveState();
                } else {
                    const friendlyErrorMsg = `**發生了一些錯誤。 / Something went wrong.**\n我們無法完成您的請求，這可能是因為網路不穩、API 金鑰失效或伺服器繁忙。\n\n*系統提示 / System Details: \`${error.message}\`*`;
                    appState.chats[requestTabId].push({ role: 'error', content: friendlyErrorMsg });
                    saveState();
                    if (appState.activeId === requestTabId) renderChat();
                }
            } finally {
                stopBtn.style.display = 'none';
                currentAbortController = null;
            }
        }

        // ==========================================
        // 互動綁定區 / Interaction bindings
        // ==========================================
        window.createNewItem = function(type) {
            const newId = generateId(type);
            appState.items.push({ id: newId, type: type, name: `untitled ${type}` });
            appState.chats[newId] = [{ role: 'ai', content: `Workspace created. Start typing to interact.` }];
            appState.tokens[newId] = 0;
            appState.activeId = newId; 
            saveState();
            renderSidebar();
            renderChat();
        };

        document.addEventListener('click', (event) => { if (event.target !== contextMenu) contextMenu.style.display = 'none'; });

        document.getElementById('renameOption').addEventListener('click', () => {
            if (!targetIdToModify) return;
            const li = document.querySelector(`li[data-id="${targetIdToModify}"]`);
            if (!li) return;

            const item = appState.items.find(i => i.id === targetIdToModify);
            li.innerHTML = `<input type="text" class="edit-input" value="">`;
            const input = li.querySelector('input');
            input.value = item.name; // 防範 XSS
            input.select();

            const saveNewName = () => {
                item.name = input.value.trim() || `untitled ${item.type}`;
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
            delete appState.tokens[targetIdToModify];

            if (appState.activeId === targetIdToModify) {
                appState.activeId = appState.items.length > 0 ? appState.items[0].id : null;
            }
            saveState();
            renderSidebar();
            renderChat();
            contextMenu.style.display = 'none';
        });

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

        stopBtn.addEventListener('click', () => { if (currentAbortController) currentAbortController.abort(); });
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
        document.addEventListener('click', () => { modeDropdown.classList.remove('show'); });

        // ==========================================
        // 設定與資料管理 Modal 邏輯 / Settings and Data Management Modal logic
        // ==========================================
        const modal = document.getElementById('settingsModal');
        const openSettingsBtn = document.getElementById('openSettingsBtn');
        const closeModalBtn = document.getElementById('closeModalBtn');
        const saveKeyBtn = document.getElementById('saveKeyBtn');
        const apiKeyInput = document.getElementById('apiKeyInput');
        const contextLimitInput = document.getElementById('contextLimitInput');

        function openSettingsModal() {
            const currentSettings = getSettings();
            apiKeyInput.value = currentSettings.apiKey;
            contextLimitInput.value = currentSettings.contextLimit;
            modal.style.display = 'flex';
        }
        
        openSettingsBtn.addEventListener('click', openSettingsModal);
        closeModalBtn.addEventListener('click', () => { modal.style.display = 'none'; });
        saveKeyBtn.addEventListener('click', () => {
            const key = apiKeyInput.value.trim();
            const limit = parseInt(contextLimitInput.value) || 15;
            if(key) {
                saveSettings(key, limit);
                modal.style.display = 'none';
            } else {
                alert('系統提示：請輸入有效的 API 金鑰才能開始對話喔！\nSystem Notice: Please enter a valid API Key to start the conversation!');
            }
        });

        // 修復 3: 實作導出、導入與清空資料的功能 / Fix 3: Implement Export, Import, and Clear data features
        document.getElementById('exportDataBtn').addEventListener('click', () => {
            const dataStr = JSON.stringify(appState, null, 2);
            const blob = new Blob([dataStr], { type: "application/json" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `antrocode_backup_${new Date().toISOString().slice(0,10)}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });

        document.getElementById('importFileInput').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(event) {
                try {
                    const importedData = JSON.parse(event.target.result);
                    if (importedData.items && importedData.chats) {
                        appState = importedData;
                        saveState();
                        renderSidebar();
                        renderChat();
                        alert('✅ 資料導入成功！/ Data imported successfully!');
                        modal.style.display = 'none';
                    } else {
                        throw new Error('格式不正確 / Invalid format');
                    }
                } catch (err) {
                    alert('❌ 導入失敗，檔案格式不正確！/ Import failed, invalid file format!');
                }
            };
            reader.readAsText(file);
            e.target.value = ''; // 允許重複導入同個檔案 / Allow re-importing the same file
        });

        document.getElementById('clearDataBtn').addEventListener('click', () => {
            if(confirm('⚠️ 警告！這將會永久刪除您所有的對話紀錄與專案。確定要清除嗎？\nWARNING! This will permanently delete all your chat history and projects. Are you sure?')) {
                localStorage.removeItem(STORAGE_KEY);
                appState = JSON.parse(JSON.stringify(defaultState));
                saveState();
                renderSidebar();
                renderChat();
                modal.style.display = 'none';
            }
        });

        // 啟動應用程式 / Start the application
        renderSidebar();
        renderChat();

    </script>
</body>
</html>"""

def main():
    output_filename = "antrocode_ui_pro_max.html"
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(HTML_TEMPLATE)
    print(f"✅ 成功！已經將具備【完善防呆儲存機制】與【資料管理中心】的 HTML 寫入到 {output_filename} 中。")
    file_path = 'file://' + os.path.realpath(output_filename)
    webbrowser.open(file_path)
    print("🌐 正在為您開啟瀏覽器...")

if __name__ == "__main__":
    main()
