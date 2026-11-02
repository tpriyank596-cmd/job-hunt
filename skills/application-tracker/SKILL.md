---
name: application-tracker
description: "This skill should be used when the user asks \"show my job tracker\", \"what have I applied to\", \"mark this job as applied / rejected / interview\", \"which applications need follow-up\", \"job hunt stats\", \"how many did I apply today\", \"export my applications to a spreadsheet\", or when job-search, job-match or apply-assist need to record or check jobs. It keeps one deduplicated record of every job found, scored and applied to.\n"
metadata:
  version: "0.1.0"
---

# Application Tracker

Keep one source of truth for every job: found, scored, applied, and what happened after. All job-hunt skills read and write it, which prevents duplicate applications and powers follow-ups and daily caps.

## Storage

- File: `job-hunt/tracker.csv`, next to `job-profile.md`.
- Location priority: the user's connected computer folder (persists) → the working directory (then send the file to the user at the end and remind them to attach it next time).
- Manage it **only** through the bundled script so deduplication and validation stay consistent:
  `python3 ${CLAUDE_PLUGIN_ROOT}/skills/application-tracker/scripts/tracker.py <command> <csv> ...`
  If `${CLAUDE_PLUGIN_ROOT}` is not set, locate `tracker.py` inside this skill's `scripts/` folder.
- Back up before bulk changes: copy the CSV to `tracker.backup.csv` once per session before the first write.

## Commands

| Command | Use |
| --- | --- |
| `init <csv>` | Create the tracker (safe to run when it exists) |
| `add <csv> <jobs.json>` | Add jobs from a JSON list; duplicates are merged, not added twice |
| `update <csv> <id> field=value ...` | Change status, notes, dates, resume used, etc. |
| `check <csv> <company> <title> <location>` | Before applying: is this job already tracked/applied? Also lists the same role in other cities |
| `list <csv> [--status S] [--min-score N] [--source X] [--limit N]` | Filtered, score-sorted list |
| `due <csv> [--days N]` | Applied jobs with no update in N days (default 7) or a passed follow-up date |
| `today <csv>` | Applications made today per platform (for daily caps) |
| `stats <csv>` | Totals by status and source, response rate |

Job JSON fields (only `title` and `company` are required): `title, company, location, work_mode, source, url, apply_type, experience_required, salary, posted_date, score, confidence, recommendation, gaps, flags, status, resume_used, notes`.

Statuses: `found → shortlisted → applied → viewed → interview → offer`, plus `skipped`, `needs_user` (blocked on the user: CAPTCHA, external portal account, unanswerable question), `rejected`, `withdrawn`, `expired`. The script refuses unknown statuses and never downgrades a job that is already applied or later when it's found again.

## Behaviour

- **Write JSON to a temp file** in the scratchpad, then call `add`. Never hand-edit the CSV.
- **Dedupe** is by normalized company + title + city (handles "Pvt Ltd", "(Remote)", Bengaluru/Bangalore, Gurugram/Gurgaon/Delhi NCR) and by URL. Alternate URLs from other platforms are kept in `alt_urls`.
- **Before any application**, run `check`. If tracked with status applied or later, stop and tell the user. If the same role exists in another city with status applied, ask before applying again.
- **When showing the tracker** to the user, present a short readable list (title, company, status, score, date). For a spreadsheet view, build an .xlsx from the CSV with the xlsx skill (frozen header, filters, status column color-coded) - only when asked.
- **Follow-ups:** when `due` returns jobs, suggest a short follow-up message (drafted by resume-tailor) - never send it without approval.
- **User-reported updates** ("I got an interview call from Acme"): find the row by company and title, confirm if more than one matches, then update.

## Edge cases

- **Tracker file missing** but the user says they've been applying: ask them to attach it; if lost, start a new one and offer to rebuild history from the platforms' "Applied jobs" pages in logged-in mode.
- **Corrupted or hand-edited CSV:** the script fills missing columns; if parsing fails, restore from `tracker.backup.csv` and tell the user.
- **Same job reposted** with a new URL weeks later: it merges into the existing row (status preserved); mention "reposted" in notes.
- **Applied outside Claude:** let the user mark it applied with the date they give (`applied_date=YYYY-MM-DD`).
- **Privacy:** the tracker holds job data only - never store passwords, OTPs, Aadhaar/PAN, or bank details in it.
