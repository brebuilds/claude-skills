# Receipts — data contract

The store lives at `~/claude-private/resume/receipts/`. Private, never the shared vault:
this holds client names, contract context, and unshipped work.

Machine-appended files are **JSONL** (append-only, so parallel agents never collide on a
merge). Human-read files are **Markdown**. One object per line, no rewriting history —
corrections are appended as new lines with a later `at` timestamp.

### How corrections work (read this before writing to the store)

To correct anything, append a **new line with the same `id`** and a later `at`. Never edit
a line in place — the superseded version is the audit trail, and it is the only record of
what a résumé claimed before it was fixed.

Two mechanics make this safe, and both are load-bearing:

- **Reads collapse.** Every read path in `receipts.py` goes through `latest_by_id()` —
  last line wins. Without it, a corrected claim is counted twice and the tier distribution
  silently lies.
- **`merge` dedupes on content, not on id.** Same id + identical content is an agent
  re-run and gets skipped; same id + different content is a correction and gets through.
  It reports `(N correction(s))` when that happens.

So: a corrected claim leaves the old line visible in the file, but `status`, `claims` and
`unpromoted` all report only the current version.

```
receipts/
├── CONTEXT.md          # how to use the store (human entry point)
├── sources.jsonl       # what has been ingested
├── observations.jsonl  # objective facts found in sources
├── claims.jsonl        # professional interpretations + confidence
├── metrics.jsonl       # quantitative claims
├── projects/<slug>.md  # the Project Record (Before → Build → After)
├── signals.md          # career capability rollup
├── unclaimed.md        # found, real, not used anywhere yet  (feeds POOL.md §10)
├── questions.md        # highest-value unresolved questions  (the interview queue)
└── conflicts.md        # sources disagree; the user decides
```

---

## Confidence tiers

Every claim carries exactly one. This is the whole product — get it wrong and Receipts
becomes a résumé-inflation machine, which is the one thing it must never be.

| Tier | Means | May become a résumé line? |
|---|---|---|
| `VERIFIED` | Directly supported by inspectable evidence | Yes |
| `USER_CONFIRMED` | The user explicitly confirmed it | Yes |
| `APPROXIMATE` | The user believes the number is roughly right | Yes, **only** with hedging language preserved |
| `INFERRED` | Evidence suggests it; nobody confirmed it | **No.** Becomes a question, not a bullet |
| `CONFLICTING` | Sources disagree | **No.** Goes to `conflicts.md`, the user decides |
| `UNKNOWN` | Would be useful, not established | **No.** It is a question by definition |

### The promotion contract (why this enforces itself)

`~/claude-private/resume/POOL.md` is the existing verified claim store, and the render
pipeline already enforces a **verbatim gate**: every string rendered onto a résumé must
appear in POOL.md exactly, and `[CONFIRM]` markers hard-fail the render.

Receipts plugs into that gate rather than replacing it:

- `VERIFIED` / `USER_CONFIRMED` → may be written into POOL.md as a clean bullet.
- `APPROXIMATE` → may be written into POOL.md **with the hedge inside the string**
  (`~7,500 products`, `over 17,000 records`). The hedge survives the verbatim gate
  because it is part of the text.
- `INFERRED` / `CONFLICTING` / `UNKNOWN` → **never written to POOL.md as a bare claim.**
  If parked there for later, it carries `[CONFIRM]`, which hard-fails any render until
  the user resolves it.

Net effect: an unverified claim physically cannot reach a résumé PDF. No new enforcement
code — the July verbatim gate does the work.

### Hedging vocabulary for APPROXIMATE

Use one of these; never drop the hedge to make a line read stronger:
`~` · `roughly` · `about` · `over` · `more than` · `nearly` · `upwards of`

Never convert `APPROXIMATE` to an exact figure. `~7,500` must not become `7,500`.

---

## Objects

### SOURCE — `sources.jsonl`
```json
{"id":"src_0001","type":"repo|file|note|resume|url|export|screenshot|spreadsheet",
 "title":"acme-shopify-sync","origin":"~/projects/acme-shopify-sync",
 "date_ingested":"2026-08-15","scan_manifest":"scans/acme-shopify-sync.json",
 "quarantined":2,"status":"ingested|partial|failed","notes":""}
```

### OBSERVATION — `observations.jsonl`
Objective, checkable, no career interpretation. If a skeptic could not verify it by
opening the pointer, it is not an observation.
```json
{"id":"obs_0001","source_id":"src_0001","project":"acme-storefront",
 "description":"Variant grouping keyed on Clover itemGroup id across three modules",
 "evidence_pointer":"src/sync/variants.ts:88","confidence":"high|medium|low",
 "at":"2026-08-15T02:44:00Z"}
```

### CLAIM — `claims.jsonl`
What the observations may establish, professionally.
```json
{"id":"clm_0001","project":"acme-storefront",
 "statement":"Normalized a flat POS catalog into a variant-structured commerce model",
 "tier":"VERIFIED","supports":["obs_0001","obs_0004"],"contradicts":[],
 "user_confirmation":null,"pool_status":"unpromoted|promoted|ruled-out",
 "last_verified":"2026-08-15"}
```
`pool_status` is how a claim stops being re-surfaced forever. `ruled-out` means the user
looked and said no — never resurface it as "unclaimed."

### METRIC — `metrics.jsonl`
```json
{"id":"met_0001","project":"acme-storefront","name":"image coverage",
 "before_value":"0%","after_value":"94%","value":null,"unit":"percent",
 "approximate":false,"tier":"USER_CONFIRMED","source":"src_0003",
 "render_string":"0% to 94% image coverage"}
```
`render_string` is the exact text allowed onto a résumé — hedge already baked in. The
composer copies this string; it never re-derives one from the numbers.

### PROJECT — `projects/<slug>.md`
Markdown, because the user reads it. Required headings, in order:
`# NAME` · `## FACTS` (client, dates, role, status, ownership) · `## BEFORE` ·
`## PROBLEM` · `## CONSTRAINTS` · `## BUILD` · `## AFTER` · `## ARCHITECTURE` ·
`## METRICS` · `## HIDDEN GOLD` · `## RECEIPTS` · `## OPEN QUESTIONS` ·
`## CAREER SIGNALS` · `## EVIDENCE STRENGTH`

### CAREER SIGNAL — `signals.md`
Capability demonstrated across projects, with the projects named. A signal supported by
one project is a data point; supported by four it is a pattern, and the pattern is the
strongest thing Receipts produces.

---

## Evidence Strength (spec §12)

Scores the **evidence**, never the person. Report as `NN/100` plus the two or three
specific things that would raise it. Never render this on a résumé — it is an internal
readiness gauge.

| Dimension | Weight |
|---|---|
| Evidence confidence (tier mix of the project's claims) | 25 |
| Ownership clarity (who actually built it) | 15 |
| Measurable impact (metrics with before/after) | 20 |
| Business / operational impact | 15 |
| Technical + integration complexity | 15 |
| Production responsibility (did it run for real users) | 10 |

A small system with real operational impact outscores a large codebase with none. That
is intended: it matches how hiring managers actually read work.
