"""Registry mapping language and runtime keys to runner instances."""

from typing import Dict, Optional
from labx.runners.base import BaseLanguageRunner
from labx.runners.python_runner import PythonRunner
from labx.runners.java_runner import JavaRunner
from labx.runners.c_cpp_runner import CRunner, CppRunner
from labx.runners.embedded_runner import EmbeddedRunner


class RunnerRegistry:
    """Manages available language runners."""

    def __init__(self):
        self._runners: Dict[str, BaseLanguageRunner] = {}
        self._register_defaults()

    def _register_defaults(self):
        py = PythonRunner()
        java = JavaRunner()
        c = CRunner()
        cpp = CppRunner()
        embedded = EmbeddedRunner()

        for key in ["python", "py", "python3"]:
            self._runners[key] = py

        for key in ["java", "jvm"]:
            self._runners[key] = java

        for key in ["c", "clang"]:
            self._runners[key] = c

        for key in ["cpp", "c++", "cplusplus"]:
            self._runners[key] = cpp

        for key in ["embedded_c", "embedded", "arm", "arm7", "lpc2148"]:
            self._runners[key] = embedded

    def register(self, key: str, runner: BaseLanguageRunner):
        self._runners[key.lower()] = runner

    def get_runner(self, language_or_kind: str) -> Optional[BaseLanguageRunner]:
        return self._runners.get(language_or_kind.lower().strip())


default_registry = RunnerRegistry()

