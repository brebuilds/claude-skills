#!/usr/bin/env python3
"""
Receipts store helper.

  receipts.py init             create the store scaffold (idempotent)
  receipts.py merge            fan in observations.d/ claims.d/ metrics.d/ -> *.jsonl
  receipts.py status           coverage report: sources, projects, claims by tier
  receipts.py claims [--tier T] [--project P]
  receipts.py unpromoted       VERIFIED/USER_CONFIRMED claims not yet in POOL.md

Fan-in exists because parallel analysis agents each write their own file. Appending
to one shared JSONL from several processes interleaves partial lines and corrupts it.
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict

STORE = os.path.expanduser("~/claude-private/resume/receipts")

STREAMS = {
    "observations": "observations.d",
    "claims": "claims.d",
    "metrics": "metrics.d",
}

MARKDOWN_SEEDS = {
    "signals.md": "# Career signals\n\n*Capabilities demonstrated across projects. "
                  "A signal in one project is a data point; across four it is a pattern.*\n",
    "unclaimed.md": "# Unclaimed\n\n*Real, evidenced work that appears in no résumé, "
                    "portfolio, brag sheet or LinkedIn entry. Reconcile with POOL.md §10.*\n",
    "questions.md": "# Open questions\n\n*Ranked by expected information gain. "
                    "Ask ONE at a time. Mark `asked-unresolved` so it is not re-asked.*\n",
    "conflicts.md": "# Conflicts\n\n*Sources disagree. Never silently resolved — the user decides.*\n",
}

TIER_ORDER = ["VERIFIED", "USER_CONFIRMED", "APPROXIMATE",
              "INFERRED", "CONFLICTING", "UNKNOWN"]

POOLABLE = {"VERIFIED", "USER_CONFIRMED", "APPROXIMATE"}


def latest_by_id(rows):
    """Collapse an append-only stream to one row per id, last line winning.

    The store is append-only: a correction is a NEW line carrying the SAME id and
    a later `at`. Every read path must collapse here, or a corrected claim gets
    counted twice and the tier distribution silently lies.
    """
    latest = {}
    order = []
    for row in rows:
        rid = row.get("id")
        if rid is None:
            order.append(row)
            continue
        if rid not in latest:
            order.append(rid)
        latest[rid] = row
    return [latest[o] if isinstance(o, str) else o for o in order]


def read_jsonl(path):
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"  ! malformed line {path}:{lineno} (skipped)", file=sys.stderr)
    return rows


def cmd_init(_args):
    for sub in ["projects", "scans"] + list(STREAMS.values()):
        os.makedirs(os.path.join(STORE, sub), exist_ok=True)
    for stream in STREAMS:
        path = os.path.join(STORE, f"{stream}.jsonl")
        if not os.path.exists(path):
            open(path, "a", encoding="utf-8").close()
    path = os.path.join(STORE, "sources.jsonl")
    if not os.path.exists(path):
        open(path, "a", encoding="utf-8").close()
    for name, seed in MARKDOWN_SEEDS.items():
        full = os.path.join(STORE, name)
        if not os.path.exists(full):
            with open(full, "w", encoding="utf-8") as handle:
                handle.write(seed)
    print(f"store ready: {STORE}")
    return 0


def cmd_merge(_args):
    total = 0
    for stream, subdir in STREAMS.items():
        src_dir = os.path.join(STORE, subdir)
        target = os.path.join(STORE, f"{stream}.jsonl")
        if not os.path.isdir(src_dir):
            continue

        # Dedupe on CONTENT, not on id alone. An id that already exists but whose
        # content differs is a *correction* and must be allowed through — dropping it
        # would make the append-only correction model unusable via this path, which is
        # the documented way agent output enters the store. Only an exact re-run of the
        # same row is skipped.
        latest = {}
        for row in read_jsonl(target):
            if row.get("id"):
                latest[row["id"]] = row

        added, corrected = 0, 0
        parts = sorted(f for f in os.listdir(src_dir) if f.endswith(".jsonl"))
        with open(target, "a", encoding="utf-8") as out:
            for part in parts:
                for row in read_jsonl(os.path.join(src_dir, part)):
                    rid = row.get("id")
                    if rid and rid in latest:
                        if latest[rid] == row:
                            continue          # exact duplicate, nothing to record
                        corrected += 1        # same id, new content -> correction
                    if rid:
                        latest[rid] = row
                    out.write(json.dumps(row, ensure_ascii=False) + "\n")
                    added += 1
        for part in parts:
            os.rename(os.path.join(src_dir, part),
                      os.path.join(src_dir, part + ".merged"))
        if parts:
            note = f" ({corrected} correction(s))" if corrected else ""
            print(f"{stream}: +{added} from {len(parts)} file(s){note}")
        total += added
    if total == 0:
        print("nothing to merge")
    return 0


def cmd_status(_args):
    sources = latest_by_id(read_jsonl(os.path.join(STORE, "sources.jsonl")))
    observations = latest_by_id(read_jsonl(os.path.join(STORE, "observations.jsonl")))
    claims = latest_by_id(read_jsonl(os.path.join(STORE, "claims.jsonl")))
    metrics = latest_by_id(read_jsonl(os.path.join(STORE, "metrics.jsonl")))

    proj_dir = os.path.join(STORE, "projects")
    records = sorted(f[:-3] for f in os.listdir(proj_dir)) if os.path.isdir(proj_dir) else []

    print("RECEIPTS — coverage\n")
    print(f"  sources ingested      {len(sources)}")
    print(f"  observations          {len(observations)}")
    print(f"  claims                {len(claims)}")
    print(f"  metrics               {len(metrics)}")
    print(f"  project records       {len(records)}")

    if claims:
        tiers = Counter(c.get("tier", "UNKNOWN") for c in claims)
        print("\n  claims by tier")
        for tier in TIER_ORDER:
            if tiers.get(tier):
                flag = "" if tier in POOLABLE else "   (not résumé-eligible)"
                print(f"    {tier:<16} {tiers[tier]:>4}{flag}")

        poolable = [c for c in claims if c.get("tier") in POOLABLE]
        unpromoted = [c for c in poolable if c.get("pool_status") == "unpromoted"]
        print(f"\n  résumé-eligible       {len(poolable)}")
        print(f"  awaiting promotion    {len(unpromoted)}")

    if records:
        by_project = defaultdict(Counter)
        for claim in claims:
            by_project[claim.get("project", "?")][claim.get("tier", "UNKNOWN")] += 1
        print("\n  per project")
        for slug in records:
            counts = by_project.get(slug, Counter())
            strong = sum(counts[t] for t in POOLABLE)
            print(f"    {slug:<28} {strong} eligible / {sum(counts.values())} claims")

    questions = os.path.join(STORE, "questions.md")
    if os.path.exists(questions):
        with open(questions, encoding="utf-8") as handle:
            open_q = sum(1 for line in handle
                         if line.strip().startswith("- [ ]"))
        print(f"\n  open questions        {open_q}")
    return 0


def cmd_claims(args):
    claims = latest_by_id(read_jsonl(os.path.join(STORE, "claims.jsonl")))
    for claim in claims:
        if args.tier and claim.get("tier") != args.tier:
            continue
        if args.project and claim.get("project") != args.project:
            continue
        print(f"[{claim.get('tier','?'):<14}] {claim.get('project','?'):<22} "
              f"{claim.get('statement','')}")
    return 0


def cmd_unpromoted(_args):
    claims = latest_by_id(read_jsonl(os.path.join(STORE, "claims.jsonl")))
    rows = [c for c in claims
            if c.get("tier") in POOLABLE and c.get("pool_status") == "unpromoted"]
    if not rows:
        print("nothing awaiting promotion")
        return 0
    print("Résumé-eligible, not yet in POOL.md:\n")
    for claim in rows:
        print(f"  [{claim.get('tier')}] {claim.get('project')}")
        print(f"      {claim.get('statement')}")
        print(f"      supports: {', '.join(claim.get('supports', [])) or '(none)'}\n")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Receipts store helper")
    subs = parser.add_subparsers(dest="cmd", required=True)
    subs.add_parser("init")
    subs.add_parser("merge")
    subs.add_parser("status")
    claims = subs.add_parser("claims")
    claims.add_argument("--tier")
    claims.add_argument("--project")
    subs.add_parser("unpromoted")

    args = parser.parse_args()
    return {
        "init": cmd_init, "merge": cmd_merge, "status": cmd_status,
        "claims": cmd_claims, "unpromoted": cmd_unpromoted,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
