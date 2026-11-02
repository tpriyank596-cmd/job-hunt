---
name: job-hunt-run
description: "This skill should be used when the user wants the whole job hunt done end to end in one go - \"run my job hunt\", \"find and apply to jobs for me\", \"apply to all jobs with 2-4 years requirement\", \"apply to matching jobs on LinkedIn, Naukri and Indeed and the company sites\", \"do today's applications\", \"continue the job hunt\". It chains resume-profile, job-search, job-match, resume-tailor, apply-assist, career-portal-apply and application-tracker with the user's filters and approvals."
metadata:
  version: "0.2.0"
---

# Job Hunt Run

Run the complete pipeline - profile → search → score → filter → tailor → apply (boards and company career sites) → track → report - with as few interruptions as possible and every safety rule of the individual skills intact.

## Inputs to settle at the start (ask only what's missing, in ONE AskUserQuestion)

- **Filters** (from the request, else the profile): target roles, cities/remote, posted within (default 7 days), experience band the job must accept (e.g. "2 to 4 years" = the JD's range overlaps 2-4 and its minimum ≤ the user's experience + 0.5), minimum score (default 75 apply / 55 maybe), include "immediate joiner" roles (yes/no), platforms.
- **Approval mode:** `review each` (summary per job) or `batch` (user approves the filtered list once; jobs with any NEEDS YOU still stop).
- **Resume mode:** original · tailored for top N + one general tailored version (default) · tailored for every job.
- **Answer policy** not yet in `answers.md`: skill-years basis (paid only vs including projects), integer rounding of total experience, early joining, serving notice.
- **Career sites:** may Claude use "Continue with Google" with `google_account` on approved sites? (ask per new domain later; this only sets whether to ask).

Save every answer to `answers.md` / `job-profile.md` immediately.

## Pipeline

1. **Profile** - load `job-profile.md`; if missing → resume-profile. Make sure it has `google_account`, notice details and CTC.
2. **Tracker** - init/load; back up once per session.
3. **Search** (job-search) - all platforms in scope, guest endpoints for LinkedIn, DOM for Naukri/Indeed; dedupe; drop stale; skip tracked jobs.
4. **Score** (job-match) - full JDs for every candidate that passes the cheap filters (city, title family, experience band); add to tracker.
5. **Filter** with the run's criteria; show the user one ranked list: title · company · city · exp range · score · route (Easy Apply / Naukri / Indeed / company site). In batch mode this list IS the approval request.
6. **Route check** - open each job card once to learn Easy Apply vs external; split the list.
7. **Tailor** (resume-tailor) - build the agreed versions in one go; one page; dates/metrics verified by `check_resume.py`; send the files to the user.
8. **Apply on boards** (apply-assist) in this order to minimise context switches: Naukri (grouped by resume version, swap → apply → restore original), LinkedIn Easy Apply, Indeed.
9. **Apply on company sites** (career-portal-apply) - first collect all needed per-domain Google approvals in one question, then go site by site; hand over account creation / passwords / CAPTCHAs.
10. **Track** every outcome immediately (applied / needs_user with the one action / skipped with reason / expired).
11. **Restore** anything changed on profiles (Naukri resume) and verify.
12. **Report** (short):
    - Applied today: N (per platform) with company names
    - Needs you: each job with link + the single action (create Workday account, solve check, answer X)
    - Skipped and why (one line each)
    - Files: updated tracker, answers, resumes
    - Next run suggestion (e.g. daily scheduled search).

## Resuming

"continue" / "continue the job hunt": reload tracker, take jobs with status `found` matching the last run's filters and `needs_user` jobs the user says are now unblocked, and carry on from step 8.

## Limits

- Daily caps from apply-assist (15/platform, 30 total) unless the user raises them.
- If tools hit usage limits mid-run, stop cleanly (drafts saved, tracker updated) and say when to resume.
- Never loop on a blocked page; one retry when the user says they fixed it.
