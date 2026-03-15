import os
import webbrowser
import time

# ==========================================
# AntroCode - 100% Single-File AI Client
# ==========================================
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AntroCode - Local Environment</title>
    
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

    <style>
        /* --- Basic variables and color palette --- */
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

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background-color: var(--bg-color-main); color: var(--text-color); }
        .app-container { display: flex; height: 100vh; overflow: hidden; }

        /* --- Custom Scrollbar --- */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-color-main); }
        ::-webkit-scrollbar-thumb { background: #555555; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #777777; }

        /* --- Sidebar Configuration --- */
        .sidebar { width: 260px; background-color: var(--bg-color-sidebar); padding: 20px; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; transition: 0.3s; }
        .sidebar-scroll-area { flex: 1; overflow-y: auto; padding-right: 5px; }
        .menu-icon { font-size: 24px; cursor: pointer; color: var(--text-muted); transition: color 0.2s; margin-bottom: 20px; }
        .menu-icon:hover { color: var(--text-color); }
        .sidebar-section { margin-top: 20px; }
        .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .section-header h3 { color: var(--text-muted); font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin: 0; }
        .add-btn { background: transparent; border: none; color: var(--tech-green); font-size: 20px; cursor: pointer; transition: transform 0.2s; }
        .add-btn:hover { transform: scale(1.2); }
        .sidebar-section ul { list-style: none; }
        
        .sidebar-section li { 
            padding: 10px 12px; 
            border: 1px solid var(--border-color); 
            margin: 8px 0; 
            border-radius: 8px; 
            text-align: left; 
            background: var(--bg-color-element); 
            cursor: pointer; 
            transition: all 0.2s; 
            border-left: 4px solid transparent; 
            position: relative;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 14px;
        }
        .sidebar-section li:hover { background: #3a3a3a; }
        .sidebar-section li.active-tab { border-left-color: var(--tech-green); background: #333; font-weight: bold; }
        .edit-input { width: 100%; background: transparent; border: none; color: var(--text-color); text-align: left; outline: none; font-size: 14px; border-bottom: 1px solid var(--tech-green); }

        .sidebar-footer { margin-top: auto; padding-top: 15px; border-top: 1px solid var(--border-color); }
        .settings-btn-sidebar { width: 100%; padding: 10px; background: transparent; border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-muted); cursor: pointer; transition: 0.2s; text-align: center; font-size: 14px;}
        .settings-btn-sidebar:hover { background: var(--bg-color-element); color: var(--text-color); }

        /* --- Context Menu --- */
        .context-menu { display: none; position: absolute; background-color: var(--bg-color-sidebar); border: 1px solid var(--border-color); border-radius: 8px; padding: 5px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.7); z-index: 1000; min-width: 120px; }
        .context-menu-item { padding: 10px 20px; cursor: pointer; color: var(--text-color); font-size: 14px; transition: background 0.2s; }
        .context-menu-item:hover { background-color: var(--bg-color-element); }
        .context-menu-item.danger { color: var(--danger-color); }

        /* --- Main Content & Header --- */
        .main-content { flex: 1; display: flex; flex-direction: column; position: relative; min-width: 0; }
        .header { display: flex; justify-content: center; align-items: center; padding: 15px 20px; border-bottom: 1px solid var(--border-color); position: relative; background: rgba(18, 18, 18, 0.9); backdrop-filter: blur(10px); z-index: 5; }
        #openSidebar { position: absolute; left: 20px; display: none; margin: 0; }
        .header h2 { font-weight: 500; letter-spacing: 1px; font-size: 18px; }
        .logo-container { position: absolute; right: 20px; display: flex; align-items: center; font-weight: bold; letter-spacing: 1px; font-size: 18px;}
        .logo-container span { color: var(--tech-green); }

        /* --- Chat Display Area --- */
        .chat-display { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; scroll-behavior: smooth; }
        .chat-message { padding: 14px 18px; border-radius: 12px; line-height: 1.6; word-wrap: break-word; min-width: 0; font-size: 15px;}
        .user-message { align-self: flex-end; background-color: var(--tech-green); color: #000; border-bottom-right-radius: 4px; white-space: pre-wrap; max-width: 75%; font-weight: 500; }
        .ai-message { align-self: flex-start; background-color: var(--bg-color-element); color: var(--text-color); border-bottom-left-radius: 4px; width: 100%; max-width: 85%; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        
        .error-message { border-left: 4px solid var(--danger-color); background-color: rgba(255, 68, 68, 0.1); color: #ffcccc; }
        
        .ai-message p { margin-bottom: 12px; word-break: break-word; }
        .ai-message p:last-child { margin-bottom: 0; }
        
        /* Enhance Markdown table rendering */
        .ai-message table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px; }
        .ai-message th, .ai-message td { border: 1px solid var(--border-color); padding: 10px 12px; text-align: left; }
        .ai-message th { background-color: rgba(255, 255, 255, 0.05); font-weight: 600; }
        .ai-message tr:nth-child(even) { background-color: rgba(255, 255, 255, 0.02); }

        .code-container { position: relative; margin: 15px 0; }
        .ai-message pre { background-color: #0d1117; padding: 35px 15px 15px 15px; border-radius: 8px; overflow-x: auto; border: 1px solid #30363d; margin: 0; }
        .ai-message code { font-family: 'Fira Code', 'Consolas', monospace; background-color: rgba(0, 0, 0, 0.3); color: var(--tech-green); padding: 3px 6px; border-radius: 4px; word-break: break-word; font-size: 13px; }
        
        .ai-message pre code { background-color: transparent; padding: 0; color: #c9d1d9; word-break: normal; font-size: 14px; }

        .copy-btn { position: absolute; top: 8px; right: 8px; background: #30363d; border: 1px solid #555; color: #ccc; border-radius: 4px; padding: 4px 10px; font-size: 12px; cursor: pointer; transition: 0.2s; }
        .copy-btn:hover { background: #444; color: #fff; border-color: var(--tech-green); }
        
        .reasoning-block { border-left: 3px solid #555; padding-left: 15px; color: #888; font-style: italic; margin-bottom: 15px; background: rgba(0,0,0,0.15); padding: 12px 15px; border-radius: 0 8px 8px 0; font-size: 14px; }

        /* --- Input Area --- */
        .input-area { padding: 20px; display: flex; justify-content: center; background: linear-gradient(transparent, var(--bg-color-main) 20%); z-index: 5; }
        .input-box { width: 85%; max-width: 900px; border: 1px solid var(--border-color); border-radius: 12px; display: flex; flex-direction: column; background: var(--bg-color-sidebar); padding: 12px 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); transition: border-color 0.3s; }
        .input-box:focus-within { border-color: #555; }
        .input-box textarea { width: 100%; border: none; background: transparent; color: var(--text-color); outline: none; font-size: 15px; padding: 5px 0 10px 0; margin-bottom: 5px; resize: none; min-height: 24px; max-height: 200px; overflow-y: auto; line-height: 1.5; }
        .input-box textarea::placeholder { color: var(--text-muted); }
        .input-controls { display: flex; align-items: center; justify-content: space-between; }
        .left-controls { display: flex; align-items: center; gap: 10px; }
        
        .mode-wrapper { position: relative; }
        button.mode-btn { padding: 6px 14px; border: 1px solid var(--border-color); border-radius: 20px; background: var(--bg-color-element); color: var(--text-color); cursor: pointer; font-size: 13px; transition: all 0.2s; }
        button.mode-btn:hover { background: #444; border-color: #666; }
        
        .stop-btn { border-color: var(--danger-color) !important; color: var(--danger-color) !important; display: none; }
        .stop-btn:hover { background: rgba(255, 68, 68, 0.1) !important; }

        .mode-dropdown { display: none; position: absolute; bottom: 110%; left: 0; background-color: var(--bg-color-sidebar); border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; min-width: 150px; box-shadow: 0 -4px 10px rgba(0,0,0,0.5); z-index: 10; }
        .mode-dropdown.show { display: block; }
        .dropdown-item { padding: 10px 15px; cursor: pointer; transition: background 0.2s; text-align: center; font-size: 14px; }
        .dropdown-item:hover { background-color: var(--bg-color-element); color: var(--tech-green); }
        
        .token-counter { font-size: 12px; color: var(--text-muted); background: var(--bg-color-element); padding: 5px 12px; border-radius: 15px; border: 1px solid var(--border-color); cursor: help; }
        .token-counter span { color: var(--tech-green); font-weight: bold; }

        .empty-state { text-align: center; color: var(--text-muted); margin-top: 50px; font-style: italic; font-size: 15px; }

        /* --- Settings Modal --- */
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); backdrop-filter: blur(5px); z-index: 2000; justify-content: center; align-items: center; }
        .modal-content { background: var(--bg-color-sidebar); padding: 30px; border-radius: 12px; width: 450px; border: 1px solid var(--border-color); box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
        .modal-content h3 { margin-bottom: 20px; color: var(--text-color); font-size: 18px; display: flex; align-items: center; gap: 8px; }
        .setting-group { margin-bottom: 18px; }
        .setting-group label { display: block; font-size: 13px; color: var(--text-muted); margin-bottom: 8px; font-weight: 500; }
        .modal-input { width: 100%; padding: 12px; background: var(--bg-color-element); border: 1px solid var(--border-color); color: var(--text-color); border-radius: 8px; outline: none; font-size: 14px; transition: border-color 0.2s; }
        .modal-input:focus { border-color: var(--tech-green); }
        textarea.modal-input { resize: vertical; min-height: 80px; }
        
        .data-management { margin-top: 25px; padding-top: 20px; border-top: 1px solid var(--border-color); display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; }
        .data-btn { flex: 1; padding: 10px; background: var(--bg-color-element); border: 1px solid var(--border-color); color: var(--text-color); border-radius: 8px; cursor: pointer; font-size: 13px; transition: 0.2s; text-align: center; }
        .data-btn:hover { background: #444; }
        .data-btn.danger { color: var(--danger-color); border-color: rgba(255, 68, 68, 0.3); }
        .data-btn.danger:hover { background: rgba(255, 68, 68, 0.1); }

        .modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 25px; }
        .modal-actions button { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; transition: 0.2s; }
        .btn-cancel { background: transparent; color: var(--text-muted); border: 1px solid var(--border-color); }
        .btn-cancel:hover { background: var(--bg-color-element); color: var(--text-color); }
        .btn-save { background: var(--tech-green); color: #000; font-weight: bold; }
        .btn-save:hover { box-shadow: 0 0 10px rgba(0, 255, 170, 0.3); }
    </style>
</head>
<body>
    <div class="app-container">
        <aside class="sidebar" id="sidebar">
            <div class="menu-icon" id="closeSidebar" title="Close Sidebar">☰</div>
            <div class="sidebar-scroll-area">
                <div class="sidebar-section">
                    <div class="section-header"><h3>Agent</h3><button class="add-btn" onclick="createNewItem('agent')" title="New Agent">+</button></div>
                    <ul id="agentList"></ul>
                </div>
                <div class="sidebar-section">
                    <div class="section-header"><h3>Project</h3><button class="add-btn" onclick="createNewItem('project')" title="New Project">+</button></div>
                    <ul id="projectList"></ul>
                </div>
            </div>
            <div class="sidebar-footer">
                <button class="settings-btn-sidebar" id="openSettingsBtn">⚙️ Settings & System Prompt</button>
            </div>
        </aside>

        <main class="main-content">
            <header class="header">
                <div class="menu-icon" id="openSidebar" title="Open Sidebar">☰</div>
                <h2 id="mainHeaderTitle">AntroCode</h2>
                <div class="logo-container">
                    Antro<span>Code</span>
                </div>
            </header>
            
            <div class="chat-display" id="chatDisplay"></div>
            
            <div class="input-area">
                <div class="input-box">
                    <textarea id="chatInput" placeholder="Ask me anything... (Shift+Enter for new line)" rows="1"></textarea>
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
            <h3>⚙️ Config & Data</h3>
            <div class="setting-group">
                <label>DeepSeek API Key (Stored Locally):</label>
                <input type="password" id="apiKeyInput" class="modal-input" placeholder="sk-...">
            </div>
            <div class="setting-group">
                <label>System Prompt (Agent Persona):</label>
                <textarea id="systemPromptInput" class="modal-input" placeholder="You are a helpful coding assistant..."></textarea>
            </div>
            <div class="setting-group">
                <label>Context History Limit (Messages):</label>
                <input type="number" id="contextLimitInput" class="modal-input" placeholder="15" min="1" max="100">
            </div>
            
            <div class="data-management">
                <button class="data-btn" id="exportDataBtn">📥 Export JSON</button>
                <button class="data-btn" onclick="document.getElementById('importFileInput').click()">📤 Import JSON</button>
                <input type="file" id="importFileInput" style="display: none;" accept=".json">
                <button class="data-btn danger" id="clearDataBtn">🗑️ Clear All Data</button>
            </div>

            <div class="modal-actions">
                <button class="btn-cancel" id="closeModalBtn">Cancel</button>
                <button class="btn-save" id="saveKeyBtn">Save Configuration</button>
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
                contextLimit: parseInt(localStorage.getItem('antrocode_context_limit')) || 15,
                systemPrompt: localStorage.getItem('antrocode_system_prompt') || 'You are an expert Python developer and architect. Provide clean, efficient, and well-documented code.'
            };
        }
        function saveSettings(key, limit, prompt) {
            localStorage.setItem('antrocode_api_key', key.trim());
            localStorage.setItem('antrocode_context_limit', limit);
            localStorage.setItem('antrocode_system_prompt', prompt.trim());
        }

        const STORAGE_KEY = 'antrocode_local_state_v5'; 
        
        const defaultState = {
            items: [
                { id: 'agent-1', type: 'agent', name: 'Python Architect' }
            ],
            chats: {
                'agent-1': [{ role: 'ai', content: 'System Ready. I am your Python Architect. How can I help you build today?' }]
            },
            tokens: { 'agent-1': 0 },
            activeId: 'agent-1'
        };

        let appState;

        try {
            const savedData = localStorage.getItem(STORAGE_KEY);
            appState = savedData ? JSON.parse(savedData) : defaultState;
            if (!appState || typeof appState !== 'object') throw new Error("Invalid state structure");
            if (!appState.tokens) appState.tokens = {};
            if (!appState.chats) appState.chats = {};
            if (!Array.isArray(appState.items)) appState.items = [];
        } catch (error) {
            console.error("State reset:", error);
            appState = JSON.parse(JSON.stringify(defaultState));
        }

        function saveState() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
            } catch (error) {
                if (error.name === 'QuotaExceededError' || error.name === 'NS_ERROR_DOM_QUOTA_REACHED') {
                    alert('Warning: Local storage is full! Please delete some workspaces or export backup and clear space.');
                }
            }
        }

        function generateId(prefix) { return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).substr(2, 5)}`; }
        function estimateTokensLocally(messagesArray, generatedText) {
            let totalText = messagesArray.map(m => m.content).join(" ") + generatedText;
            return Math.ceil(totalText.length * 1.5);
        }

        const agentList = document.getElementById('agentList');
        const projectList = document.getElementById('projectList');
        const chatDisplay = document.getElementById('chatDisplay');
        const headerTitle = document.getElementById('mainHeaderTitle');
        const contextMenu = document.getElementById('customContextMenu');
        const tokenValueDisplay = document.getElementById('tokenValue');
        const stopBtn = document.getElementById('stopBtn');
        const chatInput = document.getElementById('chatInput');
        
        let targetIdToModify = null;
        let currentAbortController = null;

        function renderSidebar() {
            agentList.innerHTML = '';
            projectList.innerHTML = '';

            appState.items.forEach(item => {
                const li = document.createElement('li');
                li.innerText = item.name; 
                li.dataset.id = item.id;
                li.title = item.name; 
                
                if (item.id === appState.activeId) li.classList.add('active-tab');

                li.addEventListener('click', (e) => {
                    if (e.target.tagName === 'INPUT') return;
                    appState.activeId = item.id;
                    saveState();
                    renderSidebar(); 
                    renderChat();
                    chatInput.focus();
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
                            btn.style.borderColor = 'var(--tech-green)';
                            setTimeout(() => { btn.innerText = 'Copy'; btn.style.color = '#ccc'; btn.style.borderColor = '#555'; }, 2000);
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
                chatDisplay.innerHTML = '<div class="empty-state">No workspace selected. Create an Agent or Project to start.</div>';
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
                { role: 'system', content: userSettings.systemPrompt },
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

                if (!response.ok) throw new Error(`Server Error (${response.status}) - ${response.statusText}`);
                
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
                                        if (appState.activeId === requestTabId) tokenValueDisplay.innerText = appState.tokens[requestTabId].toLocaleString();
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
                                } catch (e) { }
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
                    currentAiMessage.content += "\n\n*(Aborted by user)*";
                    appState.chats[requestTabId].push(currentAiMessage);
                    let estimatedCost = estimateTokensLocally(apiMessages, currentAiMessage.reasoning + currentAiMessage.content);
                    appState.tokens[requestTabId] = (appState.tokens[requestTabId] || 0) + estimatedCost;
                    if (appState.activeId === requestTabId && msgDiv) { renderChat(); }
                    saveState();
                } else {
                    appState.chats[requestTabId].push({ role: 'error', content: `**Connection Error.**\n\`${error.message}\`` });
                    saveState();
                    if (appState.activeId === requestTabId) renderChat();
                }
            } finally {
                stopBtn.style.display = 'none';
                currentAbortController = null;
                chatInput.focus(); 
            }
        }

        // ==========================================
        // Interaction Bindings
        // ==========================================
        window.createNewItem = function(type) {
            const newId = generateId(type);
            appState.items.push({ id: newId, type: type, name: `New ${type}` });
            appState.chats[newId] = [{ role: 'ai', content: `Workspace initialized. Using current System Prompt.` }];
            appState.tokens[newId] = 0;
            appState.activeId = newId; 
            saveState();
            renderSidebar();
            renderChat();
            chatInput.focus();
        };

        document.addEventListener('click', (event) => { if (event.target !== contextMenu) contextMenu.style.display = 'none'; });

        document.getElementById('renameOption').addEventListener('click', () => {
            if (!targetIdToModify) return;
            const li = document.querySelector(`li[data-id="${targetIdToModify}"]`);
            if (!li) return;

            const item = appState.items.find(i => i.id === targetIdToModify);
            li.innerHTML = `<input type="text" class="edit-input" value="">`;
            const input = li.querySelector('input');
            input.value = item.name; 
            input.select();

            const saveNewName = () => {
                item.name = input.value.trim() || `Untitled`;
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
                chatInput.focus();
            });
        });
        document.addEventListener('click', () => { modeDropdown.classList.remove('show'); });

        // ==========================================
        // Settings & Data Management
        // ==========================================
        const modal = document.getElementById('settingsModal');
        const openSettingsBtn = document.getElementById('openSettingsBtn');
        const closeModalBtn = document.getElementById('closeModalBtn');
        const saveKeyBtn = document.getElementById('saveKeyBtn');
        const apiKeyInput = document.getElementById('apiKeyInput');
        const contextLimitInput = document.getElementById('contextLimitInput');
        const systemPromptInput = document.getElementById('systemPromptInput');

        function openSettingsModal() {
            const currentSettings = getSettings();
            apiKeyInput.value = currentSettings.apiKey;
            contextLimitInput.value = currentSettings.contextLimit;
            systemPromptInput.value = currentSettings.systemPrompt;
            modal.style.display = 'flex';
        }
        
        openSettingsBtn.addEventListener('click', openSettingsModal);
        closeModalBtn.addEventListener('click', () => { modal.style.display = 'none'; chatInput.focus(); });
        saveKeyBtn.addEventListener('click', () => {
            const key = apiKeyInput.value.trim();
            const limit = parseInt(contextLimitInput.value) || 15;
            const prompt = systemPromptInput.value.trim() || 'You are a helpful coding assistant.';
            if(key) {
                saveSettings(key, limit, prompt);
                modal.style.display = 'none';
                chatInput.focus();
            } else {
                alert('System Notice: Please enter a valid API Key!');
            }
        });

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
                        alert('Data imported successfully!');
                        modal.style.display = 'none';
                    } else throw new Error('Invalid format');
                } catch (err) { alert('Import failed: Invalid file format.'); }
            };
            reader.readAsText(file);
            e.target.value = ''; 
        });

        document.getElementById('clearDataBtn').addEventListener('click', () => {
            if(confirm('WARNING! This will permanently delete all your chat history and projects. Are you sure?')) {
                localStorage.removeItem(STORAGE_KEY);
                appState = JSON.parse(JSON.stringify(defaultState));
                saveState();
                renderSidebar();
                renderChat();
                modal.style.display = 'none';
            }
        });

        // Initialize App
        renderSidebar();
        renderChat();
        
        // Auto focus input field on startup
        window.onload = () => setTimeout(() => chatInput.focus(), 100);

    </script>
