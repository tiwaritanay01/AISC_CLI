"""
Production WSGI Web Server for local development and Render.
Serves public/ static assets, catalog, PowerShell scripts, and custom delivery APIs.
"""

import os
import sys
import json
from pathlib import Path
import requests
from flask import Flask, send_from_directory, request, jsonify, redirect, Response

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
if not PUBLIC_DIR.exists():
    PUBLIC_DIR = BASE_DIR / "labx-host" / "public"

app = Flask(__name__, static_folder=None)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response

def get_current_host():
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.headers.get("X-Forwarded-Host", request.host)
    return f"{proto}://{host}".rstrip("/")

@app.route("/health", methods=["GET"])
def health_check():
    cat_file = PUBLIC_DIR / "catalog.json"
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
    return redirect(f"https://dpaste.org/{paste_id}/raw", code=302)

@app.route("/api/publish", methods=["POST", "OPTIONS"])
def publish_code():
    if request.method == "OPTIONS":
        return Response("", status=204)
    try:
        data = request.get_json(force=True, silent=True) or {}
        filename = data.get("filename", "experiment.py")
        code = data.get("code", "")
        script = data.get("script")
        if not script and not code:
            return jsonify({"error": "Missing payload."}), 400
        if not script:
            script = f'# LabX Remote Delivery\n$filename = "{filename}"\n$code = @\'\n{code}\n\'@\nSet-Content -Path (Join-Path $PWD $filename) -Value $code -Encoding utf8\n'
        host_url = get_current_host()
        resp = requests.post("https://dpaste.org/api/", data={"content": script, "syntax": "powershell", "expiry_days": 30, "format": "url"}, timeout=10)
        if resp.status_code in (200, 201):
            paste_id = resp.text.strip().rstrip("/").split("/")[-1]
            return jsonify({"success": True, "paste_id": paste_id, "short_url": f"{host_url}/s/{paste_id}", "command": f"irm {host_url}/s/{paste_id} | iex"}), 200
        return jsonify({"error": f"Status {resp.status_code}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    target = PUBLIC_DIR / "index.html"
    if not target.exists():
        return Response("Not Found", status=404)
    return Response(target.read_text(encoding="utf-8"), mimetype="text/html; charset=utf-8")

@app.route("/<path:filepath>", methods=["GET"])
def static_files(filepath):
    target = PUBLIC_DIR / filepath
    if not target.exists() or target.is_dir():
        if (PUBLIC_DIR / "index.html").exists():
            return index()
        return Response("Not Found", status=404)
    ext = target.suffix.lower()
    if ext in [".ps1", ".json", ".html", ".sh"]:
        return Response(target.read_text(encoding="utf-8"), mimetype="text/plain; charset=utf-8" if ext in [".ps1", ".sh"] else "application/json; charset=utf-8" if ext == ".json" else "text/html; charset=utf-8")
    if ext in [".c", ".java", ".py", ".md", ".txt"]:
        return Response(target.read_bytes(), mimetype="text/plain; charset=utf-8")
    return send_from_directory(target.parent, target.name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
