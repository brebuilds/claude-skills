#!/usr/bin/env python3
"""
Receipts pre-flight secret scanner (spec §20).

Deterministic. Runs BEFORE any repository or folder content reaches model
context. Produces a manifest partitioning files into:

  safe        -> may be read by an analysis agent
  quarantined -> a secret pattern or secret-bearing filename matched
  skipped     -> binary / vendored / generated, not worth reading

INVARIANT: this script never emits a matched secret value. It emits
path + rule name + line number only. That is enough to act on and
impossible to leak.

Usage:
  scan_secrets.py <path> [--json out.json] [--max-bytes N]

Exit codes:
  0  scan completed (check manifest["quarantined"] for findings)
  2  path does not exist
"""

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Filename-level exclusions. A file matching these NEVER gets read, regardless
# of content. Cheaper and safer than content-scanning a .env.
# ---------------------------------------------------------------------------
# Extensions that hold CODE, not data. A file named secrets.tsx is almost
# always code that *handles* secrets (real career evidence) rather than a file
# that *contains* them, so these fall through to content scanning instead of
# being quarantined on name alone. Over-quarantining destroys evidence.
CODE_EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".rb", ".go", ".rs",
    ".java", ".kt", ".swift", ".php", ".c", ".h", ".cpp", ".cs", ".sh", ".zsh",
    ".bash", ".sql", ".vue", ".svelte", ".astro", ".md", ".mdx", ".tf", ".hcl",
}

# .env.example / .env.sample / .env.template document required variables
# without holding real values. They are strong architecture evidence, so they
# get content-scanned rather than blanket-quarantined.
ENV_TEMPLATE = re.compile(r"^\.env\.(example|sample|template|dist)$", re.I)

SECRET_FILENAMES = [
    (re.compile(r"^\.env($|\.)"), "dotenv"),
    (re.compile(r"^\.npmrc$"), "npmrc"),
    (re.compile(r"^\.netrc$"), "netrc"),
    (re.compile(r"^\.pgpass$"), "pgpass"),
    (re.compile(r"^id_(rsa|dsa|ecdsa|ed25519)$"), "ssh-private-key"),
    (re.compile(r"\.(pem|key|p12|pfx|jks|keystore)$"), "key-material"),
    (re.compile(r"^(credentials|secrets?|token|tokens)(\.|$)"), "credential-file"),
    (re.compile(r"service[-_]account.*\.json$"), "gcp-service-account"),
    (re.compile(r"^\.?terraform\.tfstate"), "terraform-state"),
    (re.compile(r"^\.htpasswd$"), "htpasswd"),
]

# Directories never descended into.
SKIP_DIRS = {
    ".git", "node_modules", ".next", ".nuxt", ".svelte-kit", "dist", "build",
    "out", "coverage", "__pycache__", ".pytest_cache", ".mypy_cache",
    "venv", ".venv", "env", ".tox", "vendor", ".terraform", ".gradle",
    "Pods", "DerivedData", ".idea", ".vscode", ".cache", ".parcel-cache",
    "target", ".turbo", ".vercel", ".serverless", "bower_components",
}

# Extensions we never send to a model (binary or noise).
SKIP_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".tiff", ".psd",
    ".ai", ".eps", ".svg", ".pdf", ".zip", ".gz", ".tar", ".bz2", ".xz", ".7z",
    ".mp4", ".mov", ".avi", ".mkv", ".webm", ".mp3", ".wav", ".flac", ".aiff",
    ".woff", ".woff2", ".ttf", ".otf", ".eot", ".dylib", ".so", ".dll", ".exe",
    ".o", ".a", ".class", ".jar", ".wasm", ".pyc", ".db", ".sqlite", ".sqlite3",
    ".lock", ".map", ".min.js", ".min.css",
}

# Lockfiles: huge, zero career signal, skip by exact name.
SKIP_NAMES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
    "poetry.lock", "Gemfile.lock", "composer.lock", "Cargo.lock",
    ".DS_Store", "go.sum",
}

