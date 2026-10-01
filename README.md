# ARRC Winter Research Talent Program

Recruitment site for the KAIST ARRC Symbiotic AIR4BTS winter hackathon and internship, published with GitHub Pages from `docs/` on `main`.

| URL | File |
| --- | --- |
| https://kaist-arrc.github.io/winter-school-26/ | `docs/index.html` — promotional poster |
| …/details/ | `docs/details/index.html` — detailed poster |
| …/concepts/ | `docs/concepts/index.html` — AIR4BTS concept guide |
| …/teaser.html | `docs/teaser.html` — redirect to `/` for old links |

## Layout

```
docs/     the public site — edit these files directly (no build step)
  styles.css   shared poster styles   promo.css    promotional poster
  assets/      logos, share image, concept illustrations
notes/    internal, never published: program facts, Google Form questions,
          director brief, operating review, source images and audits
tools/    stamp_css.py (CSS cache versions), render_og.py (share image),
          extract_concept_illustrations.py
tests/    test_site.py
```

## Editing

1. Edit the HTML/CSS in `docs/`. Keep agreed program terms consistent between the promo and detail posters.
2. After any CSS change, run `python tools/stamp_css.py`. It sets `?v=<content hash>` on stylesheet links so browsers load the new CSS instead of a cached copy.
3. Check: `python -m unittest discover tests`.
4. Preview: `python -m http.server 4173 --directory docs`, then open http://localhost:4173.

Re-render the share image after changing `tools/og-image.html`: `python tools/render_og.py` (needs Playwright Chromium).

Official logos come from https://arrc.kaist.ac.kr/assets/brand/ (checked 2026-09-21). Contact: arrc@kaist.ac.kr.
