"""
Native Vercel Serverless Function handler using standard library BaseHTTPRequestHandler.
Zero dependencies, instant execution, handles /health, /api/publish, and /s/<id>.
"""

from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip('/')
        matched_path = self.headers.get('x-matched-path', '').rstrip('/')

        # Handle health check
        if path == '/health' or matched_path == '/health' or path.endswith('/health') or 'health' in path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = {
                "status": "healthy",
                "service": "AISC_CLI",
                "version": "1.0.0",
                "experiments_count": 29
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        if '/s/' in path or '/s/' in matched_path:
            target_str = matched_path if '/s/' in matched_path else path
            paste_id = target_str.split('/s/')[-1].strip('/')
            self.send_response(302)
            self.send_header('Location', f'https://dpaste.org/{paste_id}/raw')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip('/')
        matched_path = self.headers.get('x-matched-path', '').rstrip('/')

        if path.endswith('/publish') or matched_path.endswith('/publish') or 'publish' in path:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
            except Exception:
                data = {}

            filename = data.get("filename", "experiment.py")
            code = data.get("code", "")
            script = data.get("script")

            if not script and not code:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing code or script payload."}).encode('utf-8'))
                return

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

            host = self.headers.get('X-Forwarded-Host', self.headers.get('Host', 'nirpin.vercel.app'))
            proto = self.headers.get('X-Forwarded-Proto', 'https')
            host_url = f"{proto}://{host}"

            post_data = urllib.parse.urlencode({
                "content": script,
                "syntax": "powershell",
                "expiry_days": "30",
                "format": "url"
            }).encode('utf-8')

            req = urllib.request.Request(
                "https://dpaste.org/api/",
                data=post_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw_url = resp.read().decode('utf-8').strip()
                    paste_id = raw_url.rstrip("/").split("/")[-1]
                    res = {
                        "success": True,
                        "paste_id": paste_id,
                        "raw_url": f"https://dpaste.org/{paste_id}/raw",
                        "short_url": f"{host_url}/s/{paste_id}",
                        "command": f"irm {host_url}/s/{paste_id} | iex",
                        "filename": filename
                    }
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(res).encode('utf-8'))
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()
