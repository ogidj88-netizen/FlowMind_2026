# FlowMind — Topic Intelligence Lite v1

## Role
Topic Intelligence Lite is a pre-production intelligence filter.
Its purpose is to reduce weak topic selection before production starts.

It does NOT:
- generate videos
- write scripts
- predict guaranteed virality
- replace human approval

It DOES:
- collect market signals
- cluster and score topic candidates
- reject weak topics
- output a production-ready topic queue

## Architecture
Collector
→ Analyzer
→ Validator
→ Topic Packet Generator
→ Topic Queue

## Data Sources (Whitelist v1)

Core sources:
1. Google Trends
2. YouTube market check
3. Reddit pain support

Optional later:
- Google Ads Keyword Planner
- YouTube Suggest
- News/RSS

Rule:
Core v1 must work without optional sources.

## Source Roles

### Google Trends
- rising queries
- related queries
- demand direction
- trend strength

### YouTube market check
- freshness of top competing videos
- market saturation
- evidence of current content coverage

### Reddit pain support
- repeated user pain
- real-world phrasing of problems
- emotional intensity around topic

## Module Responsibilities

### Collector
- gathers raw signals from approved sources
- stores normalized source records

### Analyzer (LLM)
- deduplicates similar inputs
- clusters related signals into topic candidates
- extracts pain points
- classifies topic type
- does NOT invent topics without source signals

### Validator
- scores each topic candidate
- applies veto rules
- applies self-competition check
- decides verdict

### Topic Packet Generator
- converts approved topic candidates into production-ready packets

## Topic Types
Each topic must be classified as one of:
- EVERGREEN
- NEWS
- PROBLEM
- OPPORTUNITY
- WARNING

Purpose:
Different topic types have different value, urgency, and shelf-life.

## Process Flow
Seed Keywords
→ Google Trends expansion
→ candidate queries/signals
→ YouTube market check
→ Reddit pain scan
→ Analyzer clustering + pain extraction + topic type classification
→ Validator scoring + vetoes
→ Topic Packet generation
→ Topic Queue

## Topic Packet Output
Each approved topic must produce:
1. Topic Title
2. Topic Type
3. Why Now
4. Search Signal Summary
5. Pain Point Summary
6. Market Gap Summary
7. Production Fit
8. Monetization Safety
9. Human Usefulness
10. Priority Score
11. Recommended Angle
12. Verdict

## Scoring Model
Maximum score: 30

### A. Search Demand (0–7)
- is there real demand?
- is interest rising or stable?
- are there strong related queries?

### B. Pain Intensity (0–5)
- do people show real confusion, loss, fear, or urgency?
- is the pain repeated?

### C. Market Gap (0–5)
- is the topic under-covered or covered with outdated content?
- is it not overheated right now?

### D. Production Fit (0–4)
- can FlowMind produce this well with current pipeline quality?

### E. Monetization Safety (0–3)
- does the topic avoid unsafe monetization or policy risk?

### F. Human Usefulness (0–5)
- does this topic genuinely help the viewer?
- does it provide actionable clarity, not empty intrigue?

### G. Self-Competition Penalty (-0 to -5)
- if the channel already covered a very similar topic recently,
  reduce score or reject

## Signal Quality Filter
Each candidate signal set must be classified as:
- STRONG
- MEDIUM
- WEAK

### STRONG
- search signal exists
- pain signal exists
- market is not overheated

### MEDIUM
- only 1–2 of the above are present

### WEAK
- weak, noisy, or contradictory signal set

Rule:
WEAK topics do not enter production.

## Hard Kill Rules
Immediate reject if any of the following is true:
1. Search demand is absent or near-zero
2. Topic is overheated by fresh competitor coverage
3. Topic is strongly monetization-risky
4. Topic has weak production fit
5. Topic has no clear human usefulness
6. Topic duplicates recent own-channel content too closely
7. Signal quality is WEAK

## Own-Content Duplication Rule
Before approval, every topic must be checked against recent channel history.

If a closely similar topic was already published recently:
- reject
or
- apply strong penalty

Purpose:
Prevent channel cannibalization and repetitive content cycles.

## Output Contract
The module outputs only:
- Top 10 Topic Packets
- Top 5 shortlist
- Top 3 priority topics
- Kill List
- Topic Queue

It does NOT output:
- raw dumps for manual reading
- unscored idea lists
- vague “interesting trends”

## Placement in FlowMind
[Topic Intelligence Lite]
        ↓
[Topic Queue]
        ↓
[Pre-Production Gate]
        ↓
[FlowMind Production]
        ↓
[QA]
        ↓
[Telegram Approval]
        ↓
[Upload]

## MVP Boundary
v1 does NOT include:
- virality prediction engine
- forecasting system
- sentiment analysis
- conflict detection
- complex news intelligence
- full keyword ecosystem crawling
- automatic final decision without human approval

## Final Principle
Topic Intelligence Lite v1 is not a trend oracle.
It is a disciplined, search-first filtering system
that reduces weak topic selection before production begins.
