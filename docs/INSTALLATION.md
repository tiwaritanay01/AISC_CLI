# LabX Remote Installation Guide

This guide details installation procedures for students, laboratory administrators, and developers across Windows, Linux, and macOS.

---

## 1. Windows Installation (Recommended for Students)

### Option A: Automated PowerShell One-Liner

Open PowerShell (as regular user, administrator rights not required) and run:

```powershell
irm https://labx-remote.netlify.app/install.ps1 | iex
```

**What this script does:**
1. Creates a dedicated installation directory at `%LOCALAPPDATA%\Programs\LabX`.
2. Downloads the standalone `labx.exe` (35.9 MB) with bundled Python runtime, Typer, Rich, HTTPX, and RapidFuzz.
3. Automatically adds the directory to your Windows User `PATH` environment variable.

### Option B: Standalone Executable Download & Manual PATH Setup

1. Download `labx.exe` directly from the release page or your institution's Netlify URL:
   ```
   https://labx-remote.netlify.app/downloads/labx.exe
   ```
2. Move `labx.exe` to a permanent folder, for example `C:\Tools\LabX\`.
3. Add `C:\Tools\LabX` to your user PATH:
   - Press <kbd>Win</kbd> + <kbd>R</kbd>, type `sysdm.cpl`, and press **Enter**.
   - Navigate to the **Advanced** tab and click **Environment Variables**.
   - Under **User variables**, select `Path` and click **Edit**.
   - Click **New** and paste `C:\Tools\LabX`. Click **OK**.
4. Open a new terminal window and verify:
   ```cmd
   labx --version
   ```

---

## 2. Linux & macOS Installation

### Automated Bash Installer

Open your terminal and run:

```bash
curl -fsSL https://labx-remote.netlify.app/install.sh | bash
```

The script installs the binary to `~/.local/bin/labx` and configures `~/.bashrc` or `~/.zshrc`.

---

## 3. Python Package (pip / PyPI)

For students who already maintain a Python environment (Python 3.9+):

```bash
pip install labx-remote
```

Verify installation:
```bash
labx list
```

---

## 4. Setting Up Supported Language Compilers

LabX automatically detects host compilers. Install the toolchains relevant to your curriculum:

### Python
- Download from [python.org](https://www.python.org/downloads/).
- **Important:** Ensure **"Add python.exe to PATH"** is checked during installation.

### Java (JDK 17+)
- Download Eclipse Temurin OpenJDK from [adoptium.net](https://adoptium.net/).
- Ensure the JDK `bin/` directory is present in system `PATH`.
- Verify with `javac -version` and `java -version`.

### C & C++ (GCC / G++)
- **Windows**: Install MSYS2 or MinGW-w64:
  ```powershell
  winget install MSYS2.MSYS2
  ```
  Then in MSYS2 terminal:
  ```bash
  pacman -S mingw-w64-ucrt-x86_64-gcc
  ```
  Add `C:\msys64\ucrt64\bin` to Windows `PATH`.
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update && sudo apt install build-essential
  ```
- **macOS**:
  ```bash
  xcode-select --install
  ```

### Embedded C (ARM7 / Microcontrollers)
- Keil µVision IDE: [keil.com](https://www.keil.com/demo/eval/arm.htm)
- Proteus VSM Circuit Simulation: [labcenter.com](https://www.labcenter.com/)
- Flash Magic (ISP UART Flashing): [flashmagictool.com](https://www.flashmagictool.com/)

