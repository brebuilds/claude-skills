# OIB.Guide Listing Drafter — Tools

Three load-bearing tools. Anything beyond these three is scope creep.

## Tools

| Tool | Status | What it does |
|---|---|---|
| `airtable-mcp.md` | exists | Read Design row + Listing Template + Brand + Product Type; write the draft Listing row (or stage in memory until publish) |
| `brand-oib-guide-skill.md` | exists (stale — needs refresh) | Voice anchor + banned-vocab gate |
| `etsy-listing-writer-skill.md` | exists | Structure: title formula, 13 tags strategy, 6-section description, attributes |

## What we DON'T use here

- **Printify MCP** — this agent doesn't talk to Printify directly. `/api/publish` does. Keeping the boundary clean.
- **Mockup tools** (mockup-composer, PSD service) — listing IMAGES are a separate agent's problem. This agent owns COPY only.
- **Performance/analytics tools** — that's the Recommender Bot's job (project #42), not the drafter's.

## Tool sequencing

In every generation:
1. Airtable MCP → fetch Design + Brand + Template + Product Type
2. brand-oib-guide skill → load voice + banned vocab into context
3. etsy-listing-writer skill → generate title + tags + description structure
4. Self-check: banned-vocab gate (regenerate if hit)
5. Airtable MCP → write draft Listing row (or return as JSON to caller)
