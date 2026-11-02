---
name: job-match
description: "This skill should be used when the user asks \"how well do I match this job\", \"score these jobs\", \"is this job a good fit for me\", \"rank these jobs\", \"which of these should I apply to\", pastes a job description or job link and wants a fit check, or when job-search hands over a list of jobs to rank. It scores each job against the candidate profile and explains the fit, gaps and red flags.\n"
metadata:
  version: "0.1.0"
---

# Job Match

Score how well each job fits the candidate, explain why in plain language, and recommend apply / maybe / skip. Be honest: a low score with a clear reason is more useful than inflated scores.

## Inputs

- Candidate profile (`job-profile.md`). If missing, run resume-profile first; for a single pasted JD, a resume alone is enough.
- One or more jobs with their full description. If only a link is given, open it. If the description is partial (login wall), score anyway but set confidence to low.

## Scoring

Use the rubric in `references/scoring-rubric.md`. Summary:

| Area | Weight |
| --- | --- |
| Must-have skills | 35 |
| Experience fit | 20 |
| Role / title fit | 15 |
| Location & work mode | 10 |
| Nice-to-have skills | 10 |
| CTC fit | 5 |
| Other signals (notice period, domain, education requirement) | 5 |

Steps for each job:

1. **Separate the JD's requirements** into must-haves (words like "required", "must", "minimum", "strong experience in", or listed first under Requirements) and nice-to-haves ("preferred", "plus", "good to have", "bonus"). If the JD doesn't distinguish, treat the first 5 technical requirements as must-haves.
2. **Match skills** against the profile: primary skills count fully; secondary skills count half; synonyms count (see rubric). Skills that appear only in the JD's boilerplate (company tech stack paragraph) don't count as requirements.
3. **Apply hard knockouts** (score capped at 40, recommendation "skip") when: experience gap is 3+ years below the minimum; a mandatory requirement is clearly unmet (specific degree, security clearance, on-site in a city the user won't move to, a language the user doesn't speak); company is in `exclude_companies`.
4. **Compute the score** (0-100) and confidence (high / medium / low).
5. **Recommend:** 75+ apply, 55-74 maybe (say what would make it worth it), below 55 skip.

## Output per job

Keep it short and readable:

```
<Title> - <Company> (<Location>, <work mode>)   Score: 82/100  · Apply
Why it fits: 4/5 must-haves (Python, FastAPI, MongoDB, AWS); 3 yrs vs 2-5 required
Gaps: Kubernetes (must-have), no Kafka (nice-to-have)
Notes: CTC not disclosed · posted 2 days ago · 40 applicants · Easy Apply
⚠ only if there is a red flag
```

For a batch, show a ranked list (highest first) with one line each, then details only for the top 5 unless asked for more. Write the score, recommendation and gaps to the tracker (application-tracker).

## Edge cases

- **Inflated JDs** (10+ "must-haves" for a mid-level role): weight the first 5 more heavily and note "JD lists many requirements; core ones matter most".
- **Title mismatch but skills match** (e.g. "Member of Technical Staff", "SDE II", "Associate Engineer"): judge by responsibilities, not the title.
- **Experience written oddly** ("0-0 yrs", "1-30 yrs", missing): treat as unspecified, don't penalize, lower confidence.
- **Overqualified** (user has 5+ years more than the max): don't hard-skip, but note the likely level/CTC mismatch.
- **CTC unknown:** give full neutral points (don't penalize) and say "CTC not disclosed".
- **CTC below current:** flag clearly; it's the user's call.
- **Notice period:** if the JD says "immediate joiners only" or "≤15 days" and the profile says 60-90 days, flag it as a likely blocker.
- **Skills stated in chat but not on the resume:** count them, but note "not on resume - add before applying" so resume-tailor can fix it.
- **Never invent experience** to raise a score.
