# bundle-builder Wizard Script

Follow this script turn-by-turn. **One topic per turn.** Wait for the user's answer before advancing. Sub-questions on the same topic are OK in the same turn.

## Pre-flight

Before Turn 1, verify the user has named what the agent / system is FOR (the X in "build me a bundle for X"). If unclear:

> "What is this agent or system for? (Client name, internal job, brand, etc.)"

Once target is named, proceed.

---

## Turn 1 — Scope: single agent or multi-specialist system

**Ask:**

> "Is this one focused job, or a workflow with multiple distinct stages? (Example: 'draft listing copy' is one job. 'New lead → qualify → research → draft comms → track deal' is a multi-stage workflow.)"

**Push back if the answer is vague:**

- "It does a bunch of stuff" → "Pick the shape first. One agent or multiple stages?"

**Capture:** `SYSTEM_SHAPE` = `single` | `multi`

**If `single`:** continue to Turn 2 (single-agent flow).

**If `multi`:** insert an extra turn (Turn 1b) to define the stages, then proceed to Turn 2.

---

## Turn 1b (multi-specialist only) — Define the flow

**Ask:**

> "List the stages in order. Give each a short functional name (e.g., Lead Qualifier, Property Research, Client Communication)."

**Follow-ups in same turn:**

> "Which stage owns the handoff decision (the orchestrator)?"
> "Is there a natural human review gate between any stages?"

**Push back if:**

- Fewer than 2 stages → "A multi-specialist system needs at least two stages."
- More than 8 → "Top 6–8. Which stages can be merged?"
- Vague functional names → "What does this stage *do*? One verb if possible."

**Capture:**

- `STAGES[]` (ordered list of stage names)
- `ORCHESTRATOR_STAGE` (which stage routes)
- `HUMAN_GATES[]` (between which stages)

Continue to Turn 2.

---

## Turn 2 — Identity (single) OR System Identity (multi)

**Single:**

> "Who is this agent? Give it a name and a one-sentence role."
> "Voice — formal, casual, or brand-matched? Pick one."

**Multi:**

> "Give the overall system a short name and one-sentence purpose (e.g., 'OIB Autonomy Stack — turns raw design files into published, brand-voiced listings')."
> "Does the system have a shared voice or tone? If yes, describe it; if no, say 'per-specialist'."

**Push back (both shapes):**

- Name is cute/branded → "Functional names only. What would you call this on an org chart?"
- Role/purpose is vague → "What action does it take or enable? Specific."

**Capture:**

- `AGENT_NAME` or `SYSTEM_NAME`
- `ROLE_SENTENCE` or `SYSTEM_PURPOSE`
- `VOICE` (or `VOICE=per-specialist`)

---

## Turn 3 — Routing (single) OR Shared Context Sources (multi)

**Single:**

> "Where does this agent find context? List the 3–5 source-of-truth places."
> "Is any of that scattered or duplicated?"
> "Is anything missing that we'd have to create?"

**Multi:**

> "What shared sources does the *whole system* read from? (e.g., the OIB Airtable base, brand-oib-guide skill, ~/claude-memory/4-pod/)"
> "Per-specialist sources are handled later — right now we're looking for the common foundation."

**Push back (both):**

- Fewer than 3 → "Three minimum for reliability."
- More than 6 shared → "Top 5 common. The rest belong to individual specialists."

**Capture:**

- `SHARED_SOURCES` (Airtable base IDs, folder paths, skill names, MCPs)
- `SCATTERED_FLAGS`
- `MISSING_FLAGS`

---

## Turn 4 — Capability

**Single:**

> "What 3 tools does this agent actually need?"
> "Does each tool exist, or do we need to build it?"

**Multi:**

> "List up to 5 *system-wide* tools that multiple specialists will share (e.g., Airtable MCP, brand-oib-guide skill, /api/publish, etsy-listing-writer)."
> "We'll capture specialist-specific tools later."

**Push back (both):**

- More than 5 → "That's a framework, not load-bearing tools. Which 3–5 are truly shared?"
- Vague ("the listing thing") → "What does it do? Name the interface or skill."

**Capture:**

