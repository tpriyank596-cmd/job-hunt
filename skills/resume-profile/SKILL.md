---
name: resume-profile
description: "This skill should be used when the user shares a resume or CV and wants it turned into a job-search profile, says \"read my resume\", \"build my job profile\", \"update my profile\", \"I changed my expected CTC / notice period / location\", or when another job-hunt skill (job-search, job-match, resume-tailor, apply-assist) needs the candidate profile and none exists yet. It parses the resume into a structured profile of skills, experience, roles and preferences that every other skill uses.\n"
metadata:
  version: "0.1.0"
---

# Resume Profile

Build and maintain one structured candidate profile (`job-profile.md`) from the user's resume plus their stated preferences. Every other job-hunt skill reads this profile, so accuracy matters more than polish.

## Inputs

1. **Resume file** - PDF, DOCX, TXT, or pasted text. If none is attached, ask for it. Never invent resume content.
2. **Preferences** (ask only for what is missing, in one grouped question):
   - Target roles / titles (up to 5)
   - Locations (cities), and remote / hybrid / on-site preference
   - Total experience (confirm the number computed from the resume)
   - Current CTC and expected CTC (in LPA) - optional, the user may skip
   - Notice period (immediate / 15 / 30 / 60 / 90 days, or serving notice with last working day)
   - Company preferences: types to include (product, startup, MNC, service) and any companies to exclude (e.g. current employer)
   - Work authorization / relocation willingness if relevant
   - Google account to use for "Continue with Google" on company career sites (email only - never a password)
   - Whether they can join earlier than the notice period, and whether they are serving notice now

## Steps

1. **Read the resume fully.** For PDFs, extract text; if extraction returns little or garbled text (scanned resume), rasterize pages and read them visually. For DOCX, extract text including tables and text boxes (skills are often in tables).
2. **Extract** into the profile template below. Rules:
   - Compute total experience from job dates. Handle "Present"/"Current", overlapping jobs (count overlap once), gaps (note them, don't hide them), and internships (list separately, don't add to full-time years unless the user says so).
   - Split skills into **primary** (used in recent roles, appears in bullet points) and **secondary** (only listed in a skills section or older roles). This split drives match scoring.
   - Normalize skill names (e.g. "ReactJS"/"React.js" → React, "Postgres" → PostgreSQL) but keep the user's exact wording in a `resume_terms` list for ATS keyword matching later.
   - Capture measurable achievements verbatim (numbers, scale, impact) - resume-tailor reuses them.
   - Record what is NOT on the resume when the user mentions it in chat, tagged `(stated, not on resume)`.
3. **Show the profile summary to the user** in plain language (a short list, not the raw file) and ask them to correct anything wrong. Pay attention to: experience years, primary skills, notice period, CTC.
4. **Save** the confirmed profile as `job-profile.md`:
   - If the user has a connected folder on their computer, save it there in a `job-hunt/` folder so it persists across chats.
   - Otherwise save it in the working directory and send it to the user, and tell them to attach it next time (or keep it in a project).
5. **Answer bank:** create `answers.md` next to the profile from `references/answers-template.md` and fill what is known; screening answers are always taken from it.
6. **Updates:** when the user changes a preference or uploads a new resume, update only the changed fields, bump `last_updated`, and keep the previous resume's file name in `resume_history`.

## Profile template

```markdown
# Job Profile
last_updated: YYYY-MM-DD
resume_file: <file name>
resume_history: []

## Basics
name:
current_title:
current_company:
total_experience_years:        # e.g. 3.5
relevant_experience_years:     # in the target roles' domain
location_current:
locations_target: []
work_mode: remote | hybrid | onsite | any
notice_period:
current_ctc_lpa:               # optional
expected_ctc_lpa:              # optional, may be a range
open_to_relocation: yes | no
exclude_companies: []
company_types_preferred: []
google_account:                # for Continue-with-Google on approved career sites; never store passwords
early_joining:                 # e.g. "can join in 15 days" (stated)
serving_notice: yes | no

## Target roles
- <title 1>
- <title 2>

## Skills
primary: []
secondary: []
resume_terms: []               # exact wording from resume, for ATS matching

## Experience
- company / title / start - end / key achievements (verbatim, with numbers)

## Education
- degree / institute / year

## Certifications & links
- GitHub / portfolio / LinkedIn URL if on resume

## Gaps & notes
- employment gaps, career switches, things not on resume (stated)
```

## Edge cases

- **Multiple resumes** (e.g. backend vs. AI/ML versions): keep one profile but add a `resume_variants` list mapping each file to the roles it targets; job-search and apply-assist pick the variant by role.
- **Fresher / under 1 year:** use projects, internships and education as primary evidence; set `total_experience_years: 0` and list internships separately.
- **Senior / lead roles:** capture team size managed and scope (budget, systems owned).
- **Career switch:** note it under Gaps & notes so job-match does not penalize transferable experience unfairly.
- **Resume in another language or with heavy design (columns, icons):** read visually if text order is scrambled.
- **Sensitive data:** do not copy Aadhaar, PAN, passport numbers, date of birth or full home address into the profile even if they appear on the resume. Keep city only.
- **Conflicting info** (resume says 4 years, user says 5): ask which is right; don't silently pick.
