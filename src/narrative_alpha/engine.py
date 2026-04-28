from __future__ import annotations

from collections import defaultdict
from datetime import date

from .models import AlphaTarget, Narrative, NarrativeRelationship, SourceItem, Stage


KEYWORDS_TO_NARRATIVE = {
    "inference": "AI Inference Cost Deflation",
    "gpu": "AI Inference Cost Deflation",
    "japan": "Japan Re-industrialization",
    "semiconductor": "Japan Re-industrialization",
    "nuclear": "Nuclear Renaissance",
    "uranium": "Nuclear Renaissance",
    "grid": "AI Power Grid Bottleneck",
    "power": "AI Power Grid Bottleneck",
}

NARRATIVE_SUBTITLES = {
    "AI Inference Cost Deflation": "Falling inference costs shift value to inference infra beneficiaries.",
    "Japan Re-industrialization": "Policy + capex inflection support Japan semicap ecosystem.",
    "Nuclear Renaissance": "Power-demand growth revives nuclear fuel and component demand.",
    "AI Power Grid Bottleneck": "AI load growth is stressing power systems before capacity catches up.",
}

KEY_QUESTIONS = {
    "AI Inference Cost Deflation": "Can lower serving cost translate into durable enterprise demand?",
    "Japan Re-industrialization": "Will the capex cycle persist once subsidies normalize?",
    "Nuclear Renaissance": "Can regulatory reform keep pace with rising power demand?",
    "AI Power Grid Bottleneck": "Will grid upgrade timelines match AI infrastructure deployment speed?",
}

PARENT_MAP = {
    "Japan Re-industrialization": "US-China Tech Decoupling",
}

RELATIONSHIPS = {
    "AI Inference Cost Deflation": [
        NarrativeRelationship("causal", "AI Power Grid Bottleneck", "Lower costs accelerate usage, raising aggregate compute demand."),
    ],
    "AI Power Grid Bottleneck": [
        NarrativeRelationship("contradictory", "AI Energy Optimization", "Demand-overwhelm and optimization narratives can conflict."),
    ],
}