- `SHARED_TOOLS[]` (name + exists / needs-build status per tool)

---

## Turn 5 — Memory

**Single:**

> "What does this agent remember between runs?"
> "Per-conversation state? Per-entity state (per-design, per-customer)? Global learning?"

**Multi:**

> "Does the *system* share any cross-specialist memory (e.g., a shared Listings table, a common Brand vault)?"
> "Per-specialist memory is handled in the specialist interviews."

**Push back (both):**

- "Everything" → "Pick the two most important things it must retain. The rest can be stateless."
- "Nothing" → "Even a simple audit trail? At minimum, what does the next specialist in the chain need to know?"

**Capture:**

- `SHARED_MEMORY` (state type + where it lives)

---

## Turn 6 — Boundary

**Single:**

> "What can this agent NEVER do?"
> "What should it flag to a human?"
> "Give me at least 3 hard nos."

**Multi:**

> "Are there system-level boundaries that apply to *every* specialist?"
> "Example: 'Never publish without dryRun first' is a system boundary even if specialists do different work."

**Push back (both):**

- Fewer than 3 hard nos → "The boundary needs teeth. Give me three real refusals."
- "Don't be mean" / soft boundaries → "That's a preference, not a refusal. What action is literally off-limits?"

**Capture:**

- `SYSTEM_HARD_NOS[]` or `HARD_NOS[]`
- `ESCALATIONS[]`

---

## Turn 7 — Scaling axis

**Single or Multi (same question):**

> "12 months from now — does this need to scale on *volume*, *variation*, or *sophistication*? Pick one."

- Volume = more invocations of the same job(s). Build for queues + rate limits.
- Variation = more flavors of the same job(s). Build for parameterization + per-variant vaults.
- Sophistication = smarter execution over time. Build for feedback loops + leave the seam open.

**Capture:** `SCALING_AXIS` = volume | variation | sophistication

---

## Turn 8 — Kill Condition (mandatory — applies to both single and multi)

**Ask (do not skip or soften):**

> "What is the explicit condition under which this entire bundle or system should be archived or deleted?"

**Push back hard if the answer is vague or optimistic:**
- "When it stops being useful" → "Give me a measurable signal, not a feeling. What does 'not useful' actually look like in data or behavior?"
- "When Bre decides" → "Bre is not a reliable kill switch. The condition must be observable by the system or another agent."

**Capture:** `KILL_CONDITION`

**Note for later:** This gets written into every generated README.md and is non-negotiable.

---

## Turn 9 — Specialist-level design (multi only) OR Recap (single)

**If `single`:** jump to Turn 10 (recap + generation).

**If `multi`:** for each stage in `STAGES[]`, run a mini 5-Q interview (collapsible turns — ask all five in one pass if the user is confident):

For each stage name:

1. **Identity** — role sentence + voice for this specialist
2. **Routing** — 2–3 sources this specialist reads that others don't need
3. **Capability** — 1–2 specialist-specific tools (in addition to shared ones)
4. **Memory** — what this specialist must remember (per-entity state, handoff cache, etc.)
5. **Boundary** — 2–3 hard nos specific to this stage (in addition to system nos)

Also ask per specialist (if multi):

> "What is the one thing this specialist receives from the previous stage, and what single artifact does it hand off to the next?"

**Capture per specialist:**

- `SPECIALIST_IDENTITY`, `SPECIALIST_ROUTING`, `SPECIALIST_TOOLS`, `SPECIALIST_MEMORY`, `SPECIALIST_BOUNDARY`
- `HANDOFF_IN`, `HANDOFF_OUT`

---

## Turn 10 — Recap + generation confirmation

**Single recap example:**

> "Here's what you described:
> - One agent: OIB.Guide Listing Drafter
> - Job: draft listing copy
> - Sources: 4 (Designs table, Brand Info, Listing Templates, etsy-listing-writer skill)
> - 3 tools: Airtable MCP, brand-oib-guide skill, etsy-listing-writer
> - Memory: per-design check before overwriting
> - Hard nos: 3 (never publish without dryRun, never use banned vocab, never write SKU codes)
> - Scaling: volume
> - Kill condition: No new designs classified in 90 days
>
> Looks right? (y/n)"

