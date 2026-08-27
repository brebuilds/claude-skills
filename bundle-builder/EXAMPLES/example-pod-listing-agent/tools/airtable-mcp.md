# Tool — Airtable MCP

## Status
Exists. Already configured.

## What this agent uses it for

**Reads:**
- `Designs` row by ID — title, SKU code, brand link, category link, tags, source files attachment
- `Brand Info` row for OIB.Guide (`[OIB Brand Info record ID]`) — SKU prefix, brand fields
- `Listing Templates` row matched to the target Product Type — title formula, base tags, pricing rules
- `Product Type` row by blueprint ID match — SKU code, category link
- `Categories` row linked from Product Type — SKU code
- `Listings` row(s) for this Design × Brand to check duplicates

**Writes:**
- `Listings` row — Title, Description, Tags, Design link, Brand link, Product Type link, Pricing, Sync Status = `ready-to-publish`

## Base + table IDs

- Base: `[production base ID]`
- Designs: `[Designs table ID]`
- Listings: `[Listings table ID]`
- Listing Templates: `[Listing Templates table ID]`
- Brand Info: `[Brand Info table ID]`
- Product Type: `[Product Type table ID]`
- Categories: `[Categories table ID]`

## Gotchas

- Record-link fields come back as plain string IDs from REST, not `{id, name}` objects. The MCP wraps them differently. If reading via raw REST, expect strings.
- `SKU Code` field exists on multiple tables. Always namespace mentally: Brand.SKU Code = prefix, Designs.SKU Code = per-design code, Product Type.SKU Code = product type code, Category.SKU Code = category code, Sizes/Colors.SKU Code = axis code.
- Rate limit: ~5 requests/sec per base. Batch where possible.
