from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

from .engine import build_narratives, cluster_sources
from .models import Narrative, SourceItem


def load_sources(path: Path) -> list[SourceItem]:
    data = json.loads(path.read_text())
    items: list[SourceItem] = []
    for row in data:
        items.append(
            SourceItem(
                source_id=row["source_id"],
                source_name=row["source_name"],
                source_tier=int(row["source_tier"]),
                published_on=date.fromisoformat(row["published_on"]),
                headline=row["headline"],
                summary=row["summary"],
                entities=row.get("entities", []),
            )
        )
    return items


def load_price_csv(path: Path) -> dict[str, float]:
    prices: dict[str, float] = {}
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices[row["ticker"]] = float(row["price"])
    return prices


def render_markdown_digest(narratives: list[Narrative], as_of: date) -> str:
    emerging = sum(1 for n in narratives if n.stage.value == "Emerging")
    strengthening = sum(1 for n in narratives if n.stage.value == "Strengthening")
    consensus = sum(1 for n in narratives if n.stage.value == "Consensus")

    lines = [
        f"# Narrative Alpha Digest — {as_of.isoformat()}",
        "",
        f"**Summary:** {emerging} emerging / {strengthening} strengthening / {consensus} consensus / {len(narratives)} total",
        "",
    ]

    for nar in narratives:
        lines.extend(
            [
                f"## [{nar.stage.value}] {nar.title}",
                f"- **Subtitle:** {nar.subtitle}",
                f"- **Strength Score:** {nar.strength_score}/100",
                f"- **First Seen:** {nar.first_seen.isoformat()}",
                f"- **Big-Cap Signal:** {nar.big_cap_signal}",
                f"- **Key Question:** {nar.key_question}",
                "- **Source Trail:**",
            ]
        )
        for s in nar.source_trail:
            lines.append(f"  - (Tier {s.source_tier}) {s.published_on.isoformat()} — {s.source_name}: {s.headline}")

        if nar.alpha_targets:
            lines.append("- **Alpha Targets:**")
            for t in nar.alpha_targets:
                lines.append(
                    f"  - {t.ticker} ({t.name}) | Thesis: {t.thesis} | Move since mapping: {t.pct_change:.2f}%"
                )
        else:
            lines.append("- **Alpha Targets:** none yet")

        lines.append("")

    return "\n".join(lines)


def run_pipeline(
    source_json: Path,
    baseline_price_csv: Path,
    latest_price_csv: Path,
    output_markdown: Path,
    as_of: date | None = None,
) -> list[Narrative]:
    run_date = as_of or date.today()
    sources = load_sources(source_json)
    baseline_prices = load_price_csv(baseline_price_csv)
    latest_prices = load_price_csv(latest_price_csv)

    clusters = cluster_sources(sources)
    narratives = build_narratives(clusters, run_date, latest_prices, baseline_prices)
    digest = render_markdown_digest(narratives, run_date)
    output_markdown.write_text(digest)
    return narratives
