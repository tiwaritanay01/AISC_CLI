"""Configuration management for LabX CLI."""

import json
import os
from pathlib import Path
from typing import Optional

DEFAULT_REMOTE_URL = "https://cli-t0km.onrender.com"
ENV_REMOTE_URL_KEY = "LABX_REMOTE_URL"
DEFAULT_TIMEOUT_SECONDS = 15.0


def get_labx_home_dir() -> Path:
    """Return the base LabX configuration and cache directory (~/.labx)."""
    home = Path.home() / ".labx"
    home.mkdir(parents=True, exist_ok=True)
    return home


def get_cache_dir() -> Path:
    """Return the cache directory (~/.labx/cache)."""
    cache_dir = get_labx_home_dir() / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_config_file_path() -> Path:
    """Return the path to ~/.labx/config.json."""
    return get_labx_home_dir() / "config.json"


def load_config() -> dict:
    """Load configuration dictionary from disk."""
    config_file = get_config_file_path()
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_config(config: dict) -> None:
    """Save configuration dictionary to disk."""
    config_file = get_config_file_path()
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_remote_url(override_url: Optional[str] = None) -> str:
    """Resolve the remote repository base URL.

    Priority:
    1. CLI argument override (if passed)
    2. Environment variable LABX_REMOTE_URL
    3. User config file ~/.labx/config.json
    4. Default fallback: https://labx-remote.netlify.app
    """
    if override_url and override_url.strip():
        return override_url.strip().rstrip("/")

    env_url = os.getenv(ENV_REMOTE_URL_KEY)
    if env_url and env_url.strip():
        return env_url.strip().rstrip("/")

    cfg = load_config()
    if "remote_url" in cfg and cfg["remote_url"].strip():
        return cfg["remote_url"].strip().rstrip("/")

    return DEFAULT_REMOTE_URL.rstrip("/")

