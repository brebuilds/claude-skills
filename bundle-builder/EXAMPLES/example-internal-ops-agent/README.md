# Stacks Inventory Auditor

**Built:** 2026-05-26
**Why this exists:** Stacks is Bre's POD ops library layer (vs `pod-dashboard` which is the cockpit). The inventory is currently chaotic — files scattered across Drive / Dropbox / local. An auditor agent that walks, classifies, and tags lets every downstream pipeline (POD Listing Drafter, Recommender Bot, batch publish) operate on clean inputs.
**Scaling axis:** Sophistication — same volume, but classification needs to get SMARTER over time as Bre adds new brands, new product types, new edge cases. Build for feedback loops + leave the seam open.
**Status:** scaffolded (structural example) — needs real source paths, classifier definition, and feedback-loop wiring before any real run.

## What this agent does

Walks the design-file inventory, classifies each file (file type, brand hint, readiness state, recommended next step), and writes the classification back to the Stacks Airtable Inventory table.

Single job: audit and tag uncategorized inventory files.

## Sophistication-axis specifics

This agent is built to get smarter over time. See `memory/feedback-loop.md` for the stub of:
- How classifications get verified (human review)
- How verified-correct + verified-incorrect feed back into the classifier
- Where the smarter-over-time learning lives (separate from per-run state)

## Try it

(After filling in real specifics:)
1. Open `CLAUDE.md`
2. Point at a real source folder (e.g., one Drive subfolder)
3. Run the pipeline on a small sample (10-20 files)
4. Verify classifications are sensible
5. Surface what's wrong, feed back into the feedback loop

## Builder notes

(Empty — fill in after first sessions.)

Likely first surprises:
- Classifier accuracy starts mediocre, improves with feedback (this is the sophistication axis paying off)
- File-walker discovers more sources than expected (Bre's "stragglers" rarely stay where they're filed)
- Brand-hint detection from filename alone is fragile; visual content classification more reliable but more expensive
