# ARRC Winter Research Talent Program

> **작업 중 / Work in progress.** 프로그램 내용은 검토·수정 중이며 일정과 모집 조건은 미확정입니다. 최종 모집 공고가 아닙니다.

Editable Korean poster and internal operating review for the 2026–2027 program. Built from the supplied poster and director’s message, with no build dependencies.

## Run

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://localhost:4173. Serve the repository directory, not its parent.

- **포스터 편집**: click text to edit; use **편집 켜짐 / 미리보기** to toggle editing.
- Edits save to this browser’s local storage. They do not change repository files or sync to colleagues.
- **내용 저장 / 불러오기**: export/import editable content as JSON.
- **HTML 내보내기**: download a standalone editable HTML, including the reference image, CSS and JavaScript. Its initial content becomes its reset baseline. Fonts use an optional Google Fonts import; offline system fonts are supported.
- **인쇄 / PDF**: print the active view. The poster is designed for A3 portrait; select A3 and disable browser headers/footers. Longer edits may increase page count.
- **운영 검토**: six editable internal review proposals based on the director’s message, explicitly separate from confirmed recruitment terms.
- **원본 이미지**: view the source for comparison.

## Files

- `index.html`: semantic poster content and internal review. Edit this to change defaults.
- `styles.css`: colors, typography, layout, responsive and print styles.
- `app.js`: text editing, local persistence, JSON exchange, standalone HTML export.
- `assets/poster-reference.jpg`: user-supplied source; retained only for comparison in the editor. Artwork is raster, while poster text and cards are editable HTML.

## Editorial status

This is a redesigned editable reconstruction, not a pixel-exact tracing. The main program structure, dates, support details and evaluation criteria follow the source. The introduction adapts the director’s intent; the internal review contains new suggestions, marked unconfirmed. Verify all dates, funding/partner commitments, eligibility and application details before publication. The director’s relative launch timing conflicts with the poster’s late-October/early-November publicity window; no date was silently resolved. No registration link or unconfirmed quota was invented.

The public read-only poster is deployed with GitHub Pages. JSON import uses text-only insertion and validates known field names.

## GitHub Pages

The public site is built into `docs/` and deployed from the `main` branch `/docs` directory. The public poster is read-only: editor controls, local-storage editing, and the internal operating review are excluded. The source editor remains at the repository root for local use.

After editing source content or styling, rebuild before committing:

```sh
python3 scripts/build_public.py
```

## Official institutional branding

Institution name and contact details were checked against https://arrc.kaist.ac.kr/ and https://arrc.kaist.ac.kr/about on 2026-09-21. The center is the KAIST Augmented Reality Research Center (ARRC), within KAIST KI-ITAIC; contact: arrc@kaist.ac.kr.

Unmodified logo sources:
- https://arrc.kaist.ac.kr/assets/brand/kaist-logo.png
- https://arrc.kaist.ac.kr/assets/brand/arrc-logo.png

The published header uses these official assets instead of the source illustration's embedded studio branding. Program-specific partner/support text remains draft content from the supplied poster.

## Current program direction

Target: finalize the announcement before the Chuseok holiday. Publication/application opening is a separate date still to be agreed; subsequent dates remain provisional.

The current research theme is supporting face-to-face one-to-one conversations with AI glasses, Quest, and related devices, through information, visual context, and interaction support. Website examples are proposals, not fixed assignments or guaranteed device capabilities. The scope centers on face-to-face conversation. Device configurations and team ownership remain open for discussion.
