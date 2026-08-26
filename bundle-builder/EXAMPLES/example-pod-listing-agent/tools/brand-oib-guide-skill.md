# Tool — brand-oib-guide skill

## Status
Exists at `~/.claude/skills/brand-oib-guide/SKILL.md`. **STALE** per gap report 4.1 — last updated 2026-03-08, has TODO placeholders for Etsy/Printify/Airtable IDs that are now real. **Refresh before relying on it in production.**

## What this agent uses it for

Voice anchor + banned-vocab gate. Loaded into context before every generation step.

## What the skill provides

- OIB.Guide brand voice spec (tone, audience, locality)
- Banned vocabulary list (the tourism-board cliché set)
- Example listings that hit the mark (positive examples)
- Pricing intent baseline per product type (separate from Pricing Rules table)
- Locality knowledge: Brunswick County towns, landmarks, in-jokes

## Cross-reference

A trimmed extract of this skill is duplicated in `brand-vault/voice.md` for this specific bundle. If they disagree, the skill at `~/.claude/skills/brand-oib-guide/` wins — update the vault.

## Refresh prerequisites (gap 4.1)

Before this skill is fully trusted at scale:
1. Backfill real Etsy Shop ID, Printify Shop ID, Airtable Base ID
2. Pull voice examples from existing successful TFH listings + apply OIB-localization
3. Add the banned-vocabulary list explicitly (currently scattered in comments)
4. Note the OIB vs Outer Banks distinction (frequent confusion)
