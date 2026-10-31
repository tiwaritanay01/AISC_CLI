"""Tests for the RapidFuzz fuzzy search engine."""

import pytest
from labx.search import ExperimentSearchEngine


def test_exact_numeric_id_matching(sample_catalog):
    engine = ExperimentSearchEngine(sample_catalog)

    # Simple ID string
    res = engine.search("3")
    assert len(res) == 1
    assert res[0].item.id == 3
    assert res[0].match_type == "exact_id"
    assert res[0].score == 100.0

    # Padded or prefixed ID
    res = engine.search("01")
    assert res[0].item.id == 1

    res = engine.search("#4")
    assert res[0].item.id == 4

    res = engine.search("exp 3")
    assert res[0].item.id == 3


def test_exact_title_and_alias_matching(sample_catalog):
    engine = ExperimentSearchEngine(sample_catalog)

    # Title match (case insensitive)
    item, _, is_amb = engine.resolve("dijkstra's shortest path routing algorithm")
    assert item is not None
    assert item.id == 4
    assert not is_amb

    # Alias match
    item, _, is_amb = engine.resolve("socket programming")
    assert item is not None
    assert item.id == 3
    assert not is_amb

    item, _, is_amb = engine.resolve("fibonacci")
    assert item is not None
    assert item.id == 1
    assert not is_amb


def test_fuzzy_matching_with_typos(sample_catalog):
    engine = ExperimentSearchEngine(sample_catalog)

    # Typo: "socket programing" -> Java Sockets
    item, matches, is_amb = engine.resolve("socket programing")
    assert item is not None
    assert item.id == 3

    # Abbreviation / partial: "dyn routing" -> Dijkstra
    item, matches, is_amb = engine.resolve("dyn routing")
    assert item is not None
    assert item.id == 4

    # Typo: "factrial" -> Factorial
    item, matches, is_amb = engine.resolve("factrial")
    assert item is not None
    assert item.id == 1


def test_unknown_query(sample_catalog):
    engine = ExperimentSearchEngine(sample_catalog)
    item, matches, is_amb = engine.resolve("completely unrelated quantum teleportation string")
    assert item is None
    assert len(matches) == 0
    assert not is_amb


def test_search_rank_order(sample_catalog):
    engine = ExperimentSearchEngine(sample_catalog)
    results = engine.search("routing")
    assert len(results) > 0
    assert results[0].item.id == 4

