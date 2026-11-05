"""
Production WSGI Web Server for Render and local development.
Delegates to api.index module for unified serverless & WSGI execution.
"""

import os
from api.index import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting AISC_CLI Web Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
