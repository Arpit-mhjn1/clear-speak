import sys

html = open('app_old.html', encoding='utf-16').read()

css_addition = """
    /* Sidebar Navigation */
    .app-container {
      display: flex;
      flex-direction: row;
      flex-grow: 1;
      overflow: hidden;
    }
    
    .sidebar {
      width: 250px;
      background-color: var(--container-bg);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      padding: 20px 0;
      transition: margin-left 0.3s ease;
      z-index: 90;
    }
    .sidebar.hidden {
      margin-left: -250px;
    }
    
    .sidebar-menu {
      display: flex;
      flex-direction: column;
      gap: 5px;
      padding: 0 15px;
    }
    .menu-item {
      display: flex;
      align-items: center;
      gap: 15px;
      padding: 12px 20px;
      border-radius: 8px;
      color: var(--text-secondary);
      text-decoration: none;
      font-weight: 500;
      transition: all 0.2s ease;
      font-size: 1.05rem;
    }
    .menu-item:hover {
      background-color: rgba(0, 229, 255, 0.1);
      color: var(--accent-color);
    }
    .menu-item.active {
      background-color: var(--accent-color);
      color: var(--bg-color);
    }
    .menu-icon { font-size: 1.2rem; }
    
    .main-content {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      height: calc(100vh - 67px);
    }
    
    .toggle-btn {
      background: none;
      border: none;
      color: var(--text-color);
      font-size: 1.5rem;
      cursor: pointer;
      margin-right: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .toggle-btn:hover { color: var(--accent-color); }
"""

html = html.replace('/* Main Dashboard Layout */', css_addition + '\n    /* Main Dashboard Layout */')

nav_replacement = """  <!-- Top Navigation -->
  <nav>
    <div style="display: flex; align-items: center;">
      <button id="sidebarToggle" class="toggle-btn">☰</button>
      <a href="index.html" class="nav-brand">
        <img src="logo.png" alt="ClearSpeak">
        ClearSpeak
      </a>
    </div>
    <div class="nav-links">
      <a href="index.html">&larr; Back to Home</a>
    </div>
  </nav>

  <div class="app-container">
    <!-- Side Navigation -->
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-menu">
        <a href="index.html" class="menu-item">
          <span class="menu-icon">🏠</span> Home
        </a>
        <a href="app.html" class="menu-item active">
          <span class="menu-icon">📹</span> Live Translator
        </a>
        <a href="tts.html" class="menu-item">
          <span class="menu-icon">🔊</span> Text-to-Speech
        </a>
        <a href="https://drive.google.com/drive/folders/1U-Pr4r1-cupgNOOq9NH_uTsQnPSVEKco" target="_blank" class="menu-item">
          <span class="menu-icon">📚</span> Dictionary Data
        </a>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content">"""

html = html.replace("""  <!-- Navigation -->
  <nav>
    <a href="index.html" class="nav-brand">
      <img src="logo.png" alt="ClearSpeak">
      ClearSpeak
    </a>
    <div class="nav-links">
      <a href="index.html">&larr; Back to Home</a>
    </div>
  </nav>""", nav_replacement)

html = html.replace("""    </div>
  </div>

  <script>""", """    </div>
    </main>
  </div>

  <script>
    // Sidebar Toggle
    document.getElementById('sidebarToggle').addEventListener('click', () => {
      document.getElementById('sidebar').classList.toggle('hidden');
    });""")

with open('app.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed app.html successfully")
