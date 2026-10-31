"""Security tests: zip-slip, path traversal, and malicious input handling."""

import io
import zipfile
from pathlib import Path
import pytest

from labx.downloader import is_safe_path, ExperimentDownloader
from labx.client import LabXRemoteClient


def test_zip_slip_path_traversal_detection(tmp_path):
    target_dir = tmp_path / "extraction_zone"
    target_dir.mkdir()

    # Attempting to escape extraction_zone using ../
    evil_path = target_dir / ".." / "evil.txt"
    assert is_safe_path(target_dir, evil_path) is False

    # Deep traversal
    very_evil_path = target_dir / "sub" / ".." / ".." / "system32.dll"
    assert is_safe_path(target_dir, very_evil_path) is False

    # Valid subpaths
    good_path1 = target_dir / "file.txt"
    good_path2 = target_dir / "dir" / "subdir" / "file.txt"
    assert is_safe_path(target_dir, good_path1) is True
    assert is_safe_path(target_dir, good_path2) is True


def test_malicious_zip_extraction_fails_safely(tmp_path):
    target_dir = tmp_path / "extract_dir"
    target_dir.mkdir()

    # Create in-memory ZIP with malicious ../ filename
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as zf:
        zf.writestr("../traversal_attack.txt", "MALICIOUS CONTENT")
        zf.writestr("safe_file.txt", "SAFE CONTENT")
    zip_buf.seek(0)

    # Save to disk
    malicious_zip_path = tmp_path / "attack.zip"
    malicious_zip_path.write_bytes(zip_buf.getvalue())

    # Extraction must skip ../traversal_attack.txt and extract only safe_file.txt
    with zipfile.ZipFile(malicious_zip_path, "r") as zf:
        for member in zf.infolist():
            dest = target_dir / member.filename
            if is_safe_path(target_dir, dest):
                dest.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(dest, "wb") as dst:
                    dst.write(src.read())

    # Assert attack was deflected: escaped file does NOT exist outside target_dir
    escaped_file = tmp_path / "traversal_attack.txt"
    assert not escaped_file.exists()
    assert (target_dir / "safe_file.txt").exists()

