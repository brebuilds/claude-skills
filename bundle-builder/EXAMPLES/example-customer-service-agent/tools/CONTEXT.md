# Brightside Inquiry Handler — Tools

Three load-bearing tools.

## Tools

| Tool | Status | What it does |
|---|---|---|
| `communication-channel.md` | exists (Vapi voice AI per project_brightside_voice_ai) | Inbound channel — voice call, transcribed to text, or webhook from contact form |
| `knowledge-base.md` | needs build (per-location) | Location-specific FAQ + policy lookup. Format TBD (Airtable, Notion, or vector DB). |
| `escalation.md` | needs build | Routes flagged inquiries to the right human contact per location |

## What we DON'T use here

- Direct patient-record access — out of scope, NEVER allowed.
- Outbound marketing — different agent.
- Scheduling system writes — read-only until human confirms (per boundary).