**Multi recap example:**

> "Here's what you described:
> - System: OIB Autonomy Stack (5 stages + orchestrator)
> - Shared sources: Airtable base + brand-oib-guide skill
> - System hard nos: never publish without dryRun first
> - Scaling: volume
> - Kill condition: Batch publish runs drop below 5/week for 3 consecutive weeks
> - Stages:
>   1. File Intake Auditor → receives raw file path, hands off classified Design row
>   2. Listing Drafter → receives Design + Product Type, hands off draft listing + copy
>   ...
>
> Looks right? (y/n)"

**On confirm:**

1. Ask: "Bundle / system slug? (kebab-case, e.g. `oib-listing-drafter` or `oib-autonomy-stack`)"
2. Ask: "Destination path? (default: `~/claude-memory/agents/{slug}/` — gets the bundle Syncthing'd to Hetzner + embedded in Bre Brain automatically)"
3. Generate the folder tree (see output formats below)
4. End with the literal sentence: "Use this in 1-2 real sessions, then come back and tell me what's missing."

---

## Output formats

### Single-agent output (scaling axis applied)

```
[slug]/
├── CLAUDE.md                 ← Identity (Layer 0)
├── CONTEXT.md                ← Routing map (Layer 1)
├── README.md                 ← Why this exists + scaling axis + kill condition
├── brand-vault/
│   ├── CONTEXT.md
│   ├── voice.md
│   └── boundary.md
├── tools/
│   ├── CONTEXT.md
│   └── [tool-name].md
├── memory/
│   └── CONTEXT.md
├── 00-first-run-test.md      ← Mandatory test case + post-run notes
├── kill-condition.md         ← Explicit decommissioning trigger
└── triggers/ OR pipeline/    ← depending on shape
    ├── CONTEXT.md
    └── queue.md (if volume) OR feedback-loop.md (if sophistication)
```

### Multi-specialist system output

```
[slug]/
├── CLAUDE.md                 ← System identity + purpose
├── CONTEXT.md                ← Shared sources + handoff contracts
├── README.md                 ← System overview + scaling axis + kill condition
├── orchestrator/
│   ├── CLAUDE.md             ← 5-Q for the router
│   ├── CONTEXT.md
│   └── handoff-card-template.md
├── specialists/
│   ├── [stage-1-slug]/
│   │   ├── CLAUDE.md         ← 5-Q + handoff contract
│   │   ├── CONTEXT.md
│   │   ├── identity.md       ← short role statement
│   │   ├── rules.md          ← how it operates
│   │   ├── examples.md
│   │   └── handoff.md        ← what it receives, what it produces
│   ├── [stage-2-slug]/
│   │   └── ...
│   └── ...
├── brand-vault/              ← shared or per-specialist (variation axis)
├── tools/                    ← shared tools only
├── memory/                   ← shared memory only
├── 00-first-run-test.md      ← System-level minimal end-to-end test
├── kill-condition.md         ← System-level decommissioning trigger
└── triggers/ OR pipeline/    ← system-level flow (if needed)
```

When `SCALING_AXIS = variation`, `brand-vault/` contains subfolders per variant.

When `SCALING_AXIS = volume`, `triggers/queue.md` is generated with rate-limit notes.

When `SCALING_AXIS = sophistication`, `memory/feedback-loop.md` is generated as a stub.

---

## Behavior notes specific to multi-specialist

- The orchestrator always receives the full 5-Q interview first.
- Each specialist receives its own abbreviated 5-Q (identity, routing, capability, memory, boundary) + an explicit handoff contract (HANDOFF_IN / HANDOFF_OUT).
- The shared `handoff-card-template.md` is always generated in the orchestrator folder when `SYSTEM_SHAPE = multi`.
- System-level boundaries cascade down; specialist boundaries are additive, not replacements.
- Every specialist folder also receives its own `00-first-run-test.md` (specialist-level minimal test) and references the system-level kill condition.

---

## End of script

Stop after generation. Do not expand scope. Do not add features Bre did not confirm in the recap. Let the scaffold breathe for 1–2 real sessions before the next iteration.