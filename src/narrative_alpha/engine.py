from __future__ import annotations

from collections import defaultdict
from datetime import date
from statistics import mean

from .models import AlphaTarget, Narrative, SourceItem, Stage


KEYWORDS_TO_NARRATIVE = {
    "inference": "AI Inference Cost Deflation",
    "gpu": "AI Inference Cost Deflation",
    "japan": "Japan Re-industrialization",
    "semiconductor": "Japan Re-industrialization",
    "nuclear": "Nuclear Renaissance",
    "uranium": "Nuclear Renaissance",
}

NARRATIVE_SUBTITLES = {
    "AI Inference Cost Deflation": "Falling inference costs expand AI deployment economics.",
    "Japan Re-industrialization": "Capital reshoring and policy support are lifting Japan industrial capex.",
    "Nuclear Renaissance": "Policy + power demand are reviving nuclear investment and supply chains.",
}

KEY_QUESTIONS = {
    "AI Inference Cost Deflation": "Will enterprise adoption accelerate faster than model commoditization pressure?",
    "Japan Re-industrialization": "Can policy momentum convert into sustained private capex?",
    "Nuclear Renaissance": "Will permitting reform keep pace with data-center-driven power demand?",
}

TARGET_RULES = {
    "AI Inference Cost Deflation": [
        ("CRDO", "Credo Technology", "Connectivity silicon demand increases with inference traffic."),
        ("ANET", "Arista Networks", "East-west traffic growth supports high-performance networking."),
    ],
    "Japan Re-industrialization": [
        ("8035.T", "Tokyo Electron", "Semicap spending benefits from domestic fab expansion."),
        ("6857.T", "Advantest", "Test equipment demand rises with advanced-node expansion."),
    ],
    "Nuclear Renaissance": [
        ("CCJ", "Cameco", "Fuel cycle leverage to expanding reactor demand."),
        ("BWXT", "BWX Technologies", "Nuclear component specialization benefits from build-out."),
    ],
}


def cluster_sources(items: list[SourceItem]) -> dict[str, list[SourceItem]]:
    clusters: dict[str, list[SourceItem]] = defaultdict(list)
    for item in items:
        haystack = f"{item.headline} {item.summary}".lower()
        matched = None
        for keyword, narrative_name in KEYWORDS_TO_NARRATIVE.items():
            if keyword in haystack:
                matched = narrative_name
                break
        clusters[matched or "Unclassified"].append(item)
    return clusters


def _score_source_count(count: int) -> float:
    capped = min(count, 8)
    return (capped / 8) * 100


def _score_tier_mix(items: list[SourceItem]) -> float:
    if not items:
        return 0.0
    tier_weights = {1: 1.0, 2: 0.65, 3: 0.35}
    weighted = [tier_weights.get(item.source_tier, 0.2) for item in items]
    return mean(weighted) * 100


def _score_recency_acceleration(items: list[SourceItem], as_of: date) -> float:
    if not items:
        return 0.0
    recent_7d = sum(1 for i in items if (as_of - i.published_on).days <= 7)
    return min(100.0, recent_7d / 4 * 100)


def _score_reinforcement(items: list[SourceItem]) -> float:
    if not items:
        return 0.0
    unique_sources = len({i.source_name for i in items})
    citation_chain_penalty = max(0, len(items) - unique_sources)
    base = min(100, unique_sources / 5 * 100)
    return max(0.0, base - citation_chain_penalty * 8)


def compute_strength_score(items: list[SourceItem], as_of: date) -> int:
    source_count = _score_source_count(len(items)) * 0.25
    tier_mix = _score_tier_mix(items) * 0.30
    recency = _score_recency_acceleration(items, as_of) * 0.25
    reinforcement = _score_reinforcement(items) * 0.20
    return round(source_count + tier_mix + recency + reinforcement)


def stage_from_score(score: int) -> Stage:
    if score <= 35:
        return Stage.EMERGING
    if score <= 70:
        return Stage.STRENGTHENING
    return Stage.CONSENSUS


def build_alpha_targets(title: str, price_map: dict[str, float], baseline_map: dict[str, float]) -> list[AlphaTarget]:
    targets: list[AlphaTarget] = []
    for ticker, name, thesis in TARGET_RULES.get(title, []):
        mapped_price = baseline_map.get(ticker, 0.0)
        latest_price = price_map.get(ticker, mapped_price)
        targets.append(
            AlphaTarget(
                ticker=ticker,
                name=name,
                thesis=thesis,
                mapped_price=mapped_price,
                latest_price=latest_price,
            )
        )
    return targets


def big_cap_signal(title: str, items: list[SourceItem]) -> str:
    text = " ".join(f"{i.headline} {i.summary}".lower() for i in items)
    if any(name in text for name in ["microsoft", "nvidia", "tsmc", "apple", "amazon"]):
        return "Large-cap acknowledgment detected"
    if title == "Unclassified":
        return "No big-cap signal"
    return "No large-cap confirmation yet"


def build_narratives(
    clusters: dict[str, list[SourceItem]],
    as_of: date,
    price_map: dict[str, float],
    baseline_map: dict[str, float],
) -> list[Narrative]:
    narratives: list[Narrative] = []
    for idx, (title, items) in enumerate(clusters.items(), start=1):
        ordered = sorted(items, key=lambda s: s.published_on)
        score = compute_strength_score(ordered, as_of)
        stage = stage_from_score(score)
        narrative_title = title
        subtitle = NARRATIVE_SUBTITLES.get(narrative_title, "Signals detected but narrative is not yet classified.")
        narratives.append(
            Narrative(
                narrative_id=f"NAR-{idx:03d}",
                title=narrative_title,
                subtitle=subtitle,
                first_seen=ordered[0].published_on,
                stage=stage,
                strength_score=score,
                source_trail=ordered,
                alpha_targets=build_alpha_targets(narrative_title, price_map, baseline_map),
                big_cap_signal=big_cap_signal(narrative_title, ordered),
                key_question=KEY_QUESTIONS.get(narrative_title, "What additional Tier 1 evidence is required?"),
            )
        )
    stage_rank = {Stage.EMERGING: 0, Stage.STRENGTHENING: 1, Stage.CONSENSUS: 2}
    return sorted(narratives, key=lambda n: (stage_rank[n.stage], n.source_trail[-1].published_on), reverse=False)
