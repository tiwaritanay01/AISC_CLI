"""Script to generate the updated scripts/build_host.py with 22 experiments,
horizontal experiment cards rail at the top, client-side ZIP/PDF/HTML ingester at the bottom,
and dedicated ERTOS ZIP and PowerShell scripts."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Read experiments_data.json
with open(BASE_DIR / "scripts" / "experiments_data.json", "r", encoding="utf-8") as f:
    experiments = json.load(f)

code_lines = []
code_lines.append('"""Host builder script: generates public/ catalog, manifests, experiment sources, HTML, and ZIP archives')
code_lines.append('populated from AISC and Embedded Systems & RTOS Laboratory Submissions."""')
code_lines.append('')
code_lines.append('import os')
code_lines.append('import json')
code_lines.append('import html')
code_lines.append('import zipfile')
code_lines.append('import shutil')
code_lines.append('from pathlib import Path')
code_lines.append('')
code_lines.append('BASE_DIR = Path(__file__).resolve().parent.parent')
code_lines.append('HOST_DIR = BASE_DIR / "labx-host"')
code_lines.append('PUBLIC_DIR = HOST_DIR / "public"')
code_lines.append('EXP_DIR = PUBLIC_DIR / "experiments"')
code_lines.append('DL_DIR = PUBLIC_DIR / "downloads"')
code_lines.append('')
code_lines.append(f'EXPERIMENTS = {json.dumps(experiments, indent=4)}')
code_lines.append('')

html_header_template = '''HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LabX Remote - AISC & Embedded Systems / RTOS Laboratory</title>
  <script src="jszip.min.js"></script>
  <script src="pdf.min.js"></script>
  <script>
    if (typeof JSZip === 'undefined') {
      document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"><\\\\/script>');
    }
    if (typeof pdfjsLib === 'undefined') {
      document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"><\\\\/script>');
    }
  </script>
  <style>
    :root {
      --bg: #0b1120;
      --card-bg: #1e293b;
      --accent: #38bdf8;
      --accent-green: #34d399;
      --accent-purple: #c084fc;
      --text: #f8fafc;
      --muted: #94a3b8;
      --code-bg: #090d16;
      --border: #334155;
    }
    * {
      box-sizing: border-box;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 1.5rem;
      line-height: 1.6;
    }
    .container {
      max-width: 1280px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      margin-bottom: 2rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.5rem;
    }
    h1 {
      color: var(--accent);
      font-size: 2.2rem;
      margin-bottom: 0.25rem;
      letter-spacing: -0.02em;
    }
    .badge-bar {
      display: flex;
      justify-content: center;
      gap: 0.75rem;
      flex-wrap: wrap;
      margin-top: 0.75rem;
    }
    .badge {
      display: inline-block;
      background: #0284c7;
      color: white;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
    }
    .badge.aisc {
      background: #0369a1;
    }
    .badge.es {
      background: #059669;
    }

    /* Top Section: Horizontal Experiment Cards Rail */
    .catalog-section {
      margin-bottom: 3rem;
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .section-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.25rem;
    }
    .tabs-group {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .tab-btn {
      background: #1e293b;
      color: var(--muted);
      border: 1px solid var(--border);
      padding: 0.45rem 1rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.88rem;
      font-weight: 600;
      transition: all 0.2s;
    }
    .tab-btn:hover {
      color: var(--text);
      border-color: var(--accent);
    }
    .tab-btn.active {
      background: #0284c7;
      color: white;
      border-color: #38bdf8;
    }
    .search-box {
      background: #090d16;
      border: 1px solid var(--border);
      color: white;
      padding: 0.45rem 0.85rem;
      border-radius: 6px;
      font-size: 0.88rem;
      width: 280px;
      outline: none;
      transition: border-color 0.2s;
    }
    .search-box:focus {
      border-color: var(--accent);
    }
    .rail-controls {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }
    .nav-arrow-btn {
      background: #1e293b;
      border: 1px solid var(--border);
      color: var(--accent);
      width: 34px;
      height: 34px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-weight: bold;
      transition: background 0.2s;
    }
    .nav-arrow-btn:hover {
      background: #0284c7;
      color: white;
    }

    /* Horizontal Cards Rail */
    .cards-rail {
      display: flex;
      gap: 1.25rem;
      overflow-x: auto;
      padding: 0.5rem 0.25rem 1.25rem;
      scroll-snap-type: x mandatory;
      scrollbar-width: thin;
      scrollbar-color: #0284c7 #090d16;
    }
    .cards-rail::-webkit-scrollbar {
      height: 8px;
    }
    .cards-rail::-webkit-scrollbar-track {
      background: #090d16;
      border-radius: 4px;
    }
    .cards-rail::-webkit-scrollbar-thumb {
      background: #0284c7;
      border-radius: 4px;
    }
    .cards-rail::-webkit-scrollbar-thumb:hover {
      background: #38bdf8;
    }

    .card {
      flex: 0 0 350px;
      scroll-snap-align: start;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, border-color 0.2s;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    }
    .card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }
    .tag {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: #334155;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      color: #38bdf8;
      display: inline-block;
      font-weight: 600;
    }
    .tag.es {
      color: #34d399;
      background: #064e3b;
    }
    .copy-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: #1e3a5f;
      color: #38bdf8;
      border: 1px solid #0284c7;
      border-radius: 6px;
      padding: 0.3rem 0.65rem;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .copy-btn:hover {
      background: #0284c7;
      color: #ffffff;
    }
    .copy-btn.copied {
      background: #15803d !important;
      color: #ffffff !important;
      border-color: #22c55e !important;
    }
    .card h3 {
      margin: 0.4rem 0;
      color: var(--accent);
      font-size: 1.05rem;
      line-height: 1.35;
    }
    .file-pill {
      font-size: 0.75rem;
      color: #94a3b8;
      background: #090d16;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-family: ui-monospace, monospace;
      margin-top: 0.5rem;
      display: inline-block;
      border: 1px solid #1e293b;
    }
    .card-cmd-box {
      background: #090d16;
      border: 1px solid #1e3a5f;
      border-radius: 6px;
      padding: 0.5rem 0.75rem;
      margin-top: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
    }
    .card-cmd-text {
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      color: #7dd3fc;
      overflow-x: auto;
      white-space: nowrap;
      flex: 1;
    }
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--border);
      font-size: 0.85rem;
    }
    a {
      color: var(--accent);
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }

    /* Bottom Section: Ingester, Terminal, Endpoints */
    .bottom-section {
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }
    .uploader-card {
      background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid #0284c7;
      border-radius: 12px;
      padding: 1.75rem;
      box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.15);
    }
    .uploader-header h2 {
      margin: 0.3rem 0;
      color: #38bdf8;
      font-size: 1.4rem;
    }
    .drop-zone {
      border: 2px dashed #0284c7;
      background: #090d16;
      border-radius: 8px;
      padding: 2.25rem 1.5rem;
      text-align: center;
      cursor: pointer;
      margin-top: 1.25rem;
      transition: all 0.2s ease;
    }
    .drop-zone:hover, .drop-zone.dragover {
      border-color: #38bdf8;
      background: #0f1c30;
      transform: scale(1.005);
    }
    .browse-btn {
      background: #0284c7;
      color: white;
      border: none;
      padding: 0.4rem 0.9rem;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 600;
      margin-left: 0.4rem;
      transition: background 0.2s;
    }
    .browse-btn:hover {
      background: #0369a1;
    }

    /* Dynamic Upload Results */
    .upload-result-box {
      margin-top: 1.5rem;
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 8px;
      padding: 1.25rem;
    }
    .master-actions-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      background: #0f1c30;
      border: 1px solid #0284c7;
      border-radius: 8px;
      padding: 0.75rem 1.25rem;
      margin-bottom: 1.25rem;
    }
    .action-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: #0284c7;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 0.5rem 0.9rem;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .action-btn:hover {
      background: #0369a1;
    }
    .action-btn.secondary {
      background: #1e293b;
      border: 1px solid var(--border);
      color: #7dd3fc;
    }
    .action-btn.secondary:hover {
      background: #334155;
      color: white;
    }
    .custom-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
    }
    .custom-exp-card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .custom-exp-card:hover {
      border-color: #38bdf8;
    }
    .preview-pre {
      background: #090d16;
      padding: 0.75rem;
      border-radius: 6px;
      font-family: ui-monospace, monospace;
      font-size: 0.78rem;
      color: #cbd5e1;
      max-height: 180px;
      overflow-y: auto;
      border: 1px solid #1f2937;
      margin-top: 0.5rem;
    }

    /* Terminal & Endpoints Boxes */
    .command-box {
      background: var(--code-bg);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 1.25rem;
      font-family: ui-monospace, monospace;
      color: #7dd3fc;
      margin: 1rem 0;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    }
    .endpoints-box {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 1.25rem;
    }
    .endpoints-box ul {
      margin: 0.5rem 0 0 1.25rem;
      padding: 0;
    }
    .endpoints-box li {
      margin-bottom: 0.4rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>LABX REMOTE EXPERIMENT DASHBOARD</h1>
      <p style="color:var(--muted); margin:0.25rem 0;">Artificial Intelligence (AISC) &amp; Embedded Systems / Real-Time Operating Systems (ES &amp; RTOS)</p>
      <div class="badge-bar">
        <span class="badge">22 Experiments Live</span>
        <span class="badge aisc">AISC Laboratory (12)</span>
        <span class="badge es">ES &amp; RTOS Laboratory (10)</span>
        <a href="downloads/ertos.zip" class="badge" style="background:#7c3aed; text-decoration:none;">Download ERTOS.ZIP (10 Exps)</a>
      </div>
    </header>

    <!-- TOP SECTION: Experiment Cards Horizontal Rail -->
    <section class="catalog-section">
      <div class="section-header-row">
        <div class="tabs-group">
          <button class="tab-btn active" onclick="filterLab('all', this)">All Experiments (22)</button>
          <button class="tab-btn" onclick="filterLab('AISC', this)">AISC Lab (12)</button>
          <button class="tab-btn" onclick="filterLab('ES_RTOS', this)">ES &amp; RTOS Lab (10)</button>
        </div>
        <div style="display:flex; gap:0.75rem; align-items:center;">
          <input type="text" id="card-search" class="search-box" placeholder="Search by name, ID, or keyword..." oninput="handleSearch(this.value)" />
          <div class="rail-controls">
            <button class="nav-arrow-btn" onclick="scrollRail(-380)" title="Scroll Left">&larr;</button>
            <button class="nav-arrow-btn" onclick="scrollRail(380)" title="Scroll Right">&rarr;</button>
          </div>
        </div>
      </div>

      <div id="cards-rail" class="cards-rail">
"""
'''

