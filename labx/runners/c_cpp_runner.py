"""C and C++ compilation and execution adapter."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional

from labx.models import RunConfig
from labx.runners.base import BaseLanguageRunner


def get_compiler_env(compiler_name: str) -> dict:
    """Return environment dictionary with compiler's parent bin directory prepended to PATH."""
    env = os.environ.copy()
    bin_path = shutil.which(compiler_name)
    if bin_path:
        bin_dir = str(Path(bin_path).resolve().parent)
        current_path = env.get("PATH", "")
        if not current_path.startswith(bin_dir):
            env["PATH"] = f"{bin_dir}{os.pathsep}{current_path}"
    return env


class CRunner(BaseLanguageRunner):
    """Compiles C source with gcc and executes the compiled binary."""

    @property
    def name(self) -> str:
        return "C"

    def check_prerequisites(self) -> Tuple[bool, str]:
        gcc_bin = shutil.which("gcc")
        if not gcc_bin:
            return False, "'gcc' compiler not found in PATH."
        return True, f"Found gcc: {gcc_bin}"

    def get_toolchain_help(self) -> str:
        return (
            "GCC is required to compile C experiments.\n"
            "• Windows: Install MinGW-w64 or MSYS2: https://www.msys2.org/ or 'winget install MSYS2'\n"
            "• Linux: Run 'sudo apt install build-essential'.\n"
            "• macOS: Run 'xcode-select --install'."
        )

    def get_execution_env(self) -> dict:
        return get_compiler_env("gcc")

    def _get_binary_name(self, entry: str) -> str:
        base = Path(entry).stem
        return f"{base}.exe" if sys.platform == "win32" else base

    def compile(self, exp_dir: Path, run_config: RunConfig) -> Tuple[bool, str]:
        c_files = list(exp_dir.glob("*.c"))
        if not c_files:
            return False, f"No .c source files found in {exp_dir}."

        bin_name = self._get_binary_name(run_config.entry)
        cmd = ["gcc", "-Wall", "-O2"] + [f.name for f in c_files] + ["-o", bin_name, "-lm"]
        env = self.get_execution_env()

        try:
            res = subprocess.run(
                cmd,
                cwd=str(exp_dir),
                capture_output=True,
                text=True,
                errors="replace",
                env=env,
                check=False
            )
            if res.returncode != 0:
                err_output = res.stderr or res.stdout or f"gcc exited with code {res.returncode}"
                return False, f"Compilation failed:\n{err_output}"
            return True, "C source compilation succeeded."
        except Exception as exc:
            return False, f"Error launching gcc: {exc}"

    def build_execution_command(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[List[str]]:
        entry = run_config.entry
        if component_name and component_name in run_config.components:
            entry = run_config.components[component_name].entry

        bin_name = self._get_binary_name(entry)
        bin_path = exp_dir / bin_name

        if not bin_path.exists():
            return None

        cmd = [str(bin_path.resolve())]
        if extra_args:
            cmd.extend(extra_args)
        return cmd


class CppRunner(BaseLanguageRunner):
    """Compiles C++ source with g++ and executes the compiled binary."""

    @property
    def name(self) -> str:
        return "C++"

    def check_prerequisites(self) -> Tuple[bool, str]:
        gpp_bin = shutil.which("g++")
        if not gpp_bin:
            return False, "'g++' compiler not found in PATH."
        return True, f"Found g++: {gpp_bin}"

    def get_toolchain_help(self) -> str:
        return (
            "G++ is required to compile C++ experiments.\n"
            "• Windows: Install MinGW-w64 or MSYS2: https://www.msys2.org/ or 'winget install MSYS2'\n"
            "• Linux: Run 'sudo apt install g++'.\n"
            "• macOS: Run 'xcode-select --install'."
        )

    def get_execution_env(self) -> dict:
        return get_compiler_env("g++")

    def _get_binary_name(self, entry: str) -> str:
        base = Path(entry).stem
        return f"{base}.exe" if sys.platform == "win32" else base

    def compile(self, exp_dir: Path, run_config: RunConfig) -> Tuple[bool, str]:
        cpp_files = list(exp_dir.glob("*.cpp")) + list(exp_dir.glob("*.cc"))
        if not cpp_files:
            return False, f"No C++ source files found in {exp_dir}."

        bin_name = self._get_binary_name(run_config.entry)
        cmd = ["g++", "-Wall", "-O2", "-std=c++17"] + [f.name for f in cpp_files] + ["-o", bin_name]
        env = self.get_execution_env()

        try:
            res = subprocess.run(
                cmd,
                cwd=str(exp_dir),
                capture_output=True,
                text=True,
                errors="replace",
                env=env,
                check=False
            )
            if res.returncode != 0:
                err_output = res.stderr or res.stdout or f"g++ exited with code {res.returncode}"
                return False, f"Compilation failed:\n{err_output}"
            return True, "C++ source compilation succeeded."
        except Exception as exc:
            return False, f"Error launching g++: {exc}"

    def build_execution_command(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[List[str]]:
        entry = run_config.entry
        if component_name and component_name in run_config.components:
            entry = run_config.components[component_name].entry

        bin_name = self._get_binary_name(entry)
        bin_path = exp_dir / bin_name

        if not bin_path.exists():
            return None

        cmd = [str(bin_path.resolve())]
        if extra_args:
            cmd.extend(extra_args)
        return cmd
