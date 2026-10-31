"""Main entry point for running labx as a module or with PyInstaller."""

import sys

# Ensure UTF-8 output on Windows consoles/pipes
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from labx.cli import app

if __name__ == "__main__":
    app()