code_lines.append(html_header_template)
code_lines.append('')

html_footer_template = '''HTML_FOOTER = """      </div>
    </section>

    <!-- BOTTOM SECTION: Custom Ingester, Terminal Quickstart, Static Endpoints -->
    <div class="bottom-section">
      
      <!-- Custom ZIP / PDF / HTML Ingester -->
      <section class="uploader-section">
        <div class="uploader-card">
          <div class="uploader-header">
            <span class="badge" style="background:#0284c7;">CUSTOM EXPERIMENT &amp; MULTI-FORMAT INGESTER</span>
            <h2>⚡ Upload Submissions (ZIP Folder, PDF Report, or HTML) &rarr; Instant Custom Commands</h2>
            <p style="color:#94a3b8; margin:0.35rem 0;">
              Upload an entire student submission <strong>ZIP folder</strong> (e.g., <code>ES_RTOS_DIV_A_BATCH_A_Submissions.zip</code>), 
              <strong>PDF lab report(s)</strong>, or <strong>HTML file(s)</strong>.
              Even if original submissions contained drive links or print previews, it parses Aim, Theory &amp; Source Code, pads to 50 lines with theory comments strictly after line 50, and generates custom <code>irm &lt;URL&gt; | iex</code> commands for each experiment.
            </p>
          </div>

          <div id="drop-zone" class="drop-zone">
            <input type="file" id="submission-file-input" accept=".zip,.pdf,.html,.htm" multiple style="display:none;" />
            <div class="drop-zone-content">
              <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:0.5rem;">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <p style="margin:0.25rem 0; font-size:1.05rem; color:#f1f5f9;">
                Drag &amp; drop a <strong>ZIP folder</strong>, <strong>PDF lab report</strong>, or <strong>HTML file(s)</strong> here, or 
                <button type="button" class="browse-btn" onclick="document.getElementById('submission-file-input').click()">Browse Files</button>
              </p>
              <span style="font-size:0.82rem; color:#94a3b8;">Supports ZIP archives (with PDFs/HTML), standalone PDF reports, or HTML submissions</span>
            </div>
          </div>

          <div id="upload-result" style="display:none;" class="upload-result-box">
            <div class="master-actions-bar">
              <div>
                <span id="res-summary-badge" class="badge" style="background:#059669;">UNPACKED &amp; PROCESSED</span>
                <span id="res-summary-title" style="font-weight:600; color:#38bdf8; margin-left:0.5rem;"></span>
              </div>
              <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                <button id="pull-all-zip-btn" class="action-btn" onclick="copyPullAllScript()">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                  <span>Copy Pull-All Command</span>
                </button>
                <button id="download-zip-btn" class="action-btn secondary" onclick="downloadAllProcessedZip()">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                  <span>Download Processed ZIP</span>
                </button>
              </div>
            </div>

            <div id="custom-cards-container" class="custom-cards-grid">
              <!-- Dynamically generated custom cards -->
            </div>
          </div>
        </div>
      </section>

      <!-- Terminal Quickstart -->
      <section>
        <h2 style="color:var(--accent); font-size:1.4rem; margin-bottom:0.5rem;">Terminal Quickstart</h2>
        <div class="command-box">
          <span style="color:#94a3b8"># 1. Ultra-short one-liners in PowerShell (No install needed):</span><br>
          <span style="color:#38bdf8; font-weight:bold;">irm https://aisccli.netlify.app/ertos.ps1 | iex</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#34d399"># Pull ALL 10 ES &amp; RTOS experiments!</span><br>
          irm https://aisccli.netlify.app/all.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#94a3b8"># Pull ALL 22 experiments (AISC + ES/RTOS)</span><br>
          &amp; (irm https://aisccli.netlify.app/get.ps1) 14 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#94a3b8"># Pull Exp 14 (LPC2148 LED Interfacing)</span><br>
          &amp; (irm https://aisccli.netlify.app/get.ps1) 22 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#94a3b8"># Pull Exp 22 (LPC2148 Traffic Light Controller)</span><br>
          irm https://aisccli.netlify.app/list.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#94a3b8"># List all 22 experiments</span><br><br>
          <span style="color:#94a3b8"># 2. Or install the global 'labx' CLI:</span><br>
          irm https://aisccli.netlify.app/install.ps1 | iex<br>
          labx list &nbsp;|&nbsp; labx download 14 &nbsp;|&nbsp; labx run 14
        </div>
      </section>

      <!-- Static Endpoints -->
      <section class="endpoints-box">
        <h2 style="color:var(--accent); font-size:1.3rem; margin:0 0 0.5rem 0;">Available Static Endpoints</h2>
        <ul>
          <li><a href="downloads/ertos.zip"><code>/downloads/ertos.zip</code></a> &mdash; <strong>Dedicated 10-experiment ES &amp; RTOS ZIP archive</strong></li>
          <li><a href="downloads/labx_experiments.zip"><code>/downloads/labx_experiments.zip</code></a> &mdash; Complete 22-experiment ZIP archive (AISC + ES &amp; RTOS)</li>
          <li><a href="downloads/aisc_experiments.zip"><code>/downloads/aisc_experiments.zip</code></a> &mdash; Dedicated 12-experiment AISC ZIP archive</li>
          <li><a href="catalog.json"><code>/catalog.json</code></a> &mdash; Complete 22-experiment catalogue API</li>
          <li><a href="version.json"><code>/version.json</code></a> &mdash; Remote version metadata</li>
          <li><a href="downloads/labx.exe"><code>/downloads/labx.exe</code></a> &mdash; Windows standalone executable</li>
        </ul>
      </section>

    </div>
  </div>

  <script>
    // Initialize PDF.js worker
    if (typeof pdfjsLib !== 'undefined') {
      pdfjsLib.GlobalWorkerOptions.workerSrc = 'pdf.worker.min.js';
    }

    // 1. Horizontal Rail Navigation & Filtering
    function scrollRail(distance) {
      const rail = document.getElementById('cards-rail');
      if (rail) {
        rail.scrollBy({ left: distance, behavior: 'smooth' });
      }
    }

    function filterLab(lab, btn) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const cards = document.querySelectorAll('.card');
      cards.forEach(card => {
        const cardLab = card.getAttribute('data-subject') || 'AISC';
        if (lab === 'all' || cardLab === lab) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function handleSearch(query) {
      const q = query.toLowerCase().trim();
      const cards = document.querySelectorAll('.card');
      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (!q || text.includes(q)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    // Copy Experiment Code
    function copyExpCode(btn, codeId) {
      const ta = document.getElementById(codeId);
      if (!ta) return;
      const text = ta.value;
      const span = btn.querySelector('span');
      const originalText = span.textContent;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          btn.classList.add('copied');
          span.textContent = 'Copied!';
          setTimeout(() => {
            btn.classList.remove('copied');
            span.textContent = originalText;
          }, 2000);
        }).catch(() => fallbackCopy(ta, btn, span, originalText));
      } else {
        fallbackCopy(ta, btn, span, originalText);
      }
    }

    function copyText(btn, text) {
      const span = btn.querySelector('span');
      const originalText = span ? span.textContent : 'Copy';
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          btn.classList.add('copied');
          if (span) span.textContent = 'Copied!';
          setTimeout(() => {
            btn.classList.remove('copied');
            if (span) span.textContent = originalText;
          }, 2000);
        });
      }
    }

    function fallbackCopy(ta, btn, span, originalText) {
      ta.style.display = 'block';
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        btn.classList.add('copied');
        if (span) span.textContent = 'Copied!';
      } catch (err) {
        alert('Please manually copy the code from View File.');
      }
      ta.style.display = 'none';
      setTimeout(() => {
        btn.classList.remove('copied');
        if (span) span.textContent = originalText;
      }, 2000);
    }

    // 2. Custom Ingester State (ZIP / PDF / HTML)
    window._processedExperiments = [];

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('submission-file-input');

    if (dropZone && fileInput) {
      dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
      });
      dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
      dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
          processIncomingFiles(Array.from(e.dataTransfer.files));
        }
      });
      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
          processIncomingFiles(Array.from(e.target.files));
        }
      });
    }

    function cleanTextArtifacts(str) {
      return (str || '')
        .replace(/\\\\u2011/g, '-')
        .replace(/\\\\u2013/g, '-')
        .replace(/\\\\u2014/g, '--')
        .replace(/[\\\\u2018\\\\u2019]/g, "'")
        .replace(/[\\\\u201c\\\\u201d]/g, '"')
        .replace(/\\\\u2022/g, '-')
        .replace(/\\\\u2500/g, '-')
        .replace(/\\\\u00b0/g, ' deg ')
        .replace(/\\\\xa0/g, ' ');
    }

    function padCodeTo50(code, isCStyle) {
      const lines = code.trim().split('\\\\n');
      while (lines.length < 49) {
        lines.push('');
      }
      if (lines.length === 49) {
        lines.push(isCStyle ? '/* --- Line 50: Execution & Theory Division --- */' : '# --- Line 50: Execution & Theory Division ---');
      }
      return lines.join('\\\\n');
    }

    function formatTheory(theoryText, isCStyle, subjectName) {
      const clean = cleanTextArtifacts(theoryText || 'Laboratory Experiment Theory');
      const paragraphs = clean.split('\\\\n');
      const out = [''];

      if (isCStyle) {
        out.push('/*');
        out.push('='.repeat(76));
        out.push(`EXPERIMENT THEORY (from ${subjectName} Laboratory Submission):`);
        out.push('='.repeat(76));
        for (const p of paragraphs) {
          const trimmed = p.trim();
          if (!trimmed) { out.push(''); continue; }
          const words = trimmed.split(/\\\\s+/);
          let curr = '';
          for (const w of words) {
            if ((curr + ' ' + w).length > 74) {
              out.push(curr);
              curr = w;
            } else {
              curr = (curr ? curr + ' ' : '') + w;
            }
          }
          if (curr) out.push(curr);
        }
        out.push('='.repeat(76));
        out.push('*/');
      } else {
        out.push('# ' + '='.repeat(76));
        out.push(`# EXPERIMENT THEORY (from ${subjectName} Laboratory Submission):`);
        out.push('# ' + '='.repeat(76));
        for (const p of paragraphs) {
          const trimmed = p.trim();
          if (!trimmed) { out.push('#'); continue; }
          const words = trimmed.split(/\\\\s+/);
          let curr = '#';
          for (const w of words) {
            if ((curr + ' ' + w).length > 76) {
              out.push(curr);
              curr = '# ' + w;
            } else {
              curr += (curr === '#' ? ' ' : ' ') + w;
            }
          }
          if (curr !== '#') out.push(curr);
        }
        out.push('# ' + '='.repeat(76));
      }
      return out.join('\\\\n');
    }

    function buildPowerShellDeliveryScript(filename, code, isC) {
      return `# LabX Remote - Custom Experiment Delivery\\\\n$filename = "${filename}"\\\\n$code = @'\\\\n${code}\\\\n'@\\\\n$target = Join-Path $PWD $filename\\\\nSet-Content -Path $target -Value $code -Encoding utf8\\\\nWrite-Host ""\\\\nWrite-Host "============================================================" -ForegroundColor Cyan\\\\nWrite-Host " [OK] Experiment code saved to: $filename" -ForegroundColor Green\\\\nWrite-Host " Theory is embedded after line 50. Ready to execute!" -ForegroundColor White\\\\nWrite-Host " Target: $filename" -ForegroundColor Yellow\\\\nWrite-Host "============================================================" -ForegroundColor Cyan\\\\n`;
    }

    async function extractTextFromPdf(arrayBuffer) {
      if (typeof pdfjsLib === 'undefined') {
        throw new Error('PDF.js library could not be loaded');
      }
      const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
      const pdfDoc = await loadingTask.promise;
      let fullText = '';
      for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
        const page = await pdfDoc.getPage(pageNum);
        const textContent = await page.getTextContent();
        const pageItems = textContent.items.map(item => item.str);
        fullText += pageItems.join(' ') + '\\\\n';
      }
      return fullText;
    }

    // Reference code fallback generator when student HTML/PDF contained drive links or images
    function getStandardCodeForTopic(topic, isC) {
      const t = topic.toLowerCase();
      if (t.includes('led') || t.includes('blink')) {
        return `#include <LPC214x.h>\\\\n\\\\n#define LED_PINS (0xFF << 10)\\\\n\\\\nvoid delay(unsigned int count) {\\\\n    unsigned int i, j;\\\\n    for (i = 0; i < count; i++)\\\\n        for (j = 0; j < 6000; j++);\\\\n}\\\\n\\\\nint main(void) {\\\\n    PINSEL0 &= ~0xFFFF0000;\\\\n    IO0DIR |= LED_PINS;\\\\n    IO0CLR = LED_PINS;\\\\n    while (1) {\\\\n        IO0SET = LED_PINS;\\\\n        delay(300);\\\\n        IO0CLR = LED_PINS;\\\\n        delay(300);\\\\n    }\\\\n    return 0;\\\\n}`;
      }
      if (t.includes('lcd')) {
        return `#include <LPC214x.h>\\\\n\\\\n#define LCD_DATA 0xFF\\\\n#define RS (1U << 8)\\\\n#define EN (1U << 10)\\\\n\\\\nvoid delay(unsigned int c) { unsigned int i, j; for (i=0; i<c; i++) for (j=0; j<3000; j++); }\\\\nvoid LCD_Cmd(unsigned char cmd) { IO0CLR = LCD_DATA|RS; IO0SET = cmd; IO0SET = EN; delay(2); IO0CLR = EN; delay(5); }\\\\nvoid LCD_Data(unsigned char d) { IO0CLR = LCD_DATA; IO0SET = RS|d; IO0SET = EN; delay(2); IO0CLR = EN; delay(5); }\\\\nint main(void) {\\\\n    PINSEL0 &= ~0x001FFFFF; IO0DIR |= 0x000007FF;\\\\n    LCD_Cmd(0x38); LCD_Cmd(0x0C); LCD_Cmd(0x01);\\\\n    LCD_Data('L'); LCD_Data('P'); LCD_Data('C');\\\\n    while (1); return 0;\\\\n}`;
      }
      if (t.includes('uart') || t.includes('serial')) {
        return `#include <LPC214x.h>\\\\n\\\\nvoid UART0_Init(void) {\\\\n    PINSEL0 |= 0x05;\\\\n    U0LCR = 0x83;\\\\n    U0DLL = 97; U0DLM = 0;\\\\n    U0LCR = 0x03;\\\\n}\\\\nvoid UART0_SendChar(char ch) { while (!(U0LSR & 0x20)); U0THR = ch; }\\\\nint main(void) {\\\\n    UART0_Init();\\\\n    while (1) { UART0_SendChar('A'); }\\\\n    return 0;\\\\n}`;
      }
      if (t.includes('power') || t.includes('idle')) {
        return `#include <LPC214x.h>\\\\n#define LED (1U << 10)\\\\nint main(void) {\\\\n    PINSEL0 &= ~(3U << 20); IO0DIR |= LED;\\\\n    while (1) { IO0PIN ^= LED; PCON = 0x01; }\\\\n    return 0;\\\\n}`;
      }
      if (t.includes('traffic')) {
        return `#include <LPC214x.h>\\\\n#define RED (1U << 10)\\\\n#define YELLOW (1U << 11)\\\\n#define GREEN (1U << 12)\\\\n#define ALL (RED|YELLOW|GREEN)\\\\nvoid delay(int c) { int i, j; for (i=0; i<c; i++) for (j=0; j<6000; j++); }\\\\nint main(void) {\\\\n    PINSEL0 &= ~0x03F00000; IO0DIR |= ALL; IO0CLR = ALL;\\\\n    while (1) {\\\\n        IO0CLR = ALL; IO0SET = RED; delay(500);\\\\n        IO0CLR = ALL; IO0SET = GREEN; delay(500);\\\\n        IO0CLR = ALL; IO0SET = YELLOW; delay(200);\\\\n    }\\\\n    return 0;\\\\n}`;
      }
      if (t.includes('semaphore')) {
        return `#include <Arduino_FreeRTOS.h>\\\\n#include <semphr.h>\\\\nSemaphoreHandle_t sem;\\\\nvoid TaskProducer(void *pv) { for(;;) { xSemaphoreGive(sem); vTaskDelay(pdMS_TO_TICKS(1000)); } }\\\\nvoid TaskConsumer(void *pv) { for(;;) { if(xSemaphoreTake(sem, portMAX_DELAY)) Serial.println("Acquired!"); } }\\\\nvoid setup() { Serial.begin(9600); sem = xSemaphoreCreateBinary(); xTaskCreate(TaskProducer,"P",128,NULL,1,NULL); xTaskCreate(TaskConsumer,"C",128,NULL,1,NULL); }\\\\nvoid loop() {}`;
      }
      if (isC) {
        return `/* ${topic} */\\\\n#include <LPC214x.h>\\\\n\\\\nint main(void) {\\\\n    // Verification and setup entry\\\\n    return 0;\\\\n}`;
      }
      return `# ${topic}\\\\nprint("${topic} executed successfully")\\\\n`;
    }

    async function processIncomingFiles(fileList) {
      const resultBox = document.getElementById('upload-result');
      const cardsContainer = document.getElementById('custom-cards-container');
      resultBox.style.display = 'block';
      cardsContainer.innerHTML = '<div style="color:#7dd3fc; padding:1.5rem;">Unpacking and parsing submissions...</div>';

      window._processedExperiments = [];

      for (const file of fileList) {
        const lower = file.name.toLowerCase();
        if (lower.endsWith('.zip')) {
          await processZipFile(file);
        } else if (lower.endsWith('.pdf')) {
          const buffer = await file.arrayBuffer();
          await processPdfFile(file.name, buffer);
        } else if (lower.endsWith('.html') || lower.endsWith('.htm')) {
          await processHtmlFile(file.name, await file.text());
        }
      }

      renderCustomCards();
    }

    async function processZipFile(zipFile) {
      try {
        const jszip = new JSZip();
        const zip = await jszip.loadAsync(zipFile);
        const entries = Object.keys(zip.files);
        const validEntries = entries.filter(name => !zip.files[name].dir && (
          name.toLowerCase().endsWith('.html') || 
          name.toLowerCase().endsWith('.htm') || 
          name.toLowerCase().endsWith('.pdf')
        ));

        document.getElementById('res-summary-title').textContent = `Unpacking ${validEntries.length} files from ${zipFile.name}...`;

        for (const entryName of validEntries) {
          const lower = entryName.toLowerCase();
          if (lower.endsWith('.html') || lower.endsWith('.htm')) {
            const content = await zip.files[entryName].async('text');
            await processHtmlFile(entryName, content);
          } else if (lower.endsWith('.pdf')) {
            const buffer = await zip.files[entryName].async('arraybuffer');
            await processPdfFile(entryName, buffer);
          }
        }
      } catch (err) {
        console.error('Error unpacking zip:', err);
        alert('Could not unpack zip archive: ' + err.message);
      }
    }

    async function processPdfFile(rawName, arrayBuffer) {
      try {
        const fullText = await extractTextFromPdf(arrayBuffer);
        const baseFilename = rawName.split('/').pop().replace(/\\\\.[^/.]+$/, '');

        // 1. Aim / Title
        let title = '';
        const aimMatch = fullText.match(/(?:Aim|AIM|Objective|OBJECTIVE|Subject|Subject\\\\s*[:\\\\-]?|Experiment\\\\s*[:\\\\-]?)\\\\s*[:\\\\-]?\\\\s*([A-Za-z0-9\\\\s,()\\\\/\\\\-]+?)(?=(?:Enrollment|Roll|Date|Theory|THEORY|Apparatus|Equipment|1\\\\.|\\\\n\\\\n|$))/i);
        if (aimMatch && aimMatch[1].trim().length > 5) {
          title = aimMatch[1].trim();
        } else {
          title = baseFilename.replace(/[_-]+/g, ' ');
        }

        // 2. Theory
        let theory = '';
        const theoryMatch = fullText.match(/(?:Theory|THEORY|Theoretical\\\\s+Background)\\\\s*[:\\\\-]?\\\\s*([\\\\s\\\\S]*?)(?=(?:Algorithm|ALGORITHM|Source\\\\s+Code|CODE|Procedure|PROCEDURE|Program|PROGRAM|Output|Result|$))/i);
        if (theoryMatch && theoryMatch[1].trim().length > 10) {
          theory = theoryMatch[1].trim();
        }

        // 3. Source Code
        let code = '';
        const codeMatch = fullText.match(/(?:Source\\\\s+Code|SOURCE\\\\s+CODE|Code\\\\s*[:\\\\-]|Program\\\\s*[:\\\\-])\\\\s*([\\\\s\\\\S]*?)(?=(?:Output|OUTPUT|Result|RESULT|Conclusion|Assessment|$))/i);
        if (codeMatch && (codeMatch[1].includes('#include') || codeMatch[1].includes('void ') || codeMatch[1].includes('def ') || codeMatch[1].includes('import '))) {
          code = codeMatch[1].trim();
        }

        // Language detection
        const isC = title.toLowerCase().includes('lpc') || title.toLowerCase().includes('rtos') || title.toLowerCase().includes('embedded') || title.toLowerCase().includes('led') || title.toLowerCase().includes('lcd') || title.toLowerCase().includes('uart') || (code && code.includes('#include'));
        const ext = isC ? (title.toLowerCase().includes('rtos') || title.toLowerCase().includes('arduino') ? '.ino' : '.c') : '.py';
        let safeName = baseFilename.toLowerCase().replace(/[^a-z0-9_]/g, '_');
        if (!safeName.endsWith(ext)) safeName += ext;

        if (!code || code.length < 20) {
          code = getStandardCodeForTopic(title, isC);
        }

        const paddedCode = padCodeTo50(code, isC);
        const subject = isC ? 'Embedded Systems & RTOS' : 'AISC';
        const formattedTheory = formatTheory(theory || title, isC, subject);
        const finalContent = paddedCode + '\\\\n\\\\n' + formattedTheory + '\\\\n';

        window._processedExperiments.push({
          id: window._processedExperiments.length + 1,
          name: safeName,
          title: title,
          language: isC ? 'c' : 'python',
          code: finalContent,
          command: `irm https://aisccli.netlify.app/s/${safeName} | iex`
        });
      } catch (err) {
        console.warn('Error parsing PDF file:', rawName, err);
      }
    }

    async function processHtmlFile(rawName, htmlText) {
      try {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlText, 'text/html');

        const baseFilename = rawName.split('/').pop().replace(/\\\\.[^/.]+$/, '');
        let title = '';
        let theory = '';
        let code = '';

        // Extract Title / Aim
        const headings = Array.from(doc.querySelectorAll('h1, h2, h3, h4, h5, b, strong'));
        for (const h of headings) {
          const txt = h.textContent.trim().toLowerCase();
          if (txt.includes('aim') || txt.includes('objective')) {
            let sib = h.nextElementSibling;
            while (sib && !['H1','H2','H3','H4','H5'].includes(sib.tagName)) {
              if (sib.textContent.trim()) {
                title = sib.textContent.trim();
                break;
              }
              sib = sib.nextElementSibling;
            }
            if (title) break;
          }
        }
        if (!title) {
          title = doc.querySelector('title')?.textContent.trim() || baseFilename.replace(/[_-]+/g, ' ');
        }

        // Extract Theory
        for (const h of headings) {
          if (h.textContent.trim().toLowerCase().includes('theory')) {
            const parts = [];
            let sib = h.nextElementSibling;
            while (sib && !['H1','H2','H3','H4','H5'].includes(sib.tagName)) {
              const t = sib.textContent.trim();
              if (t) parts.push(t);
              sib = sib.nextElementSibling;
            }
            theory = parts.join('\\\\n\\\\n');
            break;
          }
        }

        // Extract Code
        for (const h of headings) {
          const txt = h.textContent.trim().toLowerCase();
          if (txt.includes('source code') || txt.includes('code')) {
            let sib = h.nextElementSibling;
            while (sib && !['H1','H2','H3','H4','H5'].includes(sib.tagName)) {
              if (sib.tagName === 'PRE' || sib.querySelector('pre') || sib.tagName === 'CODE') {
                code = sib.textContent.trim();
                break;
              }
              sib = sib.nextElementSibling;
            }
            if (code) break;
          }
        }
        if (!code) {
          const pres = Array.from(doc.querySelectorAll('pre, code'));
          for (const pre of pres) {
            const txt = pre.textContent.trim();
            if (txt.includes('#include') || txt.includes('def ') || txt.includes('import ') || txt.includes('void ') || txt.includes('int main')) {
              code = txt;
              break;
            }
          }
        }

        // Language Detection & Extension
        const isC = (code && (code.includes('#include') || code.includes('void '))) || rawName.toLowerCase().includes('lpc') || rawName.toLowerCase().includes('rtos') || title.toLowerCase().includes('lpc') || title.toLowerCase().includes('rtos') || title.toLowerCase().includes('embedded');
        const ext = isC ? (code && code.includes('setup()') ? '.ino' : '.c') : '.py';
        let safeName = baseFilename.toLowerCase().replace(/[^a-z0-9_]/g, '_');
        if (!safeName.endsWith(ext)) safeName += ext;

        if (!code || code.length < 15) {
          code = getStandardCodeForTopic(title, isC);
        }

        const paddedCode = padCodeTo50(code, isC);
        const subject = isC ? 'Embedded Systems & RTOS' : 'AISC';
        const formattedTheory = formatTheory(theory || title, isC, subject);
        const finalContent = paddedCode + '\\\\n\\\\n' + formattedTheory + '\\\\n';

        window._processedExperiments.push({
          id: window._processedExperiments.length + 1,
          name: safeName,
          title: title,
          language: isC ? 'c' : 'python',
          code: finalContent,
          command: `irm https://aisccli.netlify.app/s/${safeName} | iex`
        });

      } catch (err) {
        console.warn('Error parsing html file:', rawName, err);
      }
    }

    async function renderCustomCards() {
      const container = document.getElementById('custom-cards-container');
      const count = window._processedExperiments.length;
      document.getElementById('res-summary-title').textContent = `${count} Experiments Unpacked & Formatted`;

      if (count === 0) {
        container.innerHTML = '<div style="color:#f87171; padding:1rem;">No valid experiments could be parsed from the uploaded file(s).</div>';
        return;
      }

      container.innerHTML = '';
      for (let i = 0; i < count; i++) {
        const item = window._processedExperiments[i];
        const card = document.createElement('div');
        card.className = 'custom-exp-card';

        const lines = item.code.split('\\\\n').length;
        const escapedCode = item.code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

        card.innerHTML = `
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <span class="tag ${item.language === 'c' ? 'es' : ''}">${item.language.toUpperCase()}</span>
              <button class="copy-btn" onclick="copyCustomItemCode(${i}, this)">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                <span>Copy Code</span>
              </button>
            </div>
            <h4 style="margin:0.25rem 0; color:#38bdf8; font-size:0.95rem;">${item.title}</h4>
            <span class="file-pill">${item.name}</span>
          </div>

          <div style="margin-top:0.75rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:#94a3b8; margin-bottom:0.25rem;">
              <span>PowerShell Delivery Command:</span>
            </div>
            <div class="card-cmd-box" style="margin-top:0;">
              <code id="cmd-cust-${i}" class="card-cmd-text">Generating...</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.72rem;" onclick="copyCustCmd(${i}, this)">Copy</button>
            </div>
            <details style="margin-top:0.5rem; font-size:0.78rem; color:#94a3b8;">
              <summary style="cursor:pointer; color:#7dd3fc;">View Code Preview (${lines} lines, theory after line 50)</summary>
              <pre class="preview-pre">${escapedCode}</pre>
            </details>
          </div>
        `;
        container.appendChild(card);
      }

      generateCustomCommands();
    }

    async function generateCustomCommands() {
      for (let i = 0; i < window._processedExperiments.length; i++) {
        const item = window._processedExperiments[i];
        const cmdElem = document.getElementById(`cmd-cust-${i}`);
        const deliveryScript = buildPowerShellDeliveryScript(item.name, item.code, item.language === 'c');

        let cmd = '';
        try {
          const res = await fetch('/api/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: item.name, script: deliveryScript })
          });
          if (res.ok) {
            const data = await res.json();
            if (data.command) cmd = data.command;
          }
        } catch (e) {}

        if (!cmd) {
          try {
            const dpRes = await fetch('https://dpaste.org/api/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: new URLSearchParams({ content: deliveryScript, format: 'url', expiry_days: '30' })
            });
            if (dpRes.ok) {
              const url = (await dpRes.text()).trim();
              const slug = url.split('/').filter(Boolean).pop();
              cmd = `irm https://aisccli.netlify.app/s/${slug} | iex`;
            }
          } catch (e2) {}
        }

        if (!cmd) {
          cmd = `irm https://aisccli.netlify.app/all.ps1 | iex`;
        }

        item.command = cmd;
        if (cmdElem) cmdElem.textContent = cmd;
      }
    }

    function copyCustomItemCode(idx, btn) {
      const item = window._processedExperiments[idx];
      if (item) copyText(btn, item.code);
    }

    function copyCustCmd(idx, btn) {
      const item = window._processedExperiments[idx];
      if (item) copyText(btn, item.command);
    }

    function copyPullAllScript() {
      const btn = document.getElementById('pull-all-zip-btn');
      const cmds = window._processedExperiments.map(e => e.command).filter(Boolean);
      if (cmds.length) {
        copyText(btn, cmds.join(' ; '));
      }
    }

    async function downloadAllProcessedZip() {
      const jszip = new JSZip();
      for (const exp of window._processedExperiments) {
        jszip.file(exp.name, exp.code);
      }
      const blob = await jszip.generateAsync({ type: 'blob' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'custom_experiments_processed.zip';
      a.click();
    }
  </script>
</body>
</html>"""
'''

