# Brand Vault — Stacks Internal

Read-only reference for the Stacks Inventory Auditor.

## Contents

- `voice.md` — minimal (this agent's output is for internal consumption only)
- `boundary.md` — strict — file-system-touching agents need hard fences

## Why this vault is thin

Internal-ops agents don't need rich brand-voice scaffolding. Output is classification labels, not customer-facing copy. Boundary is where the real weight lives — file system mutations are dangerous.
