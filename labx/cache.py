"""Local metadata caching for offline and fast access."""

import json
from pathlib import Path
from typing import Optional, Dict, Any

from labx.config import get_cache_dir
from labx.models import Catalog, ExperimentManifest


class LabXCache:
    """Manages cached catalogues and manifests on the local disk."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or get_cache_dir()
        self.manifest_dir = self.cache_dir / "manifests"
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        self.catalog_file = self.cache_dir / "catalog.json"

    def save_catalog(self, catalog_dict: Dict[str, Any]) -> None:
        """Write raw catalog JSON to disk cache."""
        try:
            with open(self.catalog_file, "w", encoding="utf-8") as f:
                json.dump(catalog_dict, f, indent=2)
        except Exception:
            pass

    def load_catalog(self) -> Optional[Catalog]:
        """Load catalog from disk cache if present and valid."""
        if not self.catalog_file.exists():
            return None
        try:
            with open(self.catalog_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Catalog.from_dict(data)
        except Exception:
            return None

    def save_manifest(self, exp_id: int, manifest_dict: Dict[str, Any]) -> None:
        """Save experiment manifest to disk cache."""
        dest = self.manifest_dir / f"exp_{exp_id:02d}.json"
        try:
            with open(dest, "w", encoding="utf-8") as f:
                json.dump(manifest_dict, f, indent=2)
        except Exception:
            pass

    def load_manifest(self, exp_id: int) -> Optional[ExperimentManifest]:
        """Retrieve cached experiment manifest if available."""
        target = self.manifest_dir / f"exp_{exp_id:02d}.json"
        if not target.exists():
            return None
        try:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ExperimentManifest.from_dict(data)
        except Exception:
            return None

    def clear(self) -> None:
        """Clear all cached metadata."""
        if self.catalog_file.exists():
            try:
                self.catalog_file.unlink()
            except Exception:
                pass
        for item in self.manifest_dir.glob("*.json"):
            try:
                item.unlink()
            except Exception:
                pass

