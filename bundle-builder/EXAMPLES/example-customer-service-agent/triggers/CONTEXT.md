# Brightside Inquiry Handler — Triggers

Event-driven. One invocation per inquiry.

## Invocation patterns

- **Vapi webhook** — voice call transcript posted to agent endpoint
- **Contact form submission** — form payload routed to agent
- **Email** — IMAP/forwarder lands inquiry as agent input
- **Manual review queue** — flagged-and-rerouted inquiries from a human

## Per-location routing

On invocation, the location identifier (Riverside / Northgate / Harborview) determines which `brand-vault/<location>/` to read. Without a location, the agent refuses.

## See also

- `inquiry-received.md` — the step-by-step flow per invocation
