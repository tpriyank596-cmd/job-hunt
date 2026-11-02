---
name: job-search
description: "This skill should be used when the user asks to \"find jobs\", \"search jobs for me\", \"find jobs matching my resume\", \"look for backend jobs in Bangalore\", \"show new jobs on LinkedIn / Naukri / Indeed\", \"jobs at a specific company\", \"run my daily job search\", or wants a job digest. It searches LinkedIn, Naukri.com, Indeed and company career pages using the candidate profile, removes duplicates and stale listings, and hands the results to job-match for scoring.\n"
metadata:
  version: "0.1.0"
---

# Job Search

Find relevant, current job openings across LinkedIn, Naukri.com, Indeed (India) and company career pages, based on the candidate profile.

## Before searching

1. **Load the profile** (`job-profile.md`). If it is missing, run the resume-profile skill first. If the user only wants a quick one-off search ("find Python jobs in Bangalore"), proceed with what they said and note that results will be better with a profile.
2. **Load the tracker** if it exists (see application-tracker) so already-seen and already-applied jobs are skipped.
3. **Decide the mode:**
   - **Logged-in mode** - Claude in Chrome tools are available and the user is signed in. Gives full results, Easy Apply filters, applicant counts. Load the chrome-browser skill before the first browser step.
   - **Public mode** - no browser access. Use web search and fetching of public pages. Results are partial; say so once in the summary.

## Building queries

- Create one query per **target role × location** pair. Include close title variants (e.g. "Backend Engineer", "Python Developer", "Software Engineer - Backend"), max 3 variants per role.
- Add the 3-5 most important primary skills as keywords only when the title alone is too broad.
- Apply filters from the profile: experience range (profile years −1 to +2), location / remote, posted date (default: last 7 days; daily digest: last 24 hours).
- For specific companies the user names, search that company's careers page directly as well as the job boards.
- Platform URL patterns and filter parameters are in `references/platforms.md`. URLs change; if a URL pattern fails, use the site's own search box instead.
- **Logged-in LinkedIn hides job IDs in the new UI** - collect listings and full JDs through the same-origin guest endpoints (`/jobs-guest/jobs/api/seeMoreJobPostings/search` and `/jobs-guest/jobs/api/jobPosting/<id>`) from a LinkedIn tab; see `apply-assist/references/browser-techniques.md` §6. Run long loops in the background and render large results into the page to read them (§3, §4).
- **Naukri:** read search pages and job pages from the DOM (§5); never call Naukri's JSON APIs (they demand reCAPTCHA). Store results in localStorage across page loads.
- **Indeed:** read cards from `a[data-jk]`; stop at any Cloudflare check.
- **Experience filter:** when the user gives a band (e.g. 2-4 years), keep jobs whose range overlaps it; read the JD too - headers and JDs often disagree (e.g. header 3-8, JD "4+"), and record both.

## Collecting results

For each listing, capture: title, company, location, work mode, experience required, salary (if shown), posted date, source platform, job URL, apply type (Easy Apply / Naukri apply / external portal), applicant count (if shown), and the full job description text (open the job page; snippets are not enough for matching).

**Pacing (logged-in mode):** open pages at a human pace, at most ~40 job pages per platform per session, and stop if the site shows a CAPTCHA, "unusual activity" warning, or logs the user out - tell the user and do not try to get around it.

## Cleaning results

1. **Deduplicate** across platforms using the key `normalized company + normalized title + city`. Normalize by lowercasing, removing "Pvt Ltd/Private Limited/Inc/Technologies", and removing seniority noise like "(Remote)" in titles. Keep the listing with the most direct apply route (company page > Easy Apply > Naukri > Indeed > reposts) and record the other URLs as alternates.
2. **Drop stale listings:** posted more than 30 days ago, "No longer accepting applications", "Job expired", or a 404 page.
3. **Skip** jobs already in the tracker with any status, and companies in `exclude_companies`.
4. **Flag suspicious postings** (keep them, but mark ⚠): asks for a registration/training fee, personal Gmail/Yahoo contact only, salary far above market with vague duties, "work from home data entry" style descriptions, WhatsApp-only contact, company not findable online. See `references/platforms.md` for more red flags.
5. **Flag consultancy reposts:** listings by staffing agencies that hide the client company. Keep them but label "via consultancy".

## Output

1. Pass the cleaned list to **job-match** for scoring.
2. Add every new job to the tracker with status `found` (application-tracker).
3. Report to the user: how many found per platform, how many after dedupe, and the top matches (from job-match) as a short list - title, company, location, score, apply type, link. Mention anything that limited the search (public mode, a site blocked, a CAPTCHA).

## Daily digest mode

When run on a schedule ("run my daily job search"): use posted-in-last-24-hours filters, report only NEW jobs scoring 70+, and keep the message short. Never apply in this mode. If nothing new qualifies, say so in one line.

## Edge cases

- **Zero results:** broaden one step at a time - widen posted date to 14 days, add title variants, add nearby cities or remote, relax experience by +1 year - and tell the user what was broadened.
- **Too many results (100+):** tighten to the top primary skills and the last 3 days; score only the first ~50.
- **Location aliases:** treat Bangalore/Bengaluru, Gurgaon/Gurugram, Bombay/Mumbai, NCR/Delhi/Noida/Gurugram as matches.
- **"Remote" that isn't:** check the description for "remote within city", "initially WFO", or "hybrid" and record the real work mode.
- **Same company, multiple similar openings** (e.g. 3 "SDE II" postings for different teams): keep each if the team or location differs; otherwise dedupe.
- **Login walls in public mode:** LinkedIn often hides full descriptions to logged-out visitors. Record the job with `description: partial` so job-match lowers confidence, and suggest logged-in mode.
- **Non-English or international listings** outside target locations: drop unless the user wants international roles.
