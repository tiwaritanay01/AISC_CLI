"""
Vercel Serverless Function entry point for LabX CLI distribution.
Exposes the Flask WSGI app for Vercel Python runtime.
"""

import sys
import os
from pathlib import Path

# Add project root directory to sys.path so server module can be imported
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from server import app

# Vercel looks for 'app' variable at module level
__all__ = ["app"]

