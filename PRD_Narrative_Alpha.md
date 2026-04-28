# Product Requirements Document
## Narrative Alpha
### A narrative lifecycle tracker for alpha discovery

- **Author:** Aaron Cai
- **Date:** April 28, 2026
- **Version:** 0.1 — Draft
- **Status:** Internal / Concept Stage

## 1. Problem

### 1.1 Core Insight
Financial markets are driven by narratives. A narrative’s lifecycle—from first emergence in specialist research to mainstream media consensus—is predictable in structure, even if unpredictable in timing. Alpha exists in the early stages of this lifecycle, before the narrative gets priced into large-cap bellwethers. By the time a story appears in WSJ headlines or CNBC panels, the alpha window is largely closed.

### 1.2 The Narrative Lifecycle
Based on observed patterns in how market narratives form and propagate:
1. **Emergence:** An industry expert, sell-side analyst, or sector specialist raises a thesis. It appears in a research note, a conference presentation, or a niche publication. Very few people are paying attention.
2. **Reinforcement:** A second or third credible source picks up the thesis. An investment bank publishes a follow-up. A quality media outlet (FT, Bloomberg) writes an analytical piece. The narrative starts to harden from speculation into framework.
3. **Consensus:** The narrative becomes common knowledge. Multiple banks have coverage. Mainstream media runs features. LinkedIn thought leadership floods in. Social media saturates. The narrative is now fully priced — what was alpha is now beta.

The product exists to make this lifecycle visible and actionable.

### 1.3 What’s Broken Today
- No tool shows narrative progression across sources in a unified view. Investors manually track themes across Bloomberg, sell-side portals, Twitter, and news feeds.
- Information source quality varies enormously (Tier 1 research vs. self-media noise), but most aggregators treat all content equally.
- Narrative strength is felt intuitively but never measured. There is no quantified signal for “how far along is this story.”
- Alpha mapping from narrative to investable targets is done ad hoc in analysts’ heads, never systematized or tracked for validation.

### 1.4 Why Now
- LLMs can now parse, classify, and cluster unstructured text from research notes, earnings calls, and media articles at scale.
- The explosion of AI-generated content makes signal extraction harder for humans but easier for machines — the noise floor is rising, which increases demand for curation.
- MCP and agentic infrastructure allow real-time connection to multiple data feeds without building bespoke integrations for each source.

## 2. Product Vision

### 2.1 One-Liner
Detect narratives before they become consensus. Map alpha targets. Validate with price.

### 2.2 What It Is
Narrative Alpha is a daily digest product that tracks market narratives through their lifecycle—from first emergence in specialist sources to mainstream consensus—and maps each narrative to investable targets whose price action serves as the validation signal.

### 2.3 What It Is Not
- Not a news aggregator. It does not show you articles. It shows you narratives and their progression.
- Not a stock screener. Alpha targets are derived from narrative logic, not quantitative screens.
- Not a trading signal service. It provides narrative intelligence to inform investment thinking, not buy/sell recommendations.
- Not anchored to large caps. Mag7 and other bellwethers serve as stage markers (if they move, the narrative is already consensus), not as the alpha targets themselves.

### 2.4 Core Loop
The user’s daily interaction follows this loop:
1. **Scan:** Open the daily digest. See which narratives are emerging, strengthening, or reaching consensus. Understand what’s new today.
2. **Evaluate:** Drill into an emerging narrative. See the source trail (who said what, when, at what credibility tier). Assess whether the narrative has substance.
3. **Map:** Review the alpha targets mapped to the narrative. Understand the thesis for each target. Decide whether to research further or take a position.
4. **Validate:** Over days/weeks, see whether the mapped targets actually price up. If they do, the narrative call was correct. This builds conviction calibration over time.

## 3. User & Use Cases

### 3.1 Primary User
Sophisticated individual investor or buy-side professional who:
- Reads FT, Bloomberg, WSJ, and sell-side research regularly
- Thinks in narratives and themes, not just tickers
- Has the analytical ability to evaluate a thesis but lacks the time to systematically track narrative progression across dozens of sources
- Wants to find alpha before consensus forms, and wants a system that makes that process repeatable

