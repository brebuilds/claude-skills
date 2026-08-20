---
name: receipts
description: Career forensics — reconstruct what the user actually did from the evidence they left behind (repos, files, notes, vault, old résumés), separate evidence from inference, and feed verified claims into POOL.md. Use for "what did I actually do on X", "mine this repo for résumé evidence", "am I underselling this project", "find my hidden gold", "what numbers do I have", "receipts for this claim", "is this claim backed", "build a project record", "what am I not claiming", or any moment the user describes shipped work casually and the real scope is probably larger. Also use before tailoring a résumé when the pool looks thin for a target role.
---

# Receipts — your career, reconstructed

**Tagline:** you did more than you remember.

Most career tooling starts with "tell me what you did." Receipts starts with **"give me
the evidence, we'll figure out what you did."** People systematically under-report their
own work: they forget projects, normalize hard things, describe architecture as "setting
something up," and lose accomplishments across years of repos and notes.

The goal is **not** better writing. The goal is to understand what actually happened.
Good writing is the consequence.

## The one rule

# RECEIPTS, NOT HYPE.

Never make work impressive by exaggerating it. Make it impressive by understanding it.
Precise truth outperforms inflated language, and it survives an interview.

Never invent a number. Never imply ownership that has not been established. Never let an
inference quietly become a fact. When you do not know, that is a question, not a bullet.

---

## Where this sits (read before doing anything)

Receipts is the **mining layer upstream of an existing, working system**. It does not
replace anything.

```
evidence (repos, files, notes, vault, old résumés)
   ↓  RECEIPTS   ← this skill: discover, verify, interview, appraise
~/claude-private/resume/receipts/     ← the evidence store
   ↓  promotion (only VERIFIED / USER_CONFIRMED / hedged APPROXIMATE)
~/claude-private/resume/POOL.md       ← the existing verified claim store
   ↓  verbatim gate (already built, July 2026 — [CONFIRM] hard-fails)
pipeline/ → generated/                ← styled PDF + ATS text + cover letter
```

Consequences, and they are load-bearing:

- **Never write a résumé bullet directly.** Write a claim into the store, promote it into
  POOL.md, let the existing pipeline render it. The verbatim gate is the honesty
  enforcement — bypassing it is how false claims reach a real job application.
- **Never create a second career store.** POOL.md stays the source of truth for what is
  claimable. Receipts holds evidence and provenance; POOL.md holds what is sayable.
- **POOL.md §10 UNMINED BUILDS is the hand-written version of `unclaimed.md`.** Keep them
  reconciled; when a §10 line is mined, mark it and move the detail into the store.

Read `references/schema.md` before writing to the store. It is the data contract.

---

## The pipeline — never skip a stage

```
SOURCE → OBSERVATION → CLAIM → VERIFICATION → PROJECT → CAREER SIGNAL → OUTPUT
```

Going straight from SOURCE to OUTPUT is exactly how résumé generators produce confident
fiction. Each arrow is a place where confidence can drop, and it must be allowed to.

**Stage 0 — security pre-flight (mandatory, no exceptions).**
Before any repo or folder content reaches model context:

```bash
python3 ~/.claude/skills/receipts/scripts/scan_secrets.py <path> \
  --json ~/claude-private/resume/receipts/scans/<slug>.json
```

Analysis agents read **only** paths in the manifest's `safe` list. Quarantined files are
never opened, and a detected secret is recorded as *path + rule* — never the value.
`~/claude-private/secrets/` is off-limits entirely.

If the scan quarantines something that looks like real evidence (a source file *named*
`secrets.ts` usually means the user built secret handling — that is architecture evidence),
say so rather than silently losing it.

**Stage 1 — ingest.** Register each source in `sources.jsonl`. Existing résumés,
portfolio text, and LinkedIn exports are ingested as **claims to verify, not truth.**

**Stage 2 — dig.** Dispatch archaeology subagents (below). They return observations only.

**Stage 3 — cluster + audit + mine.** Group observations into projects, audit claims for
support, extract metrics.

**Stage 4 — appraise.** Hidden gold and career signals.

**Stage 5 — interview.** Ask the user the single highest-value open question. Main session
only (a subagent cannot talk to them).

**Stage 6 — compose.** Only from the verified project record. Main session only.

---

## The subagent roster

The spec describes ten agents; four of them are dispatched here. They exist as subagents
for one concrete reason: **context isolation**. A 750-file repo sweep would consume the
main window, and the main session needs its context for the interview, which is the part
that requires actually talking to the user.

