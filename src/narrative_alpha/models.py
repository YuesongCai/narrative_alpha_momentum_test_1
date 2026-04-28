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
    published_on: date
    headline: str
    summary: str
    entities: list[str] = field(default_factory=list)


@dataclass(slots=True)
class AlphaTarget:
    ticker: str
    name: str
    thesis: str
    mapped_price: float
    latest_price: float

    @property
    def pct_change(self) -> float:
        if self.mapped_price == 0:
            return 0.0
        return (self.latest_price - self.mapped_price) / self.mapped_price * 100


@dataclass(slots=True)
class Narrative:
    narrative_id: str
    title: str
    subtitle: str
    first_seen: date
    stage: Stage
    strength_score: int
    source_trail: list[SourceItem]
    alpha_targets: list[AlphaTarget]
    big_cap_signal: str
    key_question: str
