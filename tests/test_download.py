"""Tests for individual and bulk experiment downloads."""

from pathlib import Path
import pytest

from labx.client import LabXRemoteClient
from labx.downloader import ExperimentDownloader, is_safe_path
from labx.models import CatalogItem


def test_individual_download_via_live_server(live_server, tmp_path):
    client = LabXRemoteClient(base_url=live_server)
    downloader = ExperimentDownloader(client)

    item = CatalogItem(
        id=3,
        slug="java-socket-programming",
        title="Java Socket Programming (Client-Server)",
        language="java",
        aliases=["socket programming"],
        description="Two-way client-server network communication using Java TCP Sockets",
        manifest_url="experiments/03/manifest.json"
    )

    success = downloader.download_individual(item, tmp_path, force=True)
    assert success is True

    exp_dir = tmp_path / "Experiment03_java_socket_programming"
    assert exp_dir.exists()
    assert (exp_dir / "Server.java").exists()
    assert (exp_dir / "Client.java").exists()
    assert (exp_dir / "manifest.json").exists()
    assert (exp_dir / "README.md").exists()

    # Verify content of Server.java
    content = (exp_dir / "Server.java").read_text(encoding="utf-8")
    assert "ServerSocket" in content


def test_individual_download_overwrite_protection(live_server, tmp_path):
    client = LabXRemoteClient(base_url=live_server)
    downloader = ExperimentDownloader(client)

    item = CatalogItem(
        id=1,
        slug="factorial-fibonacci-python",
        title="Factorial and Fibonacci Generator",
        language="python",
        aliases=["factorial"],
        description="Math sequences",
        manifest_url="experiments/01/manifest.json"
    )

    # First download
    assert downloader.download_individual(item, tmp_path, force=True) is True

    # Pre-existing file with custom modification
    exp_dir = tmp_path / "Experiment01_factorial_fibonacci_python"
    custom_marker = exp_dir / "user_notes.txt"
    custom_marker.write_text("student notes", encoding="utf-8")

    # Second download with force=True should preserve unrelated files
    assert downloader.download_individual(item, tmp_path, force=True) is True
    assert custom_marker.exists()
    assert custom_marker.read_text(encoding="utf-8") == "student notes"


def test_all_experiments_zip_download(live_server, tmp_path):
    client = LabXRemoteClient(base_url=live_server)
    downloader = ExperimentDownloader(client)

    success = downloader.download_all_zip("downloads/labx_experiments.zip", tmp_path, force=True)
    assert success is True

    # Check extracted experiments
    extracted_dirs = list(tmp_path.glob("Experiment*"))
    assert len(extracted_dirs) == 10

    # Check Experiment 10 (Embedded C)
    exp10 = tmp_path / "Experiment10_arm7_lpc2148_gpio_timer"
    assert exp10.exists()
    assert (exp10 / "main.c").exists()
    assert (exp10 / "LPC214x.h").exists()
    assert (exp10 / "Makefile").exists()


def test_path_safety_check(tmp_path):
    base = tmp_path / "safe_dir"
    base.mkdir()

    # Normal inside path
    safe_target = base / "subdir" / "file.txt"
    assert is_safe_path(base, safe_target) is True

    # Path traversal attempt outside base
    unsafe_target = base / ".." / "escaped.txt"
    assert is_safe_path(base, unsafe_target) is False

