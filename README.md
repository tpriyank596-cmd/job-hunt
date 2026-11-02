# job-hunt (v0.2)

Find, match, tailor for, apply to and track jobs on LinkedIn, Naukri.com, Indeed (India) and company career sites, using your resume.

## Skills

| Skill | What it does | Say things like |
| --- | --- | --- |
| job-hunt-run | Runs the whole pipeline in one go with your filters and approvals | "apply to all 2-4 year GenAI jobs in Bangalore, NCR and remote", "continue the job hunt" |
| resume-profile | Reads your resume and preferences into one profile + answer bank | "build my job profile from this resume" |
| job-search | Searches LinkedIn, Naukri, Indeed and career pages; removes duplicates, stale and scam listings | "find GenAI jobs posted this week" |
| job-match | Scores each job 0-100 with reasons and gaps | "rank these jobs" |
| resume-tailor | One-page tailored resumes (DOCX + PDF) from your true facts, cover letters, screening answers - never invents experience | "tailor my resume for this JD" |
| apply-assist | Applies on LinkedIn Easy Apply, Naukri and Indeed in your Chrome; swaps and restores your Naukri resume when asked | "apply for the rest", "apply at Indeed jobs" |
| career-portal-apply | Applies on company sites (Greenhouse, Lever, Ashby, Workable, Workday, Darwinbox…); uses Continue with Google only on sites you approve | "finish the company-site applications" |
| application-tracker | One deduplicated tracker: statuses, follow-ups, daily counts | "how many jobs did we apply today?" |

## Install from GitHub

1. Download or clone this repo (Code → Download ZIP, or `git clone`).
2. In Claude, add it as a plugin (upload the folder/zip in your plugin settings).
3. Continue with Setup below.

> Your own profile, answers, tracker and resumes are created at runtime and are listed in `.gitignore`, so they are never committed. Keep them out of any fork.

> Automating applications may conflict with some job sites' terms of use. The plugin keeps a human in the loop and caps daily volume, but you are responsible for how you use it.

## Setup

1. Install the plugin.
2. Install Claude in Chrome; sign in yourself to LinkedIn, Naukri, Indeed - and to Google in that Chrome with the account you want career sites to use.
3. "Build my job profile" with your resume attached. Your data lives in a `job-hunt/` folder: `job-profile.md`, `answers.md`, `resume-facts.json`, `portals.md`, `tracker.csv`, tailored resumes. Keep it in a connected folder or attach it in each new chat.
4. Then: "run my job hunt" (or any single skill).

## What it will and won't do

- Submits an application only after your yes for that job, or your explicit batch approval ("apply for the rest").
- Uses "Continue with Google" with your profile's Google account only on career sites you approve, one site at a time.
- Never types passwords, OTPs or verification codes; never creates accounts (it tells you the one click/step to do, then continues); never solves CAPTCHAs or Cloudflare checks.
- Never invents experience; answers come only from your profile and answer bank, and unknowns are asked.
- Changes to your profiles (e.g. replacing the Naukri resume) only with approval - and restores the original afterwards.
- Caps: 15 applications per platform and 30 total per day unless you raise them; human-paced browsing; stops on any platform warning.

## Requirements

- Python 3 (standard library) for the tracker; Node with the `docx` package, LibreOffice and poppler-utils for resume PDFs (preinstalled in Claude's workspace).
- No API keys.

## Changelog

- 0.2.0 - job-hunt-run and career-portal-apply skills; tested browser techniques (hidden file-input capture, LinkedIn guest search, Naukri chatbot, Indeed smartapply); resume builder scripts with one-page fitting and fact checks; Naukri resume swap/restore; answer bank template; tracker no longer merges different postings at the same company.
- 0.1.0 - first version.
