"""Base abstractions and result types for language execution runners."""

import os
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional, Dict

from labx.models import RunConfig


@dataclass
class ExecutionResult:
    """Outcome of compilation and/or process execution."""
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    compiled: bool = True
    compiler_message: str = ""
    error_message: Optional[str] = None


def get_safe_stream(stream):
    """Verify that a stream has a valid OS fileno, safe for subprocess."""
    try:
        if stream is not None and hasattr(stream, "fileno"):
            stream.fileno()
            return stream
    except Exception:
        pass
    return None


class BaseLanguageRunner(ABC):
    """Abstract execution adapter for programming languages and toolchains."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Friendly language name."""
        pass

    @abstractmethod
    def check_prerequisites(self) -> Tuple[bool, str]:
        """Check whether required compiler/runtime is installed on the host system."""
        pass

    @abstractmethod
    def get_toolchain_help(self) -> str:
        """Return user guidance on how to install or configure the compiler/runtime."""
        pass

    def compile(self, exp_dir: Path, run_config: RunConfig) -> Tuple[bool, str]:
        """Compile source files if required by the language. Returns (success, message)."""
        return True, "No compilation required."

    def get_execution_env(self) -> dict:
        """Return process environment with compiler directory added to PATH if needed."""
        return os.environ.copy()

    def run(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> int:
        """Execute the program and stream output directly to terminal. Return exit code."""
        # 1. Check prerequisites
        ok, reason = self.check_prerequisites()
        if not ok:
            print(f"\n[LabX Runner Error] Missing toolchain: {reason}", file=sys.stderr)
            print(self.get_toolchain_help(), file=sys.stderr)
            return 127

        # 2. Compile if necessary
        comp_ok, comp_msg = self.compile(exp_dir, run_config)
        if not comp_ok:
            print(f"\n[LabX Compilation Failed]\n{comp_msg}", file=sys.stderr)
            return 1

        # 3. Resolve command to execute
        cmd = self.build_execution_command(exp_dir, run_config, component_name, extra_args)
        if not cmd:
            print(f"\n[LabX Runner Error] Unable to determine execution command for {self.name}.", file=sys.stderr)
            return 1

        print(f"\n[LabX] Executing: {' '.join(cmd)}")
        print("─" * 60)

        # 4. Execute using argument arrays (safe from shell injection)
        safe_in = get_safe_stream(sys.stdin) or subprocess.DEVNULL
        safe_out = get_safe_stream(sys.stdout)
        safe_err = get_safe_stream(sys.stderr)

        env = self.get_execution_env()

        try:
            process = subprocess.Popen(
                cmd,
                cwd=str(exp_dir),
                stdin=safe_in,
                stdout=safe_out,
                stderr=safe_err,
                env=env
            )
            return process.wait()
        except FileNotFoundError as exc:
            print(f"\n[LabX Execution Error] Executable not found: {exc}", file=sys.stderr)
            return 127
        except Exception as exc:
            print(f"\n[LabX Execution Error] {exc}", file=sys.stderr)
            return 1
        finally:
            print("─" * 60)

    @abstractmethod
    def build_execution_command(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[List[str]]:
        """Construct the argv list for execution."""
        pass