### 3.2 Key Use Cases
- **UC1 — Morning Scan:** User opens the digest at 7am. Sees that a new narrative (“AI inference cost deflation”) entered the Emerging stage yesterday, sourced from a Bernstein research note. Two existing narratives strengthened overnight. One narrative crossed into Consensus. Total time: 3 minutes.
- **UC2 — Deep Dive on Emerging Narrative:** User taps into the “AI inference cost deflation” narrative. Sees the source trail: Bernstein was first (Tier 1), The Information followed (Tier 2). No Tier 3 social amplification yet. Alpha targets: Credo Tech (connectivity silicon), Arista Networks (east-west traffic). Neither has moved yet. User decides to research CRDO further.
- **UC3 — Validation Review:** User checks the “Japan re-industrialization” narrative they’ve been tracking for 6 weeks. Alpha targets Tokyo Electron (+18%), Shin-Etsu (+9%), Advantest (+12%) have all priced up since the narrative was first flagged. TSM mentioned Japan expansion on their earnings call — the big-cap signal confirms the narrative is approaching consensus. The system worked.
- **UC4 — Noise Filtering:** A viral Twitter thread claims “nuclear energy is dead” based on a single regulatory hearing. The system classifies this as Tier 3 social noise with no Tier 1 or Tier 2 reinforcement. The existing “nuclear renaissance” narrative remains at Strengthening stage with no downgrade. User ignores the noise.

## 4. Information Architecture

### 4.1 Narrative Object Model
Each narrative in the system is a structured object with the following properties:

| Field | Type | Description |
|---|---|---|
| narrative_id | string | Unique identifier |
| title | string | Short narrative label (e.g., “AI Inference Cost Deflation”) |
| subtitle | string | One-sentence thesis summary |
| stage | enum | Emerging \| Strengthening \| Consensus |
| strength_score | 0–100 | Composite score based on source count, tier mix, recency, and cross-source reinforcement |
| first_seen | date | Date of earliest source signal |
| source_trail | array | Ordered list of sources with tier, org, date, and summary |
| alpha_targets | array | Mapped investable targets with ticker, thesis, and price change since mapping |
| big_cap_signal | string | Whether/how large-cap bellwethers have acknowledged the narrative (stage indicator, not alpha target) |
| key_question | string | The critical unresolved question that determines whether the narrative has staying power |

### 4.2 Source Tier System
Sources are classified into three tiers based on credibility and signal value. The tier system is central to the product’s value proposition — it is what separates this from a generic news feed.

| Tier | Source Type | Examples | Signal Value |
|---|---|---|---|
| Tier 1 | Primary Research | Sell-side research notes, company filings, earnings call transcripts, industry expert commentary | Highest. First-mover signal. Narrative origin point. |
| Tier 2 | Quality Media | FT, Bloomberg, WSJ, The Economist, Nikkei, The Information, Barron’s | High. Reinforcement signal. When Tier 2 picks up a Tier 1 thesis, the narrative is strengthening. |
| Tier 3 | Social / Self-Media | FinTwit, LinkedIn, Substack, 小红书, 雪球, Seeking Alpha, Reddit | Saturation signal. When Tier 3 is active, the narrative is approaching or at consensus. Alpha window closing. |

Key principle: Tier 3 activity without Tier 1 origin is noise. Tier 1 activity without Tier 2/3 follow-through is an emerging signal worth watching. The progression from Tier 1 → Tier 2 → Tier 3 is the narrative lifecycle itself.

### 4.3 Strength Score Methodology
The strength score (0–100) is a composite of four factors:
- **Source Count (25%):** Number of distinct sources mentioning the narrative. Diminishing returns after 8+ sources.
- **Tier Mix (30%):** Weighted by tier. Tier 1 sources contribute more than Tier 3. A narrative with 2 Tier 1 sources scores higher than one with 10 Tier 3 sources.
- **Recency Acceleration (25%):** How quickly new sources are appearing. A narrative that gets 3 new mentions this week is strengthening faster than one that got 3 mentions over 2 months.
- **Cross-Source Reinforcement (20%):** Are different sources saying the same thing independently, or are they citing each other? Independent convergence is a stronger signal than citation chains.

Stage thresholds: Emerging (0–35), Strengthening (36–70), Consensus (71–100). These are calibrated over time based on historical narrative outcomes.

## 5. Alpha Mapping & Validation

### 5.1 Alpha Target Identification
For each narrative, the system identifies investable targets through:
1. **Direct mentions:** Companies explicitly named in source materials as beneficiaries of the narrative theme.
2. **Supply chain mapping:** If the narrative is about a downstream trend (e.g., AI inference growth), trace upstream to identify enabling infrastructure (connectivity silicon, networking, power).
3. **Analogy targets:** Companies in adjacent sectors or geographies that have benefited from structurally similar narratives in the past.
4. **Contrarian targets:** Companies that are currently out of favor but would be re-rated if the narrative proves true.

Each alpha target includes a thesis statement explaining the logical connection between the narrative and the target’s potential price action.

