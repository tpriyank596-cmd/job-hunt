# ATS-safe resume guidelines

Applicant tracking systems (Workday, Greenhouse, Lever, Taleo, Naukri's parser, LinkedIn's parser) extract text from the resume. Layouts that look good to humans often break parsing.

## Layout
- One column. Two-column layouts often get read left-then-right line by line, mixing sections.
- No content inside tables, text boxes, headers or footers (contact details in a header are often lost).
- No images, icons, skill-level bars, charts or logos. Write "Python" not a 4/5 star graphic.
- Standard fonts: Calibri, Arial, Helvetica, Garamond, Georgia; 10-12 pt body, 14-16 pt name.
- Margins 0.5-1 inch. Plain bullets (•) only.

## Headings
Use standard names so parsers map sections correctly: Summary, Skills, Experience (or Work Experience), Projects, Education, Certifications.

## Content
- Contact line: name, phone, email, city, LinkedIn URL, GitHub/portfolio URL. No photo, date of birth, marital status, Aadhaar/PAN, or full address.
- Dates: `MMM YYYY - MMM YYYY` or `MMM YYYY - Present`, consistently.
- Job title, company, city on one line per role.
- Bullets start with an action verb and include a number where truthful (latency, scale, users, cost, time saved).
- Write both the acronym and the full form once for key terms when space allows (e.g. "Retrieval-Augmented Generation (RAG)").
- Keep skills as plain comma-separated text grouped by category (Languages, Frameworks, Databases, Cloud/DevOps, AI/ML).

## File
- Prefer PDF generated from text (not a scan). Some portals want DOCX; provide both.
- File name: `<Name>_Resume_<Company>_<Role>.pdf`, ASCII only, no spaces.
- Under 2 MB.

## Self-check before handing over
1. Extract text from the produced PDF and confirm the reading order is correct and nothing is missing.
2. Search the extracted text for each JD must-have keyword the user truly has; confirm each appears at least once.
3. Confirm no fact differs from the original resume (titles, dates, employers, metrics).
