# Stacks Inventory Auditor — Memory

## Per-conversation state
**None.** Each invocation is one file or one batch; no thread context.

## Per-entity state (per-file)
**Yes — keyed by content hash.**

Before classifying, check the Inventory table for an existing row with the same content hash:
- If yes + classification not stale → skip (already done)
- If yes + classification stale (>30 days or marked `needs-review`) → reclassify
- If no → classify + write new row

This prevents re-classifying the same file every nightly sweep. Files don't change content; new uploads get new hashes.

## Global learning
**YES — sophistication scaling axis.**

See `feedback-loop.md`. The classifier's accuracy improves over time as Bre (or a reviewer) verifies/corrects classifications. Verified-correct + verified-incorrect feed back as training context for the classifier prompt or rules.

## What lives where

| State | Lives in | Survives between runs? |
|---|---|---|
| Current file metadata | Agent invocation | No |
| Per-file classification | Stacks Inventory table | Yes |
| Content hash → classification cache | Stacks Inventory table | Yes |
| Verified-correct examples | Feedback loop (see `feedback-loop.md`) | Yes — drives improvement |
| Classifier prompt / rules | `tools/classifier.md` (versioned) | Yes |