### 5.2 Validation Framework
The product’s credibility comes from its validation loop. This is what separates it from opinion.
- When a narrative is first tagged as Emerging, its alpha targets are recorded with their current prices.
- The system tracks price changes of all alpha targets from the date of first mapping.
- If targets price up materially while the narrative progresses from Emerging → Strengthening → Consensus, this is a validated call. The system learns.
- If targets don’t move or move against the thesis, the narrative is flagged for review. Was the mapping wrong, or was the narrative itself wrong?
- Over time, the system builds a track record: hit rate by narrative stage at time of mapping, average alpha captured by stage, and typical time-to-validation.

### 5.3 Big-Cap as Stage Marker (Not Target)
Large-cap bellwethers (Mag7, TSMC, major banks, etc.) serve a specific function: they are lagging indicators of narrative maturity.
- When a Mag7 company mentions the narrative on an earnings call, the narrative has reached mainstream attention.
- When a big-cap stock moves on the narrative, the alpha window for that narrative is effectively closed.
- This is useful information — it tells you when to stop looking for alpha in a particular theme and when to shift to a new emerging narrative.

The big-cap signal is tracked per narrative as a status field, not as an investable recommendation.

## 6. Data Sources & Pipeline

### 6.1 Priority Sources (V1 — English)
| Tier | Source | Access Method | Content Type |
|---|---|---|---|
| Tier 1 | Sell-side research (GS, MS, JPM, Bernstein, etc.) | Research portals / PDF ingestion / partnership | Research notes, sector initiations, thematic pieces |
| Tier 1 | Earnings call transcripts | Seeking Alpha / company IR / FactSet | Management commentary, guidance language |
| Tier 2 | FT, Bloomberg, WSJ, The Information | RSS / API / web scraping | Analysis, features, opinion |
| Tier 2 | Nikkei Asia, Barron’s, The Economist | RSS / API | Regional and sector deep dives |
| Tier 3 | FinTwit, LinkedIn, Substack | API / scraping / social listening tools | Saturation signal, sentiment gauge |

### 6.2 Processing Pipeline
The pipeline runs on a daily batch cadence (with potential for intraday triggers on high-signal events):
1. **Ingest:** Pull new content from all configured sources. Assign source tier automatically based on origin.
2. **Parse & Extract:** LLM-based extraction of key claims, entities (companies, sectors, technologies), and thesis statements from each piece of content.
3. **Cluster:** Group extracted claims into narrative clusters using semantic similarity. New claims either join existing narratives or seed new ones.
4. **Score:** Recalculate strength scores for all active narratives. Detect stage transitions (Emerging → Strengthening, Strengthening → Consensus).
5. **Map:** For new or changed narratives, run alpha target identification. For existing targets, update price validation data.
6. **Generate:** Produce the daily digest with narrative summaries, source trails, alpha targets, and validation status.

### 6.3 The “Underwater” Information Problem
A key challenge: some of the highest-value signals are in sources that are hard to access systematically.
- Sell-side research is behind paywalls and portal logins. Access varies by user.
- Expert network calls and conference notes are often shared informally, not published.
- The most valuable Tier 1 signals may be in a PDF that someone forwarded, not in a public feed.

V1 approach: allow users to manually submit sources (forward a PDF, paste a link, share a screenshot) into the system. These user-contributed sources are processed through the same pipeline and can seed or reinforce narratives. This turns the “underwater” problem into a feature: users who contribute high-quality Tier 1 sources get better narrative detection.

## 7. Daily Digest Format
The digest is the primary output. It must be scannable in under 3 minutes but drillable for depth.

### 7.1 Header
- Date
- Summary counts: N emerging / N strengthening / N consensus / N new today
- One-line highlight: the single most notable narrative development today

### 7.2 Narrative Cards (Ordered by Alpha Opportunity)
Narratives are ordered by alpha opportunity, which means Emerging narratives appear first (highest alpha potential), followed by Strengthening, then Consensus. Within each stage, order by recency of last source activity.

Each card shows:
- Stage badge + lifecycle indicator (visual dots showing progression)
- Title + subtitle (the narrative and its one-line thesis)
- Strength score bar (0–100 with visual)
- Source trail (collapsed by default; expandable to see full source list with tier indicators)
- Alpha targets (ticker, name, thesis, price change since mapping)
- Big-cap signal (current status of large-cap acknowledgment)
- Key question (the critical uncertainty)

### 7.3 Delivery
V1: email digest (HTML) sent at a configurable time.

V2: in-app digest with push notifications for stage transitions and significant price moves on alpha targets.

