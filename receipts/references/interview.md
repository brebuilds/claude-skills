# The interview (spec agent 5)

Ask the **smallest number of questions that produces the largest increase in career
clarity.** One primary question at a time, always.

This runs in the main session, never in a subagent — it is a conversation with the user.

## Why one at a time

A twelve-part questionnaire gets abandoned, and an abandoned interview leaves the record
worse than before: half-answered, stale, and demoralising to return to. One sharp
question gets answered in twenty seconds and immediately upgrades a tier.

Bad:
> Tell me the timeline, team size, architecture, scale, outcomes, revenue, user count and technologies.

Good:
> Before you built this, did they have an online product catalog at all?

Then, after they answer:
> Roughly how many raw product records were in the POS?

Then:
> Did you build the synchronization yourself, or configure something that existed?

## Ranking: which question to ask first

Score each candidate question by **expected information gain** — how many claims it
upgrades, times how much it changes the story.

Ask in roughly this order, because each unlocks the value of the next:

1. **Before-state.** Highest value, almost always. "What existed before?" converts a task
   into a transformation, and transformation is what gets hired. *"I connected two
   systems"* and *"they had no online catalog at all and now they sell online"* describe
   the same work.
2. **Ownership.** Did they build it, configure it, or direct it? Everything downstream
   depends on this, and getting it wrong is the one error that ends an interview badly.
3. **Ambiguity.** Were they handed a spec, or did they find the real problem? This is the
   single most under-recorded axis and the one that separates senior from mid.
4. **Scale.** Numbers that bound the work — records, users, products, dollars, duration.
5. **Constraints.** What made it hard: budget, legacy systems, seasonality, staffing.
6. **Business impact.** What changed for the organization, in their terms not technical ones.
7. **Measurable outcome.** The number that proves the impact.

Skip any question whose answer is already `VERIFIED` in the store. Asking the user to confirm
something the evidence already proves burns their patience on nothing, and patience is the
scarce resource here.

## Question bank

**Before-state**
- Did this exist in any form before you started?
- What were they doing instead? How long did it take them?
- What were they paying for that this replaced?
- What was broken often enough that someone complained about it?

**Ownership**
- Did you build this, or configure something that already existed?
- Was anyone else writing code on this?
- Who decided the architecture?
- If this broke at 9pm, who got called?

**Ambiguity**
- What did they originally ask you for?
- Was that actually the problem?
- Did anyone tell you how to solve it, or did you work that out?
- What did you decide *not* to do?

**Scale**
- Roughly how many records/products/users/orders?
- Over what period?
- How much data moved?

**Constraints**
- What made this harder than it should have been?
- What couldn't you change?
- Was there a deadline that shaped the design?

**Impact**
- What can they do now that they couldn't before?
- Did this save money, time, or headcount? Roughly how much?
- Is it still running?
- Would they notice if it stopped?

That last one is quietly the best impact question in the bank. "Would they notice if it
stopped" separates a demo from production, and the user answers it instantly and honestly
where "what was the business impact" makes them freeze.

## Recording answers

Immediately, before asking anything else:

- Confident, specific answer → `USER_CONFIRMED`
- Hedged answer ("I think around 17,000") → `APPROXIMATE`, and **preserve their hedge
  verbatim** in `render_string` ("over 17,000", "~17,000"). Never quietly firm it up.
- "I don't remember" → leave the tier alone, mark the question `asked-unresolved` so it
  is not asked again next session. Re-asking a question the user already failed to answer
  is the fastest way to make them stop using this.
- An answer that contradicts existing evidence → `CONFLICTING`, into `conflicts.md`.
  Their memory is a source, not an override. Say so gently and show both.

Then recompute the project record and decide whether another question is worth asking. It
usually is not — one good answer per session beats an interrogation.

## "I just remembered something" (spec §7B)

The user will volunteer things out of nowhere. When they do:

1. Interpret it
2. Identify the likely project — ask if genuinely ambiguous, do not guess between clients
3. Record as `USER_CONFIRMED` user-supplied evidence
4. Reassess the project record
5. Note any new question it opens
6. Tell them what it changed — "that moves the mockup system from unclaimed into the
   Acme Storefront record, and it's now your strongest creative-tooling evidence"

Step 6 matters. Seeing a stray memory immediately become structured evidence is what
makes the user keep volunteering them, and volunteered memories are the highest-quality
source in the whole system.
