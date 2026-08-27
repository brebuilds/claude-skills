# Trigger — Inquiry Received

## Flow

1. **Validate location ID** — if missing or unknown, refuse.
2. **Load context** — read shared `brand-vault/voice.md` + `brand-vault/boundary.md` PLUS location-specific overrides at `brand-vault/<location>/`.
3. **Classify inquiry type** — appointment / billing / dental question / general info / complaint / emergency.
4. **Boundary check** — does the inquiry trigger any flag in `boundary.md`? If yes → escalate, stop here.
5. **Knowledge base lookup** — if inquiry topic is in the location's KB, retrieve the answer.
6. **Compose response** — using location voice + KB answer. NEVER beyond the KB scope.
7. **Confirm before any write action** — if response involves scheduling/changing anything, read back to caller, require explicit confirmation.
8. **Log + close** — capture the classification + outcome for review.

## Out of scope
- Multi-turn back-and-forth beyond ~3 turns → escalate to human.
- Anything triggering an emergency flag → immediate emergency message + escalation.
