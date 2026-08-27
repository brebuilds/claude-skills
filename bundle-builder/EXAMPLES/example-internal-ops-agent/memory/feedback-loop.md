# Feedback Loop — Sophistication Axis

This agent is on the sophistication scaling axis. Its classifier needs to get smarter over time. This file is the seam where that learning hooks in.

**Status: stub.** The wiring is intentionally not built yet — leave the seam open. Fill in the specifics after 1-2 real classification runs surface what's actually going wrong.

## The loop shape

1. **Classify** — agent labels a file
2. **Verify** — human (or another agent) marks the label as correct / incorrect / partial
3. **Learn** — verified-correct + verified-incorrect feed back into the classifier
4. **Re-classify low-confidence + previously-wrong items** — next sweep, accuracy is higher

## Where verifications come from (options to decide)

- Bre manually reviewing a queue of `needs-review` items
- The downstream POD Listing Drafter — if a design tagged "oib-guide" produces broken brand-voice output, that's a signal the classification was wrong
- A second classifier (different model / different approach) — disagreements flag for review

## Where the learning lives (options to decide)

- **Prompt examples**: verified-correct goes into the classifier prompt as in-context examples (cheap, fast, plateau)
- **Rules updates**: when a pattern emerges, add a rule to the rule-based fast-path (medium, persistent)
- **Fine-tuned model**: when scale justifies it (expensive, persistent, slow to update)

Recommended starting point: prompt examples + rules. Skip fine-tuning until the volume justifies it.

## Anti-patterns

- Don't auto-trust corrections without confirmation — a single "incorrect" mark shouldn't overwrite a thousand other "correct" examples
- Don't let the feedback loop grow unbounded — cap example count, age out old examples
- Don't conflate "low confidence" with "wrong" — low confidence means the agent KNOWS it might be wrong, that's different from being wrong

## Fill in after first 1-2 sessions

- What verification mechanism is actually viable? (Bre's bandwidth, downstream signal availability, etc.)
- What's the most common wrong-classification pattern? (That's where the rules should expand first.)
- What's the cadence of re-classification of previously-wrong items?
