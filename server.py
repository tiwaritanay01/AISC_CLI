"""
Production WSGI Web Server for Render
Serves LabX Remote static assets, catalog, PowerShell scripts, and custom delivery APIs.
"""

import os
import sys
import json
import gzip
import base64
import urllib.parse
from pathlib import Path
import requests
from flask import Flask, send_from_directory, request, jsonify, redirect, Response

# Directory paths
BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "labx-host" / "public"

app = Flask(__name__, static_folder=None)

# Ensure CORS on all responses
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Render monitoring."""
    cat_file = PUBLIC_DIR / "catalog.json"
    count = 27
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
        host_url = request.host_url.rstrip("/")
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
                # If dpaste returns full URL, extract ID
                paste_id = raw_url.rstrip("/").split("/")[-1]
                custom_cmd = f"irm {host_url}/s/{paste_id} | iex"
                return jsonify({
                    "success": True,
                    "command": custom_cmd,
                    "url": f"{host_url}/s/{paste_id}",
                    "id": paste_id
                })
        except Exception as exc:
            pass

        # Fallback to stateless compressed /r link if dpaste is unreachable
        compressed = base64.urlsafe_b64encode(gzip.compress(script.encode("utf-8"))).decode("utf-8").rstrip("=")
        custom_cmd = f"irm '{host_url}/r?f={urllib.parse.quote(filename)}&d={compressed}' | iex"
        return jsonify({
            "success": True,
            "command": custom_cmd,
            "url": f"{host_url}/r?f={urllib.parse.quote(filename)}&d={compressed}",
            "fallback": True
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/r", methods=["GET"])
def raw_script():
    """Serves raw script from compressed query parameter `d`."""
    filename = request.args.get("f", "experiment.py")
    data = request.args.get("d", "")

    if not data:
        return Response('Write-Error "Missing data parameter (d)."', mimetype="text/plain; charset=utf-8", status=400)

    try:
        # Add padding back
        pad = len(data) % 4
        if pad:
            data += "=" * (4 - pad)
        decoded = base64.urlsafe_b64decode(data.encode("utf-8"))
        try:
            content = gzip.decompress(decoded).decode("utf-8")
        except Exception:
            content = decoded.decode("utf-8")

        return Response(content, mimetype="text/plain; charset=utf-8")
    except Exception as exc:
        return Response(f'Write-Error "Decoding failed: {exc}"', mimetype="text/plain; charset=utf-8", status=400)


@app.route("/", methods=["GET"])
def index():
    """Serves index.html at root with dynamic host adaptation."""
    target = PUBLIC_DIR / "index.html"
    if not target.exists():
        return Response("Not Found", status=404)
    content = target.read_text(encoding="utf-8")
    current_host = request.host_url.rstrip("/")
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
        # Fallback to index.html for SPA routes if any
        if (PUBLIC_DIR / "index.html").exists():
            return index()
        return Response("Not Found", status=404)

    ext = target.suffix.lower()

    # Dynamic host adaptation for scripts and web pages
    if ext in [".ps1", ".json", ".html", ".sh"]:
        content = target.read_text(encoding="utf-8")
        current_host = request.host_url.rstrip("/")
        content = content.replace("https://aisccli.netlify.app", current_host)
        content = content.replace("https://cli-t0km.onrender.com", current_host)
        
        mimetype = "text/plain; charset=utf-8" if ext in [".ps1", ".sh"] else (
            "application/json; charset=utf-8" if ext == ".json" else "text/html; charset=utf-8"
        )
        return Response(content, mimetype=mimetype)

    # Force text/plain for source code files
    if ext in [".c", ".java", ".py", ".md", ".txt"]:
        return Response(target.read_bytes(), mimetype="text/plain; charset=utf-8")

    return send_from_directory(target.parent, target.name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting AISC_CLI Web Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)

