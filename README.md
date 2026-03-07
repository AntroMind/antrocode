# 🚀 AntroCode

AntroCode is a lightweight, purely front-end rendered AI coding assistant interface. Generated and launched via a single Python script, it seamlessly connects to the **DeepSeek API**, providing developers with an immersive, dark-mode hacker-style workspace.

No complex environment setup or backend database required—just plug in your API Key and instantly get a dedicated AI assistant with "local memory" and "multitasking" capabilities.

---

## ✨ Features

- **💾 Local Storage State Management**
  - Chat history and workspace states are automatically saved in your browser's local storage.
  - Even if you accidentally press F5, refresh the page, or close the tab, your hard work is perfectly safe!
- **🗂️ Multi-Workspace Support**
  - Create multiple `Agent` and `Project` tabs to organize your workflow.
  - Each tab has its own **isolated context memory**, ensuring you never get your context crossed when switching between different tasks.
- **⚡ Async Background Processing**
  - Switch tabs freely while the AI is thinking or generating long code snippets.
  - The AI's response will be accurately saved to the original tab where the prompt was initiated—zero cross-contamination!
- **🎨 Immersive Hacker UI**
  - Features a minimalist `#121212` dark background paired with `#00FFAA` tech-green accents.
  - Built-in `marked.js` and `highlight.js` perfectly render Markdown formatting and syntax highlighting.
- **🔄 Seamless Model Switching**
  - One-click toggle between `Think` (DeepSeek Reasoner) and `Fast` (DeepSeek Chat) modes to suit your coding needs.

---

