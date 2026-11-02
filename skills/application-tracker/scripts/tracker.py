#!/usr/bin/env python3
"""Job application tracker backed by a single CSV file (standard library only).

Usage:
  tracker.py init     <csv>
  tracker.py add      <csv> <jobs.json>        # JSON list of job objects; duplicates are merged
  tracker.py update   <csv> <id> field=value [field=value ...]
  tracker.py check    <csv> <company> <title> <location>   # is this job already tracked?
  tracker.py list     <csv> [--status S[,S]] [--min-score N] [--source X] [--limit N]
  tracker.py due      <csv> [--days N]         # applied jobs with no update for N days (default 7)
  tracker.py today    <csv>                    # applications made today, per source (for daily caps)
  tracker.py stats    <csv>

All output is JSON on stdout. Exit code 1 with {"error": ...} on bad input.
"""
import csv
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timedelta

FIELDS = [
    "id", "key", "title", "company", "location", "work_mode", "source", "url", "alt_urls",
    "apply_type", "experience_required", "salary", "posted_date", "found_date", "score",
    "confidence", "recommendation", "gaps", "flags", "status", "applied_date", "resume_used",
    "follow_up_date", "notes", "last_updated",
]
STATUSES = [
    "found", "shortlisted", "skipped", "needs_user", "applied", "viewed", "interview",
    "offer", "rejected", "withdrawn", "expired",
]
# Status that should never be overwritten by a re-discovery of the same job.
PROTECTED = {"applied", "viewed", "interview", "offer", "rejected", "withdrawn"}

COMPANY_NOISE = re.compile(
    r"\b(pvt|private|ltd|limited|llp|inc|incorporated|corp|corporation|co|company|"
    r"technologies|technology|tech|solutions|services|software|india|global|labs)\b\.?",
    re.I,
)
# Strip only bracketed text that is location/work-mode noise, e.g. "(Remote)", "[Noida]"; keep
# meaningful qualifiers such as "(Generative AI, ML, AWS)" so different roles don't merge.
NOISE_WORDS = r"remote|hybrid|onsite|on-site|wfh|work from home|urgent|hiring|immediate joiners?|bangalore|bengaluru|noida|gurgaon|gurugram|delhi|ncr|mumbai|pune|hyderabad|chennai|kolkata|india"
TITLE_NOISE = re.compile(r"[\(\[]\s*(?:" + NOISE_WORDS + r")(?:\s*[/,|-]\s*(?:" + NOISE_WORDS + r"))*\s*[\)\]]|\b(remote|hybrid|onsite|on-site|wfh|urgent|hiring|immediate joiner[s]?)\b", re.I)
CITY_ALIASES = {
    "bengaluru": "bangalore", "gurugram": "gurgaon", "bombay": "mumbai", "new delhi": "delhi",
    "madras": "chennai", "calcutta": "kolkata", "navi mumbai": "mumbai", "noida": "delhi ncr",
    "delhi": "delhi ncr", "gurgaon": "delhi ncr", "ghaziabad": "delhi ncr", "faridabad": "delhi ncr",
}


def fail(msg):
    print(json.dumps({"error": msg}))
    sys.exit(1)