## 8. Design Principles
1. **Simplicity over completeness.** The digest should have 5–10 active narratives at any time, not 50. Aggressive filtering is a feature.
2. **Source credibility is the product.** The tier system is not a nice-to-have; it is the core value. If we can’t maintain source quality, the product has no moat.
3. **Narratives, not news.** We never show individual articles. We show narrative progression. An article is evidence for a narrative, not content to be consumed.
4. **Validation builds trust.** The system must be honest about its track record. Showing failed narrative calls is as important as showing successful ones.
5. **Alpha targets are hypotheses, not recommendations.** The system maps narratives to potential beneficiaries. It does not give investment advice. The user provides the judgment.
6. **Show your work.** Every narrative stage assessment must be traceable to its source trail. Every alpha target must have a stated thesis. Nothing is a black box.

## 9. MVP Scope & Phasing

### 9.1 V0 — Manual Proof of Concept
Before building anything automated, validate the concept manually:
- Curator (human, likely the author) manually identifies 5–8 narratives per week from their own reading.
- Writes up source trails, alpha targets, and key questions by hand.
- Distributes as a weekly email or document to a small group of trusted readers.
- Collects feedback: Is the narrative framing useful? Are the alpha targets interesting? Is the lifecycle staging accurate?
- Tracks alpha target prices to build initial validation data.

Success criteria for V0: 10+ readers confirm they took an action (researched a target, adjusted a thesis, avoided a noise trap) based on the digest within 4 weeks.

### 9.2 V1 — Semi-Automated Daily Digest
- Automated source ingestion from 5–10 English-language sources (RSS + API).
- LLM-powered narrative extraction and clustering.
- Manual review and curation layer: human editor approves, edits, or rejects LLM-generated narratives before publication.
- Automated alpha target price tracking once targets are mapped.
- Daily email digest with the card format described in Section 7.
- User can submit sources manually (PDF upload, URL paste).

### 9.3 V2 — Fully Automated + Interactive
- Fully automated narrative detection with human-in-the-loop for quality control on edge cases only.
- Interactive web/mobile app with real-time narrative updates.
- Push notifications for stage transitions and alpha target price moves.
- Historical narrative archive with searchable track record.
- Multi-language support (add Chinese sources: 财联社, 万得, 雪球).
- Community layer: users can contribute sources and comment on narrative assessments.

## 10. Risks & Open Questions

### 10.1 Risks
- Data access: Tier 1 research is the highest-value source but the hardest to access programmatically. The product’s value ceiling is limited by the quality of sources it can ingest.
- Narrative subjectivity: What constitutes a “narrative” vs. a “news event” vs. “noise” is inherently subjective. LLM clustering will make mistakes. The human curation layer in V1 is essential.
- Alpha decay: If the product becomes popular, it could reduce the alpha it identifies by accelerating narrative propagation. This is a long-term concern, not an immediate one.
- Confirmation bias: Users may anchor on narratives that confirm their existing views and ignore disconfirming ones. The system should actively surface narratives that challenge popular positions.
- Regulatory: Depending on jurisdiction and framing, mapping narratives to alpha targets could be interpreted as investment advice. Legal review needed before any public launch.

### 10.2 Open Questions
- How many active narratives should the system track simultaneously? Too few misses signals; too many creates noise.
- Should narratives have an expiration or archival logic? What happens to a narrative that stalls at Emerging for 60 days?
- What is the right cadence — daily digest, or should high-signal events trigger intraday alerts?
- Should the alpha target mapping be fully automated or always have a human-in-the-loop? Automated mapping scales but risks lower quality.
- How to handle conflicting narratives (e.g., “AI will drive energy demand up” vs. “AI will optimize energy consumption down”)? Are these separate narratives or two sides of one?
- Business model: subscription? Freemium with depth gated? Part of a larger platform?

## 11. Success Metrics

| Metric | Definition | Target (V1, 6 months) |
|---|---|---|
| Narrative Hit Rate | % of Emerging narratives that progress to Strengthening with alpha targets showing positive price action | >40% of flagged narratives validate within 60 days |
| Alpha Capture | Average price move of alpha targets from date of first mapping to narrative reaching Consensus | >8% average move on validated targets |
| Early Detection | Average days between Narrative Alpha flagging a theme and first mainstream media coverage (WSJ/Bloomberg feature) | >10 days lead time on average |
| Digest Open Rate | % of subscribers who open the daily email | >65% daily open rate |
| Action Rate | % of readers who report researching an alpha target or adjusting a thesis based on the digest | >30% weekly action rate |

---

**End of Document**
