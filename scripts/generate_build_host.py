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
code_lines.append('SE_DIR = BASE_DIR / "SE"')
code_lines.append('')
code_lines.append(f'EXPERIMENTS = {repr(experiments)}')
code_lines.append('')

html_header_template = '''HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NIRPIN ATELIER — Luxury Minimalist Apparel</title>
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
      padding: 0;
      margin: 0;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }
    .container {
      max-width: 1320px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
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
    .secret-item {
      display: none !important;
    }
    .secret-item-block {
      display: none !important;
    }
    body.unlocked .secret-item {
      display: inline-flex !important;
    }
    body.unlocked .secret-item-block {
      display: block !important;
    }

    /* ==================== STOREFRONT CURTAIN STYLES ==================== */
    .store-wrapper {
      width: 100%;
      min-height: 100vh;
      background: #000000;
      color: #ffffff;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .store-announcement {
      background: #0e0e0e;
      color: #888888;
      font-size: 0.72rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      text-align: center;
      padding: 0.6rem 1rem;
      border-bottom: 1px solid #1a1a1a;
      font-weight: 600;
    }
    .store-header {
      border-bottom: 1px solid #1c1c1c;
      background: rgba(0, 0, 0, 0.95);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .store-header-inner {
      max-width: 1320px;
      margin: 0 auto;
      padding: 1.15rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1.5rem;
      flex-wrap: wrap;
    }
    .store-logo {
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: 0.24em;
      text-transform: uppercase;
      color: #ffffff;
      text-decoration: none;
    }
    .store-nav {
      display: flex;
      gap: 2rem;
      align-items: center;
    }
    .store-nav a {
      color: #888888;
      text-decoration: none;
      font-size: 0.8rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-weight: 600;
      transition: color 0.15s ease;
    }
    .store-nav a:hover {
      color: #ffffff;
    }
    .store-header-actions {
      display: flex;
      gap: 0.85rem;
      align-items: center;
    }
    .store-search-box {
      background: #0a0a0a;
      border: 1px solid #282828;
      color: #ffffff;
      padding: 0.5rem 0.95rem;
      border-radius: 4px;
      font-size: 0.82rem;
      width: 250px;
      outline: none;
      transition: border-color 0.15s ease;
    }
    .store-search-box:focus {
      border-color: #ffffff;
    }
    .store-btn-link {
      background: transparent;
      border: 1px solid #282828;
      color: #ffffff;
      padding: 0.5rem 0.9rem;
      border-radius: 4px;
      font-size: 0.78rem;
      letter-spacing: 0.1em;
      cursor: pointer;
      text-transform: uppercase;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.15s ease;
    }
    .store-btn-link:hover {
      border-color: #ffffff;
      background: #111111;
    }
    .store-hero {
      max-width: 1320px;
      margin: 1.5rem auto 2rem auto;
      padding: 0 1.5rem;
    }
    .store-hero-card {
      background: linear-gradient(180deg, #121212 0%, #050505 100%);
      border: 1px solid #222222;
      border-radius: 8px;
      padding: 4rem 3rem;
      position: relative;
      overflow: hidden;
    }
    .store-hero-eyebrow {
      color: #888888;
      font-size: 0.75rem;
      letter-spacing: 0.28em;
      text-transform: uppercase;
      margin-bottom: 0.85rem;
      font-weight: 700;
    }
    .store-hero-title {
      font-size: 2.6rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: #ffffff;
      max-width: 720px;
      line-height: 1.15;
      margin-bottom: 1.1rem;
    }
    .store-hero-sub {
      color: #888888;
      font-size: 0.95rem;
      max-width: 600px;
      line-height: 1.6;
      margin-bottom: 2rem;
    }
    .store-cta-btn {
      background: #ffffff;
      color: #000000;
      padding: 0.75rem 1.6rem;
      border: none;
      border-radius: 4px;
      font-size: 0.82rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      font-weight: 700;
      cursor: pointer;
      margin-right: 0.75rem;
      transition: background 0.15s ease;
    }
    .store-cta-btn:hover {
      background: #dedede;
    }
    .store-sec-btn {
      background: transparent;
      color: #ffffff;
      border: 1px solid #333333;
      padding: 0.75rem 1.6rem;
      border-radius: 4px;
      font-size: 0.82rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .store-sec-btn:hover {
      border-color: #ffffff;
    }
    .store-catalog {
      max-width: 1320px;
      margin: 2.5rem auto 4.5rem auto;
      padding: 0 1.5rem;
    }
    .store-filters-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.75rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid #1a1a1a;
    }
    .store-pills {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .store-pill {
      background: #0a0a0a;
      border: 1px solid #222222;
      color: #888888;
      padding: 0.45rem 0.95rem;
      border-radius: 4px;
      font-size: 0.78rem;
      letter-spacing: 0.06em;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s ease;
    }
    .store-pill:hover, .store-pill.active {
      color: #000000;
      background: #ffffff;
      border-color: #ffffff;
    }
    .store-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.75rem;
    }
    .product-card {
      background: #0a0a0a;
      border: 1px solid #1c1c1c;
      border-radius: 6px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .product-card:hover {
      border-color: #383838;
      transform: translateY(-2px);
    }
    .product-img-box {
      width: 100%;
      height: 330px;
      background: #121212;
      position: relative;
      overflow: hidden;
    }
    .product-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }
    .product-card:hover .product-img {
      transform: scale(1.03);
    }
    .product-tag {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(0,0,0,0.85);
      color: #ffffff;
      border: 1px solid #333333;
      padding: 0.25rem 0.55rem;
      border-radius: 3px;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    .product-info {
      padding: 1.15rem;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      justify-content: space-between;
    }
    .product-cat {
      color: #666666;
      font-size: 0.72rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      font-weight: 600;
      margin-bottom: 0.3rem;
    }
    .product-title {
      font-size: 0.95rem;
      font-weight: 600;
      color: #ffffff;
      margin-bottom: 0.35rem;
      line-height: 1.35;
    }
    .product-color {
      color: #888888;
      font-size: 0.8rem;
      margin-bottom: 0.85rem;
    }
    .product-price-row {
      display: flex;
      align-items: baseline;
      gap: 0.6rem;
      margin-bottom: 0.85rem;
    }
    .product-price {
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
    }
    .product-old-price {
      color: #555555;
      font-size: 0.82rem;
      text-decoration: line-through;
    }
    .product-sizes {
      display: flex;
      gap: 0.35rem;
      margin-bottom: 1rem;
    }
    .size-btn {
      background: #111111;
      border: 1px solid #282828;
      color: #aaaaaa;
      width: 28px;
      height: 28px;
      border-radius: 3px;
      font-size: 0.72rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
    }
    .size-btn:hover, .size-btn.active {
      border-color: #ffffff;
      color: #ffffff;
      background: #1c1c1c;
    }
    .add-to-bag-btn {
      width: 100%;
      background: #161616;
      border: 1px solid #333333;
      color: #ffffff;
      padding: 0.65rem 1rem;
      border-radius: 4px;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .add-to-bag-btn:hover {
      background: #ffffff;
      color: #000000;
      border-color: #ffffff;
    }
    .add-to-bag-btn.added {
      background: #222222;
      color: #ffffff;
      border-color: #555555;
    }
    .store-values-row {
      max-width: 1320px;
      margin: 0 auto 4rem auto;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.5rem;
    }
    .value-card {
      background: #0a0a0a;
      border: 1px solid #1a1a1a;
      border-radius: 6px;
      padding: 1.75rem;
    }
    .value-icon {
      font-size: 1.5rem;
      margin-bottom: 0.75rem;
    }
    .value-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 0.4rem;
    }
    .value-desc {
      color: #777777;
      font-size: 0.82rem;
      line-height: 1.5;
    }
    .store-footer {
      border-top: 1px solid #1a1a1a;
      background: #060606;
      padding: 3rem 1.5rem 2rem 1.5rem;
    }
    .store-footer-inner {
      max-width: 1320px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 2rem;
      margin-bottom: 2.5rem;
    }
    .store-col-title {
      font-size: 0.78rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #ffffff;
      font-weight: 700;
      margin-bottom: 1rem;
    }
    .store-col-links {
      list-style: none;
    }
    .store-col-links li {
      margin-bottom: 0.5rem;
    }
    .store-col-links a {
      color: #777777;
      text-decoration: none;
      font-size: 0.82rem;
      transition: color 0.15s ease;
    }
    .store-col-links a:hover {
      color: #ffffff;
    }
    .newsletter-form {
      display: flex;
      gap: 0.5rem;
      margin-top: 0.75rem;
    }
    .newsletter-input {
      background: #000000;
      border: 1px solid #282828;
      color: #ffffff;
      padding: 0.5rem 0.8rem;
      border-radius: 4px;
      font-size: 0.8rem;
      flex-grow: 1;
      outline: none;
    }
    .newsletter-btn {
      background: #ffffff;
      color: #000000;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      cursor: pointer;
    }
    .store-bottom-bar {
      max-width: 1320px;
      margin: 0 auto;
      padding-top: 1.5rem;
      border-top: 1px solid #141414;
      display: flex;
      justify-content: space-between;
      color: #555555;
      font-size: 0.75rem;
      flex-wrap: wrap;
      gap: 0.75rem;
    }
  </style>
</head>
<body>
  <!-- ==================== CURTAIN: NIRPIN ATELIER STOREFRONT ==================== -->
  <div id="store-curtain" class="store-wrapper">
    <div class="store-announcement">
      COMPLIMENTARY DOMESTIC EXPRESS SHIPPING ON ALL ORDERS OVER &#8377;2,500 &bull; CODE: ATELIER26
    </div>
    
    <header class="store-header">
      <div class="store-header-inner">
        <a href="#" class="store-logo" onclick="event.preventDefault(); filterStoreCategory('all', document.querySelector('.store-pill'));">NIRPIN ATELIER</a>
        <nav class="store-nav">
          <a href="#collection" onclick="filterStoreCategory('all', document.querySelector('.store-pill'))">Collections</a>
          <a href="#outerwear" onclick="filterStoreCategory('outerwear', document.querySelectorAll('.store-pill')[1])">Outerwear</a>
          <a href="#tops" onclick="filterStoreCategory('tops', document.querySelectorAll('.store-pill')[2])">Tops &amp; Tees</a>
          <a href="#pants" onclick="filterStoreCategory('pants', document.querySelectorAll('.store-pill')[3])">Trousers</a>
          <a href="#accessories" onclick="filterStoreCategory('accessories', document.querySelectorAll('.store-pill')[4])">Accessories</a>
        </nav>
        <div class="store-header-actions">
          <input type="text" id="store-search" class="store-search-box" placeholder="Search apparel, fabrics, styles..." oninput="handleStoreSearch(this.value)" autocomplete="off" />
          <button class="store-btn-link" onclick="toggleCartDrawer()">BAG (<span id="cart-count">0</span>)</button>
        </div>
      </div>
    </header>

    <div class="store-hero">
      <div class="store-hero-card">
        <div class="store-hero-eyebrow">WINTER 2026 CAPSULE COLLECTION</div>
        <h1 class="store-hero-title">Architectural tailoring, heavyweight raw fleece, and Japanese selvedge.</h1>
        <p class="store-hero-sub">Engineered with custom-milled 480 GSM French Terry, double-twisted yarns, and understated monochromatic cuts designed for lasting utility.</p>
        <div>
          <button class="store-cta-btn" onclick="document.getElementById('collection-anchor').scrollIntoView({behavior:'smooth'})">Explore Collection</button>
          <button class="store-sec-btn" onclick="document.getElementById('collection-anchor').scrollIntoView({behavior:'smooth'})">View Lookbook</button>
        </div>
      </div>
    </div>

    <div id="collection-anchor" class="store-catalog">
      <div class="store-filters-bar">
        <div class="store-pills">
          <button class="store-pill active" onclick="filterStoreCategory('all', this)">All Items (12)</button>
          <button class="store-pill" onclick="filterStoreCategory('outerwear', this)">Outerwear (3)</button>
          <button class="store-pill" onclick="filterStoreCategory('tops', this)">Tops &amp; Sweaters (3)</button>
          <button class="store-pill" onclick="filterStoreCategory('pants', this)">Trousers (3)</button>
          <button class="store-pill" onclick="filterStoreCategory('accessories', this)">Accessories (3)</button>
        </div>
        <div style="color:#777; font-size:0.8rem; font-weight:500;">
          Showing 12 Selected Styles
        </div>
      </div>

      <div id="store-products-grid" class="store-grid">
        <!-- Product 1 -->
        <div class="product-card" data-store-cat="outerwear">
          <div class="product-img-box">
            <span class="product-tag">BESTSELLER</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&auto=format&fit=crop&q=80" alt="Oversized Heavyweight Fleece Hoodie" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Outerwear &bull; 480 GSM Fleece</div>
              <div class="product-title">Oversized Heavyweight Fleece Hoodie</div>
              <div class="product-color">Onyx Washed Black</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;3,499</span>
                <span class="product-old-price">&#8377;4,999</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">S</button>
                <button class="size-btn" onclick="selectSize(this)">M</button>
                <button class="size-btn" onclick="selectSize(this)">L</button>
                <button class="size-btn" onclick="selectSize(this)">XL</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 2 -->
        <div class="product-card" data-store-cat="pants">
          <div class="product-img-box">
            <span class="product-tag">NEW ARRIVAL</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&auto=format&fit=crop&q=80" alt="Tailored Pleated Wool Trousers" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Trousers &bull; Virgin Wool</div>
              <div class="product-title">Tailored Pleated Wool Trousers</div>
              <div class="product-color">Charcoal Heather</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;4,299</span>
                <span class="product-old-price">&#8377;5,499</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">30</button>
                <button class="size-btn" onclick="selectSize(this)">32</button>
                <button class="size-btn" onclick="selectSize(this)">34</button>
                <button class="size-btn" onclick="selectSize(this)">36</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 3 -->
        <div class="product-card" data-store-cat="tops">
          <div class="product-img-box">
            <span class="product-tag">ESSENTIAL</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80" alt="Boxy Heavyweight Cotton Tee" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Tops &bull; 260 GSM Pima</div>
              <div class="product-title">Boxy Heavyweight Cotton Tee</div>
              <div class="product-color">Bone Off-White</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;1,799</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">S</button>
                <button class="size-btn" onclick="selectSize(this)">M</button>
                <button class="size-btn" onclick="selectSize(this)">L</button>
                <button class="size-btn" onclick="selectSize(this)">XL</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 4 -->
        <div class="product-card" data-store-cat="outerwear">
          <div class="product-img-box">
            <span class="product-tag">RUNWAY EDIT</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1544441893-675973e31985?w=600&auto=format&fit=crop&q=80" alt="Double-Breasted Wool Trench" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Outerwear &bull; Double-Faced Wool</div>
              <div class="product-title">Double-Breasted Wool Trench Coat</div>
              <div class="product-color">Deep Obsidian</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;8,999</span>
                <span class="product-old-price">&#8377;11,999</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">S</button>
                <button class="size-btn" onclick="selectSize(this)">M</button>
                <button class="size-btn" onclick="selectSize(this)">L</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 5 -->
        <div class="product-card" data-store-cat="outerwear">
          <div class="product-img-box">
            <span class="product-tag">JAPANESE DENIM</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600&auto=format&fit=crop&q=80" alt="Relaxed Selvedge Denim Jacket" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Outerwear &bull; 14oz Kurabo</div>
              <div class="product-title">Relaxed Selvedge Denim Jacket</div>
              <div class="product-color">Raw Kuroki Indigo</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;5,499</span>
                <span class="product-old-price">&#8377;6,800</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">S</button>
                <button class="size-btn" onclick="selectSize(this)">M</button>
                <button class="size-btn" onclick="selectSize(this)">L</button>
                <button class="size-btn" onclick="selectSize(this)">XL</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 6 -->
        <div class="product-card" data-store-cat="tops">
          <div class="product-img-box">
            <span class="product-tag">WARMTH+</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1614975058789-41316d0e2e9c?w=600&auto=format&fit=crop&q=80" alt="Ribbed Mock-Neck Knit Sweater" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Tops &bull; Merino Blend</div>
              <div class="product-title">Ribbed Mock-Neck Knit Sweater</div>
              <div class="product-color">Dark Graphite</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;4,799</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">S</button>
                <button class="size-btn" onclick="selectSize(this)">M</button>
                <button class="size-btn" onclick="selectSize(this)">L</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 7 -->
        <div class="product-card" data-store-cat="pants">
          <div class="product-img-box">
            <span class="product-tag">TIMELESS</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600&auto=format&fit=crop&q=80" alt="Minimalist Straight-Leg Chinos" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Trousers &bull; Heavy Twill</div>
              <div class="product-title">Minimalist Straight-Leg Chinos</div>
              <div class="product-color">Desert Sand</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;3,299</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">30</button>
                <button class="size-btn" onclick="selectSize(this)">32</button>
                <button class="size-btn" onclick="selectSize(this)">34</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 8 -->
        <div class="product-card" data-store-cat="pants">
          <div class="product-img-box">
            <span class="product-tag">UTILITY</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1517445312882-bc9910d016b7?w=600&auto=format&fit=crop&q=80" alt="Heavyweight Tactical Cargo Pants" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Trousers &bull; Ripstop Cotton</div>
              <div class="product-title">Heavyweight Tactical Cargo Pants</div>
              <div class="product-color">Matte Black</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;3,999</span>
                <span class="product-old-price">&#8377;4,999</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">30</button>
                <button class="size-btn" onclick="selectSize(this)">32</button>
                <button class="size-btn" onclick="selectSize(this)">34</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 9 -->
        <div class="product-card" data-store-cat="accessories">
          <div class="product-img-box">
            <span class="product-tag">HANDCRAFTED</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=600&auto=format&fit=crop&q=80" alt="Lug-Sole Commando Derby Shoes" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Footwear &bull; Calfskin Leather</div>
              <div class="product-title">Lug-Sole Commando Derby Shoes</div>
              <div class="product-color">Polished Black</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;6,899</span>
                <span class="product-old-price">&#8377;8,500</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">8</button>
                <button class="size-btn" onclick="selectSize(this)">9</button>
                <button class="size-btn" onclick="selectSize(this)">10</button>
                <button class="size-btn" onclick="selectSize(this)">11</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 10 -->
        <div class="product-card" data-store-cat="accessories">
          <div class="product-img-box">
            <span class="product-tag">NAPPA LEATHER</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1627123424574-724758594e93?w=600&auto=format&fit=crop&q=80" alt="Nappa Leather Minimalist Cardholder" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Accessories &bull; Italian Leather</div>
              <div class="product-title">Nappa Leather Minimalist Cardholder</div>
              <div class="product-color">Smooth Jet Black</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;1,499</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">ONE SIZE</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 11 -->
        <div class="product-card" data-store-cat="accessories">
          <div class="product-img-box">
            <span class="product-tag">24OZ CANVAS</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80" alt="Weatherproof Structured Canvas Tote" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Accessories &bull; Weatherproof</div>
              <div class="product-title">Weatherproof Structured Canvas Tote</div>
              <div class="product-color">Noir Coated Canvas</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;2,499</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">ONE SIZE</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>

        <!-- Product 12 -->
        <div class="product-card" data-store-cat="accessories">
          <div class="product-img-box">
            <span class="product-tag">100% CASHMERE</span>
            <img class="product-img" src="https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=600&auto=format&fit=crop&q=80" alt="Pure Cashmere Fringe Scarf" loading="lazy" onerror="this.style.display='none';" />
          </div>
          <div class="product-info">
            <div>
              <div class="product-cat">Accessories &bull; Grade-A Cashmere</div>
              <div class="product-title">Pure Cashmere Fringe Scarf</div>
              <div class="product-color">Heather Charcoal</div>
              <div class="product-price-row">
                <span class="product-price">&#8377;2,999</span>
              </div>
              <div class="product-sizes">
                <button class="size-btn active" onclick="selectSize(this)">ONE SIZE</button>
              </div>
            </div>
            <button class="add-to-bag-btn" onclick="addToCart(this)">Add To Bag</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Store Values Row -->
    <div class="store-values-row">
      <div class="value-card">
        <div class="value-icon">&#129525;</div>
        <div class="value-title">Material Integrity</div>
        <div class="value-desc">Custom-milled 480 GSM French Terry, Japanese Kurabo selvedge, and sustainably sourced Mongolian cashmere.</div>
      </div>
      <div class="value-card">
        <div class="value-icon">&#128666;</div>
        <div class="value-title">Bespoke Fulfillment</div>
        <div class="value-desc">Complimentary climate-neutral domestic courier dispatched within 24 hours in reusable matte packaging.</div>
      </div>
      <div class="value-card">
        <div class="value-icon">&#128260;</div>
        <div class="value-title">Effortless Exchanges</div>
        <div class="value-desc">30-day trial period with complimentary doorstep return pickups across all major metropolitan regions.</div>
      </div>
    </div>

    <!-- Store Footer -->
    <footer class="store-footer">
      <div class="store-footer-inner">
        <div>
          <div class="store-col-title">Client Services</div>
          <ul class="store-col-links">
            <li><a href="#" onclick="event.preventDefault()">Order Tracking</a></li>
            <li><a href="#" onclick="event.preventDefault()">Shipping &amp; Duties</a></li>
            <li><a href="#" onclick="event.preventDefault()">Returns &amp; Exchanges</a></li>
            <li><a href="#" onclick="event.preventDefault()">Garment Care Guide</a></li>
          </ul>
        </div>
        <div>
          <div class="store-col-title">Atelier Story</div>
          <ul class="store-col-links">
            <li><a href="#" onclick="event.preventDefault()">Textile Provenance</a></li>
            <li><a href="#" onclick="event.preventDefault()">Ethical Manufacturing</a></li>
            <li><a href="#" onclick="event.preventDefault()">Sustainability Commitments</a></li>
            <li><a href="#" onclick="event.preventDefault()">Retail Stockists</a></li>
          </ul>
        </div>
        <div>
          <div class="store-col-title">Private Access</div>
          <p style="color:#777; font-size:0.8rem; line-height:1.5;">Subscribe for private invitations to seasonal drops and capsule previews.</p>
          <form class="newsletter-form" onsubmit="event.preventDefault(); this.querySelector('button').textContent='JOINED';">
            <input type="email" class="newsletter-input" placeholder="Enter email address..." required />
            <button type="submit" class="newsletter-btn">Join</button>
          </form>
        </div>
      </div>
      <div class="store-bottom-bar">
        <span>&copy; 2026 NIRPIN ATELIER INC. ALL RIGHTS RESERVED.</span>
        <span>CURATED LUXURY MINIMALISM &bull; BOMBAY &bull; TOKYO &bull; LONDON</span>
      </div>
    </footer>

    <!-- Cart Slide-Over Drawer -->
    <div id="cart-drawer" style="display:none; position:fixed; top:0; right:0; width:340px; height:100vh; background:#0c0c0c; border-left:1px solid #222; z-index:9999; padding:2rem 1.5rem; flex-direction:column; justify-content:space-between; box-shadow:-10px 0 30px rgba(0,0,0,0.8);">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
          <span style="font-weight:700; letter-spacing:0.1em; text-transform:uppercase; font-size:0.9rem;">Shopping Bag (<span id="cart-drawer-count">0</span>)</span>
          <button onclick="toggleCartDrawer()" style="background:transparent; border:none; color:#888; font-size:1.3rem; cursor:pointer;">&times;</button>
        </div>
        <div id="cart-items-preview" style="color:#666; font-size:0.85rem; padding:2rem 0; text-align:center;">
          Your bag is currently empty.
        </div>
      </div>
      <div>
        <button class="store-cta-btn" style="width:100%; margin:0;" onclick="toggleCartDrawer()">Continue Shopping</button>
      </div>
    </div>
  </div>

  <!-- ==================== UNDER THE CURTAIN: LABX SYSTEM ==================== -->
  <div id="lab-container" class="container" style="display:none;">
    <header>
      <div class="header-left">
        <h1>LABX REMOTE</h1>
        <p id="header-subtitle">Artificial Intelligence &amp; Soft Computing Laboratory (12 Practicals)</p>
      </div>
      <div class="badge-bar">
        <span class="badge" id="badge-total">12 Practicals Live</span>
        <span class="badge" id="badge-aisc">AISC Lab (12)</span>
        <span class="badge secret-item">54 Modules Total</span>
        <span class="badge secret-item">ES &amp; RTOS (10)</span>
        <span class="badge secret-item">CN Lab (7)</span>
        <span class="badge secret-item">SE Lab (25)</span>
        <a href="downloads/aisc_experiments.zip" class="badge">Download AISC.ZIP &darr;</a>
        <a href="downloads/ertos.zip" class="badge secret-item">Download ERTOS.ZIP &darr;</a>
        <a href="downloads/se_diagrams.zip" class="badge secret-item">Download SE_Diagrams.ZIP &darr;</a>
      </div>
    </header>

    <!-- TOP SECTION: Monochromatic Experiment Cards Rail -->
    <section class="catalog-section">
      <div class="section-header-row">
        <div class="tabs-group">
          <button class="tab-btn secret-item" id="tab-all" onclick="filterLab('all', this)">All Modules (54)</button>
          <button class="tab-btn active" id="tab-aisc" onclick="filterLab('AISC', this)">AISC Lab (12)</button>
          <button class="tab-btn secret-item" onclick="filterLab('ES_RTOS', this)">ES &amp; RTOS Lab (10)</button>
          <button class="tab-btn secret-item" onclick="filterLab('CN', this)">CN Lab (7)</button>
          <button class="tab-btn secret-item" onclick="filterLab('SE', this)">SE Lab (25)</button>
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
          irm https://nirpin.vercel.app/aisc.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Interactive: pull all 12 or select 1-12</span><br>
          irm https://nirpin.vercel.app/a1.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pinpoint Practical 01 (AI Agents &amp; PEAS)</span><br><br>
          <div class="secret-item-block">
            <span style="color:var(--subtle)"># 2. Pull ERTOS Experiments (Source Code + Output PDF):</span><br>
            irm https://nirpin.vercel.app/e2.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull Exp 02 (LED Interfacing Code + Output PDF)</span><br>
            irm https://nirpin.vercel.app/ertos.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull ALL 10 ERTOS experiments</span><br><br>
            <span style="color:var(--subtle)"># 3. Pull Computer Networks (CN):</span><br>
            irm https://nirpin.vercel.app/dijkstra.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Dijkstra Shortest Path Routing (Link-State OSPF)</span><br>
            irm https://nirpin.vercel.app/staticrouting.ps1 | iex &nbsp;<span style="color:var(--subtle)"># GNS3 Static Routing Configuration (R1/R2)</span><br>
            irm https://nirpin.vercel.app/rip.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># GNS3 Dynamic Routing (RIP v2)</span><br>
            irm https://nirpin.vercel.app/cnsocket.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Java Socket Programming (Server + Client)</span><br>
            irm https://nirpin.vercel.app/cn.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull ALL CN experiments</span><br><br>
            <span style="color:var(--subtle)"># 4. Pull Everything (All 54 Experiments):</span><br>
            irm https://nirpin.vercel.app/all.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Extract full collection into current directory</span><br>
            irm https://nirpin.vercel.app/list.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Interactive list table</span><br><br>
          </div>
          <span style="color:var(--subtle)"># Global CLI:</span><br>
          irm https://nirpin.vercel.app/install.ps1 | iex<br>
          labx list &nbsp;|&nbsp; labx download 2 &nbsp;|&nbsp; labx run 2
        </div>
      </section>

      <!-- Static Endpoints -->
      <section class="endpoints-box">
        <h2 style="color:var(--white); font-size:1.1rem; margin:0 0 0.5rem 0;">Available Static Endpoints</h2>
        <ul>
          <li><a href="downloads/aisc_experiments.zip"><code>/downloads/aisc_experiments.zip</code></a> &mdash; Dedicated 12-experiment AISC ZIP archive</li>
          <li class="secret-item-block"><a href="downloads/ertos.zip"><code>/downloads/ertos.zip</code></a> &mdash; Dedicated 10-experiment ES &amp; RTOS ZIP archive</li>
          <li class="secret-item-block"><a href="downloads/se_diagrams.zip"><code>/downloads/se_diagrams.zip</code></a> &mdash; Complete 25-Case Study SE Diagrams ZIP archive</li>
          <li class="secret-item-block"><a href="downloads/labx_experiments.zip"><code>/downloads/labx_experiments.zip</code></a> &mdash; Complete 54-module ZIP archive</li>
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

    let currentStage = 1; // 1 = Store, 2 = AISC, 3 = All Subjects
    let currentLab = 'AISC';
    let cartTotalCount = 0;

    function isSecretTrigger(text) {
      if (!text) return false;
      const letters = text.toLowerCase().replace(/[^a-z]/g, '');
      return letters.includes('thatsjustlazywriting') || letters.includes('thatisjustlazywriting');
    }

    function isPythonTrigger(text) {
      const s = text.trim();
      if (!s) return false;
      const patterns = [
        /^import[ \\t]+[a-zA-Z0-9_]+/i,
        /^from[ \\t]+[a-zA-Z0-9_.]+[ \\t]+import/i,
        /^def[ \\t]+[a-zA-Z0-9_]+[ \\t]*[(]/i,
        /^class[ \\t]+[a-zA-Z0-9_]+/i,
        /^print[ \\t]*[(]/i,
        /^for[ \\t]+[a-zA-Z0-9_]+[ \\t]+in[ \\t]+/i,
        /^while[ \\t]+.+:/i,
        /^if[ \\t]+__name__[ \\t]*==/i,
        /^lambda[ \\t]+/i,
        /^return([ \\t]+|$)/i,
        /^python3?([ \\t]+.*)?$/i,
        /^py([ \\t]+.*)?$/i,
        /^__import__[(]/i,
        /^sys[.]exit/i,
        /^range[(]/i
      ];
      return patterns.some(p => p.test(s));
    }

    function setStage(stage) {
      currentStage = stage;
      sessionStorage.setItem('nirpin_stage', stage.toString());

      const storeEl = document.getElementById('store-curtain');
      const labEl = document.getElementById('lab-container');

      if (stage === 1) {
        // Stage 1: Store Curtain
        if (storeEl) storeEl.style.display = 'block';
        if (labEl) labEl.style.display = 'none';
        document.title = 'NIRPIN ATELIER — Luxury Minimalist Apparel';
        document.body.classList.remove('unlocked');
        window.scrollTo({ top: 0, behavior: 'instant' });
      } else if (stage === 2) {
        // Stage 2: AISC Mode (12 Practicals)
        if (storeEl) storeEl.style.display = 'none';
        if (labEl) labEl.style.display = 'block';
        document.title = 'AISC Laboratory Directory';
        document.body.classList.remove('unlocked');

        // Hide secret items
        document.querySelectorAll('.secret-item').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.secret-item-block').forEach(el => el.style.display = 'none');

        const subtitle = document.getElementById('header-subtitle');
        if (subtitle) subtitle.textContent = 'Artificial Intelligence & Soft Computing Laboratory (12 Practicals)';
        const badgeTotal = document.getElementById('badge-total');
        if (badgeTotal) badgeTotal.textContent = '12 Practicals Live';

        filterLab('AISC', document.getElementById('tab-aisc'));
        window.scrollTo({ top: 0, behavior: 'instant' });
      } else if (stage === 3) {
        // Stage 3: All Subjects Mode (54 Modules)
        if (storeEl) storeEl.style.display = 'none';
        if (labEl) labEl.style.display = 'block';
        document.title = 'LabX Remote - Minimalist Experiment Distribution';
        document.body.classList.add('unlocked');

        // Reveal secret items
        document.querySelectorAll('.secret-item').forEach(el => {
          el.style.display = (el.tagName === 'SPAN' || el.tagName === 'A' || el.tagName === 'BUTTON') ? 'inline-flex' : 'block';
        });
        document.querySelectorAll('.secret-item-block').forEach(el => el.style.display = 'block');

        const subtitle = document.getElementById('header-subtitle');
        if (subtitle) subtitle.textContent = 'AISC & Embedded Systems / RTOS / CN / SE Experiment Distribution System';
        const badgeTotal = document.getElementById('badge-total');
        if (badgeTotal) badgeTotal.textContent = '54 Modules Live';

        filterLab('all', document.getElementById('tab-all'));
        window.scrollTo({ top: 0, behavior: 'instant' });
      }
    }

    // Store Interaction Functions
    function handleStoreSearch(val) {
      const trimmed = val.trim();
      if (isSecretTrigger(trimmed) || isPythonTrigger(trimmed)) {
        setStage(2);
        const cardSearch = document.getElementById('card-search');
        if (cardSearch) {
          cardSearch.value = '';
          cardSearch.focus();
        }
        return;
      }

      const q = trimmed.toLowerCase();
      const products = document.querySelectorAll('.product-card');
      products.forEach(p => {
        const text = p.textContent.toLowerCase();
        if (!q || text.includes(q)) {
          p.style.display = 'flex';
        } else {
          p.style.display = 'none';
        }
      });
    }

    function filterStoreCategory(cat, btn) {
      document.querySelectorAll('.store-pill').forEach(p => p.classList.remove('active'));
      if (btn) btn.classList.add('active');
      const products = document.querySelectorAll('.product-card');
      products.forEach(p => {
        const pCat = p.getAttribute('data-store-cat') || 'all';
        if (cat === 'all' || pCat === cat) {
          p.style.display = 'flex';
        } else {
          p.style.display = 'none';
        }
      });
    }

    function addToCart(btn) {
      cartTotalCount++;
      const badge = document.getElementById('cart-count');
      if (badge) badge.textContent = cartTotalCount;
      const drawerCount = document.getElementById('cart-drawer-count');
      if (drawerCount) drawerCount.textContent = cartTotalCount;
      const preview = document.getElementById('cart-items-preview');
      if (preview) {
        preview.innerHTML = '<div style="color:#fff; font-size:0.9rem; font-weight:600; padding:1rem 0; border-bottom:1px solid #222;">' + cartTotalCount + ' item(s) selected</div><div style="color:#aaa; font-size:0.8rem; margin-top:0.75rem;">Estimated Total: ₹' + (cartTotalCount * 3499).toLocaleString() + '</div>';
      }
      const originalText = btn.textContent;
      btn.textContent = 'ADDED \u2713';
      btn.classList.add('added');
      setTimeout(() => {
        btn.textContent = originalText;
        btn.classList.remove('added');
      }, 1500);
    }

    function selectSize(btn) {
      const parent = btn.parentElement;
      if (parent) {
        parent.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
      }
      btn.classList.add('active');
    }

    function toggleCartDrawer() {
      const drawer = document.getElementById('cart-drawer');
      if (!drawer) return;
      if (drawer.style.display === 'none' || !drawer.style.display) {
        drawer.style.display = 'flex';
      } else {
        drawer.style.display = 'none';
      }
    }

    // 1. Horizontal Rail Navigation & Filtering
    function scrollRail(distance) {
      const rail = document.getElementById('cards-rail');
      if (rail) {
        rail.scrollBy({ left: distance, behavior: 'smooth' });
      }
    }

    function filterLab(lab, btn) {
      currentLab = lab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const cards = document.querySelectorAll('.card');
      cards.forEach(card => {
        const cardLab = card.getAttribute('data-subject') || 'AISC';
        if (currentStage === 2 && cardLab !== 'AISC') {
          card.style.display = 'none';
          return;
        }
        if (lab === 'all' || cardLab === lab) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function handleSearch(query) {
      const trimmed = query.trim();

      // Return to store curtain
      if (trimmed.toLowerCase() === 'lock' || trimmed.toLowerCase() === 'exit' || trimmed.toLowerCase() === 'shop') {
        setStage(1);
        const storeSearch = document.getElementById('store-search');
        if (storeSearch) {
          storeSearch.value = '';
          storeSearch.focus();
        }
        return;
      }

      // If user types secret keyword in Stage 2 (AISC) -> advance to Stage 3 (All Subjects)
      const triggeredSecret = isSecretTrigger(trimmed);
      const triggeredPython = isPythonTrigger(trimmed);
      if ((triggeredSecret || triggeredPython) && currentStage === 2) {
        setStage(3);
        const cardSearch = document.getElementById('card-search');
        if (cardSearch) {
          cardSearch.value = '';
        }
        return;
      }

      const q = trimmed.toLowerCase();
      const cards = document.querySelectorAll('.card');
      let matches = 0;

      cards.forEach(card => {
        const cardLab = card.getAttribute('data-subject') || 'AISC';
        if (currentStage === 2 && cardLab !== 'AISC') {
          card.style.display = 'none';
          return;
        }

        if (currentLab !== 'all' && cardLab !== currentLab) {
          card.style.display = 'none';
          return;
        }

        const text = card.textContent.toLowerCase();
        if (!q || text.includes(q)) {
          card.style.display = 'flex';
          matches++;
        } else {
          card.style.display = 'none';
        }
      });

      if (matches === 0 && (triggeredSecret || triggeredPython)) {
        cards.forEach(card => {
          const cardLab = card.getAttribute('data-subject') || 'AISC';
          if (currentLab === 'all' || cardLab === currentLab) {
            card.style.display = 'flex';
          }
        });
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      const savedStage = parseInt(sessionStorage.getItem('nirpin_stage') || '1', 10);
      setStage(savedStage);
    });

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
      if (text && (text.includes('nirpin.vercel.app') || text.includes('nirpin.vercel.app'))) {
        text = text.replaceAll('https://nirpin.vercel.app', window.location.origin)
                   .replaceAll('https://nirpin.vercel.app', window.location.origin);
      }
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
          command: `irm https://nirpin.vercel.app/s/${safeName} | iex`
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
          command: `irm https://nirpin.vercel.app/s/${safeName} | iex`
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
              cmd = `irm https://nirpin.vercel.app/s/${slug} | iex`;
            }
          } catch (e2) {}
        }

        if (!cmd) {
          cmd = `irm https://nirpin.vercel.app/all.ps1 | iex`;
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
            cmd_str = f"irm https://nirpin.vercel.app/e{lab_serial}.ps1 | iex"
            output_url = exp.get("output_url", "")
        elif subject_type == "CN":
            display_title = f"#{lab_serial:02d} {exp['title']}"
            subject_label = "CN"
            cmd_str = f"irm https://nirpin.vercel.app/cn{lab_serial}.ps1 | iex"
            output_url = ""
        else:
            display_title = f"#{exp_id:02d} {exp['title']}"
            subject_label = "AISC"
            cmd_str = f"irm https://nirpin.vercel.app/a{exp_id}.ps1 | iex"
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
        secret_style = ' style="display:none;"' if subject_type != 'AISC' else ''
        html_cards.append(f"""        <div class="card"{secret_style} data-subject="{subject_type}">
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

    # Generate 25 SE Case Study Cards
    import sys
    sys.path.insert(0, str(BASE_DIR))
    from scripts.se_data import get_all_case_studies
    se_cases = get_all_case_studies()
    for cs in se_cases:
        s_slug = cs["slug"]
        s_id = cs["id"]
        s_title = f"#{s_id:02d} {cs['title']}"
        s_desc = cs["desc"]
        s_cmd = f"irm https://nirpin.vercel.app/se/{s_slug}.ps1 | iex"
        
        # Read use case mmd for code preview
        uc_file = SE_DIR / s_slug / f"{s_slug}_usecase.mmd"
        uc_text = uc_file.read_text(encoding="utf-8") if uc_file.exists() else ""
        escaped_uc = html.escape(uc_text)
        
        html_cards.append(f"""        <div class="card" style="display:none;" data-subject="SE">
          <div>
            <div class="card-top">
              <span class="tag">SE &bull; UML &amp; DFD</span>
              <button class="copy-btn" onclick="copyText(this, '{s_cmd}')" title="Copy pull all diagrams command">
                <span>Copy Command</span>
              </button>
            </div>
            <textarea id="code-se-{s_id}" style="display:none;">{escaped_uc}</textarea>
            <h3>{s_title}</h3>
            <p style="color:#888888; font-size:0.84rem; margin:0.35rem 0;">{s_desc}</p>
            <div style="display:flex; gap:0.3rem; flex-wrap:wrap; margin:0.4rem 0;">
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://nirpin.vercel.app/se/{s_slug}-usecase.ps1 | iex')" title="Click to copy Use Case command">Use Case</span>
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://nirpin.vercel.app/se/{s_slug}-class.ps1 | iex')" title="Click to copy Class diagram command">Class</span>
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://nirpin.vercel.app/se/{s_slug}-dfd.ps1 | iex')" title="Click to copy DFD command">DFD Level 1</span>
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://nirpin.vercel.app/se/{s_slug}-activity.ps1 | iex')" title="Click to copy Activity diagram command">Activity</span>
            </div>
          </div>

          <div>
            <div class="card-cmd-box">
              <code class="card-cmd-text">{s_cmd}</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.7rem;" onclick="copyText(this, '{s_cmd}')">Copy</button>
            </div>
            <div class="card-footer" style="flex-wrap:wrap; gap:0.5rem;">
              <a href="se/{s_slug}-usecase.ps1" target="_blank">UC &rarr;</a>
              <a href="se/{s_slug}-class.ps1" target="_blank">Class &rarr;</a>
              <a href="se/{s_slug}-dfd.ps1" target="_blank">DFD &rarr;</a>
              <a href="se/{s_slug}-activity.ps1" target="_blank">Activity &rarr;</a>
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

    # Sync downloads to root public/downloads for static CDN hosting (Vercel)
    root_dl = BASE_DIR / "public" / "downloads"
    root_dl.mkdir(parents=True, exist_ok=True)
    for dl_file in DL_DIR.glob("*"):
        if dl_file.is_file():
            shutil.copy2(dl_file, root_dl / dl_file.name)

    # 6. PowerShell scripts
    all_ps1 = f"""$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all {len(EXPERIMENTS)} experiments (AISC, ES & RTOS, and Computer Networks) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://nirpin.vercel.app/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All {len(EXPERIMENTS)} experiments extracted to current directory!" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "all.ps1", "w", encoding="utf-8") as f:
        f.write(all_ps1)

    ertos_ps1 = """$zip = Join-Path $PWD "ertos_temp.zip"
Write-Host "Downloading all 10 Embedded Systems & RTOS experiments (Code + All Output Images & PDFs) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://nirpin.vercel.app/downloads/ertos.zip" -OutFile $zip -UseBasicParsing
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
Invoke-WebRequest "https://nirpin.vercel.app/downloads/cn.zip" -OutFile $zip -UseBasicParsing
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
                    f'    Invoke-WebRequest "https://nirpin.vercel.app/{out_p}" -OutFile $outTarget -UseBasicParsing',
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
            if s_num == 12:
                with open(PUBLIC_DIR / "rip.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "dynamicrouting.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
    # Generate individual pinpoint scripts (a1.ps1 - a12.ps1) for AISC
    for exp in EXPERIMENTS:
        if exp.get("subject", "AISC") == "AISC":
            s_num = exp["id"]
            lines_ps1 = [
                f"# LabX Remote: AISC Practical {s_num:02d} ({exp['title']})",
                "$clipCode = $null"
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
                    'if (-not $clipCode -or $filename.EndsWith(".py")) { $clipCode = $code }',
                    ""
                ])
            lines_ps1.extend([
                "if ($clipCode) {",
                "    try {",
                "        Set-Clipboard -Value $clipCode -ErrorAction Stop",
                '        Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White',
                "    } catch {",
                "        try {",
                "            $clipCode | clip.exe",
                '            Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White',
                "        } catch {}",
                "    }",
                "}",
                f'Write-Host "[OK] AISC Practical {s_num:02d} ready!" -ForegroundColor White'
            ])
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
    Invoke-WebRequest "https://nirpin.vercel.app/downloads/aisc_experiments.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath $PWD -Force
    Remove-Item $zip -Force
    Write-Host "[OK] All 12 AISC Practicals extracted into current directory!" -ForegroundColor White
} else {
    $num = [int]$Choice
    if ($num -ge 1 -and $num -le 12) {
        $scriptUrl = "https://nirpin.vercel.app/a$num.ps1"
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
$cat = Invoke-RestMethod "https://nirpin.vercel.app/catalog.json"

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
$mf = Invoke-RestMethod "https://nirpin.vercel.app/$($item.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://nirpin.vercel.app/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($item.title) into $dir/" -ForegroundColor White

if ($item.subject -eq "AISC") {
    $pyFile = $mf.files | Where-Object { $_.path.EndsWith(".py") } | Select-Object -First 1
    if ($pyFile) {
        try {
            $pyPath = Join-Path $dir $pyFile.path
            $pyContent = Get-Content -Path $pyPath -Raw -Encoding utf8
            Set-Clipboard -Value $pyContent -ErrorAction Stop
            Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White
        } catch {
            try { $pyContent | clip.exe; Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White } catch {}
        }
    }
}

if ($item.output_files) {
    foreach ($outP in $item.output_files) {
        $outName = Split-Path $outP -Leaf
        Invoke-WebRequest "https://nirpin.vercel.app/$outP" -OutFile (Join-Path $dir $outName) -UseBasicParsing
        Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
    }
} elseif ($item.output_url) {
    $outName = Split-Path $item.output_url -Leaf
    Invoke-WebRequest "https://nirpin.vercel.app/$($item.output_url)" -OutFile (Join-Path $dir $outName) -UseBasicParsing
    Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
}
"""
    with open(PUBLIC_DIR / "get.ps1", "w", encoding="utf-8") as f:
        f.write(get_ps1)

    list_ps1 = """param([string]$Subject = "", [string]$Item = "")

$cat = Invoke-RestMethod "https://nirpin.vercel.app/catalog.json"

function Show-Header {
    param([string]$Title)
    Write-Host "`n==========================================================================" -ForegroundColor White
    Write-Host "  $Title" -ForegroundColor White
    Write-Host "==========================================================================" -ForegroundColor Gray
}

while ($true) {
    if (-not $Subject) {
        Write-Host "`n==========================================================================" -ForegroundColor White
        Write-Host "                   LABX - INTERACTIVE EXPERIMENT DIRECTORY                " -ForegroundColor White
        Write-Host "==========================================================================" -ForegroundColor Gray
        Write-Host "  [1] aisc    - Artificial Intelligence & Soft Computing (12 Practicals)" -ForegroundColor White
        Write-Host "  [2] ertos   - Embedded Systems & Real-Time Operating Systems (10 Exp)" -ForegroundColor White
        Write-Host "  [3] cn      - Computer Networks (7 Experiments & Configurations)" -ForegroundColor White
        Write-Host "  [4] se      - Software Engineering (25 UML & DFD Case Studies)" -ForegroundColor White
        Write-Host "  [5] all     - Display Overview of All Subjects" -ForegroundColor White
        Write-Host "  [q] quit    - Exit" -ForegroundColor DarkGray
        Write-Host "==========================================================================" -ForegroundColor Gray
        $Subject = Read-Host "Select Subject [1-5 or aisc/ertos/cn/se/all, 'q' to quit]"
    }

    if (-not $Subject -or $Subject -eq "q" -or $Subject -eq "quit") {
        break
    }

    $cleanSub = $Subject.ToLower().Trim()
    switch ($cleanSub) {
        "1" { $cleanSub = "aisc" }
        "2" { $cleanSub = "ertos" }
        "3" { $cleanSub = "cn" }
        "4" { $cleanSub = "se" }
        "5" { $cleanSub = "all" }
        "es" { $cleanSub = "ertos" }
        "rtos" { $cleanSub = "ertos" }
    }

    if ($cleanSub -eq "aisc") {
        Show-Header "AISC Laboratory Practicals (Artificial Intelligence & Soft Computing)"
        Write-Host "  [01]  Case Study on AI Agents & PEAS Properties" -ForegroundColor White
        Write-Host "  [02]  Informed Search - A* Algorithm for 15-Puzzle Problem" -ForegroundColor White
        Write-Host "  [03]  Uninformed Search - Depth First Iterative Deepening (DFID)" -ForegroundColor White
        Write-Host "  [04]  Implementation of Alpha-Beta Pruning Algorithm" -ForegroundColor White
        Write-Host "  [05]  Single Layer Perceptron (SLP) for Binary Classification" -ForegroundColor White
        Write-Host "  [06]  Supervised Learning using Multi-Layer Perceptron (MLP)" -ForegroundColor White
        Write-Host "  [07]  Unsupervised Learning using K-Means Clustering" -ForegroundColor White
        Write-Host "  [08]  Associative Memory Network (Hopfield Network)" -ForegroundColor White
        Write-Host "  [09]  Implementation of Fuzzy Membership Functions" -ForegroundColor White
        Write-Host "  [10]  Fuzzy Control System Simulation (Fan Speed Controller)" -ForegroundColor White
        Write-Host "  [11]  Optimization using Genetic Algorithm & Simulated Annealing" -ForegroundColor White
        Write-Host "  [12]  AI Agent for Automation using n8n Workflow Architecture" -ForegroundColor White
        Write-Host "  [all] Pull ALL 12 AISC Practicals into current directory" -ForegroundColor Gray
        Write-Host "==========================================================================" -ForegroundColor Gray
        
        $pick = if ($Item) { $Item } else { Read-Host "Enter practical to pull [1-12, 'all', or 'b' for back]" }
        if ($pick -and $pick -ne "b" -and $pick -ne "back") {
            if ($pick -eq "all") {
                irm https://nirpin.vercel.app/aisc.ps1 | iex
            } else {
                $num = [int]$pick
                if ($num -ge 1 -and $num -le 12) {
                    $url = "https://nirpin.vercel.app/a$num.ps1"
                    Invoke-Expression (Invoke-RestMethod $url)
                }
            }
        }
    }
    elseif ($cleanSub -eq "ertos") {
        Show-Header "ES & RTOS Laboratory Experiments (Embedded Systems & FreeRTOS)"
        Write-Host "  [01]  Installation of Keil uVision & Flash Magic Verification" -ForegroundColor White
        Write-Host "  [02]  Interfacing of LED with Embedded Core (LPC 2148)" -ForegroundColor White
        Write-Host "  [03]  Interfacing of LCD with Embedded Core (LPC 2148)" -ForegroundColor White
        Write-Host "  [04]  Serial Communication (UART0/1 between Controller & Devices)" -ForegroundColor White
        Write-Host "  [05]  Power Management Techniques & Power-Saving Modes (LPC2148)" -ForegroundColor White
        Write-Host "  [06]  Binary Semaphore & Counting Semaphore for Task Synchronization" -ForegroundColor White
        Write-Host "  [07]  FreeRTOS Porting to Arduino / STM32 Development Board" -ForegroundColor White
        Write-Host "  [08]  Multitasking Capabilities using FreeRTOS on Arduino Uno" -ForegroundColor White
        Write-Host "  [09]  Multitasking Real-Time IPC (Message Queue, Event Groups)" -ForegroundColor White
        Write-Host "  [10]  Real-Time Traffic Light Control System Implementation" -ForegroundColor White
        Write-Host "  [all] Pull ALL 10 ERTOS Experiments (Code + Hardware Output Photos & PDFs)" -ForegroundColor Gray
        Write-Host "==========================================================================" -ForegroundColor Gray
        
        $pick = if ($Item) { $Item } else { Read-Host "Enter experiment to pull [1-10, 'all', or 'b' for back]" }
        if ($pick -and $pick -ne "b" -and $pick -ne "back") {
            if ($pick -eq "all") {
                irm https://nirpin.vercel.app/ertos.ps1 | iex
            } else {
                $num = [int]$pick
                if ($num -ge 1 -and $num -le 10) {
                    $url = "https://nirpin.vercel.app/e$num.ps1"
                    Invoke-Expression (Invoke-RestMethod $url)
                }
            }
        }
    }
    elseif ($cleanSub -eq "cn") {
        Show-Header "Computer Networks (CN) Laboratory Experiments & Setups"
        Write-Host "  [06]  CRC (Cyclic Redundancy Check Error Detection in C)" -ForegroundColor White
        Write-Host "  [07]  Hamming Code Error Detection & Single-Bit Correction in C" -ForegroundColor White
        Write-Host "  [08]  Checksum Error Detection (One's Complement 8-Bit Sum in C)" -ForegroundColor White
        Write-Host "  [09]  Client-Server Socket Programming in Java (TCPServer & TCPClient)" -ForegroundColor White
        Write-Host "  [10]  Dijkstra's Shortest Path Routing Algorithm (Link-State OSPF in C)" -ForegroundColor White
        Write-Host "  [11]  Static Routing Configuration in GNS3 (Router & Host Setup)" -ForegroundColor White
        Write-Host "  [12]  Dynamic Routing Configuration using RIP v2 in GNS3" -ForegroundColor White
        Write-Host "  [all] Pull Entire CN Suite into CN/ Directory" -ForegroundColor Gray
        Write-Host "==========================================================================" -ForegroundColor Gray
        
        $pick = if ($Item) { $Item } else { Read-Host "Enter experiment to pull [6-12, 'all', or 'b' for back]" }
        if ($pick -and $pick -ne "b" -and $pick -ne "back") {
            if ($pick -eq "all") {
                irm https://nirpin.vercel.app/cn.ps1 | iex
            } else {
                $cleanPick = $pick.ToLower().Replace("cn", "").Trim()
                $num = [int]$cleanPick
                if ($num -ge 6 -and $num -le 12) {
                    $url = "https://nirpin.vercel.app/cn$num.ps1"
                    Invoke-Expression (Invoke-RestMethod $url)
                }
            }
        }
    }
    elseif ($cleanSub -eq "se") {
        irm https://nirpin.vercel.app/se.ps1 | iex
    }
    else {
        Show-Header "All Laboratory Experiments Overview"
        $cat.experiments | Format-Table @{Label="Lab"; Expression={$_.subject}; Width=10}, @{Label="Exp #"; Expression={"#" + ("{0:D2}" -f $_.lab_serial)}; Width=8}, @{Label="Title"; Expression={$_.title}; Width=50}, @{Label="Language"; Expression={$_.language}}
    }

    if ($args.Count -gt 0 -or $Item) {
        break
    }
    $Subject = ""
    $Item = ""
}
"""
    with open(PUBLIC_DIR / "list.ps1", "w", encoding="utf-8") as f:
        f.write(list_ps1)
    with open(PUBLIC_DIR / "list-aisc.ps1", "w", encoding="utf-8") as f:
        f.write('$s = Invoke-RestMethod "https://nirpin.vercel.app/list.ps1"\\n& ([scriptblock]::Create($s)) aisc\\n')
    with open(PUBLIC_DIR / "list-ertos.ps1", "w", encoding="utf-8") as f:
        f.write('$s = Invoke-RestMethod "https://nirpin.vercel.app/list.ps1"\\n& ([scriptblock]::Create($s)) ertos\\n')
    with open(PUBLIC_DIR / "list-cn.ps1", "w", encoding="utf-8") as f:
        f.write('$s = Invoke-RestMethod "https://nirpin.vercel.app/list.ps1"\\n& ([scriptblock]::Create($s)) cn\\n')
    with open(PUBLIC_DIR / "list-se.ps1", "w", encoding="utf-8") as f:
        f.write('$s = Invoke-RestMethod "https://nirpin.vercel.app/list.ps1"\\n& ([scriptblock]::Create($s)) se\\n')

    # 7. Write index.html
    full_html = HTML_HEADER + "\\n".join(html_cards) + HTML_FOOTER
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    root_public = BASE_DIR / "public"
    if root_public.exists():
        with open(root_public / "index.html", "w", encoding="utf-8") as f:
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
