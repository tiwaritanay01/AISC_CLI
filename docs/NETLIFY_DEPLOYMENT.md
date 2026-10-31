# Netlify Deployment Guide for LabX Remote

This guide explains how to deploy the LabX Remote static catalogue and file distribution backend to **Netlify**.

---

## 1. Hosting Directory Structure

The deployable folder is located at `labx-host/`:

```
labx-host/
├── netlify.toml          # Netlify headers, CORS, and build settings
├── README.md             # Repository documentation
└── public/               # Target publish directory
    ├── index.html        # Interactive student homepage and catalogue viewer
    ├── catalog.json      # Experiment metadata catalogue API
    ├── version.json      # Remote version and heartbeat endpoint
    ├── install.ps1       # Automated Windows PowerShell installer
    ├── downloads/
    │   ├── labx.exe      # Windows standalone executable binary
    │   └── labx_experiments.zip # Complete 10-experiment ZIP archive
    └── experiments/
        ├── 01/           # Factorial & Fibonacci in Python
        ├── 02/           # Matrix Operations in C
        ├── 03/           # Client-Server Sockets in Java
        ├── 04/           # Dijkstra Routing in C++
        ├── 05/           # Sliding Window Protocol in C
        ├── 06/           # Memory Paging Simulation in Python
        ├── 07/           # Multi-threaded Echo Server in Java
        ├── 08/           # Lexical Analyzer in C
        ├── 09/           # Binary Search Tree in C++
        └── 10/           # ARM7 LPC2148 GPIO Driver in Embedded C
```

---

## 2. Pre-Deployment Build

Before publishing, ensure the static assets and ZIP archive are freshly generated:

```bash
python scripts/build_host.py
```

This updates `catalog.json`, generates `downloads/labx_experiments.zip`, copies source files, and stages the website.

---

## 3. Deployment Methods

### Method A: Netlify CLI (Command-Line)

1. Install the Netlify CLI if not already installed:
   ```bash
   npm install -g netlify-cli
   ```
2. Log in to your Netlify account:
   ```bash
   netlify login
   ```
3. Deploy the publish directory directly:
   ```bash
   cd labx-host
   netlify deploy --prod --dir=public
   ```
4. Netlify will output your production live site URL (e.g., `https://labx-remote.netlify.app`).

### Method B: Git Continuous Deployment (Recommended for Teams)

1. Push the `CLI_AISC` repository to GitHub or GitLab.
2. In the Netlify Dashboard, click **"Add new site"** &rarr; **"Import an existing project"**.
3. Select your repository.
4. Set the build settings:
   - **Base directory**: `labx-host`
   - **Publish directory**: `public`
   - **Build command**: `python ../scripts/build_host.py` (or leave empty if pre-built)
5. Click **Deploy Site**. Every Git push to main will automatically trigger a deployment.

### Method C: Drag-and-Drop (Zero-CLI)

1. Log into [app.netlify.com](https://app.netlify.com).
2. Go to the **Sites** tab.
3. Drag the folder `labx-host/public` directly into the designated drop zone.
4. Netlify will publish the site in seconds.

---

## 4. Header & CORS Configuration

Netlify configuration is declared in `labx-host/netlify.toml`:

```toml
[build]
  publish = "public"

[[headers]]
  for = "/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, HEAD, OPTIONS"
    Access-Control-Allow-Headers = "*"
    Cache-Control = "public, max-age=3600"

[[headers]]
  for = "/*.json"
  [headers.values]
    Content-Type = "application/json; charset=utf-8"
```

This ensures that `labx.exe` and web browser clients can freely query `catalog.json` and stream download ZIPs and manifests without CORS restrictions.

---

## 5. Configuring the CLI to Use Your Netlify Site

Once deployed, point your local LabX CLI to your site URL:

### Via Environment Variable
```powershell
$env:LABX_REMOTE_URL = "https://YOUR-SITE.netlify.app"
```

### Via CLI Option
```bash
labx list --url https://YOUR-SITE.netlify.app
labx download 3 --url https://YOUR-SITE.netlify.app
```

