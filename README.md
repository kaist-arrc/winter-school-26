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

The common research theme is “AR/XR로 돕는 1:1 대면 대화”: supporting face-to-face one-to-one conversations through information, visual context, and interaction support. AI glasses are presented as a primary device option because their first-person camera, microphone, audio, and—on supported models—display can support contextual, hands-free experiences. Participants still choose target devices according to their research focus and implementation approach; Quest and other XR devices remain valid options. Website examples are proposals, not fixed assignments or guaranteed device capabilities. Program benefits include access to research devices and support for using AI tools. Specific inventories and support arrangements remain to be finalized.

### AI glasses landscape reviewed

The program framing was checked on 2026-09-22 against current official developer and challenge material:

- Meta positions AI glasses development around camera, audio, optional display, and hands-free mobile extensions: https://developers.meta.com/wearables/
- Android XR distinguishes audio glasses, display glasses, wired XR glasses, and headsets, with capabilities and interaction varying by form factor: https://developer.android.com/develop/xr
- Snap’s official Spectacles community maintains a hackathon showcase: https://developers.snap.com/spectacles/spectacles-community/hackathon-showcase
- The IEEE SLT 2026 SmartGlasses Challenge focuses on egocentric multi-talker speech interaction: https://aslp-lab.github.io/SmartGlasses/

These references support making AI glasses visible in the recruitment hook, asking teams to justify device choice, and judging a focused real-world interaction rather than hardware complexity. They do not establish which devices ARRC owns or can provide; inventory, SDK access, account setup, and support capacity still require internal confirmation.

## Two poster versions

- `teaser.html`: attention-focused poster, with a conversation hook, brief research directions, device choice, benefits and a link to details. Public URL: https://kaist-arrc.github.io/winter-school-26/teaser.html
- `docs/index.html`: information-rich public program poster, generated from the source editor. Public URL: https://kaist-arrc.github.io/winter-school-26/
- `teaser.css`: promotional poster layout. Both versions include a draft notice and use the official institution assets.

Run `python3 scripts/build_public.py` after changing either version. Keep agreed program terms consistent between both sources. The promotional poster currently invites readers to view details; it does not present an application button while registration is unconfirmed.
