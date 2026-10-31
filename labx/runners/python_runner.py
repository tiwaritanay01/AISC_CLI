"""Python execution adapter."""

import shutil
import sys
from pathlib import Path
from typing import List, Tuple, Optional

from labx.models import RunConfig
from labx.runners.base import BaseLanguageRunner


class PythonRunner(BaseLanguageRunner):
    """Executes Python scripts using python, py, or sys.executable."""

    @property
    def name(self) -> str:
        return "Python"

    def _resolve_python_executable(self) -> Optional[str]:
        """Detect the best Python binary on this system."""
        # 1. If currently in a Python runtime
        if sys.executable and Path(sys.executable).is_file():
            return sys.executable

        # 2. Check py launcher on Windows
        if shutil.which("py"):
            return "py"

        # 3. Check python / python3
        for candidate in ["python3", "python"]:
            found = shutil.which(candidate)
            if found:
                return found

        return None

    def check_prerequisites(self) -> Tuple[bool, str]:
        py_bin = self._resolve_python_executable()
        if py_bin:
            return True, f"Python found: {py_bin}"
        return False, "Python interpreter not found in PATH."

    def get_toolchain_help(self) -> str:
        return (
            "Python is required to run this experiment.\n"
            "• Download and install Python from: https://www.python.org/downloads/\n"
            "• Windows: Ensure 'Add python.exe to PATH' is checked during installation.\n"
            "• Linux/macOS: Run 'sudo apt install python3' or 'brew install python3'."
        )

    def build_execution_command(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[List[str]]:
        py_bin = self._resolve_python_executable() or "python"
        entry_file = run_config.entry

        # Check if a specific component was requested
        if component_name and component_name in run_config.components:
            comp = run_config.components[component_name]
            entry_file = comp.entry
            if comp.run_cmd:
                cmd = list(comp.run_cmd)
                if extra_args:
                    cmd.extend(extra_args)
                return cmd

        target_file = exp_dir / entry_file
        if not target_file.exists():
            # Search for entry filename case-insensitively
            for f in exp_dir.glob("*.py"):
                if f.name.lower() == entry_file.lower():
                    target_file = f
                    break

        cmd = [py_bin, str(target_file.name)]
        if extra_args:
            cmd.extend(extra_args)
        return cmd

