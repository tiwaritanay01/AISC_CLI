# LabX Remote Architecture & Design Specification

This document details the architectural design, security model, and component interactions of **LabX Remote**.

---

## 1. High-Level Architecture

LabX Remote employs a two-tier decoupled client-server architecture:

```mermaid
flowchart TD
    subgraph Remote["Netlify Static Distribution Layer"]
        A["catalog.json"]
        B["version.json"]
        C["experiments/XX/manifest.json"]
        D["experiments/XX/sources..."]
        E["downloads/labx_experiments.zip"]
    end

    subgraph Client["Student Local Environment (CLI)"]
        CLI["LabX CLI / labx.exe"]
        Cache["Local Disk Cache (~/.labx/cache)"]
        Search["RapidFuzz Search Engine"]
        Downloader["Streaming Downloader & Safe Extractor"]
        Registry["Language Runner Registry"]
    end

    subgraph Toolchains["Host Compilers & Runtimes"]
        Py["Python (py / python3)"]
        Jdk["Java JDK (javac + java)"]
        Gcc["GNU GCC (gcc.exe)"]
        Gpp["GNU G++ (g++.exe)"]
        Emb["Embedded IDE (Keil / Proteus / ARM GCC)"]
    end

    CLI -->|1. Query Catalog| A
    CLI -->|2. Check Version| B
    CLI -->|Fallback when offline| Cache
    CLI --> Search
    CLI --> Downloader
    Downloader -->|Fetch Source Files| D
    Downloader -->|Fetch Bulk ZIP| E
    CLI --> Registry
    Registry --> Py
    Registry --> Jdk
    Registry --> Gcc
    Registry --> Gpp
    Registry --> Emb
```

---

## 2. Remote Hosting Layer (Netlify)

The remote layer is hosted as a serverless static repository on Netlify.
It serves as an API backend without requiring a relational database or stateful server:

- **Predictable URL Scheme**:
  - `GET /catalog.json` - High-level catalog containing metadata for all experiments.
  - `GET /version.json` - System version and backend heartbeat.
  - `GET /experiments/{id}/manifest.json` - Detailed metadata, algorithm, aim, theory, and source file list.
  - `GET /experiments/{id}/{filename}` - Individual source and header files.
  - `GET /downloads/labx_experiments.zip` - Complete pre-packaged experiment archive.
- **CORS & Cache Controls**: Configured via `netlify.toml` with `Access-Control-Allow-Origin: *` to allow access from any client.

---

## 3. Fuzzy Matching & Resolution Engine

When a student types `labx download <query>`, LabX resolves the input through a 5-tier matching priority:

```mermaid
flowchart TD
    Q["Input Query"] --> T1{"1. Exact Numeric ID?"}
    T1 -- Yes --> R1["Return Exact ID Match (Score 100)"]
    T1 -- No --> T2{"2. Exact Title Match?"}
    T2 -- Yes --> R2["Return Exact Title Match (Score 100)"]
    T2 -- No --> T3{"3. Exact Alias Match?"}
    T3 -- Yes --> R3["Return Exact Alias Match (Score 100)"]
    T3 -- No --> T4{"4. Normalized String Match?"}
    T4 -- Yes --> R4["Return Normalized Match (Score 98)"]
    T4 -- No --> T5["5. RapidFuzz WRatio Scorer"]
    T5 --> Amb{"Ambiguity Check (Gap < 8%?)"}
    Amb -- Yes --> Prompt["Prompt Interactive Choice / Disambiguate"]
    Amb -- No --> R5["Return Top Scored Match"]
```

---

## 4. Execution Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant CLI as LabX CLI
    participant Netlify as Remote Host
    participant Cache as Local Cache
    participant Runner as Language Runner
    participant HostOS as Operating System / Compiler

    Student->>CLI: labx run 3
    CLI->>Cache: Check for cached manifest #3
    alt Manifest in Cache
        Cache-->>CLI: Return cached manifest
    else Manifest missing & online
        CLI->>Netlify: GET /experiments/03/manifest.json
        Netlify-->>CLI: Return manifest
    end
    CLI->>CLI: Locate Experiment folder in CWD
    CLI->>Runner: Delegate to JavaRunner
    Runner->>HostOS: Check javac & java availability in PATH
    HostOS-->>Runner: Compilers present
    Runner->>HostOS: javac -encoding UTF-8 Server.java Client.java
    HostOS-->>Runner: Compilation Exit Code 0
    Runner->>HostOS: java -cp . Server
    HostOS-->>Student: Stream real-time stdout/stderr to terminal
    HostOS-->>CLI: Return process exit code
```

---

## 5. Security Architecture

1. **Path Traversal (Zip-Slip) Protection**:
   - `is_safe_path(base_dir, target_path)` validates that every extracted file resolves strictly within the target working directory.
   - Archive entries with `../` or absolute drive roots (`C:\Windows\...`) are discarded before extraction.
2. **Subprocess Isolation**:
   - Compilers and scripts are invoked using argument arrays (e.g. `["gcc", "-Wall", "main.c"]`) rather than shell string interpolation (`shell=True`), preventing command injection.
3. **Stream Safety & Headless Compatibility**:
   - File descriptors are validated (`fileno()`) before subprocess attachment, preventing pipe crashes in automated or pseudo-terminal environments.
4. **Non-Destructive Overwrites**:
   - User files in the working directory are protected with interactive overwrite confirmations unless `--force` is explicitly provided.

