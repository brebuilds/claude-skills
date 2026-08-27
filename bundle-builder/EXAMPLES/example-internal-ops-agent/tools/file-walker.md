# Tool — File Walker

## Status
Needs build (partial).

## What this agent uses it for
Read-only enumeration of source folders. For each file: path, name, size, modified date, content hash (for de-dup), preview (if available).

## Per-source status
- Drive: API works, OAuth done per `reference_hetzner_rclone_gdrive` memory (rclone read-only)
- Dropbox: needs OAuth + listing implementation
- Local: standard FS walk, already trivial

## Output schema
```json
{
  "path": "string",
  "name": "string",
  "size_bytes": 0,
  "modified": "ISO timestamp",
  "content_hash": "sha256",
  "preview_url": "string|null",
  "source": "drive|dropbox|local"
}
```

## Boundary
READ-ONLY. Never modifies, moves, or deletes.
