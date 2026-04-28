# Narrative Alpha (Prototype)

This repository now contains a runnable implementation of the Narrative Alpha concept (not only a PRD).

## What is implemented
- Source ingestion from JSON (`data/sources.json`)
- Tier-aware narrative clustering (`src/narrative_alpha/engine.py`)
- Strength score calculation using the PRD weightings (source count, tier mix, recency acceleration, cross-source reinforcement)
- Stage classification (`Emerging`, `Strengthening`, `Consensus`)
- Alpha target mapping with thesis + price validation from baseline vs latest prices
- Daily digest generation to Markdown (`output/digest.md`)
- CLI entrypoint: `main.py`

## Quickstart
```bash
python main.py --as-of 2026-04-28
cat output/digest.md
```

## Run tests
```bash
python -m pytest -q
```

## Files
- `src/narrative_alpha/models.py`: domain objects
- `src/narrative_alpha/engine.py`: clustering, scoring, stage, mapping logic
- `src/narrative_alpha/pipeline.py`: orchestration + digest renderer
- `data/`: sample input dataset + prices
- `tests/test_pipeline.py`: pipeline regression test
- `PRD_Narrative_Alpha.md`: original PRD
