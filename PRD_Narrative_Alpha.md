# Product Requirements Document
## Narrative Alpha
### Detect narratives before consensus. Map alpha. Validate with price.

- **Author:** Aaron Yu
- **Date:** April 28, 2026
- **Version:** 0.2 — Post Self-Critique
- **Status:** Internal / Concept Stage

## Key Changes from v0.1
1. Replace single strength score with two dimensions:
   - `signal_quality` (credibility)
   - `propagation_breadth` (distribution)
2. Separate responsibilities:
   - Narrative detection: automated + human review
   - Alpha mapping: human-first (LLM-assisted suggestions)
3. Validation now based on relative performance:
   - absolute return
   - sector-relative return (primary)
   - benchmark-relative return
   - base-rate control
4. Add narrative hierarchy + relationships:
   - parent-child
   - causal
   - contradictory
5. Add cadence strategy:
   - daily scan
   - weekly deep brief
   - event-triggered alerts
6. Add multi-format ingestion:
   - PDF, screenshot/OCR, audio transcript, URL, free text

## Information Architecture (v0.2)
- `narrative_id`
- `title`
- `subtitle`
- `parent_narrative`
- `relationships[]`
- `propagation_stage` (Emerging/Strengthening/Consensus)
- `signal_quality` (0–100)
- `propagation_breadth` (0–100)
- `first_seen`
- `source_trail[]` (with `source_format`)
- `alpha_targets[]` (with absolute/relative validation metrics)
- `bellwether_signal`
- `key_question`
- `mapped_by` (curator/community/llm-suggested)

## Scoring (v0.2)
### Signal Quality (0–100)
- Tier-1 density: 50%
- Source independence: 30%
- Claim specificity: 20%

### Propagation Breadth (0–100)
- Source count: 30%
- Tier span: 40%
- Recency acceleration: 30%

### Stage Determination
- Emerging: 0–35
- Strengthening: 36–70
- Consensus: 71–100

## Validation (v0.2)
A target is considered validated only when sector-relative outperformance exceeds +5% over observation window.

## V1 Product Scope
- Semi-automated narrative detection with human curation
- Human-first alpha mapping attribution
- Multi-format source contribution
- Daily scan + weekly deep brief + event alerts
- Public validation scorecard

---

This v0.2 PRD is now reflected in the implementation under `src/narrative_alpha/`.
