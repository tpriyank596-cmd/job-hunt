---
name: resume-tailor
description: "This skill should be used when the user asks to \"tailor my resume for this job\", \"customize my resume\", \"make my resume ATS friendly for this JD\", \"write a cover letter for this job\", \"answer these screening questions\", \"write a message to the recruiter / hiring manager\", or when apply-assist needs a tailored resume, cover letter or answers for a specific job. It rewrites emphasis and wording for one job without inventing experience.\n"
metadata:
  version: "0.1.0"
---

# Resume Tailor

Produce job-specific application material from the candidate's real experience: a tailored resume, a cover letter, screening-question answers, and a short recruiter note. The single non-negotiable rule: **never add a skill, title, employer, date, degree, number or achievement that is not in the resume or stated by the user.** Tailoring changes order, emphasis and wording - not facts.

## Inputs

- The job description (full text; open the link if only a link is given)
- The original resume file and `job-profile.md`
- The job-match result for this job, if available (gaps and missing keywords)

## Tailored resume

1. **Pick the resume variant** that fits the role if the profile has several.
2. **Extract JD keywords:** must-have skills, tools, and key phrases (e.g. "event-driven architecture", "RAG pipelines"). Use the JD's exact spelling.
3. **Rewrite, don't fabricate:**
   - Reorder the skills section so JD-matching skills come first; use the JD's spelling where it's the same skill (e.g. "Postgres" → "PostgreSQL" if the JD says that).
   - Reorder bullets within each role so the most relevant come first; rephrase bullets to use JD terms where they truthfully describe the work.
   - Rewrite the summary (2-3 lines) for this role.
   - Keep every metric exactly as in the original.
   - Remove or shorten irrelevant bullets only if needed to keep length (1 page under ~5 years experience, max 2 pages otherwise).
4. **Gaps:** for must-haves the user lacks, do NOT add them. List them for the user with a suggestion (e.g. "If you've used Kubernetes in a side project, tell me and I'll add it").
5. **ATS safety:** single column, standard headings (Summary, Skills, Experience, Projects, Education), no tables for core content, no text in images/headers/footers, standard fonts, dates as `MMM YYYY`. Read `references/ats-guidelines.md` for details.
6. **Format:** produce a **DOCX and a PDF** with the bundled builder:
   - Keep the user's true facts in `job-hunt/resume-facts.json` (name, contact, roles with dates and bullet texts keyed by id, projects, education, certifications, `must_keep` strings such as dates and metrics). Build it once from the resume; every bullet is a faithful rewording of an original bullet.
   - Add one entry per tailored version under `variants` (file name, 2-3 line summary, skill groups in JD order, bullet order per role, projects). Variants may only choose, order and reword - never add facts.
   - Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/resume-tailor/scripts/make_resumes.py <facts.json> <outDir> <variant|all>`. It builds DOCX via `build_resume.js` (docx npm), converts to PDF with LibreOffice, shrinks to one page (fewer projects, then fewer bullets) and reports any `must_keep` fact missing - fix before using the file.
   - Load the docx skill only for unusual layouts or when editing the user's own .docx.
   - Save outputs in a folder the browser tools can upload from (working directory or a connected folder).
7. **File name:** `<Name>_Resume_<Company>_<Role>.pdf` (no spaces in company/role; ASCII only).
8. **Show a short change summary:** keywords added (that were already true), bullets reordered, summary rewritten, gaps not addressed. Ask for approval before apply-assist uses it.

## Versions strategy

- Many jobs: one company-specific version for each top job (score 85+ or user-named), plus ONE general version per role family (e.g. GenAI Engineer) for the rest. Same company → same version for all its roles.
- User-approved molding (record in the profile's tailoring rules): rewording project/role descriptions and regrouping skills is fine; dates, employers, titles and metrics never change.
- Skills the user confirms in chat but not on the resume (e.g. "yes, I deployed with Docker") → ask which tool and where, then add it to the facts file as a stated fact before using it.

## Cover letter

- 150-250 words, 3 short paragraphs: why this role/company (one specific detail from the JD or company), the 2-3 most relevant achievements with numbers, a closing line with notice period if relevant.
- No generic filler ("I am writing to express my interest..."), no repeating the resume line by line.
- Only produce one when the application asks for it or the user requests it.

## Screening-question answers

- Answer from the profile and resume only. Typical: years with X, current/expected CTC, notice period, relocation, work authorization, "why this company".
- For yes/no or numeric questions where the truthful answer may hurt the application (e.g. "years of Kubernetes: 0"), give the truthful answer and flag it to the user - never round up.
- If a question can't be answered from known info, mark it `NEEDS YOU` instead of guessing.
- Save reusable answers to an `answers.md` bank next to the profile so future applications stay consistent.

## Recruiter / hiring-manager note

- LinkedIn connection notes have a 300-character limit; InMail/email can be longer (under 120 words).
- Mention the specific role, one strong matching achievement, and a clear ask.
- Draft only - never send without the user's explicit approval.

## Edge cases

- **JD in a language other than English:** tailor in English unless the JD says the resume must be in that language.
- **User asks to "add X even though I haven't used it":** decline that part, and offer to add it under a "Currently learning" line only if the user really is learning it.
- **Employment gap:** don't hide it with fake dates; if the user wants, add a one-line truthful explanation (e.g. "Career break - upskilling in ML").
- **Very senior roles:** emphasize scope (team size, systems owned, budget) over tool lists.
- **Original resume is a scanned image:** rebuild it from extracted text into a clean ATS-safe layout and ask the user to check it.
- **Multiple applications to the same company:** keep the resume consistent across them (same titles and dates); recruiters compare.
