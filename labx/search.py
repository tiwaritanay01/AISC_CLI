"""Fuzzy search engine for LabX experiment resolution using RapidFuzz."""

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from rapidfuzz import fuzz

from labx.models import Catalog, CatalogItem


@dataclass
class SearchResult:
    """Represents a scored experiment match."""
    item: CatalogItem
    score: float
    match_type: str
    matched_term: str


def normalize_string(text: str) -> str:
    """Lowercase and strip punctuation/extra whitespace for consistent matching."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    return " ".join(cleaned.split())


class ExperimentSearchEngine:
    """Resolves user queries to catalog items through multi-tiered matching."""

    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    def search(self, query: str, threshold: float = 50.0) -> List[SearchResult]:
        """Search catalog experiments and return scored matches ranked by relevance."""
        raw_query = query.strip()
        if not raw_query:
            return []

        # 1. Exact numeric ID match
        # Handles "3", "03", "#3", "exp 3", "experiment 3"
        id_match = re.match(r"^(?:exp(?:eriment)?\s*#?|#)?(\d+)$", raw_query, re.IGNORECASE)
        if id_match:
            exp_id = int(id_match.group(1))
            item = self.catalog.get_by_id(exp_id)
            if item:
                return [SearchResult(item=item, score=100.0, match_type="exact_id", matched_term=str(exp_id))]

        query_lower = raw_query.lower()
        query_norm = normalize_string(raw_query)

        # 2. Exact Title Match
        for item in self.catalog.experiments:
            if item.title.lower() == query_lower:
                return [SearchResult(item=item, score=100.0, match_type="exact_title", matched_term=item.title)]

        # 3. Exact Alias Match
        for item in self.catalog.experiments:
            for alias in item.aliases:
                if alias.lower() == query_lower:
                    return [SearchResult(item=item, score=100.0, match_type="exact_alias", matched_term=alias)]

        # 4. Normalized Title or Alias Match
        for item in self.catalog.experiments:
            if normalize_string(item.title) == query_norm:
                return [SearchResult(item=item, score=98.0, match_type="normalized_title", matched_term=item.title)]
            for alias in item.aliases:
                if normalize_string(alias) == query_norm:
                    return [SearchResult(item=item, score=98.0, match_type="normalized_alias", matched_term=alias)]

        # 5. Fuzzy Matching using RapidFuzz WRatio and Token Sort
        results: List[SearchResult] = []
        for item in self.catalog.experiments:
            best_score = 0.0
            best_term = item.title
            best_type = "fuzzy_title"

            # Check Title
            title_norm = normalize_string(item.title)
            score_title = fuzz.WRatio(query_norm, title_norm)
            if score_title > best_score:
                best_score = score_title
                best_term = item.title
                best_type = "fuzzy_title"

            # Check Aliases
            for alias in item.aliases:
                alias_norm = normalize_string(alias)
                score_alias = fuzz.WRatio(query_norm, alias_norm)
                if score_alias > best_score:
                    best_score = score_alias
                    best_term = alias
                    best_type = "fuzzy_alias"

            # Check Description keywords with lower weight
            desc_norm = normalize_string(item.description)
            score_desc = fuzz.partial_ratio(query_norm, desc_norm) * 0.85
            if score_desc > best_score:
                best_score = score_desc
                best_term = item.description[:40] + "..."
                best_type = "fuzzy_description"

            if best_score >= threshold:
                results.append(
                    SearchResult(
                        item=item,
                        score=round(best_score, 1),
                        match_type=best_type,
                        matched_term=best_term
                    )
                )

        # Sort matches descending by score
        results.sort(key=lambda r: r.score, reverse=True)
        return results

    def resolve(
        self,
        query: str,
        threshold: float = 55.0,
        ambiguity_gap: float = 8.0
    ) -> Tuple[Optional[CatalogItem], List[SearchResult], bool]:
        """Resolve query to a single experiment or identify ambiguity.

        Returns:
            (selected_item, candidate_matches, is_ambiguous)
        """
        matches = self.search(query, threshold=threshold)
        if not matches:
            return None, [], False

        # If highest score is 100 or >= 95, or only one match returned
        if len(matches) == 1:
            return matches[0].item, matches, False

        top = matches[0]
        second = matches[1]

        # If top match is an exact or near-exact match
        if top.score >= 95.0 and (top.score - second.score >= 5.0):
            return top.item, matches, False

        # If gap between top and second is large enough
        if (top.score - second.score) >= ambiguity_gap:
            return top.item, matches, False

        # Otherwise, matches are too close: Ambiguity!
        # Return candidates so CLI can show interactive selection or prompt
        return None, matches, True

