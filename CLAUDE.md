# ARRC Winter School

- Public routes: `/` serves the promotional poster; `/details/` serves the detailed poster. Keep `/teaser.html` available for existing links.
- `docs/` is the site and the source: edit `docs/index.html` (promotional) and `docs/details/index.html` (detail) directly; there is no build step. `docs/teaser.html` only redirects to `/`. Internal material goes in `notes/`, never in `docs/`.
- After any CSS change run `python tools/stamp_css.py` (content-hash `?v=` cache busting), then `python -m unittest discover tests`.
- Symbiotic AIR: depict a human-to-human, same-place 1:1 discussion, not a chatbot, message exchange, remote call, or AI interlocutor.
- AI/AR glasses provide quiet contextual support while people lead the discussion and decision; consented feedback helps the support improve.
- The teaser is a concise recruitment poster led by “XR·AI로, 사람과 사람을 더 가깝게.” Keep the hackathon date, submission deadline and concrete proposal requirements prominent. Longer AIR4BTS concept explanations live in an expandable reference section and the detail poster.
- In the teaser program flow, highlight the hackathon and internship equally as the core experiences; keep the online application/evaluation stage visibly secondary and all three cards horizontally aligned.
- Center vision: Symbiotic AIR4BTS captures observable human-experience evidence with AIR Glasses and multimodal sensors, structures it as experience models and reusable XR assets, adapts it to new people/spaces/times/tasks, and feeds outcomes back into ongoing human–AI co-adaptation.
- Program narrative: define one small, meaningful real-world problem → discover, implement, and validate it in the hackathon → assetize and extend the result through the internship and follow-on research.
- Field hackathon: select 16–30 applicants from the online call, form two-person teams, and provide libraries or a basic framework tailored to submitted ideas, development devices, development computers, and AI accounts for two days of development. Both days start at 09:00; Day 1 ends with 5h+ team development, Day 2 has midpoint/faculty feedback, 6h+ development, and 17:00 presentations. Select 7–10 interns for follow-on research.
- Concept reference: https://kaist-arrc.github.io/arrc-10th/

- Eligibility: KAIST undergraduate and graduate students. Hackathon support: two days of pay at the student personnel rate for their position, meals/snacks, no accommodation.
- Idea proposals must specify situation × device. Situations: work/research meetings (goal-oriented), personal discussion (general), teaching/order-taking (one-way emphasis). Devices, numbered 1–3 as type → capability → example: 1 Audio-first (camera + audio, no display: Ray-Ban Meta); 2 Lightweight (camera + small display: Rokid AR Glasses); 3 Immersive (camera + immersive display: Meta Quest 3). Situations are lettered A–C.
- Design: both posters share `docs/site.css` and the same reader-question bands (어떻게 진행되나요? / 무엇을 제안하나요? / 무엇을 얻나요?). The situation × device 3×3 matrix is the one signature element; the cyan `--signal` color is reserved for it and gold `--gold` for the award.
