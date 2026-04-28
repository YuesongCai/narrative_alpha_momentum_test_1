from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from src.narrative_alpha.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Narrative Alpha daily digest pipeline")
    parser.add_argument("--sources", default="data/sources.json", type=Path)
    parser.add_argument("--baseline-prices", default="data/baseline_prices.csv", type=Path)
    parser.add_argument("--latest-prices", default="data/latest_prices.csv", type=Path)
    parser.add_argument("--out", default="output/digest.md", type=Path)
    parser.add_argument("--as-of", default=None, help="YYYY-MM-DD")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    args.out.parent.mkdir(parents=True, exist_ok=True)
    narratives = run_pipeline(
        source_json=args.sources,
        baseline_price_csv=args.baseline_prices,
        latest_price_csv=args.latest_prices,
        output_markdown=args.out,
        as_of=as_of,
    )
    print(f"Generated digest with {len(narratives)} narratives -> {args.out}")


if __name__ == "__main__":
    main()
