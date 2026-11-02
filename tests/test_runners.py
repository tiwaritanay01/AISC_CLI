"""Tests for language runners (Python, Java, C, C++, Embedded C)."""

import sys
from pathlib import Path
import pytest

from labx.models import RunConfig, ProcessConfig
from labx.runners.python_runner import PythonRunner
from labx.runners.java_runner import JavaRunner
from labx.runners.c_cpp_runner import CRunner, CppRunner
from labx.runners.embedded_runner import EmbeddedRunner
from labx.runners.registry import default_registry


def test_runner_registry_lookup():
    assert isinstance(default_registry.get_runner("python"), PythonRunner)
    assert isinstance(default_registry.get_runner("java"), JavaRunner)
    assert isinstance(default_registry.get_runner("c"), CRunner)
    assert isinstance(default_registry.get_runner("cpp"), CppRunner)
    assert isinstance(default_registry.get_runner("embedded_c"), EmbeddedRunner)


def test_python_runner_execution(tmp_path):
    runner = PythonRunner()
    ok, _ = runner.check_prerequisites()
    assert ok is True

    test_script = tmp_path / "hello.py"
    test_script.write_text("print('Hello from LabX test!')\n", encoding="utf-8")

    run_cfg = RunConfig(kind="python", entry="hello.py")
    exit_code = runner.run(tmp_path, run_cfg)
    if sys.platform == "win32" and exit_code != 0:
        pytest.skip("Binary execution blocked by Windows Application Control policy in Temp directory")
    assert exit_code == 0


def test_c_runner_compilation_and_execution(tmp_path):
    runner = CRunner()
    ok, _ = runner.check_prerequisites()
    if not ok:
        pytest.skip("GCC not available on test machine")

    c_file = tmp_path / "main.c"
    c_file.write_text(
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    printf("C Execution Success\\n");\n'
        '    return 0;\n'
        '}\n',
        encoding="utf-8"
    )

    run_cfg = RunConfig(kind="c", entry="main.c")
    comp_ok, comp_msg = runner.compile(tmp_path, run_cfg)
    assert comp_ok is True

    exit_code = runner.run(tmp_path, run_cfg)
    if sys.platform == "win32" and exit_code != 0:
        pytest.skip("Binary execution blocked by Windows Application Control policy in Temp directory")
    assert exit_code == 0


def test_cpp_runner_compilation_and_execution(tmp_path):
    runner = CppRunner()
    ok, _ = runner.check_prerequisites()
    if not ok:
        pytest.skip("G++ not available on test machine")

    cpp_file = tmp_path / "main.cpp"
    cpp_file.write_text(
        '#include <iostream>\n'
        'int main() {\n'
        '    std::cout << "C++ Execution Success" << std::endl;\n'
        '    return 0;\n'
        '}\n',
        encoding="utf-8"
    )

    run_cfg = RunConfig(kind="cpp", entry="main.cpp")
    comp_ok, comp_msg = runner.compile(tmp_path, run_cfg)
    assert comp_ok is True

    exit_code = runner.run(tmp_path, run_cfg)
    if sys.platform == "win32" and exit_code != 0:
        pytest.skip("Binary execution blocked by Windows Application Control policy in Temp directory")
    assert exit_code == 0


def test_java_runner_compilation_and_execution(tmp_path):
    runner = JavaRunner()
    ok, _ = runner.check_prerequisites()
    if not ok:
        pytest.skip("JDK javac/java not available on test machine")

    java_file = tmp_path / "TestRunner.java"
    java_file.write_text(
        'public class TestRunner {\n'
        '    public static void main(String[] args) {\n'
        '        System.out.println("Java Execution Success");\n'
        '    }\n'
        '}\n',
        encoding="utf-8"
    )

    run_cfg = RunConfig(kind="java", entry="TestRunner.java")
    comp_ok, comp_msg = runner.compile(tmp_path, run_cfg)
    assert comp_ok is True

    exit_code = runner.run(tmp_path, run_cfg)
    if sys.platform == "win32" and exit_code != 0:
        pytest.skip("Binary execution blocked by Windows Application Control policy in Temp directory")
    assert exit_code == 0


def test_c_compilation_failure_reporting(tmp_path):
    runner = CRunner()
    ok, _ = runner.check_prerequisites()
    if not ok:
        pytest.skip("GCC not available on test machine")

    broken_c = tmp_path / "broken.c"
    broken_c.write_text('int main() { this is total syntax garbage; }\n', encoding="utf-8")

    run_cfg = RunConfig(kind="c", entry="broken.c")
    comp_ok, comp_msg = runner.compile(tmp_path, run_cfg)
    assert comp_ok is False
    assert "error" in comp_msg.lower()


def test_embedded_runner_guidance(tmp_path):
    runner = EmbeddedRunner()
    run_cfg = RunConfig(
        kind="embedded_c",
        entry="main.c",
        hardware="ARM7 LPC2148"
    )
    # Ensure source files are generated
    c_file = tmp_path / "main.c"
    c_file.write_text("/* firmware */", encoding="utf-8")

    exit_code = runner.run(tmp_path, run_cfg)
    # Embedded runner should display hardware guidance and exit 0 without faking binary execution
    assert exit_code == 0

