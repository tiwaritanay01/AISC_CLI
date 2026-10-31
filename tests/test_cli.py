"""End-to-End CLI command tests using Typer CliRunner."""

import os
from pathlib import Path
from typer.testing import CliRunner
import pytest

from labx.cli import app
from labx import __version__

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_cli_root_command(live_server):
    result = runner.invoke(app, ["--url", live_server])
    assert result.exit_code == 0
    assert "LABX REMOTE" in result.stdout
    assert "Connected to remote catalogue" in result.stdout


def test_cli_list_command(live_server):
    result = runner.invoke(app, ["list", "--url", live_server])
    assert result.exit_code == 0
    assert "Experiment Catalogue" in result.stdout
    assert "Factorial" in result.stdout
    assert "Socket" in result.stdout


def test_cli_search_command(live_server):
    result = runner.invoke(app, ["search", "socket", "--url", live_server])
    assert result.exit_code == 0
    assert "Search Results for 'socket'" in result.stdout
    assert "Java Socket Programming" in result.stdout


def test_cli_info_command(live_server):
    result = runner.invoke(app, ["info", "3", "--url", live_server])
    assert result.exit_code == 0
    assert "Experiment 03" in result.stdout
    assert "Aim:" in result.stdout
    assert "Theory:" in result.stdout
    assert "Algorithm:" in result.stdout


def test_cli_download_and_run_workflow(live_server, tmp_path):
    # 1. Download Experiment 1 (Python) into tmp_path
    res_dl = runner.invoke(app, [
        "download", "1",
        "--path", str(tmp_path),
        "--force",
        "--url", live_server
    ])
    assert res_dl.exit_code == 0
    assert "Downloaded Experiment 01" in res_dl.stdout

    # Verify files created in tmp_path
    exp_dir = tmp_path / "Experiment01_factorial_fibonacci_python"
    assert exp_dir.exists()
    assert (exp_dir / "main.py").exists()

    # 2. Run Experiment 1 from that directory
    res_run = runner.invoke(app, [
        "run", "1",
        "--path", str(tmp_path),
        "--url", live_server
    ])
    assert res_run.exit_code == 0
    assert "Executing:" in res_run.stdout

    # 3. Remove experiment
    res_rm = runner.invoke(app, [
        "remove", "1",
        "--path", str(tmp_path),
        "--force"
    ])
    assert res_rm.exit_code == 0
    assert not exp_dir.exists()


def test_cli_download_all_zip(live_server, tmp_path):
    res = runner.invoke(app, [
        "download", "all",
        "--path", str(tmp_path),
        "--force",
        "--url", live_server
    ])
    assert res.exit_code == 0
    assert "Extracted" in res.stdout
    assert (tmp_path / "Experiment04_dijkstra_routing_cpp").exists()
