# Career portal flows

Layouts change; read the page before each click and prefer finding elements by label.

## Identify the portal

| Domain contains | Portal | Account? | Google sign-in? | Notes |
| --- | --- | --- | --- | --- |
| `boards.greenhouse.io`, `job-boards.greenhouse.io`, `?gh_jid=` | Greenhouse | No | - | One page: name, email, phone, resume, LinkedIn, custom questions, optional EEO. Button "Submit application". |
| `jobs.lever.co` | Lever | No | - | One page; "Submit application". Sometimes hCaptcha → hand over. |
| `jobs.ashbyhq.com` | Ashby | No | - | One page; resume autofill offered. |
| `apply.workable.com` | Workable | No | - | Multi-section single page. LinkedIn Easy Apply "applicantTrackingSystemName=Workable" jobs may still ask US work-authorization questions → NEEDS YOU. |
| `jobs.smartrecruiters.com` | SmartRecruiters | Optional | Sometimes | "Apply without account" usually available. |
| `myworkdayjobs.com`, `wd1/wd3/wd5.myworkdaysite.com` | Workday | **Yes, per company** | Rare | "Create Account" with password + email verification → user does it once. After sign-in: My Information → My Experience (resume parse) → Application Questions → Voluntary Disclosures → Review → Submit. |
| `successfactors`, `jobs.sap.com`, `career*.sapsf` | SuccessFactors | Yes | Sometimes (LinkedIn/Google) | Long profile forms. |
| `taleo.net` | Taleo | Yes | No | User creates account. |
| `icims.com` | iCIMS | Yes | Sometimes | Email + "Next"; may send a code → hand over. |
| `darwinbox.in`, `*.darwinbox.com` | Darwinbox | Often | Often Google | Common with Indian companies. |
| `keka.com/careers`, `*.keka.com` | Keka | No (most) | - | Simple form. |
| `zohorecruit.com`, `zohorecruit.in` | Zoho Recruit | Optional | Google/LinkedIn | "Apply with Google" fills basics. |
| `eightfold.ai`, `*.eightfold.ai` | Eightfold (e.g. Amex, some banks) | Yes/optional | Sometimes | Upload resume first; parsed profile needs checking. |
| `freshteam.com` | Freshteam | No | - | Simple form. |
| company domain + WordPress "contact-form-7" | Plain form | No | - | Often has `cf7-captcha` → hand over. |

## Continue with Google (approved sites only)

1. Click the portal's "Sign in with Google" / "Continue with Google" button.
2. A popup or redirect to `accounts.google.com` opens:
   - **Account chooser** listing accounts → click the one equal to `google_account`. Nothing typed.
   - **"Sign in" email box / password box / 2-Step / "Verify it's you"** → STOP. Tell the user: "Google wants you to sign in - please sign in to Chrome with <google_account from the profile>, then say continue."
   - **Consent screen** "<site> wants to access your Google Account" → read the listed permissions. Only name, email address, profile picture/language → click Continue (covered by the site approval). Anything else → stop and show the scopes.
3. Back on the portal:
   - Signed in to an existing candidate profile → continue.
   - "Complete your profile" / "Create account" / terms acceptance for a NEW account → STOP (account creation is the user's). Record `account: needed` in `portals.md`.
4. Record in `portals.md`: domain, company, sign-in method, date, result.

## Uploading files

- `file_upload` works only on an `<input type="file">` and only for files this session may read (attachments, uploads/outputs folders, connected folders, working directory). The plain uploads folder copy of the original resume works; files copied only into an outputs folder may be rejected - use the working-directory copy then.
- Many sites create the file input only when the upload button is clicked, and clicking it opens a native picker Claude can't see. Use the capture technique in `apply-assist/references/browser-techniques.md` (patch `HTMLInputElement.prototype.click`, trigger the button with JS, then upload to the captured input).
- After upload, confirm the visible file name.

## Typical screening fields → source

| Field | Source |
| --- | --- |
| First / last name | Resume header (LinkedIn may show a single name followed by "." - use the resume name and leave last name as the profile has it; ask if a portal rejects it) |
| Email / phone | Profile (`email`, `phone`, +91) |
| Current location | `location_current` |
| Total experience | `answers.md` (integer and years+months forms differ) |
| Skill years | `answers.md`; unlisted skill → truthful 0 or NEEDS YOU |
| Current / expected CTC | `answers.md` (numbers-only fields: rupees per year, e.g. 800000 for 8 LPA; range not allowed → midpoint, flag it) |
| Notice period | `answers.md` |
| Serving notice? | `answers.md` |
| Work authorization (India) | `answers.md`; US/other country authorization → NEEDS YOU |
| How did you hear | The board the job came from |
| Cover letter | resume-tailor, only if required or the user asked |
| EEO / diversity | Decline to self-identify |
