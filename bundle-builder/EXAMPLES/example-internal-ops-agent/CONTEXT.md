# Stacks Inventory Auditor — Routing

## Source of truth

(Structural placeholders — wizard fills in real paths.)

1. `[Drive folder paths — e.g. oib_guide, tfh, fl, dnc folders]`
2. `[Dropbox stragglers — TBD]`
3. `[local: ~/Desktop/_to-triage/, project subfolders]`
4. `~/stackspod/` (Stacks codebase + config)
5. `[Stacks Airtable base — TBD]` (Inventory table for write-back)

## Scattered or duplicated — cleanup flags

- Files duplicated across Drive + local + Dropbox — classification should de-dup by content hash
- Brand routing inconsistent across folders (some labeled, some not)

## Missing — setup work

- Classifier model / rules — TBD (could be LLM-based with brand context, or rule-based with extensions)
- Per-source enumeration tools — Drive API works, Dropbox needs setup
- Feedback loop write target — see `memory/feedback-loop.md`

## Sub-routes

- `brand-vault/` — voice + boundary (read-only)
- `tools/` — three load-bearing (file walker, classifier, Airtable writer)
- `memory/` — per-file state + feedback loop (sophistication axis)
- `pipeline/` — sequenced stages (walk → classify → write back)
