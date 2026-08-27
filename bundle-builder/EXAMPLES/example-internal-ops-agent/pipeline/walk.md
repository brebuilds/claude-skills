# Stage — Walk

## What this stage does
Enumerate files from configured source folders. Read-only. Returns a stream of file metadata.

## Inputs
- Source folder paths (from CONTEXT.md)
- Optional: `modified_after` filter (only files newer than X) — for incremental sweeps

## Outputs
Stream of `{path, name, size_bytes, modified, content_hash, preview_url, source}` per file walker output schema.

## Boundary
Read-only. Honors `.locked` sidecars and `_locked/` folders by skipping.

## Per-source notes
(See `tools/file-walker.md` for per-source enumeration status.)
