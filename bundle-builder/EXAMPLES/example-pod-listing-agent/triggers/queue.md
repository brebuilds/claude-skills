# Queue + Rate Limits — Volume Scaling

This agent is on the **volume scaling axis** — same job, many more invocations expected over time (target: ~1000 listings across the OIB.Guide catalog).

## Per-tool rate limits

| Tool | Limit | Behavior |
|---|---|---|
| Airtable MCP | ~5 req/s per base | Batch reads where possible (e.g., load all 27 templates once, not per-invocation). Cache for the duration of a batch run. |
| `brand-oib-guide` skill | Local, no limit | Load once per batch, not per design |
| `etsy-listing-writer` skill | Local, no limit | Same |
| Anthropic API (model calls inside the agent) | Tier-dependent | Most relevant constraint at scale. Use Sonnet-tier model; Haiku is fine for the structural draft, escalate to Sonnet only for tricky brand-voice judgment calls. |

## Batch sizing

- **Single design**: ~30s end-to-end (one Airtable read pass + one model call + write back)
- **Batch of 20**: ~5 minutes if parallel = 4 concurrent agents (limited by Airtable rate, not model)
- **Batch of 100**: ~25 minutes parallel = 4, or 12 minutes parallel = 8 (if you can afford the model cost)

## Failure modes under load

1. **Airtable rate limit hit** → 429 response. Back off 1 second, retry up to 3×. If still failing, pause batch and surface to Bre.
2. **Model API hiccup** → retry once. If still failing, mark the row as `Sync Status = error` with the error message in Notes.
3. **Brand-voice gate fails 3× on same design** → escalate per `brand-vault/boundary.md`. Design's concept may not fit OIB voice cleanly.
4. **Duplicate detection hits** → skip and log. NOT an error.

## Out of scope for this queue layer

- Listing IMAGE generation queue (separate pipeline)
- Publish queue (different rate limits — Printify has its own ceiling, ~1 publish/s safe)
- Order/sale tracking
