# Brightside Inquiry Handler — Memory

## Per-conversation state
**Yes — thread context per caller.**

When a caller has multiple turns in one session (or calls back referencing a prior inquiry), the agent reads prior turns for coherence. Storage: per-call session ID, scoped to that session only.

## Per-entity state (per-patient)
**Light — repeat-caller recognition only.**

If a caller's phone number / email matches a prior inquiry, the agent surfaces the prior topic in context. Does NOT store detailed history — that's the practice's own patient-records system's job.

## Global learning
**None at this layer.**

Pattern recognition (which inquiries become common, which need new knowledge base entries) happens out-of-band, via separate review. The agent itself stays stateless across global runs.

## What lives where

| State | Lives in | Survives between runs? |
|---|---|---|
| Current inquiry text + classification | Agent invocation | No |
| Multi-turn thread within one session | Session store | Until session ends |
| Repeat-caller flag | Caller lookup table per location | Yes |
| Knowledge base | External (per location) | Yes |
| Escalation map | Per-location tool config | Yes |