def norm_text(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9+#. ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_company(s):
    return norm_text(COMPANY_NOISE.sub(" ", s or "")) or norm_text(s)


def norm_title(s):
    return norm_text(TITLE_NOISE.sub(" ", s or "")) or norm_text(s)


def norm_city(s):
    s = norm_text((s or "").split(",")[0])
    if "remote" in s or "work from home" in s:
        return "remote"
    seen = set()
    while s in CITY_ALIASES and s not in seen:  # follow chains, e.g. gurugram -> gurgaon -> delhi ncr
        seen.add(s)
        s = CITY_ALIASES[s]
    return s


def same_site(a, b):
    host = lambda u: re.sub(r"^(www|in|m)\.", "", (re.match(r"https?://([^/]+)", u or "") or [None, ""])[1].lower())
    return host(a) == host(b) and host(a) != ""


def make_key(company, title, location):
    return f"{norm_company(company)}|{norm_title(title)}|{norm_city(location)}"


def load(path):
    if not os.path.exists(path):
        fail(f"tracker not found: {path} (run init first)")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            # Tolerate files created by an older version: fill missing columns.
            rows.append({k: (r.get(k) or "") for k in FIELDS})
        return rows


def save(path, rows):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        os.replace(tmp, path)  # atomic: never leaves a half-written tracker
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def next_id(rows):
    nums = [int(r["id"][1:]) for r in rows if re.fullmatch(r"J\d+", r.get("id", ""))]
    return f"J{(max(nums) + 1) if nums else 1:04d}"


def today():
    return date.today().isoformat()


def cmd_init(path):
    if os.path.exists(path):
        print(json.dumps({"ok": True, "message": "tracker already exists", "rows": len(load(path))}))
        return
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    save(path, [])
    print(json.dumps({"ok": True, "message": "created", "path": path}))


def cmd_add(path, jobs_path):
    rows = load(path)
    try:
        with open(jobs_path, encoding="utf-8") as f:
            jobs = json.load(f)
    except Exception as e:
        fail(f"could not read jobs JSON: {e}")
    if isinstance(jobs, dict):
        jobs = [jobs]
    if not isinstance(jobs, list):
        fail("jobs JSON must be an object or a list of objects")

    by_key = {r["key"]: r for r in rows}
    by_url = {}
    for r in rows:
        for u in [r["url"]] + [x for x in r["alt_urls"].split(" ") if x]:
            if u:
                by_url[u] = r

    added, merged, skipped_invalid = [], [], []
    for j in jobs:
        if not isinstance(j, dict) or not j.get("title") or not j.get("company"):
            skipped_invalid.append(j)
            continue
        key = make_key(j.get("company"), j.get("title"), j.get("location"))
        url = (j.get("url") or "").strip()
        existing = by_url.get(url) if url else None
        if not existing:
            cand = by_key.get(key)
            # Same company+title+city but a different posting URL on the SAME site = a separate posting.
            if cand and url and cand["url"] and same_site(cand["url"], url) and cand["url"] != url:
                cand = None
            existing = cand
        if existing:
            # Merge: record the extra URL, fill blanks, refresh score; never downgrade status.
            if url and url != existing["url"] and url not in existing["alt_urls"].split(" "):
                existing["alt_urls"] = (existing["alt_urls"] + " " + url).strip()
            for k in FIELDS:
                if k in ("id", "key", "url", "alt_urls", "status", "found_date"):
                    continue
                v = j.get(k)
                if v not in (None, "") and (not existing[k] or k in ("score", "confidence", "recommendation", "gaps", "flags")):
                    existing[k] = str(v)
            new_status = j.get("status")
            if new_status in STATUSES and existing["status"] not in PROTECTED:
                existing["status"] = new_status
            existing["last_updated"] = today()
            merged.append(existing["id"])
            continue
        row = {k: "" for k in FIELDS}
        for k in FIELDS:
            if j.get(k) not in (None, ""):
                row[k] = str(j[k]) if not isinstance(j[k], list) else " ".join(map(str, j[k]))
        row["id"] = next_id(rows)
        row["key"] = key
        row["url"] = url
        row["status"] = j.get("status") if j.get("status") in STATUSES else "found"
        row["found_date"] = row["found_date"] or today()
        row["last_updated"] = today()
        rows.append(row)
        by_key[key] = row
        if url:
            by_url[url] = row
        added.append(row["id"])

    save(path, rows)
    print(json.dumps({"ok": True, "added": added, "merged_duplicates": sorted(set(merged)),
                      "invalid_skipped": len(skipped_invalid), "total_rows": len(rows)}))


def cmd_update(path, job_id, pairs):
    rows = load(path)
    row = next((r for r in rows if r["id"] == job_id or r["key"] == job_id), None)
    if not row:
        fail(f"job not found: {job_id}")
    changes = {}
    for p in pairs:
        if "=" not in p:
            fail(f"expected field=value, got: {p}")
        k, v = p.split("=", 1)
        if k not in FIELDS or k in ("id", "key"):
            fail(f"unknown or read-only field: {k}")
        if k == "status":
            if v not in STATUSES:
                fail(f"invalid status '{v}'. Allowed: {', '.join(STATUSES)}")
            if v == "applied" and not row["applied_date"] and not any(x.startswith("applied_date=") for x in pairs):
                row["applied_date"] = today()
                changes["applied_date"] = row["applied_date"]
        if k in ("applied_date", "follow_up_date", "posted_date", "found_date") and v:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                fail(f"{k} must be YYYY-MM-DD, got: {v}")
        row[k] = v
        changes[k] = v
    row["last_updated"] = today()
    save(path, rows)
    print(json.dumps({"ok": True, "id": row["id"], "changes": changes}))


def cmd_check(path, company, title, location):
    rows = load(path)
    key = make_key(company, title, location)
    hits = [r for r in rows if r["key"] == key]
    # Also flag same company + same title in any city (possible repost).
    near = [r for r in rows if r["key"] != key and r["key"].split("|")[:2] == key.split("|")[:2]]
    print(json.dumps({"key": key, "tracked": bool(hits),
                      "matches": [{"id": r["id"], "status": r["status"], "url": r["url"]} for r in hits],
                      "same_role_other_city": [{"id": r["id"], "location": r["location"], "status": r["status"]} for r in near]}))


def parse_opts(args):
    opts, i = {}, 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            opts[args[i][2:]] = args[i + 1]
            i += 2
        else:
            fail(f"unexpected argument: {args[i]}")
    return opts


def to_num(s, default=-1.0):
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


def cmd_list(path, args):
    o = parse_opts(args)
    rows = load(path)
    if "status" in o:
        wanted = set(o["status"].split(","))
        bad = wanted - set(STATUSES)
        if bad:
            fail(f"invalid status: {', '.join(bad)}")
        rows = [r for r in rows if r["status"] in wanted]
    if "min-score" in o:
        rows = [r for r in rows if to_num(r["score"]) >= to_num(o["min-score"], 0)]
    if "source" in o:
        rows = [r for r in rows if r["source"].lower() == o["source"].lower()]
    rows.sort(key=lambda r: to_num(r["score"]), reverse=True)
    if "limit" in o:
        rows = rows[: int(o["limit"])]
    cols = ["id", "title", "company", "location", "source", "score", "recommendation", "status", "apply_type", "url"]
    print(json.dumps([{c: r[c] for c in cols} for r in rows], ensure_ascii=False))


def cmd_due(path, args):
    o = parse_opts(args)
    days = int(o.get("days", 7))
    cutoff = date.today() - timedelta(days=days)
    out = []
    for r in load(path):
        if r["status"] not in ("applied", "viewed"):
            continue
        fu = r["follow_up_date"]
        if fu:
            try:
                if datetime.strptime(fu, "%Y-%m-%d").date() <= date.today():
                    out.append(r)
            except ValueError:
                pass
            continue
        last = r["last_updated"] or r["applied_date"]
        try:
            if last and datetime.strptime(last, "%Y-%m-%d").date() <= cutoff:
                out.append(r)
        except ValueError:
            pass
    print(json.dumps([{c: r[c] for c in ("id", "title", "company", "applied_date", "status", "url")} for r in out]))


def cmd_today(path):
    counts = {}
    for r in load(path):
        if r["applied_date"] == today():
            counts[r["source"] or "unknown"] = counts.get(r["source"] or "unknown", 0) + 1
    print(json.dumps({"date": today(), "applied_today": counts, "total": sum(counts.values())}))


def cmd_stats(path):
    rows = load(path)
    by_status, by_source = {}, {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        by_source[r["source"] or "unknown"] = by_source.get(r["source"] or "unknown", 0) + 1
    applied = sum(by_status.get(s, 0) for s in PROTECTED)
    responded = sum(by_status.get(s, 0) for s in ("viewed", "interview", "offer", "rejected"))
    print(json.dumps({"total": len(rows), "by_status": by_status, "by_source": by_source,
                      "applied_or_later": applied,
                      "response_rate": round(responded / applied, 2) if applied else None}))


def main(argv):
    if len(argv) < 3:
        fail(__doc__.strip())
    cmd, path, rest = argv[1], argv[2], argv[3:]
    if cmd == "init":
        cmd_init(path)
    elif cmd == "add":
        if len(rest) != 1:
            fail("usage: add <csv> <jobs.json>")
        cmd_add(path, rest[0])
    elif cmd == "update":
        if len(rest) < 2:
            fail("usage: update <csv> <id> field=value ...")
        cmd_update(path, rest[0], rest[1:])
    elif cmd == "check":
        if len(rest) != 3:
            fail("usage: check <csv> <company> <title> <location>")
        cmd_check(path, *rest)
    elif cmd == "list":
        cmd_list(path, rest)
    elif cmd == "due":
        cmd_due(path, rest)
    elif cmd == "today":
        cmd_today(path)
    elif cmd == "stats":
        cmd_stats(path)
    else:
        fail(f"unknown command: {cmd}")


if __name__ == "__main__":
    main(sys.argv)
