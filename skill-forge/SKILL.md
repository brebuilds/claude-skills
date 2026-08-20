---
name: skill-forge
description: >
  USE THIS SKILL when the user mentions creating skill packs, generating skills
  for a niche, building sellable skill bundles, skill factory, passive income
  skills, niche skill research, skill product creation, "forge a pack",
  "make skills for", mass skill creation, skill automation, or any mention of
  creating Claude Code skills as digital products. This skill is the complete
  pipeline from niche research through packaged, sellable skill bundles.
---

# Skill Forge

End-to-end skill pack factory. Takes a niche or persona, researches their pain points, architects a skill pack, writes production-ready SKILL.md files, bundles them into sellable tiers, and generates all product copy.

## When to Use

- Creating a new skill pack for a target audience
- Researching what skills a niche needs
- Generating multiple skills in a single session
- Building sellable bundles for Gumroad / AI-DHD
- Expanding the passive income skill catalog
- When SPARKY's overnight research identifies a hot niche

---

## 1. Niche Research Phase

Before writing a single skill, understand the audience.

### Input Required
Ask for ONE of these:
- **Persona**: "freelance web designer" / "real estate agent" / "etsy seller"
- **Pain point**: "client onboarding is chaos" / "can't keep up with social media"
- **Industry**: "property management" / "fitness coaching" / "e-commerce"

### Research Framework

Map the niche across these dimensions:

| Dimension | Question | Example (Freelancer) |
|-----------|----------|---------------------|
| **Daily grind** | What do they do every day that's tedious? | Write proposals, chase invoices |
| **Money leaks** | Where do they lose revenue? | Underpricing, scope creep |
| **Tool gaps** | What tools do they wish existed? | Auto-proposal from call notes |
| **Growth blockers** | What stops them scaling? | Can't systematize client work |
| **Content needs** | What content do they need but hate making? | Case studies, social proof |
| **Admin burden** | What paperwork eats their time? | Contracts, invoices, reports |
| **Decision fatigue** | What choices paralyze them? | Pricing, tech stack, hiring |
| **Knowledge gaps** | What do they need to learn but can't prioritize? | SEO, email marketing |

### Output: Niche Brief

```markdown
## Niche Brief: [Persona]

**Who they are:** [1-2 sentences]
**Their #1 frustration:** [specific, visceral]
**Revenue range:** [helps with pricing]
**Tech comfort:** [low/medium/high — affects skill complexity]
**Buying triggers:** ["I need this NOW" moments]
**Willingness to pay:** [$X-$Y for tools like this]
**Competitive landscape:** [what exists, what's missing]
```

---

## 2. Skill Architecture Phase

Design 5-8 skills that form a coherent system.

### The Skill Pack Formula

Every pack needs this shape:

```
ENTRY SKILL (1) ──→ gets them hooked, quick win
  ↓
CORE SKILLS (3-4) ──→ solve the daily grind
  ↓
POWER SKILLS (1-2) ──→ unlock growth / advanced use
  ↓
CONNECTOR SKILL (1) ──→ ties everything together
```

### Skill Design Template

For each skill in the pack:

```markdown
### [skill-name]
- **Job it does:** [one sentence — what tedious task it eliminates]
- **Input:** [what the user provides]
- **Output:** [what they get back]
- **Wow moment:** [the "holy shit this is useful" reaction]
- **Complexity:** [simple/medium/advanced]
- **Standalone value:** [would someone buy this alone? yes/no]
- **Bundle role:** [entry/core/power/connector]
```

### Naming Convention

Skill names should be:
- **Lowercase hyphenated**: `client-intake-bot`, not `ClientIntakeBot`
- **Action-oriented**: what it DOES, not what it IS
- **Niche-prefixed if needed**: `realestate-listing-writer` for clarity
- **Max 3-4 words**: shorter = better trigger matching

---

## 3. Skill Writing Phase

Write each SKILL.md following the standards.

### SKILL.md Template

