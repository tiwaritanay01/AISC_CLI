"""Java compilation and execution adapter."""

import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional

from labx.models import RunConfig
from labx.runners.base import BaseLanguageRunner


class JavaRunner(BaseLanguageRunner):
    """Compiles Java source files with javac and runs with java."""

    @property
    def name(self) -> str:
        return "Java"

    def check_prerequisites(self) -> Tuple[bool, str]:
        javac_bin = shutil.which("javac")
        java_bin = shutil.which("java")

        if not javac_bin:
            return False, "'javac' compiler not found in PATH."
        if not java_bin:
            return False, "'java' runtime not found in PATH."

        return True, f"Found JDK: javac ({javac_bin}), java ({java_bin})"

    def get_toolchain_help(self) -> str:
        return (
            "A Java Development Kit (JDK 17+) is required to compile and run Java experiments.\n"
            "• Download Eclipse Temurin or Oracle JDK: https://adoptium.net/\n"
            "• Windows: Ensure JDK's 'bin' directory is added to system PATH.\n"
            "• Linux: Run 'sudo apt install default-jdk'.\n"
            "• macOS: Run 'brew install openjdk'."
        )

    def compile(self, exp_dir: Path, run_config: RunConfig) -> Tuple[bool, str]:
        """Compile all Java source files in the experiment directory."""
        java_files = list(exp_dir.glob("*.java"))
        if not java_files:
            return False, f"No .java source files found in {exp_dir}."

        javac_cmd = ["javac", "-encoding", "UTF-8"] + [f.name for f in java_files]

        try:
            res = subprocess.run(
                javac_cmd,
                cwd=str(exp_dir),
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode != 0:
                return False, f"javac failed (exit code {res.returncode}):\n{res.stderr}\n{res.stdout}"
            return True, "Java source compilation succeeded."
        except Exception as exc:
            return False, f"Error launching javac: {exc}"

    def build_execution_command(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[List[str]]:
        entry = run_config.entry

        if component_name and component_name in run_config.components:
            comp = run_config.components[component_name]
            entry = comp.entry

        # Derive class name from entry file (e.g. Server.java -> Server)
        class_name = Path(entry).stem
        cmd = ["java", "-cp", ".", class_name]
        if extra_args:
            cmd.extend(extra_args)
        return cmd

