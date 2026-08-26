# Brightside Inquiry Handler

**Built:** 2026-05-26
**Why this exists:** Brightside Dental Group's Riverside office is its live, established location (per `project_brightside_voice_ai`). Two newly-opened locations (Northgate, Harborview) share the same intake architecture ahead of their own launch. Three locations of the same job → variation scaling axis.
**Scaling axis:** Variation — same job (classify + route inquiry) across multiple business contexts. Build for parameterization.
**Status:** scaffolded (structural example) — needs real source paths, tool names, and per-location knowledge bases filled in before any real run.

## What this agent does

Classifies an inbound patient inquiry by type (appointment / billing / dental question / general info / complaint) and routes to the appropriate response path or human handoff.

Single job: classify customer inquiries.

## Locations

- `brand-vault/riverside/` — Riverside (Brightside's original, live location)
- `brand-vault/northgate/` — Northgate (pre-launch)
- `brand-vault/harborview/` — Harborview (pre-launch)

Each location has its own voice + boundary subfolder; the agent reads `brand-vault/<location>/` based on the incoming inquiry's identifier.

## Try it

(After filling in real specifics:)
1. Open `CLAUDE.md`
2. Simulate an inquiry: text + location identifier
3. Verify the classification + route is right per the location's policy
4. Note what's missing or wrong

## Builder notes

(Empty — fill in after first sessions.)

This is a structural example. The shape works; the content placeholders need real fill-in from the wizard run.
