from datetime import date
from pathlib import Path

from src.narrative_alpha.pipeline import run_pipeline


def test_run_pipeline_generates_digest_with_revised_metrics(tmp_path: Path):
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
    assert "Signal Quality" in text
    assert "Propagation Breadth" in text
    assert "Sector-Rel" in text
    assert len(narratives) >= 4
    assert any(n.title == "AI Power Grid Bottleneck" for n in narratives)


def test_noise_rejection_filters_tier3_only_narratives(tmp_path: Path):
    out = tmp_path / "digest.md"
    run_pipeline(
        source_json=Path("data/sources.json"),
        baseline_price_csv=Path("data/baseline_prices.csv"),
        latest_price_csv=Path("data/latest_prices.csv"),
        output_markdown=out,
        as_of=date(2026, 4, 28),
    )
    text = out.read_text()
    assert "Meme battery moonshot narrative" not in text
