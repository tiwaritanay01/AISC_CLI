"""Shared test fixtures for LabX test suite."""

import http.server
import socket
import threading
import pytest
from pathlib import Path

from labx.models import Catalog, ExperimentManifest, CatalogItem, ExperimentFile, RunConfig
from labx.cache import LabXCache

HOST_PUBLIC_DIR = Path(__file__).resolve().parent.parent / "labx-host" / "public"


class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Simple HTTP request handler serving static files with log suppression."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HOST_PUBLIC_DIR), **kwargs)

    def log_message(self, format, *args):
        # Suppress standard logging during tests
        pass


@pytest.fixture(scope="session")
def live_server():
    """Spins up a lightweight background HTTP server hosting labx-host/public."""
    # Find free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        port = s.getsockname()[1]

    server = http.server.HTTPServer(("127.0.0.1", port), SilentHTTPHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}"
    yield url

    server.shutdown()
    server.server_close()


@pytest.fixture
def temp_cache(tmp_path):
    """Provides an isolated clean cache directory."""
    cache_dir = tmp_path / ".labx" / "cache"
    cache = LabXCache(cache_dir=cache_dir)
    return cache


@pytest.fixture
def sample_catalog():
    """Provides a valid test catalog."""
    return Catalog(
        version="1.0.0",
        updated_at="2026-10-31",
        experiments=[
            CatalogItem(
                id=1,
                slug="factorial-fibonacci-python",
                title="Factorial and Fibonacci Sequence Generator",
                language="python",
                aliases=["factorial", "fibonacci"],
                description="Math sequence generator in Python",
                manifest_url="experiments/01/manifest.json"
            ),
            CatalogItem(
                id=3,
                slug="java-socket-programming",
                title="Java Socket Programming (Client-Server)",
                language="java",
                aliases=["socket programming", "java sockets", "client server socket"],
                description="Two-way TCP sockets in Java",
                manifest_url="experiments/03/manifest.json"
            ),
            CatalogItem(
                id=4,
                slug="dijkstra-routing-cpp",
                title="Dijkstra's Shortest Path Routing Algorithm",
                language="cpp",
                aliases=["dijkstra", "routing algorithm", "dynamic routing"],
                description="Link-state routing simulation in C++",
                manifest_url="experiments/04/manifest.json"
            )
        ]
    )

