# HODOS website

The static Danish MVP website for HODOS — a skills and adventure school for families and adults.

## Current state

- Eleven public pages: front page, family and adult paths, method, course overview, three course-detail pages, about, practical information and contact
- The three course pages are clearly marked as pilots under development; they have no dates, prices, booking or availability claims
- No signup, payment, analytics, contact delivery or production deployment is configured
- The repository is private

## Editing and local preview

The website is generated from `build_site.py` so shared navigation, course status and wording stay consistent.

```bash
python3 build_site.py
python3 -m http.server 4173
```

Then open `http://127.0.0.1:4173/`.

- Shared visual design: `assets/site.css`
- Navigation and course filtering: `assets/site.js`
- Website copy, navigation and course data: `build_site.py`

## Project direction

HODOS helps families and adults build practical outdoor skills, sound judgement and confidence for independent adventures. The public site must remain Danish, factual and clear about what is not yet available.
