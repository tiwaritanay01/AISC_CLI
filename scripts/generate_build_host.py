"""Script to generate updated scripts/build_host.py with:
- Minimalist Black & White / Monochrome UI
- ERTOS Serial Numbers (Exp 1 - Exp 10) matching university portal
- Dual Code + Output PDF download on copy and in PowerShell commands (e1.ps1 - e10.ps1)
- Outputs from Google Drive embedded and served locally
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "scripts" / "experiments_data.json", "r", encoding="utf-8") as f:
    experiments = json.load(f)

code_lines = []
code_lines.append('"""Host builder script: generates public/ catalog, manifests, experiment sources, HTML, and ZIP archives')
code_lines.append('with Minimalist Black & White aesthetic and paired Code + Output PDF delivery."""')
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
code_lines.append('OUT_DIR = PUBLIC_DIR / "outputs"')
code_lines.append('')
code_lines.append(f'EXPERIMENTS = {repr(experiments)}')
code_lines.append('')

html_header_template = '''HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LabX Remote - Minimalist Experiment Distribution</title>
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
      --bg: #000000;
      --card-bg: #0a0a0a;
      --card-hover: #121212;
      --border: #222222;
      --border-hover: #444444;
      --text: #ffffff;
      --muted: #888888;
      --subtle: #555555;
      --code-bg: #050505;
      --white: #ffffff;
      --black: #000000;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 2rem 1.5rem;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }
    .container {
      max-width: 1320px;
      margin: 0 auto;
    }
    header {
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 2rem;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 1.5rem;
    }
    .header-left h1 {
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.03em;
      color: var(--white);
    }
    .header-left p {
      color: var(--muted);
      font-size: 0.9rem;
      margin-top: 0.35rem;
    }
    .badge-bar {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: #111111;
      color: var(--white);
      border: 1px solid var(--border);
      padding: 0.3rem 0.75rem;
      border-radius: 4px;
      font-size: 0.78rem;
      font-weight: 500;
      text-decoration: none;
      transition: all 0.15s ease;
    }
    .badge:hover {
      border-color: var(--white);
      background: #1a1a1a;
    }

    /* Top Section: Monochromatic Horizontal Rail */
    .catalog-section {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 2.5rem;
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
      gap: 0.4rem;
      flex-wrap: wrap;
    }
    .tab-btn {
      background: #0a0a0a;
      color: var(--muted);
      border: 1px solid var(--border);
      padding: 0.4rem 0.9rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 600;
      transition: all 0.15s ease;
    }
    .tab-btn:hover {
      color: var(--white);
      border-color: #555555;
    }
    .tab-btn.active {
      background: var(--white);
      color: var(--black);
      border-color: var(--white);
    }
    .search-box {
      background: #000000;
      border: 1px solid var(--border);
      color: var(--white);
      padding: 0.4rem 0.85rem;
      border-radius: 4px;
      font-size: 0.82rem;
      width: 260px;
      outline: none;
      transition: border-color 0.15s ease;
    }
    .search-box:focus {
      border-color: var(--white);
    }
    .rail-controls {
      display: flex;
      gap: 0.4rem;
      align-items: center;
    }
    .nav-arrow-btn {
      background: #0a0a0a;
      border: 1px solid var(--border);
      color: var(--white);
      width: 32px;
      height: 32px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.15s ease;
    }
    .nav-arrow-btn:hover {
      background: var(--white);
      color: var(--black);
      border-color: var(--white);
    }

    /* Cards Horizontal Rail */
    .cards-rail {
      display: flex;
      gap: 1.25rem;
      overflow-x: auto;
      padding: 0.5rem 0.25rem 1.25rem;
      scroll-snap-type: x mandatory;
      scrollbar-width: thin;
      scrollbar-color: #333333 #0a0a0a;
    }
    .cards-rail::-webkit-scrollbar {
      height: 6px;
    }
    .cards-rail::-webkit-scrollbar-track {
      background: #0a0a0a;
      border-radius: 3px;
    }
    .cards-rail::-webkit-scrollbar-thumb {
      background: #333333;
      border-radius: 3px;
    }
    .cards-rail::-webkit-scrollbar-thumb:hover {
      background: #555555;
    }

    .card {
      flex: 0 0 360px;
      scroll-snap-align: start;
      background: #050505;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.15s ease;
    }
    .card:hover {
      border-color: #444444;
      background: var(--card-hover);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }
    .tag {
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: #111111;
      padding: 0.2rem 0.5rem;
      border-radius: 3px;
      color: var(--white);
      border: 1px solid var(--border);
      display: inline-block;
      font-weight: 600;
    }
    .copy-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: var(--white);
      color: var(--black);
      border: 1px solid var(--white);
      border-radius: 4px;
      padding: 0.32rem 0.7rem;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .copy-btn:hover {
      background: #e5e5e5;
    }
    .copy-btn.copied {
      background: #222222 !important;
      color: var(--white) !important;
      border-color: #555555 !important;
    }
    .card h3 {
      margin: 0.35rem 0;
      color: var(--white);
      font-size: 1rem;
      font-weight: 600;
      line-height: 1.35;
    }
    .file-pill {
      font-size: 0.72rem;
      color: var(--muted);
      background: #000000;
      padding: 0.2rem 0.5rem;
      border-radius: 3px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      margin-top: 0.4rem;
      display: inline-block;
      border: 1px solid var(--border);
    }
    .card-cmd-box {
      background: #000000;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 0.45rem 0.75rem;
      margin-top: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
    }
    .card-cmd-text {
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      color: var(--white);
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
      font-size: 0.8rem;
    }
    a {
      color: var(--white);
      text-decoration: underline;
      text-underline-offset: 3px;
    }
    a:hover {
      color: #cccccc;
    }

    /* Bottom Section: Minimalist Ingester, Terminal, Endpoints */
    .bottom-section {
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }
    .uploader-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.75rem;
    }
    .uploader-header h2 {
      margin: 0.4rem 0 0.25rem;
      color: var(--white);
      font-size: 1.3rem;
      font-weight: 600;
    }
    .drop-zone {
      border: 1px dashed #444444;
      background: #000000;
      border-radius: 6px;
      padding: 2.5rem 1.5rem;
      text-align: center;
      cursor: pointer;
      margin-top: 1.25rem;
      transition: all 0.15s ease;
    }
    .drop-zone:hover, .drop-zone.dragover {
      border-color: var(--white);
      background: #050505;
    }
    .browse-btn {
      background: var(--white);
      color: var(--black);
      border: none;
      padding: 0.35rem 0.85rem;
      border-radius: 3px;
      cursor: pointer;
      font-weight: 600;
      margin-left: 0.35rem;
      font-size: 0.82rem;
    }
    .browse-btn:hover {
      background: #e5e5e5;
    }

    /* Dynamic Upload Results */
    .upload-result-box {
      margin-top: 1.5rem;
      background: #050505;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.25rem;
    }
    .master-actions-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      background: #0a0a0a;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.75rem 1.25rem;
      margin-bottom: 1.25rem;
    }
    .action-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: var(--white);
      color: var(--black);
      border: 1px solid var(--white);
      border-radius: 4px;
      padding: 0.45rem 0.85rem;
      font-weight: 600;
      font-size: 0.82rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .action-btn:hover {
      background: #e5e5e5;
    }
    .action-btn.secondary {
      background: #111111;
      border: 1px solid var(--border);
      color: var(--white);
    }
    .action-btn.secondary:hover {
      border-color: var(--white);
    }
    .custom-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1.25rem;
    }
    .custom-exp-card {
      background: #0a0a0a;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.1rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .preview-pre {
      background: #000000;
      padding: 0.75rem;
      border-radius: 4px;
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      color: #cccccc;
      max-height: 180px;
      overflow-y: auto;
      border: 1px solid var(--border);
      margin-top: 0.5rem;
    }

    /* Terminal & Endpoints Boxes */
    .command-box {
      background: #050505;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.25rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      color: var(--white);
      margin: 1rem 0;
      font-size: 0.88rem;
    }
    .endpoints-box {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
    }
    .endpoints-box ul {
      margin: 0.5rem 0 0 1.25rem;
    }
    .endpoints-box li {
      margin-bottom: 0.4rem;
      color: var(--muted);
    }
    .endpoints-box code {
      color: var(--white);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-left">
        <h1>LABX REMOTE</h1>
        <p>AISC &amp; Embedded Systems / RTOS Experiment Distribution System</p>
      </div>
      <div class="badge-bar">
        <span class="badge">22 Experiments Live</span>
        <span class="badge">AISC Lab (12)</span>
        <span class="badge">ES &amp; RTOS Lab (10)</span>
        <a href="downloads/ertos.zip" class="badge">Download ERTOS.ZIP &darr;</a>
      </div>
    </header>

    <!-- TOP SECTION: Monochromatic Experiment Cards Rail -->
    <section class="catalog-section">
      <div class="section-header-row">
        <div class="tabs-group">
          <button class="tab-btn active" onclick="filterLab('all', this)">All Experiments (28)</button>
          <button class="tab-btn" onclick="filterLab('AISC', this)">AISC Lab (12)</button>
          <button class="tab-btn" onclick="filterLab('ES_RTOS', this)">ES &amp; RTOS Lab (10)</button>
          <button class="tab-btn" onclick="filterLab('CN', this)">CN Lab (6)</button>
        </div>
        <div style="display:flex; gap:0.6rem; align-items:center;">
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
      
      <!-- Custom Ingester: ZIP / PDF / HTML -->
      <section class="uploader-section">
        <div class="uploader-card">
          <div class="uploader-header">
            <span class="tag">MULTI-FORMAT INGESTER</span>
            <h2>Upload Submissions (ZIP Folder, PDF Report, or HTML) &rarr; Instant Commands</h2>
            <p style="color:var(--muted); font-size:0.88rem; margin-top:0.25rem;">
              Drop a student submission <strong>ZIP archive</strong> (e.g., <code>ES_RTOS_DIV_A_BATCH_A_Submissions.zip</code>), 
              <strong>PDF lab report(s)</strong>, or <strong>HTML file(s)</strong>.
              Even if original submissions contained drive links or print previews, it extracts Aim, Theory &amp; Source Code, pads to 50 lines with theory comments strictly after line 50, and generates custom delivery commands.
            </p>
          </div>

          <div id="drop-zone" class="drop-zone">
            <input type="file" id="submission-file-input" accept=".zip,.pdf,.html,.htm" multiple style="display:none;" />
            <div class="drop-zone-content">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:0.5rem;">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <p style="font-size:0.95rem; color:var(--white);">
                Drag &amp; drop a <strong>ZIP folder</strong>, <strong>PDF lab report</strong>, or <strong>HTML file(s)</strong> here, or 
                <button type="button" class="browse-btn" onclick="document.getElementById('submission-file-input').click()">Browse Files</button>
              </p>
              <span style="font-size:0.78rem; color:var(--subtle);">Supports ZIP archives with subfolders, standalone PDFs, or HTML submissions</span>
            </div>
          </div>

          <div id="upload-result" style="display:none;" class="upload-result-box">
            <div class="master-actions-bar">
              <div>
                <span id="res-summary-badge" class="tag">UNPACKED</span>
                <span id="res-summary-title" style="font-weight:600; color:var(--white); margin-left:0.5rem; font-size:0.9rem;"></span>
              </div>
              <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                <button id="pull-all-zip-btn" class="action-btn" onclick="copyPullAllScript()">
                  <span>Copy Pull-All Command</span>
                </button>
                <button id="download-zip-btn" class="action-btn secondary" onclick="downloadAllProcessedZip()">
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
        <h2 style="color:var(--white); font-size:1.2rem; margin-bottom:0.5rem;">Terminal Quickstart</h2>
        <div class="command-box">
          <span style="color:var(--subtle)"># 1. AISC Practicals:</span><br>
          irm https://cli-t0km.onrender.com/aisc.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Interactive: pull all 12 or select 1-12</span><br>
          irm https://cli-t0km.onrender.com/a1.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pinpoint Practical 01 (AI Agents & PEAS)</span><br><br>
          <span style="color:var(--subtle)"># 2. Pull ERTOS Experiments (Source Code + Output PDF):</span><br>
          irm https://cli-t0km.onrender.com/e2.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull Exp 02 (LED Interfacing Code + Output PDF)</span><br>
          irm https://cli-t0km.onrender.com/ertos.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull ALL 10 ERTOS experiments</span><br><br>
          <span style="color:var(--subtle)"># 3. Pull Computer Networks (CN):</span><br>
          irm https://cli-t0km.onrender.com/dijkstra.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Dijkstra Shortest Path Routing (Link-State OSPF)</span><br>
          irm https://cli-t0km.onrender.com/staticrouting.ps1 | iex &nbsp;<span style="color:var(--subtle)"># GNS3 Static Routing Configuration (R1/R2)</span><br>
          irm https://cli-t0km.onrender.com/cnsocket.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Java Socket Programming (Server + Client)</span><br>
          irm https://cli-t0km.onrender.com/cn.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull ALL CN experiments</span><br><br>
          <span style="color:var(--subtle)"># 4. Pull Everything (All 27 Experiments):</span><br>
          irm https://cli-t0km.onrender.com/all.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Extract full collection into current directory</span><br>
          irm https://cli-t0km.onrender.com/list.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Interactive list table</span><br><br>
          <span style="color:var(--subtle)"># 5. Global CLI:</span><br>
          irm https://cli-t0km.onrender.com/install.ps1 | iex<br>
          labx list &nbsp;|&nbsp; labx download 2 &nbsp;|&nbsp; labx run 2
        </div>
      </section>

      <!-- Static Endpoints -->
      <section class="endpoints-box">
        <h2 style="color:var(--white); font-size:1.1rem; margin:0 0 0.5rem 0;">Available Static Endpoints</h2>
        <ul>
          <li><a href="downloads/ertos.zip"><code>/downloads/ertos.zip</code></a> &mdash; Dedicated 10-experiment ES &amp; RTOS ZIP archive</li>
          <li><a href="downloads/labx_experiments.zip"><code>/downloads/labx_experiments.zip</code></a> &mdash; Complete 22-experiment ZIP archive</li>
          <li><a href="downloads/aisc_experiments.zip"><code>/downloads/aisc_experiments.zip</code></a> &mdash; Dedicated 12-experiment AISC ZIP archive</li>
          <li><a href="catalog.json"><code>/catalog.json</code></a> &mdash; Complete catalogue JSON API</li>
          <li><a href="version.json"><code>/version.json</code></a> &mdash; Remote metadata &amp; version</li>
          <li><a href="downloads/labx.exe"><code>/downloads/labx.exe</code></a> &mdash; Windows standalone binary</li>
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

    // Dual Code + Output Download Handler
    function copyExpCodeAndDownloadOutput(btn, codeId, outputUrlsStr) {
      const ta = document.getElementById(codeId);
      if (!ta) return;
      const text = ta.value;
      const span = btn.querySelector('span');
      const originalText = span ? span.textContent : 'Copy Code';

      // 1. Copy code to clipboard
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          showCopySuccess(btn, span, outputUrlsStr ? 'Copied & Output Downloaded!' : 'Copied!');
        }).catch(() => fallbackCopy(ta, btn, span, originalText));
      } else {
        fallbackCopy(ta, btn, span, originalText);
      }

      // 2. Automatically trigger output downloads if available
      if (outputUrlsStr) {
        const urls = outputUrlsStr.split(',').filter(Boolean);
        urls.forEach((u, i) => {
          setTimeout(() => triggerDownload(u.trim()), i * 250);
        });
      }
    }

    function triggerDownload(url) {
      const a = document.createElement('a');
      a.href = url;
      a.download = url.split('/').pop();
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }

    function showCopySuccess(btn, span, message) {
      btn.classList.add('copied');
      if (span) span.textContent = message;
      setTimeout(() => {
        btn.classList.remove('copied');
        if (span) span.textContent = 'Copy Code';
      }, 2500);
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
              curr = w;
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
      return `# LabX Remote - Custom Experiment Delivery\\\\n$filename = "${filename}"\\\\n$code = @'\\\\n${code}\\\\n'@\\\\n$target = Join-Path $PWD $filename\\\\nSet-Content -Path $target -Value $code -Encoding utf8\\\\nWrite-Host ""\\\\nWrite-Host "============================================================"\\\\nWrite-Host " [OK] Experiment code saved to: $filename"\\\\nWrite-Host " Theory is embedded after line 50. Ready to execute!"\\\\nWrite-Host " Target: $filename"\\\\nWrite-Host "============================================================"\\\\n`;
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
        return `/* ${topic} */\\\\n#include <LPC214x.h>\\\\n\\\\nint main(void) {\\\\n    return 0;\\\\n}`;
      }
      return `# ${topic}\\\\nprint("${topic} executed successfully")\\\\n`;
    }

    async function processIncomingFiles(fileList) {
      const resultBox = document.getElementById('upload-result');
      const cardsContainer = document.getElementById('custom-cards-container');
      resultBox.style.display = 'block';
      cardsContainer.innerHTML = '<div style="color:var(--muted); padding:1.5rem;">Unpacking and parsing submissions...</div>';

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

        let title = '';
        const aimMatch = fullText.match(/(?:Aim|AIM|Objective|OBJECTIVE|Subject|Subject\\\\s*[:\\\\-]?|Experiment\\\\s*[:\\\\-]?)\\\\s*[:\\\\-]?\\\\s*([A-Za-z0-9\\\\s,()\\\\/\\\\-]+?)(?=(?:Enrollment|Roll|Date|Theory|THEORY|Apparatus|Equipment|1\\\\.|\\\\n\\\\n|$))/i);
        if (aimMatch && aimMatch[1].trim().length > 5) {
          title = aimMatch[1].trim();
        } else {
          title = baseFilename.replace(/[_-]+/g, ' ');
        }

        let theory = '';
        const theoryMatch = fullText.match(/(?:Theory|THEORY|Theoretical\\\\s+Background)\\\\s*[:\\\\-]?\\\\s*([\\\\s\\\\S]*?)(?=(?:Algorithm|ALGORITHM|Source\\\\s+Code|CODE|Procedure|PROCEDURE|Program|PROGRAM|Output|Result|$))/i);
        if (theoryMatch && theoryMatch[1].trim().length > 10) {
          theory = theoryMatch[1].trim();
        }

        let code = '';
        const codeMatch = fullText.match(/(?:Source\\\\s+Code|SOURCE\\\\s+CODE|Code\\\\s*[:\\\\-]|Program\\\\s*[:\\\\-])\\\\s*([\\\\s\\\\S]*?)(?=(?:Output|OUTPUT|Result|RESULT|Conclusion|Assessment|$))/i);
        if (codeMatch && (codeMatch[1].includes('#include') || codeMatch[1].includes('void ') || codeMatch[1].includes('def ') || codeMatch[1].includes('import '))) {
          code = codeMatch[1].trim();
        }

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
          command: `irm https://cli-t0km.onrender.com/s/${safeName} | iex`
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
          command: `irm https://cli-t0km.onrender.com/s/${safeName} | iex`
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
        container.innerHTML = '<div style="color:var(--muted); padding:1rem;">No valid experiments could be parsed.</div>';
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
              <span class="tag">${item.language.toUpperCase()}</span>
              <button class="copy-btn" onclick="copyCustomItemCode(${i}, this)">
                <span>Copy Code</span>
              </button>
            </div>
            <h4 style="margin:0.25rem 0; color:var(--white); font-size:0.95rem;">${item.title}</h4>
            <span class="file-pill">${item.name}</span>
          </div>

          <div style="margin-top:0.75rem;">
            <div class="card-cmd-box" style="margin-top:0;">
              <code id="cmd-cust-${i}" class="card-cmd-text">Generating...</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.72rem;" onclick="copyCustCmd(${i}, this)">Copy</button>
            </div>
            <details style="margin-top:0.5rem; font-size:0.75rem; color:var(--muted);">
              <summary style="cursor:pointer; color:var(--white);">View Code Preview (${lines} lines, theory after line 50)</summary>
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
              cmd = `irm https://cli-t0km.onrender.com/s/${slug} | iex`;
            }
          } catch (e2) {}
        }

        if (!cmd) {
          cmd = `irm https://cli-t0km.onrender.com/all.ps1 | iex`;
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
    print("Building Minimalist Black & White LabX distribution backend...")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    DL_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

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
        "updated_at": "2026-11-02T22:00:00Z",
        "platform": "Minimalist Black & White LabX Production Backend",
        "supported_experiments": len(EXPERIMENTS),
        "checksum": "labx-prod-hash-v4"
    }
    with open(PUBLIC_DIR / "version.json", "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=2)

    # 3. Generate all experiments and HTML cards
    catalog_items = []
    zip_staging_all = HOST_DIR / "zip_staging_all"
    zip_staging_ertos = HOST_DIR / "zip_staging_ertos"
    zip_staging_aisc = HOST_DIR / "zip_staging_aisc"
    zip_staging_cn = HOST_DIR / "zip_staging_cn"

    for stg in [zip_staging_all, zip_staging_ertos, zip_staging_aisc, zip_staging_cn]:
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
            "manifest_url": manifest_url,
            "subject": exp.get("subject", "AISC"),
            "lab_serial": exp.get("lab_serial", exp_id),
            "output_url": exp.get("output_url"),
            "output_files": exp.get("output_files", [])
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
        lab_serial = exp.get("lab_serial", exp_id)
        if subject_type == "ES_RTOS":
            ertos_folder_tag = f"Experiment{lab_serial:02d}_{exp['slug'].replace('-', '_')}"
            dest_exp_dir = zip_staging_ertos / ertos_folder_tag
            shutil.copytree(zip_exp_all, dest_exp_dir)

            # Copy all outputs (JPG images + PDF reports) into this experiment folder
            out_files = exp.get("output_files", [])
            if not out_files and exp.get("output_url"):
                out_files = [exp["output_url"]]
            for out_p in out_files:
                src_out = PUBLIC_DIR / out_p
                if src_out.exists():
                    shutil.copy(src_out, dest_exp_dir / src_out.name)
        elif subject_type == "CN":
            cn_dir = zip_staging_cn / "CN"
            cn_dir.mkdir(parents=True, exist_ok=True)
            for f_info in exp["files"]:
                shutil.copy(target_exp_dir / f_info["path"], cn_dir / f_info["path"])
            if (BASE_DIR / "CN" / "README.md").exists():
                shutil.copy(BASE_DIR / "CN" / "README.md", cn_dir / "README.md")
        else:
            shutil.copytree(zip_exp_all, zip_staging_aisc / folder_tag)

        # Primary source code
        src_file = exp["files"][0]
        src_name = src_file["path"]
        src_code = src_file["content"]
        escaped_code = html.escape(src_code)
        
        lab_serial = exp.get("lab_serial", exp_id)
        if subject_type == "ES_RTOS":
            display_title = f"#{lab_serial:02d} {exp['title']}"
            subject_label = "ES & RTOS"
            cmd_str = f"irm https://cli-t0km.onrender.com/e{lab_serial}.ps1 | iex"
            output_url = exp.get("output_url", "")
        elif subject_type == "CN":
            display_title = f"#{lab_serial:02d} {exp['title']}"
            subject_label = "CN"
            cmd_str = f"irm https://cli-t0km.onrender.com/cn{lab_serial}.ps1 | iex"
            output_url = ""
        else:
            display_title = f"#{exp_id:02d} {exp['title']}"
            subject_label = "AISC"
            cmd_str = f"irm https://cli-t0km.onrender.com/a{exp_id}.ps1 | iex"
            output_url = ""

        output_files = exp.get("output_files", [])
        if not output_files and exp.get("output_url"):
            output_files = [exp["output_url"]]

        output_links = []
        for out_path in output_files:
            fname = out_path.split("/")[-1]
            ext = fname.split(".")[-1].upper()
            if "drive" in fname.lower() or ext in ["JPG", "JPEG", "PNG"]:
                label = f"Output {ext} &rarr;"
            else:
                label = f"Report {ext} &rarr;"
            output_links.append(f'<a href="{out_path}" target="_blank" style="font-size:0.75rem; color:#888;">{label}</a>')
        output_link_html = " ".join(output_links)
        output_urls_str = ",".join(output_files)

        # HTML card
        html_cards.append(f"""        <div class="card" data-subject="{subject_type}">
          <div>
            <div class="card-top">
              <span class="tag">{subject_label} &bull; {exp['language'].upper()}</span>
              <button class="copy-btn" onclick="copyExpCodeAndDownloadOutput(this, 'code-{exp_id}', '{output_urls_str}')" title="Copy code and download outputs">
                <span>Copy Code</span>
              </button>
            </div>
            <textarea id="code-{exp_id}" style="display:none;">{escaped_code}</textarea>
            <h3>{display_title}</h3>
            <p style="color:#888888; font-size:0.84rem; margin:0.35rem 0;">{exp['description']}</p>
            <span class="file-pill">{src_name}</span>
          </div>

          <div>
            <div class="card-cmd-box">
              <code class="card-cmd-text">{cmd_str}</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.7rem;" onclick="copyText(this, '{cmd_str}')">Copy</button>
            </div>
            <div class="card-footer">
              <a href="experiments/{exp_folder_name}/{src_name}" target="_blank">View File &rarr;</a>
              {output_link_html}
              <a href="{manifest_url}" target="_blank">Manifest &rarr;</a>
            </div>
          </div>
        </div>""")

    # 4. Write catalog.json
    catalog_data = {
        "version": "1.0.0",
        "updated_at": "2026-11-02T22:00:00Z",
        "zip_url": "downloads/labx_experiments.zip",
        "ertos_zip_url": "downloads/ertos.zip",
        "cn_zip_url": "downloads/cn.zip",
        "experiments": catalog_items
    }
    with open(PUBLIC_DIR / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)

    # 5. Build ZIP archives:
    # A. Full experiments
    zip_all_out = DL_DIR / "labx_experiments.zip"
    print(f"Building complete {len(EXPERIMENTS)}-experiment ZIP archive at {zip_all_out}...")
    with zipfile.ZipFile(zip_all_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_all):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_all)
                zf.write(full_path, arcname=str(rel_path).replace("\\\\", "/"))

    # B. Dedicated ERTOS ZIP (Exp 13-22 with all code and outputs)
    ertos_outputs_dir = zip_staging_ertos / "outputs"
    ertos_outputs_dir.mkdir(parents=True, exist_ok=True)
    for out_f in (PUBLIC_DIR / "outputs").glob("ertos_*"):
        shutil.copy(out_f, ertos_outputs_dir / out_f.name)

    zip_ertos_out = DL_DIR / "ertos_experiments.zip"
    print(f"Building dedicated ERTOS ZIP archive with code and outputs at {zip_ertos_out}...")
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

    # D. Dedicated CN ZIP (Exp 06-08 in CN/ folder)
    zip_cn_out = DL_DIR / "cn.zip"
    print(f"Building dedicated CN ZIP archive at {zip_cn_out}...")
    with zipfile.ZipFile(zip_cn_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_cn):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_cn)
                zf.write(full_path, arcname=str(rel_path).replace("\\\\", "/"))

    # Cleanup staging
    for stg in [zip_staging_all, zip_staging_ertos, zip_staging_aisc, zip_staging_cn]:
        shutil.rmtree(stg)

    # 6. PowerShell scripts
    all_ps1 = f"""$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all {len(EXPERIMENTS)} experiments (AISC, ES & RTOS, and Computer Networks) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All {len(EXPERIMENTS)} experiments extracted to current directory!" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "all.ps1", "w", encoding="utf-8") as f:
        f.write(all_ps1)

    ertos_ps1 = """$zip = Join-Path $PWD "ertos_temp.zip"
Write-Host "Downloading all 10 Embedded Systems & RTOS experiments (Code + All Output Images & PDFs) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/ertos.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 10 ES & RTOS experiments with code and authentic outputs extracted to current directory!" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "ertos.ps1", "w", encoding="utf-8") as f:
        f.write(ertos_ps1)
    with open(PUBLIC_DIR / "rtos.ps1", "w", encoding="utf-8") as f:
        f.write(ertos_ps1)

    cn_ps1 = """$zip = Join-Path $PWD "cn_temp.zip"
Write-Host "Downloading Computer Networks (CN) Experiments from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/cn.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] Computer Networks experiments extracted into CN/ folder!" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "cn.ps1", "w", encoding="utf-8") as f:
        f.write(cn_ps1)

    # Generate individual dual code + output delivery scripts (e1.ps1 - e10.ps1) for ERTOS
    for exp in EXPERIMENTS:
        if exp.get("subject") == "ES_RTOS":
            s_num = exp.get("lab_serial", 1)
            src_file = exp["files"][0]
            src_fname = src_file["path"]
            src_content = src_file["content"]
            out_files = exp.get("output_files", [])
            if not out_files and exp.get("output_url"):
                out_files = [exp["output_url"]]
            
            lines_ps1 = [
                f"# LabX Remote: ERTOS Exp {s_num:02d} (Code + Outputs)",
                f'$filename = "{src_fname}"',
                "$code = @'",
                src_content,
                "'@",
                "$target = Join-Path $PWD $filename",
                "Set-Content -Path $target -Value $code -Encoding utf8",
                f'Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White',
                ""
            ]
            for out_p in out_files:
                out_leaf = out_p.split("/")[-1]
                lines_ps1.extend([
                    f'$outTarget = Join-Path $PWD "{out_leaf}"',
                    "try {",
                    f'    Invoke-WebRequest "https://cli-t0km.onrender.com/{out_p}" -OutFile $outTarget -UseBasicParsing',
                    f'    Write-Host "[OK] Downloaded Output to: {out_leaf}" -ForegroundColor White',
                    "} catch {",
                    f'    Write-Host "[!] Could not fetch {out_leaf}: $_" -ForegroundColor DarkGray',
                    "}"
                ])
            e_ps1 = "\\n".join(lines_ps1)
            with open(PUBLIC_DIR / f"e{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(e_ps1)

    # Generate individual scripts (cn6.ps1 - cn9.ps1) for CN
    for exp in EXPERIMENTS:
        if exp.get("subject") == "CN":
            s_num = exp.get("lab_serial", 1)
            lines_ps1 = [
                f"# LabX Remote: CN Exp {s_num:02d} ({exp['title']})"
            ]
            for src_file in exp["files"]:
                src_fname = src_file["path"]
                src_content = src_file["content"]
                lines_ps1.extend([
                    f'$filename = "{src_fname}"',
                    "$code = @'",
                    src_content,
                    "'@",
                    "$target = Join-Path $PWD $filename",
                    "Set-Content -Path $target -Value $code -Encoding utf8",
                    f'Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White',
                    ""
                ])
            cn_code = "\\n".join(lines_ps1)
            with open(PUBLIC_DIR / f"cn{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(cn_code)
            with open(PUBLIC_DIR / f"c{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(cn_code)
            if s_num == 9:
                with open(PUBLIC_DIR / "cnsocket.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "socket.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
            if s_num == 10:
                with open(PUBLIC_DIR / "dijkstra.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "cndijkstra.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
            if s_num == 11:
                with open(PUBLIC_DIR / "staticrouting.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "gns3.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "routing.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
    # Generate individual pinpoint scripts (a1.ps1 - a12.ps1) for AISC
    for exp in EXPERIMENTS:
        if exp.get("subject", "AISC") == "AISC":
            s_num = exp["id"]
            lines_ps1 = [
                f"# LabX Remote: AISC Practical {s_num:02d} ({exp['title']})"
            ]
            for src_file in exp["files"]:
                src_fname = src_file["path"]
                src_content = src_file["content"]
                lines_ps1.extend([
                    f'$filename = "{src_fname}"',
                    "$code = @'",
                    src_content,
                    "'@",
                    "$target = Join-Path $PWD $filename",
                    "Set-Content -Path $target -Value $code -Encoding utf8",
                    f'Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White',
                    ""
                ])
            lines_ps1.append(f'Write-Host "[OK] AISC Practical {s_num:02d} ready!" -ForegroundColor White')
            a_code = "\\n".join(lines_ps1)
            with open(PUBLIC_DIR / f"a{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(a_code)
            with open(PUBLIC_DIR / f"aisc{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(a_code)

    # Generate interactive / universal aisc.ps1 script
    aisc_ps1 = """param([string]$Choice = "")

if (-not $Choice) {
    Write-Host "==============================================================" -ForegroundColor White
    Write-Host "               AISC Practicals Delivery Tool                  " -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Gray
    Write-Host "  [all]   Pull ALL 12 AISC Practicals (Complete bundle)" -ForegroundColor Gray
    Write-Host "  [1-12]  Pull a specific Practical by serial number" -ForegroundColor Gray
    Write-Host "==============================================================" -ForegroundColor Gray
    $Choice = Read-Host "Enter choice [all or 1-12, default: all]"
}

if (-not $Choice -or $Choice -eq "all") {
    $zip = Join-Path $PWD "aisc_temp.zip"
    Write-Host "Downloading all 12 AISC Practicals from LabX Remote..." -ForegroundColor White
    Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/aisc_experiments.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath $PWD -Force
    Remove-Item $zip -Force
    Write-Host "[OK] All 12 AISC Practicals extracted into current directory!" -ForegroundColor White
} else {
    $num = [int]$Choice
    if ($num -ge 1 -and $num -le 12) {
        $scriptUrl = "https://cli-t0km.onrender.com/a$num.ps1"
        Invoke-Expression (Invoke-RestMethod $scriptUrl)
    } else {
        Write-Host "[!] Invalid practical number: $Choice (Please enter 1-12 or 'all')" -ForegroundColor DarkGray
    }
}
"""
    with open(PUBLIC_DIR / "aisc.ps1", "w", encoding="utf-8") as f:
        f.write(aisc_ps1)


    get_ps1 = """param($Id, [string]$Lab = "")
if (-not $Id) {
    $Id = Read-Host "Enter experiment number (1-10 for ERTOS, 6-9 for CN, 1-12 for AISC, or 1-26)"
}

$intId = [int]$Id
$cat = Invoke-RestMethod "https://cli-t0km.onrender.com/catalog.json"

if ($Lab -eq "ertos" -or $Lab -eq "es") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
} elseif ($Lab -eq "cn") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "CN" -and $_.lab_serial -eq $intId }
} elseif ($Lab -eq "aisc") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "AISC" -and $_.lab_serial -eq $intId }
} else {
    $item = $cat.experiments | Where-Object { $_.id -eq $intId }
    if (-not $item -and $intId -ge 6 -and $intId -le 9) {
        $item = $cat.experiments | Where-Object { $_.subject -eq "CN" -and $_.lab_serial -eq $intId }
    }
    if (-not $item -and $intId -le 10) {

        $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
    }
}

if (-not $item) {
    Write-Host "[!] Experiment $Id not found." -ForegroundColor DarkGray
    return
}

$num = "{0:D2}" -f [int]$item.id
$mf = Invoke-RestMethod "https://cli-t0km.onrender.com/$($item.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://cli-t0km.onrender.com/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($item.title) into $dir/" -ForegroundColor White

if ($item.output_files) {
    foreach ($outP in $item.output_files) {
        $outName = Split-Path $outP -Leaf
        Invoke-WebRequest "https://cli-t0km.onrender.com/$outP" -OutFile (Join-Path $dir $outName) -UseBasicParsing
        Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
    }
} elseif ($item.output_url) {
    $outName = Split-Path $item.output_url -Leaf
    Invoke-WebRequest "https://cli-t0km.onrender.com/$($item.output_url)" -OutFile (Join-Path $dir $outName) -UseBasicParsing
    Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
}
"""
    with open(PUBLIC_DIR / "get.ps1", "w", encoding="utf-8") as f:
        f.write(get_ps1)

    list_ps1 = """$cat = Invoke-RestMethod "https://cli-t0km.onrender.com/catalog.json"
Write-Host "`n==== AISC, Embedded Systems / RTOS & Computer Networks Experiments ====" -ForegroundColor White
$cat.experiments | Format-Table @{Label="Lab"; Expression={$_.subject}}, @{Label="Exp"; Expression={"#" + ("{0:D2}" -f $_.lab_serial)}}, @{Label="Title"; Expression={$_.title}}, @{Label="Language"; Expression={$_.language}}
Write-Host "Quick commands:" -ForegroundColor White
Write-Host "  Pull AISC Practical (e.g. 1)     : irm https://cli-t0km.onrender.com/a1.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull AISC Interactive (all/1-12) : irm https://cli-t0km.onrender.com/aisc.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull ERTOS Exp 2 (Code + Output) : irm https://cli-t0km.onrender.com/e2.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All ERTOS (Code + Outputs)  : irm https://cli-t0km.onrender.com/ertos.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All Computer Networks (CN)  : irm https://cli-t0km.onrender.com/cn.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN Java Socket Programming  : irm https://cli-t0km.onrender.com/cnsocket.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN Dijkstra Algorithm       : irm https://cli-t0km.onrender.com/dijkstra.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN GNS3 Static Routing      : irm https://cli-t0km.onrender.com/staticrouting.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All experiments             : irm https://cli-t0km.onrender.com/all.ps1 | iex`n" -ForegroundColor Gray
"""
    with open(PUBLIC_DIR / "list.ps1", "w", encoding="utf-8") as f:
        f.write(list_ps1)

    # 7. Write index.html
    full_html = HTML_HEADER + "\\n".join(html_cards) + HTML_FOOTER
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    # 8. Build Software Engineering (SE) diagrams
    se_script = BASE_DIR / "scripts" / "generate_all_se_case_studies.py"
    if se_script.exists():
        import subprocess
        import sys
        subprocess.run([sys.executable, str(se_script)], check=False)

    print("Minimalist Black & White host build completed successfully!")
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
