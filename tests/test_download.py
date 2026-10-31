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
        id=2,
        slug="a-star-15-puzzle-problem",
        title="Informed Search - A* Algorithm for 15-Puzzle Problem",
        language="python",
        aliases=["a star", "15 puzzle"],
        description="Heuristic A* search algorithm using Manhattan Distance to solve the 15-Puzzle problem.",
        manifest_url="experiments/02/manifest.json"
    )

    success = downloader.download_individual(item, tmp_path, force=True)
    assert success is True

    exp_dir = tmp_path / "Experiment02_a_star_15_puzzle_problem"
    assert exp_dir.exists()
    assert (exp_dir / "a_star_15_puzzle.py").exists()
    assert (exp_dir / "manifest.json").exists()
    assert (exp_dir / "README.md").exists()

    # Verify content of a_star_15_puzzle.py
    content = (exp_dir / "a_star_15_puzzle.py").read_text(encoding="utf-8")
    assert "manhattan" in content.lower()


def test_individual_download_overwrite_protection(live_server, tmp_path):
    client = LabXRemoteClient(base_url=live_server)
    downloader = ExperimentDownloader(client)

    item = CatalogItem(
        id=1,
        slug="ai-agents-peas-case-study",
        title="Case Study on AI Agents & PEAS Properties",
        language="python",
        aliases=["ai agents", "peas"],
        description="Comprehensive study and simulation of AI Agent types and PEAS properties.",
        manifest_url="experiments/01/manifest.json"
    )

    # First download
    assert downloader.download_individual(item, tmp_path, force=True) is True

    # Pre-existing file with custom modification
    exp_dir = tmp_path / "Experiment01_ai_agents_peas_case_study"
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
    assert len(extracted_dirs) == 12

    # Check Experiment 12 (AI Agent Automation n8n)
    exp12 = tmp_path / "Experiment12_n8n_ai_agent_automation"
    assert exp12.exists()
    assert (exp12 / "n8n_agent_simulator.py").exists()
    assert (exp12 / "n8n_workflow.json").exists()


def test_path_safety_check(tmp_path):
    base = tmp_path / "safe_dir"
    base.mkdir()

    # Normal inside path
    safe_target = base / "subdir" / "file.txt"
    assert is_safe_path(base, safe_target) is True

    # Path traversal attempt outside base
    unsafe_target = base / ".." / "escaped.txt"
    assert is_safe_path(base, unsafe_target) is False