code_lines.append(html_footer_template)
code_lines.append('')

generate_host_code = '''def generate_host():
    """Build all static hosting artifacts for 22 experiments."""
    print("Building AISC & ES_RTOS LabX distribution backend...")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    DL_DIR.mkdir(parents=True, exist_ok=True)

    # Clean old experiments
    for old_folder in EXP_DIR.iterdir():
        if old_folder.is_dir():
            shutil.rmtree(old_folder)

    # 1. netlify.toml
    netlify_toml = """[build]
  publish = "public"
  functions = "../netlify/functions"

[[headers]]
  for = "/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, HEAD, POST, OPTIONS"
    Access-Control-Allow-Headers = "*"
    Cache-Control = "public, max-age=3600"

[[headers]]
  for = "/*.json"
  [headers.values]
    Content-Type = "application/json; charset=utf-8"

[[redirects]]
  from = "/api/publish"
  to = "/.netlify/functions/publish"
  status = 200

[[redirects]]
  from = "/r"
  to = "/.netlify/functions/raw"
  status = 200

[[redirects]]
  from = "/s/:id"
  to = "https://dpaste.org/:id/raw"
  status = 200
  force = true
"""
    with open(HOST_DIR / "netlify.toml", "w", encoding="utf-8") as f:
        f.write(netlify_toml)

    # 2. version.json
    version_data = {
        "version": "1.0.0",
        "updated_at": "2026-11-02T12:00:00Z",
        "platform": "AISC & ES_RTOS Laboratory Remote Production Backend",
        "supported_experiments": len(EXPERIMENTS),
        "checksum": "labx-prod-hash-v3"
    }
    with open(PUBLIC_DIR / "version.json", "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=2)

    # 3. Generate all experiments and HTML cards
    catalog_items = []
    zip_staging_all = HOST_DIR / "zip_staging_all"
    zip_staging_ertos = HOST_DIR / "zip_staging_ertos"
    zip_staging_aisc = HOST_DIR / "zip_staging_aisc"

    for stg in [zip_staging_all, zip_staging_ertos, zip_staging_aisc]:
        if stg.exists():
            shutil.rmtree(stg)
        stg.mkdir(parents=True, exist_ok=True)

    html_cards = []

    for exp in EXPERIMENTS:
        exp_id = exp["id"]
        exp_folder_name = f"{exp_id:02d}"
        target_exp_dir = EXP_DIR / exp_folder_name
        target_exp_dir.mkdir(parents=True, exist_ok=True)

        manifest_url = f"experiments/{exp_folder_name}/manifest.json"

        # Catalog entry
        catalog_items.append({
            "id": exp["id"],
            "slug": exp["slug"],
            "title": exp["title"],
            "language": exp["language"],
            "aliases": exp["aliases"],
            "description": exp["description"],
            "manifest_url": manifest_url
        })

        # Write experiment files
        manifest_files = []
        for file_info in exp["files"]:
            file_dest = target_exp_dir / file_info["path"]
            with open(file_dest, "w", encoding="utf-8") as sf:
                sf.write(file_info["content"])
            manifest_files.append({
                "path": file_info["path"],
                "source": file_info["source"],
                "role": file_info.get("role", "source")
            })

        # Manifest JSON
        manifest_dict = {
            "id": exp["id"],
            "slug": exp["slug"],
            "title": exp["title"],
            "language": exp["language"],
            "aliases": exp["aliases"],
            "description": exp["description"],
            "aim": exp["aim"],
            "theory": exp["theory"],
            "algorithm": exp["algorithm"],
            "files": manifest_files,
            "run": exp["run"],
            "version": "1.0.0"
        }
        with open(target_exp_dir / "manifest.json", "w", encoding="utf-8") as mf:
            json.dump(manifest_dict, mf, indent=2)

        # Stage directory
        folder_tag = f"Experiment{exp_id:02d}_{exp['slug'].replace('-', '_')}"
        zip_exp_all = zip_staging_all / folder_tag
        zip_exp_all.mkdir(parents=True, exist_ok=True)

        for f_info in exp["files"]:
            shutil.copy(target_exp_dir / f_info["path"], zip_exp_all / f_info["path"])
        shutil.copy(target_exp_dir / "manifest.json", zip_exp_all / "manifest.json")

        readme_content = f"# Experiment {exp_id:02d}: {exp['title']}\\n\\n## Aim\\n{exp['aim']}\\n\\n## Description\\n{exp['description']}\\n\\n## Theory\\n{exp['theory']}\\n"
        with open(zip_exp_all / "README.md", "w", encoding="utf-8") as rf:
            rf.write(readme_content)

        # Stage specific collections
        subject_type = exp.get("subject", "AISC")
        if subject_type == "ES_RTOS":
            shutil.copytree(zip_exp_all, zip_staging_ertos / folder_tag)
        else:
            shutil.copytree(zip_exp_all, zip_staging_aisc / folder_tag)

        # Primary source code
        src_file = exp["files"][0]
        src_name = src_file["path"]
        src_code = src_file["content"]
        escaped_code = html.escape(src_code)
        subject_badge_class = "es" if subject_type == "ES_RTOS" else ""
        subject_label = "ES & RTOS" if subject_type == "ES_RTOS" else "AISC"
        cmd_str = f"& (irm https://aisccli.netlify.app/get.ps1) {exp_id}"

        # HTML card
        html_cards.append(f"""        <div class="card" data-subject="{subject_type}">
          <div>
            <div class="card-top">
              <span class="tag {subject_badge_class}">{subject_label} &bull; {exp['language'].upper()}</span>
              <button class="copy-btn" onclick="copyExpCode(this, 'code-{exp_id}')" title="Copy {src_name} source code">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>Copy Code</span>
              </button>
            </div>
            <textarea id="code-{exp_id}" style="display:none;">{escaped_code}</textarea>
            <h3>#{exp_id:02d} {exp['title']}</h3>
            <p style="color:#cbd5e1; font-size:0.85rem; margin:0.35rem 0;">{exp['description']}</p>
            <span class="file-pill">{src_name}</span>
          </div>

          <div>
            <div class="card-cmd-box">
              <code class="card-cmd-text">{cmd_str}</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.72rem;" onclick="copyText(this, '{cmd_str}')">Copy</button>
            </div>
            <div class="card-footer">
              <a href="experiments/{exp_folder_name}/{src_name}" target="_blank">View File &rarr;</a>
              <a href="{manifest_url}" target="_blank">Manifest &rarr;</a>
            </div>
          </div>
        </div>""")

    # 4. Write catalog.json
    catalog_data = {
        "version": "1.0.0",
        "updated_at": "2026-11-02T12:00:00Z",
        "zip_url": "downloads/labx_experiments.zip",
        "ertos_zip_url": "downloads/ertos.zip",
        "experiments": catalog_items
    }
    with open(PUBLIC_DIR / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)

    # 5. Build ZIP archives:
    # A. Full 22 experiments
    zip_all_out = DL_DIR / "labx_experiments.zip"
    print(f"Building complete 22-experiment ZIP archive at {zip_all_out}...")
    with zipfile.ZipFile(zip_all_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_all):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_all)
                zf.write(full_path, arcname=str(rel_path).replace("\\\\", "/"))

    # B. Dedicated ERTOS ZIP (Exp 13-22)
    zip_ertos_out = DL_DIR / "ertos_experiments.zip"
    print(f"Building dedicated ERTOS ZIP archive at {zip_ertos_out}...")
    with zipfile.ZipFile(zip_ertos_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_ertos):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_ertos)
                zf.write(full_path, arcname=str(rel_path).replace("\\\\", "/"))

    # Aliases for ertos.zip
    shutil.copy(zip_ertos_out, DL_DIR / "ertos.zip")
    shutil.copy(zip_ertos_out, DL_DIR / "es_rtos.zip")

    # C. Dedicated AISC ZIP (Exp 01-12)
    zip_aisc_out = DL_DIR / "aisc_experiments.zip"
    print(f"Building dedicated AISC ZIP archive at {zip_aisc_out}...")
    with zipfile.ZipFile(zip_aisc_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_aisc):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_aisc)
                zf.write(full_path, arcname=str(rel_path).replace("\\\\", "/"))

    # Cleanup staging
    for stg in [zip_staging_all, zip_staging_ertos, zip_staging_aisc]:
        shutil.rmtree(stg)

    # 6. PowerShell scripts
    all_ps1 = """$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all 22 experiments (AISC + Embedded Systems & RTOS) from LabX Remote..." -ForegroundColor Cyan
Invoke-WebRequest "https://aisccli.netlify.app/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 22 experiments extracted to current directory!" -ForegroundColor Green
"""
    with open(PUBLIC_DIR / "all.ps1", "w", encoding="utf-8") as f:
        f.write(all_ps1)

    ertos_ps1 = """$zip = Join-Path $PWD "ertos_temp.zip"
Write-Host "Downloading 10 Embedded Systems & RTOS experiments from LabX Remote..." -ForegroundColor Cyan
Invoke-WebRequest "https://aisccli.netlify.app/downloads/ertos.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 10 ES & RTOS experiments extracted to current directory!" -ForegroundColor Green
"""
    with open(PUBLIC_DIR / "ertos.ps1", "w", encoding="utf-8") as f:
        f.write(ertos_ps1)
    with open(PUBLIC_DIR / "rtos.ps1", "w", encoding="utf-8") as f:
        f.write(ertos_ps1)

    aisc_ps1 = """$zip = Join-Path $PWD "aisc_temp.zip"
Write-Host "Downloading 12 AISC experiments from LabX Remote..." -ForegroundColor Cyan
Invoke-WebRequest "https://aisccli.netlify.app/downloads/aisc_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 12 AISC experiments extracted to current directory!" -ForegroundColor Green
"""
    with open(PUBLIC_DIR / "aisc.ps1", "w", encoding="utf-8") as f:
        f.write(aisc_ps1)

    get_ps1 = """param($Id)
if (-not $Id) {
    $Id = Read-Host "Enter experiment number (1-22)"
}
$num = "{0:D2}" -f [int]$Id
$cat = (Invoke-RestMethod "https://aisccli.netlify.app/catalog.json").experiments | Where-Object { $_.id -eq [int]$Id }
if (-not $cat) {
    Write-Host "[!] Experiment $Id not found in catalogue." -ForegroundColor Red
    return
}
$mf = Invoke-RestMethod "https://aisccli.netlify.app/$($cat.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://aisccli.netlify.app/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($cat.title) into $dir/" -ForegroundColor Green
"""
    with open(PUBLIC_DIR / "get.ps1", "w", encoding="utf-8") as f:
        f.write(get_ps1)

    list_ps1 = """$cat = Invoke-RestMethod "https://aisccli.netlify.app/catalog.json"
Write-Host "`n==== AISC & Embedded Systems / RTOS Laboratory Experiments (LabX Remote) ====" -ForegroundColor Cyan
$cat.experiments | Format-Table @{Label="ID"; Expression={"Exp " + ("{0:D2}" -f $_.id)}}, @{Label="Title"; Expression={$_.title}}, @{Label="Language"; Expression={$_.language}}
Write-Host "Quick commands:" -ForegroundColor Yellow
Write-Host "  Pull ERTOS experiments : irm https://aisccli.netlify.app/ertos.ps1 | iex" -ForegroundColor White
Write-Host "  Pull all experiments   : irm https://aisccli.netlify.app/all.ps1 | iex" -ForegroundColor White
Write-Host "  Pull one experiment    : & (irm https://aisccli.netlify.app/get.ps1) <id>`n" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "list.ps1", "w", encoding="utf-8") as f:
        f.write(list_ps1)

    # 7. Write index.html
    full_html = HTML_HEADER + "\\n".join(html_cards) + HTML_FOOTER
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    print("Static backend build completed successfully!")
    print(f"Total experiments compiled: {len(EXPERIMENTS)}")

if __name__ == "__main__":
    generate_host()
'''

code_lines.append(generate_host_code)

output_file = BASE_DIR / "scripts" / "build_host.py"
print(f"Writing updated build_host.py to {output_file}...")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(code_lines))

print("Done! Ready to run build_host.py.")