| Agent | Covers spec agents | Dispatch when |
|---|---|---|
| `receipts-digger` | 1 Archaeologist, 3 File & Note | Documents, notes, spreadsheets, screenshots, old résumés, vault folders |
| `receipts-repo` | 2 Repo Archaeologist | A code repository |
| `receipts-auditor` | 4 Clusterer, 8 Claim Auditor, 9 Metrics Miner | Observations exist and need grouping, provenance checking, number extraction |
| `receipts-appraiser` | 6 Hidden Gold, 7 Career Signal | A project record is populated and needs interpretation |

Spec agents **5 (Interviewer)** and **10 (Output Composer)** deliberately stay in the main
session — both are conversations with the user, not batch analysis.

Run `receipts-digger` and `receipts-repo` in parallel when a project has both kinds of
evidence. Always run the auditor **after** they return, never alongside — it operates on
the pooled observation set.

---

## Commands

The user will say these in plain language; map them.

| They say | Do |
|---|---|
| "mine <repo/folder/project>" | Stage 0 → 4, produce/refresh `projects/<slug>.md`, then ask ONE question |
| "what am I not claiming" | Read `unclaimed.md` + POOL.md §10, rank by career value, propose promotions |
| "receipts for <claim>" | Trace the claim to its observations and evidence pointers; if none exist, say so plainly |
| "am I underselling <project>" | Hidden gold pass; show YOU SAID / WHAT YOU ACTUALLY DID / WHY IT MATTERS / RECEIPTS |
| "what numbers do I have" | Metrics table, split into NUMBERS WE HAVE and NUMBERS WORTH FINDING |
| "promote <claim>" | Check tier, write into POOL.md in pool format, set `pool_status` |
| "target <job posting>" | Match verified signals to requirements: STRONG / PARTIAL / NO EVIDENCE, plus skills not to claim |
| "receipts status" | Coverage: sources ingested, projects with records, claims by tier, open questions |

---

## Interview protocol (stage 5)

**Ask ONE question at a time.** Ranked by expected information gain, not by curiosity.
A questionnaire gets abandoned; one sharp question gets answered.

Bad: "Tell me the timeline, team, architecture, scale, outcomes, revenue and stack."
Good: "Before you built this, did they have an online catalog at all?"

Prioritise: before-state → ownership → scale → constraints → business impact → measurable
outcome. Before-state first, because it converts a task into a transformation.

Full question bank and ranking heuristics: `references/interview.md`.

When an answer lands, immediately write it as `USER_CONFIRMED` (or `APPROXIMATE` if they
hedge — preserve their hedge verbatim), recompute the project record, and only then
decide whether another question is worth asking.

---

## Hidden gold format

When evidence shows more than the user claimed, present it exactly this way:

> ### YOU SAID
> "I cleaned up their Shopify products."
>
> ### WHAT THE EVIDENCE SUGGESTS
> You converted a flat POS inventory model into a structured e-commerce product
> architecture, then kept it synchronized automatically.
>
> ### WHY THIS MATTERS
> data modeling · systems integration · e-commerce architecture · operational problem solving
>
> ### RECEIPTS
> `src/sync/variants.ts:88` · n8n workflow export · POOL.md §5 bullet
>
> ### MOST RELEVANT TO
> Forward-Deployed Engineer · Solutions Engineer · Automation Engineer

The reaction to aim for is **"wait, that's what I did?"** — not flattery. If the evidence
does not support the reframe, do not manufacture one; say the work is already accurately
described. "Already accurate" is a legitimate and useful result.

---

## Output composition (stage 6)

Compose only from a verified project record, never from raw sources. Styles and their
emphases: `references/outputs.md`.

Every generated line must support **SHOW RECEIPTS** — name the observations and evidence
pointers behind it. If a line cannot show receipts, it does not ship.

---

## Invariants

1. Run the secret scan before reading any repo. Every time.
2. Never write a number that is not in `metrics.jsonl` with a tier.
3. Never drop a hedge from an `APPROXIMATE` metric to make a line read stronger.
4. Never promote `INFERRED` / `CONFLICTING` / `UNKNOWN` into POOL.md without `[CONFIRM]`.
   An `INFERRED` claim never ships as a claim at all — it ships as its underlying
   observation with every ownership verb stripped, or it does not ship. This is a locked
   product decision — the rule is in `references/outputs.md` and there is no deadline
   exception to it.
5. Never merge two projects on a name guess — ask (spec §4: "Acme Store Migration" and
   "Acme Storefront" may or may not be the same body of work).
6. Conflicts go to `conflicts.md` and to the user. Never silently pick the flattering version.
7. Client names, contract terms, and unshipped work stay in `~/claude-private/`. Never
   sync career evidence into `~/claude-memory/` (shared with agents and Syncthing).
8. `ruled-out` means ruled out. Do not resurface it as unclaimed next session.
