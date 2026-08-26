# Brightside Inquiry Handler — Routing

## Source of truth

(Structural placeholders — wizard fills in real paths.)

1. `[client project folder, e.g. ~/clients/brightside-dental/]`
2. `[Vapi voice AI config — endpoint + assistant ID]`
3. `[knowledge base — likely Airtable or Notion, TBD per location]`
4. `[escalation contact map — who handles what type of inquiry]`
5. `~/claude-memory/2-clients/brightside-dental/` (when populated)

## Scattered or duplicated — cleanup flags

- Three locations (Riverside / Northgate / Harborview) each have their own config; risk of policy drift between locations. Brand-vault's location subfolders enforce per-location explicitness.

## Missing — setup work

- Per-location knowledge bases not yet structured for agent consumption (placeholder).
- Escalation contact map not yet defined (placeholder).

## Sub-routes

- `brand-vault/` — voice + boundary (with one subfolder per location — variation scaling axis)
- `tools/` — three load-bearing tools (communication channel, knowledge base, escalation)
- `memory/` — per-patient thread state
- `triggers/` — event-driven per inquiry
