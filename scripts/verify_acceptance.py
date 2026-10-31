"""End-to-End Acceptance Verification Script for LabX Remote executable."""

import http.server
import socket
import subprocess
import threading
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
HOST_PUBLIC_DIR = BASE_DIR / "labx-host" / "public"
EXE_PATH = BASE_DIR / "dist" / "labx.exe"


class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HOST_PUBLIC_DIR), **kwargs)

    def log_message(self, format, *args):
        pass


def run_e2e_tests():
    print("=" * 60)
    print(" LABX REMOTE ACCEPTANCE VERIFICATION (E2E)")
    print("=" * 60)
    assert EXE_PATH.exists(), f"labx.exe not found at {EXE_PATH}"

    # 1. Start local mock Netlify server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        port = s.getsockname()[1]

    server = http.server.HTTPServer(("127.0.0.1", port), SilentHTTPHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    server_url = f"http://127.0.0.1:{port}"
    print(f"[OK] Test server started on {server_url}")

    test_sandbox = BASE_DIR / "test_sandbox"
    fuzzy_sandbox = BASE_DIR / "test_fuzzy_sandbox"
    bulk_sandbox = BASE_DIR / "test_bulk_sandbox"
    if test_sandbox.exists():
        shutil.rmtree(test_sandbox)
    test_sandbox.mkdir(parents=True, exist_ok=True)

    try:
        # Scenario F: Clean list command
        print("\n--- SCENARIO F: Listing catalogue ---")
        res = subprocess.run([str(EXE_PATH), "list", "--url", server_url], cwd=str(test_sandbox), capture_output=True, text=True)
        assert res.returncode == 0, f"list failed: {res.stderr}"
        assert "Experiment Catalogue" in res.stdout
        assert "Java Socket Programming" in res.stdout
        print("[PASS] Scenario F: Clean catalogue load & display")

        # Scenario A: Individual experiment download
        print("\n--- SCENARIO A: Individual experiment download (labx download 3) ---")
        res = subprocess.run([str(EXE_PATH), "download", "3", "--force", "--url", server_url], cwd=str(test_sandbox), capture_output=True, text=True)
        assert res.returncode == 0, f"download 3 failed: {res.stderr}"
        exp3_dir = test_sandbox / "Experiment03_java_socket_programming"
        assert exp3_dir.exists(), "Experiment03 folder missing!"
        assert (exp3_dir / "Server.java").exists(), "Server.java missing!"
        assert (exp3_dir / "Client.java").exists(), "Client.java missing!"
        assert (exp3_dir / "manifest.json").exists(), "manifest.json missing!"
        print("[PASS] Scenario A: Individual experiment 3 downloaded correctly into CWD")

        # Scenario D: Compile & Execute
        print("\n--- SCENARIO D: Compile & Execute experiment (labx run 3) ---")
        res = subprocess.run([str(EXE_PATH), "run", "3", "--url", server_url], cwd=str(test_sandbox), capture_output=True, text=True)
        assert res.returncode == 0, f"run 3 failed: {res.stderr}\n{res.stdout}"
        assert "Java Socket Server" in res.stdout
        print("[PASS] Scenario D: Experiment 3 compiled & executed with live socket output")

        # Scenario B: Fuzzy Search & Download
        print("\n--- SCENARIO B: Fuzzy Search (labx download \"socket programing\") ---")
        fuzzy_sandbox = BASE_DIR / "test_fuzzy_sandbox"
        if fuzzy_sandbox.exists():
            shutil.rmtree(fuzzy_sandbox)
        fuzzy_sandbox.mkdir(parents=True, exist_ok=True)

        res = subprocess.run([str(EXE_PATH), "download", "socket programing", "--force", "--url", server_url], cwd=str(fuzzy_sandbox), capture_output=True, text=True)
        assert res.returncode == 0, f"fuzzy download failed: {res.stderr}"
        assert (fuzzy_sandbox / "Experiment03_java_socket_programming").exists()
        print("[PASS] Scenario B: Fuzzy search resolved typo 'socket programing' to Exp #3")

        # Scenario C: Full Collection Download
        print("\n--- SCENARIO C: Full ZIP Collection (labx download all) ---")
        bulk_sandbox = BASE_DIR / "test_bulk_sandbox"
        if bulk_sandbox.exists():
            shutil.rmtree(bulk_sandbox)
        bulk_sandbox.mkdir(parents=True, exist_ok=True)

        res = subprocess.run([str(EXE_PATH), "download", "all", "--force", "--url", server_url], cwd=str(bulk_sandbox), capture_output=True, text=True)
        assert res.returncode == 0, f"download all failed: {res.stderr}"
        exp_folders = list(bulk_sandbox.glob("Experiment*"))
        assert len(exp_folders) == 10, f"Expected 10 experiments, found {len(exp_folders)}"
        print(f"[PASS] Scenario C: Successfully downloaded & safely extracted all 10 experiments")

        # Scenario E: Offline Execution
        print("\n--- SCENARIO E: Offline Execution (server unreachable) ---")
        # Kill mock server
        server.shutdown()
        server.server_close()
        print("[OK] Server terminated (simulating offline mode)")

        # Run already downloaded experiment 3 in test_sandbox
        res = subprocess.run([str(EXE_PATH), "run", "3", "--url", "http://127.0.0.1:59999"], cwd=str(test_sandbox), capture_output=True, text=True)
        assert res.returncode == 0, f"offline run failed: {res.stderr}"
        assert "Java Socket Server" in res.stdout
        print("[PASS] Scenario E: Offline execution succeeded for previously downloaded experiment")

        print("\n" + "=" * 60)
        print(" ALL ACCEPTANCE CRITERIA MET (100% PASS)")
        print("=" * 60)

    finally:
        # Cleanup test directories
        for d in [test_sandbox, fuzzy_sandbox, bulk_sandbox, BASE_DIR / "test_c"]:
            if d.exists():
                try:
                    shutil.rmtree(d)
                except Exception:
                    pass

if __name__ == "__main__":
    run_e2e_tests()
