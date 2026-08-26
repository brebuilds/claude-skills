---
name: bundle-builder
description: Interactive wizard for designing agent bundles using the 5-question architecture (Identity, Routing, Capability, Memory, Boundary + scaling axis). Supports both single-agent bundles and multi-specialist systems (orchestrator + narrow specialists with explicit handoff contracts). Asks one question at a time, pushes back on vague answers, generates complete folder structures with starter markdown. Use when starting any new agent or multi-stage automation for a client or internal system.
---

# bundle-builder

Interactive wizard. Walks a scoped interview, then scaffolds either a single agent or a full multi-specialist system.

## When to invoke

Triggers:
- "build me a bundle for X"
- "scaffold an agent for X"
- "I need to design an automation for X"
- "let's architect [client name]'s system"
- "/bundle" slash command

## How to run

1. Read this file
2. Open `WIZARD.md` and follow it turn-by-turn
3. After all turns + recap confirmation, generate the bundle(s) at the destination Bre specifies
4. Stop. Let Bre run it for 1-2 real sessions before iterating.

## Files in this skill

| File          | Purpose |
|---------------|---------|
| `SKILL.md`    | This file — overview + triggers |
| `WIZARD.md`   | The interview script — branching single vs multi-specialist + 5-Q per specialist |
| `TEMPLATES/`  | Starter markdown the wizard copies + fills in (single + system + specialist variants) |
| `EXAMPLES/`   | Reference bundles (single-agent and multi-specialist) |

## Behavior rules — do NOT skip

- One question per turn. Wait for answer. Sub-questions on the same topic OK in the same turn.
- Push back on vague answers. Restate the question. Do not accept "I don't know."
- If user is stuck, offer 2-3 example answers. Never more.
- Never invent capability the user didn't list.
- Functional names only. No cute names. No "AgentBot 3000."
- End generation with the literal sentence: "Use this in 1-2 real sessions, then come back and tell me what's missing."
- When the flow is multi-specialist, every specialist also receives the full 5-Q structure + a handoff contract.