```markdown
---
name: [skill-name]
description: >
  [TRIGGER SENTENCE]. [8-15 trigger phrases].
  This skill [what it provides]. Use it [when to use].
---

# [Skill Title]

[1-2 sentence value proposition — what problem this kills]

## What It Does

- [Capability 1 — specific, not vague]
- [Capability 2]
- [Capability 3]
- [Capability 4]

## Quick Start

**[Use case 1]:**
> [Example prompt the user would type]

**[Use case 2]:**
> [Example prompt]

**[Use case 3]:**
> [Example prompt]

---

## [Core Section 1 — The Main Framework]

[Templates, checklists, decision matrices — the MEAT of the skill]
[This section should be 40-60% of the skill's content]
[Use tables, bullet lists, and code blocks — not paragraphs]

## [Core Section 2 — Supporting Framework]

[Secondary workflow or reference material]

## [Core Section 3 — Templates/Examples]

[Copy-paste ready templates the user can immediately use]

---

## Advanced Techniques

- [Power-user tip 1]
- [Power-user tip 2]
- [Power-user tip 3]

## Common Mistakes

- [Mistake 1 — and what to do instead]
- [Mistake 2]
- [Mistake 3]

## Integration Ideas

- Pair with **[skill]** to [benefit]
- Use with **[skill]** when [scenario]
- Connect to **[skill]** for [outcome]

<!--
CHANGELOG:
- [DATE]: Initial creation via Skill Forge
-->
```

### Quality Checklist

Before finalizing each skill:

- [ ] YAML frontmatter has exactly `name` and `description`
- [ ] Description starts with trigger verb (LOAD/USE/ACTIVATE)
- [ ] 8-15 trigger phrases in description
- [ ] Name is lowercase-hyphenated, matches directory name
- [ ] 200-400 lines (max 500)
- [ ] Has Quick Start with 3+ concrete examples
- [ ] Core sections use tables/lists, not walls of text
- [ ] Templates are copy-paste ready
- [ ] Cross-references 3-7 related skills
- [ ] No generic filler — every line earns its place

---

## 4. Bundle Architecture Phase

Group skills into sellable tiers.

### Three-Tier Bundle Model

| Tier | Name Pattern | Skills | Price | Who buys |
|------|-------------|--------|-------|----------|
| **Starter** | "[Niche] Essentials" | 2-3 entry/core | $29-39 | Curious, testing the water |
| **Pro** | "[Niche] Pro Suite" | 4-5 core/power | $59-79 | Committed, wants the system |
| **Complete** | "[Niche] Complete Stack" | All 5-8 | $99-149 | All-in, wants everything |

### Pricing Psychology

- **Starter** = 40% of Complete price (makes Complete feel like a deal)
- **Pro** = 65% of Complete price (most popular — anchoring works)
- **Complete** = anchor price (some buy it, everyone uses it to justify Pro)
- Always show all three side by side
- Mark Pro as "MOST POPULAR" even before you have data

### Bundle Naming Formula

```
[Emotional Outcome] + [Niche Word] + [Container Word]
```

Examples:
- "Effortless Client Pipeline" (freelancer)
- "Listing Domination Kit" (e-commerce)
- "Content Machine Suite" (creator)
- "Revenue Autopilot Stack" (solopreneur)

---

## 5. Product Copy Phase

Generate all copy needed to sell the bundle.

### Gumroad Product Listing

```markdown
# [Bundle Name]

**[One-line hook — the pain this kills]**

## What's Inside

[Bullet list of every skill with one-line description]

## Who This Is For

You're a [persona] who:
- [Pain point 1 — use "you" language]
- [Pain point 2]
- [Pain point 3]

## What Changes

After installing these skills, you'll:
- [Outcome 1 — specific, measurable]
- [Outcome 2]
- [Outcome 3]

## How It Works

1. Download the .skill files
2. Drop them in your `~/claude-skills/` directory
3. Start using them immediately — just describe what you need

## What You Get

| Skill | What It Does | Value |
|-------|-------------|-------|
| [name] | [one line] | $[individual price] |
| ... | ... | ... |
| **Total Value** | | **$[sum]** |
| **Your Price** | | **$[bundle price]** |

---

*Built by [Your Brand]. Works with Claude Code.*
```

### Landing Page Sections (if needed)

Use the `landing-page-recipes` skill for full page builds. Key sections:
1. Hero (pain → solution → CTA)
2. Problem agitation (3 specific frustrations)
3. What's included (skill showcase)
4. Social proof (if available)
5. Pricing table (3 tiers)
6. FAQ (5-7 questions)
7. Final CTA

