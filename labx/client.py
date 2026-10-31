"""Remote HTTP client for LabX experiment catalogue and file retrieval."""

import os
from pathlib import Path
from typing import Optional, Callable, Tuple
import httpx

from labx.config import get_remote_url, DEFAULT_TIMEOUT_SECONDS
from labx.models import Catalog, ExperimentManifest


class LabXNetworkError(Exception):
    """Raised when communication with remote server fails."""
    pass


class LabXRemoteClient:
    """HTTP client responsible for remote API queries and artifact downloads."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT_SECONDS):
        self.base_url = get_remote_url(base_url)
        self.timeout = timeout

    def _resolve_url(self, endpoint_or_url: str) -> str:
        """Resolve a relative path against the configured base URL."""
        if endpoint_or_url.startswith("http://") or endpoint_or_url.startswith("https://"):
            return endpoint_or_url
        clean_endpoint = endpoint_or_url.lstrip("/")
        return f"{self.base_url}/{clean_endpoint}"

    def check_connection(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """Verify remote connectivity and return (connected, remote_version, error_message)."""
        url = self._resolve_url("version.json")
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    version = data.get("version", "unknown")
                    return True, version, None
                else:
                    return False, None, f"Remote returned HTTP {resp.status_code}"
        except httpx.RequestError as exc:
            return False, None, f"Network error: {str(exc)}"
        except Exception as exc:
            return False, None, f"Connection failed: {str(exc)}"

    def fetch_catalog(self) -> Catalog:
        """Fetch and parse the experiment catalogue from remote host."""
        url = self._resolve_url("catalog.json")
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(url)
                resp.raise_for_status()
                data = resp.json()
                return Catalog.from_dict(data)
        except httpx.HTTPStatusError as exc:
            raise LabXNetworkError(f"HTTP {exc.response.status_code} fetching catalogue from {url}") from exc
        except httpx.RequestError as exc:
            raise LabXNetworkError(f"Failed to connect to {url}: {exc}") from exc
        except Exception as exc:
            raise LabXNetworkError(f"Error parsing catalogue: {exc}") from exc

    def fetch_manifest(self, manifest_path_or_url: str) -> ExperimentManifest:
        """Fetch and parse an individual experiment manifest."""
        url = self._resolve_url(manifest_path_or_url)
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(url)
                resp.raise_for_status()
                data = resp.json()
                return ExperimentManifest.from_dict(data)
        except httpx.HTTPStatusError as exc:
            raise LabXNetworkError(f"HTTP {exc.response.status_code} fetching manifest from {url}") from exc
        except httpx.RequestError as exc:
            raise LabXNetworkError(f"Failed to connect to manifest at {url}: {exc}") from exc
        except Exception as exc:
            raise LabXNetworkError(f"Error parsing manifest: {exc}") from exc

    def download_file(
        self,
        file_path_or_url: str,
        destination: Path,
        progress_callback: Optional[Callable[[int, Optional[int]], None]] = None
    ) -> Path:
        """Download a single remote file to local destination with optional progress updates."""
        url = self._resolve_url(file_path_or_url)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temp_dest = destination.with_suffix(f"{destination.suffix}.tmp")

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                with client.stream("GET", url) as response:
                    response.raise_for_status()
                    total_bytes = None
                    if "content-length" in response.headers:
                        try:
                            total_bytes = int(response.headers["content-length"])
                        except (ValueError, TypeError):
                            total_bytes = None

                    downloaded = 0
                    with open(temp_dest, "wb") as f:
                        for chunk in response.iter_bytes(chunk_size=16384):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if progress_callback:
                                    progress_callback(downloaded, total_bytes)

            # Atomic rename after successful download
            if temp_dest.exists():
                if destination.exists():
                    destination.unlink()
                temp_dest.rename(destination)
            return destination
        except Exception as exc:
            if temp_dest.exists():
                try:
                    temp_dest.unlink()
                except Exception:
                    pass
            raise LabXNetworkError(f"Failed to download file from {url}: {exc}") from exc

    def download_zip(
        self,
        zip_path_or_url: str,
        destination: Path,
        progress_callback: Optional[Callable[[int, Optional[int]], None]] = None
    ) -> Path:
        """Download the full ZIP archive to destination."""
        return self.download_file(zip_path_or_url, destination, progress_callback)

