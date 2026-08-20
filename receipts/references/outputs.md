# Output composition (spec agent 10)

Compose **only** from a verified project record. Never from raw sources, never from
memory of the conversation. If a fact is not in the record with a tier, it does not exist.

## Reuse the existing archetypes — do not invent a parallel taxonomy

POOL.md already tags every bullet with role archetypes, and the render pipeline selects on
those tags. The spec's output styles map onto them; keep the existing tags so composed
lines drop straight into the pool and the pipeline picks them up unchanged.

| Spec style | Pool tag | Emphasize |
|---|---|---|
| Forward-Deployed Engineer | `fde` | ambiguity · client discovery · integration · deployment · business results |
| Solutions Engineer / Architect | `arch` | systems design · stakeholders · requirements · technical communication |
| AI Engineer | `ai` | LLM systems · agents · RAG · orchestration · voice · infrastructure |
| Full-Stack Engineer | `fs` | application architecture · frontend/backend · databases · APIs · production |
| Product / Technical Product | `arch` + `ops` | problem definition · decisions · user and business impact |
| Creative Technologist | *(none yet)* | design + engineering · interactive experience · emerging tech |

POOL.md also carries two vertical overlays — `hlth` (healthcare/clinical AI) and `prop`
(tourism/real estate/hospitality) — which are lenses on the same facts, not new identities.
Respect that: an overlay re-points existing bullets, it never invents new ones.

**Creative Technologist has no tag yet.** It is a real gap — the design-plus-engineering
work is currently invisible in the pool. Do not silently add a tag. Propose it to the user and
let them decide, because a new archetype means a new reference résumé and a new assembly kit.

## Lengths

For every project produce, on request: one-line · one bullet · two bullets · three
bullets · compact · detailed technical. Same facts, different compression. Compression
must never add a claim that the longer version does not make.

## SHOW RECEIPTS

Every generated line must be traceable. Keep the mapping so that for any bullet you can
immediately answer *"what backs this?"* with claim ids and evidence pointers.

If a line cannot show receipts, it does not ship. No exceptions, including when it is the
best-sounding line you wrote.

## Promotion into POOL.md

This is the only path from Receipts to a real résumé.

1. Check the claim's tier. `VERIFIED` / `USER_CONFIRMED` → proceed. `APPROXIMATE` →
   proceed **with the hedge inside the string**. Anything else → stop, it becomes a
   question instead.
2. Write it into the correct POOL.md section (§5 experience bullets, §6 selected work,
   §8 optional modules, §10 unmined triage) in the pool's existing voice and format.
3. Tag it with the archetypes it serves: `[ai, arch]`.
4. Set `pool_status: promoted` on the claim, with the pool section recorded.
5. If it came from POOL.md §10 UNMINED BUILDS, tick that line off — the triage queue is
   the hand-written ancestor of `unclaimed.md` and the two must stay reconciled.

The pipeline's verbatim gate means the string you write into POOL.md is the exact string
that reaches the PDF. Write it as it should appear, not as a note to yourself.

## Interview stories

For each strong project: 30-second explanation · 60-second explanation · STAR response ·
technical deep dive · likely interviewer follow-ups · details worth remembering.

The follow-ups matter more than the story. A bullet that survives the résumé but collapses
under "walk me through how you handled the variant mapping" is worse than not claiming it,
because it makes everything else on the page suspect.

## Job targeting (spec §16)

Extract required capabilities from the posting, then compare against verified signals:

- **STRONG EVIDENCE** — clearly supported by verified project history
- **PARTIAL EVIDENCE** — adjacent experience, name the gap honestly
- **NO EVIDENCE** — no verified support

Then recommend: best projects for this application · best bullets · best interview stories
· **skills not to claim**.

That last one is the point. Never rewrite history to mirror a job description. The value
here is knowing what *not* to say, so the interview does not fall over.

---

## The INFERRED rule — a locked product decision

**An `INFERRED` claim never ships as a claim. It ships as its observation, or not at all.**

When a claim is `INFERRED` and wanted anyway — high value, deadline tomorrow, memory
won't confirm it — the composer may render only the underlying observation: the
inspectable fact, stripped of every ownership and agency verb.

1. Find the observation(s) the claim rests on. No observation, no line. Stop there.
2. Render the observation's content, not the claim's interpretation.
3. Forbidden until ownership is `VERIFIED` or `USER_CONFIRMED`: *architected · designed ·
   built · led · owned · created · drove · introduced* — anything asserting agency.
4. Allowed: system-subject or scope phrasing — *"the integration spanned three POS
   endpoints"*, *"the deployment covered 7,500 products"*. True regardless of who did it.
5. If stripping the agency verb leaves nothing worth saying, the line does not ship.
   That is the correct outcome, not a failure.

No deadline exception, no per-claim override, no hedged-ownership fallback. The test is
not "is this defensible" — it is **"does this survive an interviewer asking me to walk
through it."** A downgraded observation always survives, because it never claimed
anything unproven. Weakened-ownership language ("contributed to", "worked on") is
explicitly rejected: it invites exactly the follow-up question there is no answer to.