---

## 6. Packaging Phase

### File Structure

```
[niche]-skill-pack/
  ├── README.md                    # Install instructions + what's inside
  ├── INSTALL.sh                   # One-command installer
  ├── skills/
  │   ├── [skill-1]/SKILL.md
  │   ├── [skill-2]/SKILL.md
  │   └── ...
  └── bonus/
      ├── prompts.md               # 10 power prompts for the niche
      └── workflow-guide.md        # How to use the skills together
```

### Installer Script Template

```bash
#!/bin/bash
# [Pack Name] Installer
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/claude-skills}"

echo "Installing [Pack Name]..."
for skill in skills/*/; do
  name=$(basename "$skill")
  cp -r "$skill" "$SKILLS_DIR/$name"
  echo "  ✓ Installed $name"
done
echo ""
echo "Done! [X] skills installed to $SKILLS_DIR"
echo "Restart Claude Code to activate."
```

### Package as .skill files

```bash
# Package individual skills
for skill_dir in skills/*/; do
  name=$(basename "$skill_dir")
  cd skills && zip -r "../${name}.skill" "$name/" && cd ..
done

# Package complete bundle
zip -r "[niche]-complete-pack.zip" . -x "*.DS_Store" -x "__MACOSX/*"
```

---

## 7. Quality Assurance

### Test Each Skill

For every skill, verify:

1. **Trigger test**: Does saying the trigger phrase load the skill?
2. **Quick start test**: Do the example prompts produce useful output?
3. **Edge case test**: What happens with vague input? Does it ask good questions?
4. **Integration test**: Do cross-references point to real skills?
5. **Size check**: Is it under 500 lines? Over 150?

### Bundle Coherence Check

- [ ] Skills cover the full workflow (not just random tools)
- [ ] No two skills overlap >20% in functionality
- [ ] Entry skill provides immediate value in <2 minutes
- [ ] Power skills justify the price upgrade from Starter to Pro
- [ ] Connector skill makes the bundle worth more than individual skills

---

## 8. Niche Ideas Catalog

Pre-researched niches ready to forge:

| Niche | Pack Name | Key Skills | Est. Price | Market Size |
|-------|-----------|-----------|-----------|-------------|
| Real estate agents | Listing Domination | listing-writer, market-report, open-house-planner, client-followup, social-posts | $79 | Large |
| Fitness coaches | Coach Command Center | program-builder, client-check-in, meal-plan-gen, progress-tracker, content-calendar | $59 | Medium |
| Etsy sellers | Etsy Empire | listing-optimizer, keyword-researcher, photo-guide, pricing-calc, review-responder | $79 | Large |
| Course creators | Course Launch Kit | outline-builder, lesson-scripter, quiz-maker, email-sequence, launch-planner | $99 | Medium |
| Bookkeepers | Practice Autopilot | client-onboarder, report-generator, deadline-tracker, email-templates, scope-guard | $79 | Medium |
| Wedding planners | Wedding Command | timeline-builder, vendor-tracker, budget-calc, client-portal, day-of-checklist | $69 | Niche but $ |
| Podcast hosts | Pod Producer | episode-planner, show-notes-writer, guest-research, clip-maker, growth-tracker | $59 | Growing |
| Therapists/coaches | Practice Builder | intake-form, session-notes, resource-library, scheduling-helper, content-writer | $79 | Underserved |
| Property managers | Property Ops | tenant-comms, maintenance-tracker, lease-generator, inspection-report, owner-update | $89 | High value |
| Music teachers | Studio Manager | lesson-planner, practice-tracker, recital-organizer, parent-comms, repertoire-db | $49 | Niche |

---

## Cross-References

- **skill-file-standards** — Format spec for every SKILL.md
- **skill-creator** — Lower-level skill authoring tool
- **digital-product-pipeline** — Full product lifecycle management
- **landing-page-recipes** — Sales page for each pack
- **pricing-strategy** — Pricing validation and optimization
- **template-builder** — For bonus templates included in packs
- **brand-voice-library** — Consistent voice across all copy
- **github-backup-automation** — Version control for skill packs
- **gumroad-automation** — Auto-setup products on Gumroad

<!--
CHANGELOG:
- 2026-03-09: Initial creation — complete forge pipeline
-->
