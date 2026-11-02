# Platform notes

These URL patterns and parameters are commonly used but are not official APIs and can change without notice. If a pattern returns no results or an error, open the site's normal search page and use its search box and filters instead. Always URL-encode keywords and locations.

## LinkedIn Jobs

Search URL:
```
https://www.linkedin.com/jobs/search/?keywords=<query>&location=<city, India>&f_TPR=<age>&sortBy=DD
```

| Filter | Parameter | Values |
| --- | --- | --- |
| Posted within | `f_TPR` | `r86400` (24h), `r604800` (7 days), `r2592000` (30 days) |
| Easy Apply only | `f_AL` | `true` |
| Work mode | `f_WT` | `1` on-site, `2` remote, `3` hybrid (comma-separate for several) |
| Experience level | `f_E` | `1` internship, `2` entry, `3` associate, `4` mid-senior, `5` director, `6` executive |
| Sort | `sortBy` | `DD` newest first, `R` most relevant |

Notes:
- Logged-out visitors often see truncated descriptions and fewer results; mark those `description: partial`.
- Job page URL: `https://www.linkedin.com/jobs/view/<jobId>/` - use `jobId` as the stable listing ID.
- "Promoted" listings can be older than the date filter suggests; check the posted date on the job page.
- Applicant count ("Over 100 applicants") and "Actively recruiting" are useful signals; record them.
- Apply button says "Easy Apply" (in-LinkedIn form) or "Apply" (redirects to an external portal).

## Naukri.com

Search URL (slug format):
```
https://www.naukri.com/<role-keywords-hyphenated>-jobs-in-<city>?experience=<years>&jobAge=<days>
```
Example: `https://www.naukri.com/python-developer-jobs-in-bengaluru?experience=3&jobAge=7`

| Filter | Parameter | Values |
| --- | --- | --- |
| Experience (years) | `experience` | integer |
| Freshness | `jobAge` | `1`, `3`, `7`, `15`, `30` |

Notes:
- Naukri listings show experience range ("3-6 Yrs") and often a CTC range ("8-15 Lacs PA") or "Not disclosed".
- Many listings are from consultancies; the company name may be the agency. Label "via consultancy".
- "Apply" applies with the Naukri profile directly; "Apply on company site" redirects externally.
- Some applies open a set of recruiter questions (notice period, current CTC, expected CTC, relocation); answers must come from the profile.
- Naukri ranks recently updated profiles higher; profile refresh is a separate action that needs user approval.
- Recommended jobs page (logged-in): `https://www.naukri.com/mnjuser/recommendedjobs`.

## Indeed (India)

Search URL:
```
https://in.indeed.com/jobs?q=<query>&l=<city>&fromage=<days>&sort=date
```

| Filter | Parameter | Values |
| --- | --- | --- |
| Posted within | `fromage` | `1`, `3`, `7`, `14` |
| Sort | `sort` | `date` |

Notes:
- Indeed shows CAPTCHAs ("verify you are human") more readily than the others. Stop and hand over to the user when one appears.
- "Easily apply" = Indeed-hosted form; otherwise "Apply on company site".
- Many Indeed listings are aggregated from other boards; dedupe carefully against LinkedIn and Naukri.
- Job page URL contains `jk=<id>`; use it as the stable listing ID.

## Company career pages

- Often the most current and the most direct route. Common hosted portals: Workday (`*.myworkdayjobs.com`), Greenhouse (`boards.greenhouse.io/<company>`), Lever (`jobs.lever.co/<company>`), SmartRecruiters, Darwinbox, Keka, Zoho Recruit.
- Greenhouse and Lever boards are public and list all openings on one page; search them directly when the user names a company.
- These portals usually need their own account to apply; apply-assist marks them "needs your account" instead of creating one.

## Scam and low-quality red flags

Mark ⚠ and tell the user when a listing has one or more of:
- Any fee for registration, training, laptop, background check or "security deposit"
- Contact only via personal email (gmail/yahoo/outlook) or WhatsApp number
- Offer made without an interview, or "selected" messages for jobs not applied to
- Pay far above market for low-skill work, or "earn per task / data entry from home"
- Company name not findable, no website, or website created very recently
- Requests for Aadhaar/PAN/bank details before an offer letter
- Job description copied from another company or full of unrelated keywords
