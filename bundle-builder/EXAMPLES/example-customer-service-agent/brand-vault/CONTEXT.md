# Brand Vault — Multi-variant

Read-only reference for the Brightside Inquiry Handler.

## Contents

- `voice.md` — shared voice baseline across all 3 locations
- `boundary.md` — shared hard nos across all locations (healthcare baseline)
- `riverside/` — Riverside-specific voice + boundary
- `northgate/` — Northgate-specific
- `harborview/` — Harborview-specific

## Variation axis structure

This bundle is on the **variation scaling axis**: same job, multiple flavors. Each location gets its own subfolder. The agent reads the shared root files PLUS the location-specific files based on the incoming inquiry's identifier.

## Read order

1. Root `voice.md` + `boundary.md` (shared baseline)
2. `<location>/CONTEXT.md` for the routing into that location's specifics
3. `<location>/voice.md` + `<location>/boundary.md` (location overrides)

Location-specific files OVERRIDE the root when they conflict.
