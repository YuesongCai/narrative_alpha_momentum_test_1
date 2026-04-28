# Narrative Alpha (Prototype)

This repository implements a runnable Narrative Alpha prototype aligned with the v0.2 PRD refinements.

## What changed in the refined product
- Replaced single score with **two-dimensional scoring**:
  - `signal_quality` (credibility)
  - `propagation_breadth` (distribution across tiers)
- Lifecycle stage now derives from propagation breadth (Emerging/Strengthening/Consensus).
- Validation now includes **relative performance**:
  - absolute return
  - sector-relative return (primary)
  - benchmark-relative return (SPY)
  - base-rate control (same-sector peer basket)
- Added narrative relationships (`causal`, `contradictory`, `parent-child`) and optional parent narratives.
- Added source format support (`pdf`, `article`, `social`, `audio`) for multi-format ingestion.
- Added Tier-3-only narrative noise filter.

## Quickstart
```bash
python main.py --as-of 2026-04-28
cat output/digest.md
```

## Run tests
```bash
python -m pytest -q
```

## Main files
- `src/narrative_alpha/models.py`: revised domain model
- `src/narrative_alpha/engine.py`: clustering, 2D scoring, stage logic, mapping, relationships, noise filter
- `src/narrative_alpha/pipeline.py`: orchestration + digest rendering
- `data/`: sample multi-format source and price inputs
- `tests/test_pipeline.py`: regression tests for revised logic
- `PRD_Narrative_Alpha.md`: initial v0.1 PRD