# ---------------------------------------------------------------------------
# Content patterns. Prefix-anchored on real credential formats, so false
# positives stay low. Order does not matter; first match wins per line.
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "anthropic-key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{32,}"), "openai-key"),
    (re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}"), "github-token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}"), "github-pat"),
    (re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}"), "gitlab-pat"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "aws-access-key"),
    (re.compile(r"\bASIA[0-9A-Z]{16}\b"), "aws-temp-key"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}"), "slack-token"),
    (re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), "google-api-key"),
    (re.compile(r"\bshpat_[a-fA-F0-9]{32}\b"), "shopify-token"),
    (re.compile(r"\bshpss_[a-fA-F0-9]{32}\b"), "shopify-secret"),
    (re.compile(r"\bpat[A-Za-z0-9]{14}\.[a-f0-9]{64}\b"), "airtable-pat"),
    (re.compile(r"\bkey[A-Za-z0-9]{14}\b(?=.*airtable)", re.I), "airtable-key"),
    (re.compile(r"\bre_[A-Za-z0-9_]{20,}"), "resend-key"),
    (re.compile(r"\bnpm_[A-Za-z0-9]{36}\b"), "npm-token"),
    (re.compile(r"\bSG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}"), "sendgrid-key"),
    (re.compile(r"\bsk_(live|test)_[A-Za-z0-9]{20,}"), "stripe-key"),
    (re.compile(r"\brk_(live|test)_[A-Za-z0-9]{20,}"), "stripe-restricted"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private-key-block"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\."), "jwt"),
    (re.compile(r"\bhttps?://[^/\s:@]+:[^/\s@]+@[^\s\"'<>]+"), "url-with-password"),
    (re.compile(r"\b(postgres|postgresql|mysql|mongodb(\+srv)?|redis|amqp)://"
                r"[^/\s:@]+:[^/\s@]+@"), "db-connection-string"),
    # Generic assignment: KEY = "long-opaque-value". Kept last, tightest bounds.
    (re.compile(r"(?i)\b(api[_\-]?key|secret|password|passwd|token|auth[_\-]?token|"
                r"access[_\-]?token|private[_\-]?key|client[_\-]?secret)\b"
                r"\s*[:=]\s*[\"'][A-Za-z0-9_\-\.\/\+]{24,}[\"']"), "generic-assignment"),
]

# Lines matching these are exempt from generic-assignment (docs, types, examples).
BENIGN_HINTS = re.compile(
    r"(?i)(process\.env|os\.environ|getenv|import\.meta\.env|"
    r"your[_\-]?(api[_\-]?key|token|secret)|<[a-z_]+>|xxx+|\.\.\.|"
    r"example|placeholder|redacted|dummy|changeme|\$\{|\{\{)"
)


def is_secret_filename(name: str):
    """Filename-level verdict, or None to fall through to content scanning."""
    lowered = name.lower()

    # Env templates document architecture without holding values -> content scan.
    if ENV_TEMPLATE.match(lowered):
        return None

    # Source files keep their evidence value; judge them by content, not name.
    _, ext = os.path.splitext(lowered)
    if ext in CODE_EXTS:
        return None

    for pattern, rule in SECRET_FILENAMES:
        if pattern.search(lowered):
            return rule
    return None


def should_skip(name: str) -> bool:
    if name in SKIP_NAMES:
        return True
    lowered = name.lower()
    for ext in SKIP_EXTS:
        if lowered.endswith(ext):
            return True
    return False


def scan_file(path: str, max_bytes: int):
    """Return list of {rule, line} findings. Never returns matched text."""
    findings = []
    try:
        size = os.path.getsize(path)
        if size > max_bytes:
            return [{"rule": "oversize", "line": 0}]
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            for lineno, line in enumerate(handle, 1):
                if len(line) > 4000:
                    line = line[:4000]
                for pattern, rule in SECRET_PATTERNS:
                    if pattern.search(line):
                        if rule == "generic-assignment" and BENIGN_HINTS.search(line):
                            continue
                        findings.append({"rule": rule, "line": lineno})
                        break
    except (OSError, UnicodeDecodeError):
        return [{"rule": "unreadable", "line": 0}]
    return findings


def walk(root: str, max_bytes: int):
    safe, quarantined, skipped = [], [], []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".claude")]
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)

            rule = is_secret_filename(name)
            if rule:
                quarantined.append({"path": rel, "reason": "filename", "rule": rule})
                continue

            if should_skip(name):
                skipped.append(rel)
                continue

            findings = scan_file(full, max_bytes)
            hard = [f for f in findings if f["rule"] not in ("oversize", "unreadable")]
            if hard:
                quarantined.append({
                    "path": rel,
                    "reason": "content",
                    "rule": hard[0]["rule"],
                    "line": hard[0]["line"],
                    "hits": len(hard),
                })
            elif findings:
                skipped.append(rel)
            else:
                safe.append(rel)

    return safe, quarantined, skipped


def main():
    parser = argparse.ArgumentParser(description="Receipts pre-flight secret scanner")
    parser.add_argument("path")
    parser.add_argument("--json", dest="out")
    parser.add_argument("--max-bytes", type=int, default=400_000)
    args = parser.parse_args()

    root = os.path.abspath(os.path.expanduser(args.path))
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    safe, quarantined, skipped = walk(root, args.max_bytes)
    manifest = {
        "root": root,
        "counts": {
            "safe": len(safe),
            "quarantined": len(quarantined),
            "skipped": len(skipped),
        },
        "safe": sorted(safe),
        "quarantined": sorted(quarantined, key=lambda q: q["path"]),
        "skipped": sorted(skipped),
    }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2)

    print(f"safe={len(safe)}  quarantined={len(quarantined)}  skipped={len(skipped)}")
    for item in manifest["quarantined"][:40]:
        loc = f":{item['line']}" if "line" in item else ""
        print(f"  QUARANTINE  {item['path']}{loc}  [{item['rule']}]")
    if len(quarantined) > 40:
        print(f"  ... and {len(quarantined) - 40} more")
    if args.out:
        print(f"manifest -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