</body>
</html>"""

def print_banner():
    # Banner split into White (Antro) and Tech Green (Code)
    print("\033[97m █████╗ ███╗   ██╗████████╗██████╗  ██████╗ \033[92m ██████╗ ██████╗ ██████╗ ███████╗\033[0m")
    print("\033[97m██╔══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗\033[92m██╔════╝██╔═══██╗██╔══██╗██╔════╝\033[0m")
    print("\033[97m███████║██╔██╗ ██║   ██║   ██████╔╝██║   ██║\033[92m██║     ██║   ██║██║  ██║█████╗  \033[0m")
    print("\033[97m██╔══██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║\033[92m██║     ██║   ██║██║  ██║██╔══╝  \033[0m")
    print("\033[97m██║  ██║██║ ╚████║   ██║   ██║  ██║╚██████╔╝\033[92m╚██████╗╚██████╔╝██████╔╝███████╗\033[0m")
    print("\033[97m╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ \033[92m ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝\033[0m")
    print("        \033[90m[ Core Initialized - Single File Environment ]\033[0m\n")

def main():
    print_banner()
    output_filename = "antrocode.html"
    
    print("\033[90m>> Compiling interface...\033[0m", end="", flush=True)
    time.sleep(0.5) 
    
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(HTML_TEMPLATE)
        
    print("\033[92m [OK]\033[0m")
    print(f"\033[90m>> Artifact generated: {output_filename}\033[0m")
    
    file_path = 'file://' + os.path.realpath(output_filename)
    print("\033[90m>> Launching local client...\033[0m")
    time.sleep(0.3)
    webbrowser.open(file_path)
    
    print("\n\033[92m====================================================\033[0m")
    print("\033[97m System Ready. \033[92mAntroCode\033[97m is running in your browser.Give it a star！\033[0m")
    print("\033[92m====================================================\033[0m\n")

if __name__ == "__main__":
    main()