TARGET_RULES = {
    "AI Inference Cost Deflation": [
        ("CRDO", "Credo Technology", "Connectivity silicon demand increases with inference traffic.", "curator", "SMH"),
        ("ANET", "Arista Networks", "East-west traffic growth supports high-performance networking.", "curator", "SMH"),
    ],
    "Japan Re-industrialization": [
        ("8035.T", "Tokyo Electron", "Semicap spending benefits from domestic fab expansion.", "curator", "SMH"),
        ("6857.T", "Advantest", "Test equipment demand rises with advanced-node expansion.", "llm-suggested", "SMH"),
    ],
    "Nuclear Renaissance": [
        ("CCJ", "Cameco", "Fuel cycle leverage to expanding reactor demand.", "community", "XLU"),
        ("BWXT", "BWX Technologies", "Nuclear component specialization benefits from build-out.", "curator", "XLU"),
    ],
    "AI Power Grid Bottleneck": [
        ("VST", "Vistra", "Power generation scarcity premium as demand tightens.", "curator", "XLU"),
        ("CEG", "Constellation Energy", "Nuclear + baseload assets benefit from AI load growth.", "curator", "XLU"),
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


def _signal_quality(items: list[SourceItem]) -> int:
    if not items:
        return 0
    tier1_count = sum(1 for x in items if x.source_tier == 1)
    tier1_score = min(100.0, (tier1_count / 3) * 100)

    unique_sources = len({i.source_name for i in items})
    independence = min(100.0, (unique_sources / len(items)) * 100)

    quantified_tokens = ["%", "x", "gw", "bps", "million", "billion"]
    specificity_hits = sum(
        1
        for i in items
        if any(token in f"{i.headline} {i.summary}".lower() for token in quantified_tokens)
    )
    specificity = min(100.0, (specificity_hits / len(items)) * 100)
    score = tier1_score * 0.50 + independence * 0.30 + specificity * 0.20
    return round(score)


def _propagation_breadth(items: list[SourceItem], as_of: date) -> int:
    if not items:
        return 0
    source_count_score = min(100.0, len(items) / 8 * 100)

    tiers = {i.source_tier for i in items}
    tier_span_score = len(tiers) / 3 * 100

    recent_7d = sum(1 for i in items if (as_of - i.published_on).days <= 7)
    recency_acceleration = min(100.0, recent_7d / 4 * 100)

    score = source_count_score * 0.30 + tier_span_score * 0.40 + recency_acceleration * 0.30
    return round(score)


def stage_from_propagation(score: int) -> Stage:
    if score <= 35:
        return Stage.EMERGING
    if score <= 70:
        return Stage.STRENGTHENING
    return Stage.CONSENSUS


def _price(prices: dict[str, float], ticker: str) -> float:
    return prices.get(ticker, 0.0)


def build_alpha_targets(title: str, latest: dict[str, float], baseline: dict[str, float]) -> list[AlphaTarget]:
    targets: list[AlphaTarget] = []
    for ticker, name, thesis, mapped_by, sector_etf in TARGET_RULES.get(title, []):
        targets.append(
            AlphaTarget(
                ticker=ticker,
                name=name,
                thesis=thesis,
                mapped_by=mapped_by,
                sector_etf=sector_etf,
                mapped_price=_price(baseline, ticker),
                latest_price=_price(latest, ticker),
                mapped_sector_price=_price(baseline, sector_etf),
                latest_sector_price=_price(latest, sector_etf),
                mapped_benchmark_price=_price(baseline, "SPY"),
                latest_benchmark_price=_price(latest, "SPY"),
                mapped_peer_avg_price=_price(baseline, f"{sector_etf}_PEER"),
                latest_peer_avg_price=_price(latest, f"{sector_etf}_PEER"),
            )
        )
    return targets


def bellwether_signal(title: str, items: list[SourceItem]) -> str:
    text = " ".join(f"{i.headline} {i.summary}".lower() for i in items)
    if any(name in text for name in ["microsoft", "nvidia", "tsmc", "apple", "amazon"]):
        return "Bellwether acknowledgment detected"
    if title == "Unclassified":
        return "No bellwether signal"
    return "No bellwether confirmation yet"


def is_tier3_noise(items: list[SourceItem]) -> bool:
    tiers = {i.source_tier for i in items}
    return tiers == {3}


def build_narratives(
    clusters: dict[str, list[SourceItem]],
    as_of: date,
    latest_prices: dict[str, float],
    baseline_prices: dict[str, float],
) -> list[Narrative]:
    narratives: list[Narrative] = []
    for idx, (title, items) in enumerate(clusters.items(), start=1):
        if is_tier3_noise(items):
            continue
        ordered = sorted(items, key=lambda s: s.published_on)
        signal_quality = _signal_quality(ordered)
        propagation = _propagation_breadth(ordered, as_of)
        stage = stage_from_propagation(propagation)

        narratives.append(
            Narrative(
                narrative_id=f"NAR-{idx:03d}",
                title=title,
                subtitle=NARRATIVE_SUBTITLES.get(title, "Unclassified narrative candidate."),
                parent_narrative=PARENT_MAP.get(title),
                relationships=RELATIONSHIPS.get(title, []),
                first_seen=ordered[0].published_on,
                propagation_stage=stage,
                signal_quality=signal_quality,
                propagation_breadth=propagation,
                source_trail=ordered,
                alpha_targets=build_alpha_targets(title, latest_prices, baseline_prices),
                bellwether_signal=bellwether_signal(title, ordered),
                key_question=KEY_QUESTIONS.get(title, "What additional Tier-1 evidence is required?"),
            )
        )

    # order by alpha opportunity: high signal quality + low propagation first
    return sorted(narratives, key=lambda n: (-(n.signal_quality - n.propagation_breadth), -n.signal_quality, n.propagation_breadth))
