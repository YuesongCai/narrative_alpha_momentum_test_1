from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Stage(str, Enum):
    EMERGING = "Emerging"
    STRENGTHENING = "Strengthening"
    CONSENSUS = "Consensus"


@dataclass(slots=True)
class SourceItem:
    source_id: str
    source_name: str
    source_tier: int
    source_format: str
    published_on: date
    headline: str
    summary: str
    entities: list[str] = field(default_factory=list)


@dataclass(slots=True)
class AlphaTarget:
    ticker: str
    name: str
    thesis: str
    mapped_by: str
    sector_etf: str
    mapped_price: float
    latest_price: float
    mapped_sector_price: float
    latest_sector_price: float
    mapped_benchmark_price: float
    latest_benchmark_price: float
    mapped_peer_avg_price: float
    latest_peer_avg_price: float

    @staticmethod
    def _pct_change(start: float, end: float) -> float:
        if start == 0:
            return 0.0
        return (end - start) / start * 100

    @property
    def absolute_return(self) -> float:
        return self._pct_change(self.mapped_price, self.latest_price)

    @property
    def sector_return(self) -> float:
        return self._pct_change(self.mapped_sector_price, self.latest_sector_price)

    @property
    def benchmark_return(self) -> float:
        return self._pct_change(self.mapped_benchmark_price, self.latest_benchmark_price)

    @property
    def base_rate_return(self) -> float:
        return self._pct_change(self.mapped_peer_avg_price, self.latest_peer_avg_price)

    @property
    def sector_relative_return(self) -> float:
        return self.absolute_return - self.sector_return

    @property
    def benchmark_relative_return(self) -> float:
        return self.absolute_return - self.benchmark_return

    @property
    def validated(self) -> bool:
        return self.sector_relative_return > 5.0


@dataclass(slots=True)
class NarrativeRelationship:
    relation_type: str  # causal | contradictory | parent-child
    target_narrative: str
    note: str


@dataclass(slots=True)
class Narrative:
    narrative_id: str
    title: str
    subtitle: str
    parent_narrative: str | None
    relationships: list[NarrativeRelationship]
    first_seen: date
    propagation_stage: Stage
    signal_quality: int
    propagation_breadth: int
    source_trail: list[SourceItem]
    alpha_targets: list[AlphaTarget]
    bellwether_signal: str
    key_question: str
