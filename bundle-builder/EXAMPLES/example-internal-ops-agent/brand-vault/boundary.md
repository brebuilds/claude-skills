# Stacks Inventory Auditor — Boundary

## NEVER do

1. **Never MOVE files.** Read-only access to source folders. If reorganization is needed, that's a separate pipeline with explicit approval.
2. **Never DELETE files.** Even if classification says "duplicate" or "unusable." Surface the recommendation; never act.
3. **Never touch files marked Locked.** Files with a `.locked` sidecar or in a folder named `_locked/` are off-limits — don't read content, don't classify, just skip.

## Flag to human

- Classification confidence below 0.5 → flag for human review queue, don't auto-tag.
- File appears in a brand folder but content doesn't match brand voice (e.g., a TFH design in the OIB folder) → flag.
- File matches a known suspicious pattern (executable, archive over N GB, unknown filetype) → flag + skip.
- Repeated classification failures on same file (>3 attempts) → flag, mark as `requires-manual-review`.

## Why these are hard

File-system mutations are the single most dangerous thing an internal agent can do. The auditor stays strictly read-only by design. Any tool that wants to move/delete/restructure is a separate agent, with its own bundle and its own boundary.
