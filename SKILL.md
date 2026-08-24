---
name: one-page-cn-resume
description: Generate or revise a polished one-page Chinese resume PDF using this repository's fixed layout, centered position axis, quantified-result emphasis, and render validation. Use for resumes based on the bundled JSON schema; do not redesign the visual system unless explicitly requested.
---

# One-page Chinese Resume

Use `scripts/build_resume.py` instead of recreating the PDF layout.

## Workflow

1. Update a resume JSON file following `data/example.resume.json`.
2. Preserve the layout invariants:
   - A4, exactly one page.
   - Name and contact centered.
   - Company left-aligned, date right-aligned.
   - Every position title centered on the same page axis as the name.
   - Section spacing is larger than experience spacing; bullet spacing is smallest.
   - Quantified results are bolded with `<b>...</b>` in JSON.
3. Build with `python scripts/build_resume.py DATA.json --output OUTPUT.pdf`.
4. Validate with `python scripts/render_check.py OUTPUT.pdf --render-dir tmp/rendered`.
5. Inspect the rendered PNG before delivery. If the result exceeds one page, tighten wording before reducing type size.

Do not commit personal resume data unless the repository is intentionally private.
Public examples must replace names, contact details, organizations, timelines, role titles, business scenarios, and activity descriptions with neutral placeholders. Preserve only the layout structure and synthetic metric formats.
