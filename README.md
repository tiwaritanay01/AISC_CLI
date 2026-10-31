# LabX Remote CLI

[![Build & Verification](https://img.shields.io/badge/Verification-30%2F30%20PASS%20(100%25)-brightgreen)](#)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](#)

> **Production-Ready Remote Experiment Distribution & Execution Utility for Laboratory Students and Educators.**

---

## 1. Introduction

**LabX Remote** is a terminal-first command-line utility designed to streamline how students download, organize, inspect, compile, and execute laboratory experiments directly from their IDE integrated terminals (PyCharm, VS Code, Cursor, Windows Terminal, etc.).

Students **do not** need to:
- Clone monolithic Git repositories.
- Configure Python virtual environments or manually install pip packages.
- Open web browsers to copy and paste code snippets.
- Manage compiler flags or complicated multi-process execution steps.

Everything happens through intuitive, clean commands:
```bash
labx download 3
labx run 3
```

---

## 2. Quick Start

### Installation on Windows (One-Line PowerShell)

Open PowerShell and execute:
```powershell
irm https://labx-remote.netlify.app/install.ps1 | iex
```
*Or download standalone `dist/labx.exe` directly and place it in your PATH.*

### Basic CLI Commands

```bash
# Display LabX banner, version, connection status and available commands
labx

# List all available experiments in the remote catalogue
labx list

# Fuzzy search experiments by keyword, topic, or alias
labx search routing
labx search "socket programing"

# Inspect experiment aim, theory, algorithm, and files
labx info 3

# Download an individual experiment into your current working directory
labx download 3
labx download "Java Socket Programming"

# Download the complete laboratory experiment archive (all experiments)
labx download all

# Compile and run an experiment in your current directory
labx run 3
labx run socket

# Run a specific component of a multi-process experiment (e.g. server or client)
labx run 3 --component client

# Refresh local metadata cache
labx update

# Clean up / remove a downloaded experiment folder
labx remove 3
```

---

## 3. Supported Languages & Execution Adapters

LabX includes an extensible execution adapter architecture with compiler auto-detection:

| Language | Adapter | Required Compiler / Runtime | Auto Action |
|---|---|---|---|
| **Python** | `PythonRunner` | `python` / `py` | Direct interpreter invocation |
| **Java** | `JavaRunner` | JDK (`javac` + `java`) | Compiles `.java` files, Derives class name, Runs JVM |
| **C** | `CRunner` | `gcc` (MinGW / MSYS2 / GCC) | Auto-links math/pthreads, builds binary, executes |
| **C++** | `CppRunner` | `g++` (C++17) | Compiles with `-std=c++17`, builds binary, executes |
| **Embedded C** | `EmbeddedRunner` | Keil µVision / Proteus / ARM GCC | Generates verified firmware files & step-by-step toolchain guide |

---

## 4. Architecture Overview

LabX implements a decoupled, two-part architecture:
1. **Remote Hosting Layer (Netlify Static Distribution)**:
   - Hosts static API endpoints: `/catalog.json`, `/version.json`.
   - Hosts individual experiment manifests and source files: `/experiments/01/...`.
   - Hosts the bulk ZIP archive: `/downloads/labx_experiments.zip`.
   - Zero database required; CDN-cached with CORS enabled.
2. **Local Execution Layer (LabX CLI)**:
   - Standalone `labx.exe` built with PyInstaller (no local Python required).
   - Local metadata cache at `~/.labx/cache` enabling full offline execution.
   - RapidFuzz multi-tiered matching engine.
   - Safe ZIP extraction protecting against Zip-Slip path traversal vulnerabilities.

---

## 5. Development & Testing

```bash
# Install in editable development mode
pip install -e .

# Rebuild Netlify host public directory and ZIP archive
python scripts/build_host.py

# Run automated test suite (30 tests)
pytest -v

# Run full end-to-end acceptance verification (Scenarios A through F)
python scripts/verify_acceptance.py

# Build Windows standalone executable
pwsh -File scripts/build_windows.ps1
```

---

## 6. Documentation Index

- [Architecture Design & Security Specification](docs/ARCHITECTURE.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Netlify Deployment Guide](docs/NETLIFY_DEPLOYMENT.md)
- [PyPI Publishing Guide](docs/PYPI_PUBLISHING.md)
- [Test & Verification Report](docs/TEST_REPORT.md)

