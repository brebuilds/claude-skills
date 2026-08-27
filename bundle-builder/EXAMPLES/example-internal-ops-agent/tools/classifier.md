# Tool — Classifier

## Status
Needs build.

## What this agent uses it for
Given a file (metadata + preview), output classification:
- `type`: design / mockup / source-photo / template / mystery / etc.
- `brand`: oib-guide / tfh / fl / dnc / coastly / unknown
- `readiness`: ready / needs-mockup / needs-resize / needs-review / unusable
- `confidence`: 0.0 - 1.0

## Approach options (decide during real build)
- **LLM with retrieval** over brand voice + design exemplars → flexible, learns from feedback loop
- **Rule-based** (filename patterns + folder context) → faster, less flexible
- **Hybrid** → rule-based first pass, LLM for low-confidence cases

Recommended starting point: **hybrid.** Rules catch the easy 60-70%; LLM handles the rest. Sophistication axis means the LLM portion gets smarter over time via `memory/feedback-loop.md`.

## Output schema
```json
{
  "type": "string",
  "brand": "string",
  "readiness": "string",
  "confidence": 0.0,
  "reasoning": "string"
}
```
