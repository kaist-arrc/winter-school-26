# ARRC Winter Research Talent Program

Public-facing program posters with a small version date in each footer. The source editor retains a separate internal review panel.

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

- `content/program.md`: single source of truth for the public schedule, program flow, online evaluation format and poster copy.
- `content/google-form-questions.md`: questions, types and descriptions for manually configuring the Google Forms application.
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

The builder reads `content/program.md`, injects its labeled fields into generated copies of both poster sources, and writes the read-only pages to `docs/`. The homepage (`docs/index.html`) shows the promotional poster; `/details/` shows the detailed poster. Application buttons link to the Google Forms response page.

## Official institutional branding

Institution name and contact details were checked against https://arrc.kaist.ac.kr/ and https://arrc.kaist.ac.kr/about on 2026-09-21. The center is the KAIST Augmented Reality Research Center (ARRC), within KAIST KI-ITAIC; contact: arrc@kaist.ac.kr.

Unmodified logo sources:
- https://arrc.kaist.ac.kr/assets/brand/kaist-logo.png
- https://arrc.kaist.ac.kr/assets/brand/arrc-logo.png

The published header uses these official assets instead of the source illustration's embedded studio branding. Program-specific partner/support text remains draft content from the supplied poster.

## Current program direction

The public pages present the current program information without draft banners. Registration links have not been supplied; contact information remains available.

The program is open to KAIST undergraduate and graduate students. Applicants must specify a one-to-one conversation situation × device: work/research meetings (goal-oriented discussion), personal discussion (general discussion), or teaching/order-taking (emphasis on one-way communication); paired with camera + audio devices, Lightweight (camera + small display: Rokid AR Glasses), or Immersive (Quest 3).

ARRC collects hackathon ideas, provides libraries or a basic framework tailored to those ideas, and participants use them to develop over two days. Support includes two days of pay at the student personnel rate appropriate to the participant's position, meals and snacks, development devices/computers, and AI accounts. Accommodation is not provided.
### AI glasses landscape reviewed

The program framing was checked on 2026-09-22 against current official developer and challenge material:

- Meta positions AI glasses development around camera, audio, optional display, and hands-free mobile extensions: https://developers.meta.com/wearables/
- Android XR distinguishes audio glasses, display glasses, wired XR glasses, and headsets, with capabilities and interaction varying by form factor: https://developer.android.com/develop/xr
- Snap’s official Spectacles community maintains a hackathon showcase: https://developers.snap.com/spectacles/spectacles-community/hackathon-showcase
- The IEEE SLT 2026 SmartGlasses Challenge focuses on egocentric multi-talker speech interaction: https://aslp-lab.github.io/SmartGlasses/

These references support making AI glasses visible in the recruitment hook, asking teams to justify device choice, and judging a focused real-world interaction rather than hardware complexity. They do not establish which devices ARRC owns or can provide; inventory, SDK access, account setup, and support capacity still require internal confirmation.

## Two poster versions

- `teaser.html`: attention-focused poster, with a conversation hook, brief research directions, device choice, benefits and a link to details. Public URL: https://kaist-arrc.github.io/winter-school-26/ (the former `/teaser.html` URL also works)
- `docs/details/index.html`: information-rich public program poster, generated from the source editor. Public URL: https://kaist-arrc.github.io/winter-school-26/details/
- `teaser.css`: self-contained recruitment poster layout, including mobile and A3 print styles. Both versions show their version date in the footer and use the official institution assets.

Run `python3 scripts/build_public.py` after changing either version. Keep agreed program terms consistent between both sources. The promotional poster links to Google Forms for applications and to `/details/` for the full program.

## AIR4BTS concept references

Both posters link to three annotated original diagrams (expand “AIR4BTS, 연구 개념과 그림 더 보기” on the teaser) in `assets/air4bts_woo/`: the AIR–AMI–BTS framework, adaptive experience transfer, and PACES. `scripts/build_public.py` copies only these selected originals into `docs/assets/air4bts_woo/`. The remaining supplied images stay as local reference material. The posters distinguish this long-term research vision from the two-day, one-to-one conversation prototype scope.
