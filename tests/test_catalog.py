"""Tests for catalogue and manifest models, parsing, validation, and caching."""

import pytest
from labx.models import Catalog, ExperimentManifest, CatalogItem
from labx.client import LabXRemoteClient, LabXNetworkError
from labx.cache import LabXCache


def test_valid_catalog_parsing():
    raw_data = {
        "version": "1.0.0",
        "updated_at": "2026-10-31",
        "zip_url": "downloads/all.zip",
        "experiments": [
            {
                "id": 1,
                "slug": "exp-1",
                "title": "First Exp",
                "language": "python",
                "aliases": ["one"],
                "description": "First test",
                "manifest_url": "experiments/01/manifest.json"
            },
            {
                "id": 2,
                "slug": "exp-2",
                "title": "Second Exp",
                "language": "c",
                "aliases": ["two"],
                "description": "Second test",
                "manifest_url": "experiments/02/manifest.json"
            }
        ]
    }
    cat = Catalog.from_dict(raw_data)
    assert cat.version == "1.0.0"
    assert len(cat.experiments) == 2
    assert cat.get_by_id(1) is not None
    assert cat.get_by_id(1).title == "First Exp"
    assert cat.get_by_id(999) is None


def test_manifest_parsing_with_components():
    raw_manifest = {
        "id": 3,
        "slug": "java-socket",
        "title": "Java Sockets",
        "language": "java",
        "aliases": ["socket"],
        "description": "TCP client-server",
        "aim": "Implement sockets",
        "theory": "TCP sockets theory",
        "algorithm": ["Start server", "Connect client"],
        "files": [
            {"path": "Server.java", "source": "Server.java", "role": "source"},
            {"path": "Client.java", "source": "Client.java", "role": "source"}
        ],
        "run": {
            "kind": "java",
            "entry": "Server.java",
            "components": {
                "server": {"name": "Server", "entry": "Server.java"},
                "client": {"name": "Client", "entry": "Client.java"}
            }
        }
    }
    mf = ExperimentManifest.from_dict(raw_manifest)
    assert mf.id == 3
    assert len(mf.files) == 2
    assert mf.run.kind == "java"
    assert "server" in mf.run.components
    assert "client" in mf.run.components


def test_cache_save_and_load(tmp_path):
    cache = LabXCache(cache_dir=tmp_path)
    assert cache.load_catalog() is None

    sample_data = {
        "version": "1.0.0",
        "updated_at": "2026-10-31",
        "zip_url": "downloads/all.zip",
        "experiments": [
            {
                "id": 5,
                "slug": "exp-5",
                "title": "Sliding Window",
                "language": "c",
                "aliases": ["gbn"],
                "description": "Sliding window protocol",
                "manifest_url": "experiments/05/manifest.json"
            }
        ]
    }
    cache.save_catalog(sample_data)
    loaded = cache.load_catalog()
    assert loaded is not None
    assert len(loaded.experiments) == 1
    assert loaded.experiments[0].title == "Sliding Window"


def test_live_server_catalog_fetch(live_server):
    client = LabXRemoteClient(base_url=live_server)
    connected, version, err = client.check_connection()
    assert connected is True
    assert version == "1.0.0"

    catalog = client.fetch_catalog()
    assert len(catalog.experiments) >= 12
    exp3 = catalog.get_by_id(3)
    assert exp3 is not None
    assert "DFID" in exp3.title or "Depth First" in exp3.title


def test_remote_failure_handling():
    # Attempt connecting to invalid port
    client = LabXRemoteClient(base_url="http://127.0.0.1:59999", timeout=1.0)
    connected, _, err = client.check_connection()
    assert connected is False
    assert err is not None

    with pytest.raises(LabXNetworkError):
        client.fetch_catalog()

