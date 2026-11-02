# Apply flows by platform

Page layouts change often. Use these as orientation, then read the actual page before each click. Prefer finding elements by visible text/labels over fixed positions.

## LinkedIn Easy Apply

1. Job page → button labelled **Easy Apply** (plain "Apply" with an arrow icon = external site).
2. Modal with 1-5 steps: Contact info → Resume → Additional questions → (Work authorization / Voluntary self-identification) → Review.
3. Resume step: choose a previously uploaded resume or "Upload resume". Confirm the selected file name.
4. Additional questions: numeric "years of experience with X", yes/no, dropdowns, short text. Required fields are marked; the Next button stays disabled or shows an error until filled.
5. Review step shows everything; this is where to stop and get approval. The final button is **Submit application**.
6. Uncheck "Follow <company>" only if the user asked.
7. Success: a confirmation dialog / "Applied" label on the job. Close the dialog.
8. Saving a draft: closing the modal asks "Save this application?" - choose Discard unless the user wants to save.

## Naukri.com

1. Job page → **Apply** (uses the Naukri profile + resume) or **Apply on company site** (external).
2. Some jobs open a **chatbot-style questionnaire** on the right side: notice period, current CTC, expected CTC, current location, relocation, specific skill years. Each answer is typed or chosen, then "Save".
3. Stop before the last "Save"/"Submit" in the questionnaire for approval when it finalizes the application; if Naukri submits immediately on Apply with no questions, get approval **before clicking Apply**.
4. Success: "Applied" label / "You have successfully applied" message.
5. Naukri uses the profile resume; tailored resumes require replacing the profile resume (affects all recruiters) - ask before doing that.

## Indeed (India)

1. Job page → **Apply now** (Indeed-hosted, often "Easily apply") or **Apply on company site**.
2. Steps: contact info → resume (Indeed resume or uploaded file) → employer questions → review.
3. CAPTCHAs ("verify you are human") are common - stop and hand over.
4. Final button: **Submit your application**. Success page: "Your application has been submitted".

## Greenhouse / Lever (external, often no account)

- Single-page forms: name, email, phone, resume upload, LinkedIn URL, sometimes cover letter and custom questions, EEO section (optional - leave "Decline to self-identify" unless the user specifies).
- Final button: **Submit application**. Same approval rule.

## Workday / Taleo / SuccessFactors / iCIMS (external, account required)

- Require creating an account with a password and email verification → do not proceed. Mark `needs_user`, give the user the direct link, and offer to prepare answers and the tailored resume they can paste/upload.

## Common screening questions → profile field

| Question pattern | Source |
| --- | --- |
| Years of experience in X | profile Experience + skills; count only roles that used X |
| Total experience | `total_experience_years` |
| Notice period / earliest start | `notice_period` |
| Current CTC / expected CTC | `current_ctc_lpa` / `expected_ctc_lpa` (skip-able; NEEDS YOU if blank) |
| Willing to relocate / commute | `open_to_relocation`, `locations_target` |
| Work authorization / visa | profile notes; NEEDS YOU if unknown |
| Highest education | Education |
| LinkedIn / GitHub / portfolio URL | Certifications & links |
| Why do you want to join / cover note | resume-tailor, approved by user |
| Bond / shift / night shift / travel % | NEEDS YOU unless in `answers.md` |

## Learned in practice (v0.2)

- LinkedIn: many "Promoted" jobs that look like Easy Apply are external ("Apply ↗"); verify on the job card before promising Easy Apply. Easy Apply resumes uploaded once stay in the account's resume list and can be re-selected later.
- LinkedIn questions seen: commute/relocation yes-no, years with LLM / Agentic AI (text, numbers only), notice period (number), current/expected CTC (numbers only, no ranges or "LPA"), "serving notice period?" yes/no, US work authorization + H-1B sponsorship (Workable-backed postings).
- Naukri: some Apply clicks submit instantly with the profile resume; others open a chatbot (skill years, relocation yes/no, combined skill questions). Each chatbot answer needs the panel's Save.
- Indeed: Apply now can go straight to the review step using the resume saved on Indeed; contact block and resume are below the fold.
- External routes → career-portal-apply.
