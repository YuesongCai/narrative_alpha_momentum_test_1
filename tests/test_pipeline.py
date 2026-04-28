from datetime import date
from pathlib import Path

from src.narrative_alpha.pipeline import run_pipeline


def test_run_pipeline_generates_digest(tmp_path: Path):
    out = tmp_path / "digest.md"
    narratives = run_pipeline(
        source_json=Path("data/sources.json"),
        baseline_price_csv=Path("data/baseline_prices.csv"),
        latest_price_csv=Path("data/latest_prices.csv"),
        output_markdown=out,
        as_of=date(2026, 4, 28),
    )
    assert out.exists()
    text = out.read_text()
    assert "Narrative Alpha Digest" in text
    assert len(narratives) >= 3
    assert any(n.title == "AI Inference Cost Deflation" for n in narratives)
