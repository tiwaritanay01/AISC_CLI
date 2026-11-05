"""
Vercel Serverless Function entry point for LabX CLI distribution.
Self-contained Flask application handling API endpoints, health checks, and dynamic asset delivery.
"""

import os
import sys
import json
import gzip
import base64
import urllib.parse
from pathlib import Path
import requests
from flask import Flask, request, jsonify, redirect, Response, send_from_directory

# Compute base directories
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
PUBLIC_DIR = BASE_DIR / "public"
FALLBACK_PUBLIC_DIR = BASE_DIR / "labx-host" / "public"

app = Flask(__name__)

# Ensure CORS on all responses
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response


def get_current_host():
    """Extracts reliable public host and protocol behind reverse proxies (Vercel, Render)."""
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.headers.get("X-Forwarded-Host", request.host)
    return f"{proto}://{host}".rstrip("/")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Vercel and monitoring."""
    cat_file = PUBLIC_DIR / "catalog.json"
    if not cat_file.exists():
        cat_file = FALLBACK_PUBLIC_DIR / "catalog.json"
    count = 29
    if cat_file.exists():
        try:
            count = len(json.loads(cat_file.read_text(encoding="utf-8")).get("experiments", []))
        except Exception:
            pass
    return jsonify({
        "status": "healthy",
        "service": "AISC_CLI",
        "version": "1.0.0",
        "experiments_count": count
    }), 200


@app.route("/s/<paste_id>", methods=["GET"])
def redirect_paste(paste_id):
    """Redirects /s/<id> directly to dpaste.org raw content."""
    return redirect(f"https://dpaste.org/{paste_id}/raw", code=302)


@app.route("/api/publish", methods=["POST", "OPTIONS"])
def publish_code():
    """
    Receives code/script and publishes to dpaste.org,
    returning a clean one-liner PowerShell delivery command.
    """
    if request.method == "OPTIONS":
        return Response("", status=204)

    try:
        data = request.get_json(force=True, silent=True) or {}
        filename = data.get("filename", "experiment.py")
        code = data.get("code", "")
        script = data.get("script")

        if not script and not code:
            return jsonify({"error": "Missing code or script payload."}), 400

        # Build PowerShell wrapper if raw code
        if not script:
            script = f'''# LabX Remote - Custom Experiment Delivery
$filename = "{filename}"
$code = @'
{code}
'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host ""
Write-Host "[OK] Saved code to: $filename" -ForegroundColor White
'''

        # Publish to dpaste
        host_url = get_current_host()
        try:
            resp = requests.post(
                "https://dpaste.org/api/",
                data={
                    "content": script,
                    "syntax": "powershell",
                    "expiry_days": 30,
                    "format": "url"
                },
                timeout=10
            )
            if resp.status_code in (200, 201):
                raw_url = resp.text.strip()
                paste_id = raw_url.rstrip("/").split("/")[-1]
                ps_cmd = f"irm {host_url}/s/{paste_id} | iex"
                return jsonify({
                    "success": True,
                    "paste_id": paste_id,
                    "raw_url": f"https://dpaste.org/{paste_id}/raw",
                    "short_url": f"{host_url}/s/{paste_id}",
                    "command": ps_cmd,
                    "filename": filename
                }), 200
            else:
                return jsonify({"error": f"dpaste returned status {resp.status_code}"}), 502
        except requests.RequestException as e:
            return jsonify({"error": f"Upstream delivery failed: {str(e)}"}), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    """Serves index.html with dynamic host adaptation if reached via API."""
    target = PUBLIC_DIR / "index.html"
    if not target.exists():
        target = FALLBACK_PUBLIC_DIR / "index.html"
    if not target.exists():
        return Response("Not Found", status=404)
    content = target.read_text(encoding="utf-8")
    current_host = get_current_host()
    content = content.replace("https://aisccli.netlify.app", current_host)
    content = content.replace("https://cli-t0km.onrender.com", current_host)
    return Response(content, mimetype="text/html; charset=utf-8")


@app.route("/<path:filepath>", methods=["GET"])
def static_files(filepath):
    """
    Serves static assets, downloads, outputs, and PS1 scripts
    with correct MIME types and dynamic host adaptation.
    """
    target = PUBLIC_DIR / filepath
    if not target.exists() or target.is_dir():
        target = FALLBACK_PUBLIC_DIR / filepath
    if not target.exists() or target.is_dir():
        if (PUBLIC_DIR / "index.html").exists():
            return index()
        return Response("Not Found", status=404)

    ext = target.suffix.lower()

    if ext in [".ps1", ".json", ".html", ".sh"]:
        content = target.read_text(encoding="utf-8")
        current_host = get_current_host()
        content = content.replace("https://aisccli.netlify.app", current_host)
        content = content.replace("https://cli-t0km.onrender.com", current_host)
        
        mimetype = "text/plain; charset=utf-8" if ext in [".ps1", ".sh"] else (
            "application/json; charset=utf-8" if ext == ".json" else "text/html; charset=utf-8"
        )
        return Response(content, mimetype=mimetype)

    if ext in [".c", ".java", ".py", ".md", ".txt"]:
        return Response(target.read_bytes(), mimetype="text/plain; charset=utf-8")

    return send_from_directory(target.parent, target.name)


# Export app for Vercel
__all__ = ["app"]
