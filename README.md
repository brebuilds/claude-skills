# Claude Code Skills

A collection of [Claude Code](https://claude.com/claude-code) skills — reusable, versioned
capability packages that extend an agent session with domain-specific procedures, reference
material, and helper scripts.

A skill is a folder with a `SKILL.md` at its root: YAML frontmatter (`name`, `description`,
optional `version`/`tags`) followed by instructions in plain markdown. Claude Code loads only
the frontmatter into every session by default and pulls the body — plus any `references/*.md`
or `scripts/*` the skill points at — on demand, when the `description` matches what the user is
asking for. That's the engineering discipline underneath something that looks like "just a
markdown file":

- **Progressive disclosure.** The full skill body, and anything under `references/`, is not in
  context until it's needed. A 600-line skill costs nothing in the sessions that never trigger
  it, and costs only what it needs in the ones that do.
- **Trigger-condition design.** The `description` field is the only thing standing between "this
  skill fires when it should" and "this skill never fires, or fires on everything." Writing it
  well means enumerating real phrasing a user would use, not just restating the skill's name.
- **Context budgeting.** Splitting a skill into `SKILL.md` (always-relevant procedure) plus
  `references/*.md` (loaded only for the sub-case that needs it) is a deliberate choice about
  what an agent should be holding in its context window at any given moment, not just a way to
  keep files short.

The skills below are copied from a working local setup and sanitized for public release — client
names, internal API IDs, webhook URLs, and business-specific config have been replaced with
placeholders. The engineering patterns and gotchas are unchanged.

## What's here

| Skill | Engineering concept it demonstrates |
|---|---|
| [`receipts`](./receipts) | Multi-subagent orchestration with **context isolation** (four dispatched subagents, each scoped to one job so a 750-file sweep never touches the main session's context) plus a mandatory pre-flight secret scan (`scripts/scan_secrets.py`) and named anti-hallucination invariants (`EXTRACTED` vs `INFERRED` vs `CONFLICTING`, a verbatim-hedge rule for approximate numbers, and a rule that an unconfirmed claim can never render into output text). |
| [`graphify`](./graphify) | Parallel extraction across subagents (AST structural extraction and LLM semantic extraction run concurrently, not sequentially), deterministic node-ID generation so re-running extraction never creates duplicate "ghost" nodes, and an `EXTRACTED`/`INFERRED`/`AMBIGUOUS` confidence tag on every edge — an audit trail baked into the data model, not bolted on after. |
| [`skill-forge`](./skill-forge) | Meta-tooling — a skill whose job is producing other skills (niche research → skill authoring → packaging → bundling), including its own quality bar for what makes a skill sellable. |
| [`etsy-api`](./etsy-api) | Real third-party API integration: OAuth2 PKCE token flow, refresh-token rotation (Etsy issues a new refresh token on every refresh — miss that and auth silently breaks), offset-based pagination, and 429/`Retry-After` backoff handling. |
| [`printify-api`](./printify-api) | The same integration discipline against a second, differently-shaped API: page-based (not offset) pagination, a required custom `User-Agent` header to get past Cloudflare, and a composite-key gotcha where variant IDs are not globally unique. |
| [`interactive-game-builder`](./interactive-game-builder) | A browser game loop built on HTML5 Canvas — `requestAnimationFrame` update/render cycles, sprite state machines, AABB (axis-aligned bounding box) collision, and vision-cone-based enemy detection for stealth-style mechanics. |
| [`nextjs-site-scaffold`](./nextjs-site-scaffold) | An opinionated project starter: a full `create-next-app` sequence, dependency set, folder layout, and a build-out checklist, encoding "what does a project need before it's really scaffolded" as a repeatable procedure instead of tribal knowledge. |

Every skill's real signal — the "gotchas" sections in `etsy-api` and `printify-api` especially —
is left intact. Those are hard-won details (token formats, header requirements, field-name
inconsistencies) that only show up after actually integrating against the live API, not from
reading its docs.

## Worked example: `receipts`

`receipts` is a career-forensics pipeline: point it at a folder of repos, notes, screenshots, or
old résumés, and it reconstructs a verified record of what was actually done — separating what the
evidence proves from what an LLM might otherwise infer or embellish.

**Input** — the user says something like:

> "mine ~/projects/acme-storefront — what did I actually do on this?"

**What it does:**

1. **Ingest.** Every source (repo, file, note, export) is registered in `sources.jsonl`. A résumé
   or portfolio blurb is ingested as a *claim to verify*, not as truth.
2. **Secret scan pre-flight.** `scripts/scan_secrets.py` runs before any file is opened by an
   analysis agent. Files that trip a secret pattern are quarantined — recorded as *path + rule
   name only*, never the matched value — and analysis agents are only ever handed the manifest's
   `safe` list.
3. **Parallel dispatch.** `receipts-digger` (notes, screenshots, spreadsheets, old résumés) and
   `receipts-repo` (the actual codebase — architecture, integrations, data modeling, commit
   history) run as separate subagents *in parallel*, each producing plain **observations**:
   objective, checkable facts with an evidence pointer (`src/sync/variants.ts:88`), never career
   interpretation.
4. **Audit.** `receipts-auditor` runs after both return — never alongside, since it operates on
   their pooled output. It clusters observations into projects, turns them into **claims** with a
   confidence tier (`VERIFIED`, `USER_CONFIRMED`, `APPROXIMATE`, `INFERRED`, `CONFLICTING`), and
   checks each claim against *both* supporting and contradicting evidence before it's allowed to
   exist.
5. **Appraise.** `receipts-appraiser` looks at a populated project record for underestimated work
   and translates verified claims into plain-language professional capability.
6. **Interview.** The *only* stage that runs in the main session, not a subagent — because it's a
   conversation with the user, and a subagent can't have one. It asks a single highest-value
   question at a time, ranked by expected information gain, and never re-asks a question the user
   already declined to answer.

**Output shape** — a structured project record (`sources.jsonl`, `observations.jsonl`,
`claims.jsonl`, `metrics.jsonl`, one markdown file per project) where every number carries a tier,
every claim traces back to an evidence pointer, and an `INFERRED` claim is structurally incapable
of shipping into a résumé bullet as a bare assertion — it renders only as its underlying
observation, with every ownership verb stripped, unless the user explicitly confirms it.

The interesting engineering property isn't the résumé bullets it produces — it's that the pipeline
is built so that *hallucinating a claim is not a prompting problem to avoid, it's a state the data
model doesn't allow.*

## How to use these

Drop any skill folder into `~/.claude/skills/` (Claude Code's user-level skill directory):

```bash
cp -r receipts ~/.claude/skills/
```

Claude Code picks it up automatically on the next session — no restart, no registration step.
The `description` field in each `SKILL.md` frontmatter is what the agent matches against your
request to decide whether to load it, so if you rename or fork one of these, keep that field
accurate to how you'd actually phrase the request.

A few of these (`etsy-api`, `printify-api`, `nextjs-site-scaffold`) expect environment variables
or config for the service they integrate with — each `SKILL.md` documents what it needs under its
own "Setup" / "Environment Variables" section, using placeholders (`YOUR_SHOP_ID`,
`YOUR_CLIENT_ID`, etc.) in place of any real account details.

## License

MIT — see [`LICENSE`](./LICENSE).
