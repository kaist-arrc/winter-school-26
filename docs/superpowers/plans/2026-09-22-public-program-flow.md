# 외부 공개용 프로그램 흐름 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task with verification checkpoints.

**Goal:** Make one Markdown source control the public schedule, program flow, online evaluation instructions, and example content used by both poster versions.

**Architecture:** Add `content/program.md` as the canonical copy source and `content/online-evaluation-submission-example.md` as the applicant-facing template/example. Extend the dependency-free public builder to parse labeled Markdown fields and replace marked elements in both source posters before producing read-only `docs/` output.

**Tech Stack:** Static HTML/CSS, Python 3 standard library, Markdown content files, existing `scripts/build_public.py` build.

## Global Constraints

- The public flow starts at `온라인 모집`; internal “공고 확정·홍보 준비” does not appear as a public step.
- Online evaluation requires one concept image (PNG/JPG or one-page PDF) plus an approximately 300-character summary.
- Both poster versions must use the same canonical schedule and evaluation copy.
- No third-party Python dependencies or runtime server are added.
- Generated `docs/` remains read-only and must exclude editor controls and the internal review panel.

---

### Task 1: Add canonical Markdown content

**Files:**
- Create: `content/program.md`
- Create: `content/online-evaluation-submission-example.md`

**Interfaces:**
- Produces labeled fields consumed by `scripts/build_public.py`: `flow-step-1` through `flow-step-8`, `flow-date-1` through `flow-date-8`, `flow-detail-3`, `flow-detail-5`, `flow-detail-6`, `flow-detail-8`, `schedule-note`, `online-lead`, `online-1` through `online-5`, `online-format`, `online-summary`, and `online-example-title`.

- [ ] **Step 1: Write the canonical program Markdown** with a `## poster-fields` section containing one `key: value` line per field, followed by readable sections for schedule, public flow, evaluation, and editorial notes.
- [ ] **Step 2: Write the submission template/example Markdown** including required fields, image guidance, a copyable blank template, and a complete example titled “처음 만난 사람과의 대화를 돕는 AI 글래스”.
- [ ] **Step 3: Check the files** with `rg -n "flow-step-1|온라인 모집|1장|300|예시" content` and confirm all required fields are present.

### Task 2: Mark poster sources for content injection

**Files:**
- Modify: `index.html` in the timeline and online-evaluation card
- Modify: `teaser.html` in the process list and CTA/support copy

**Interfaces:**
- Consumes the field names from Task 1 through `data-program-key="..."` attributes.

- [ ] **Step 1: Mark the public flow elements** in `index.html` with `data-program-key` attributes and remove the internal first step so the visible timeline begins with online recruitment.
- [ ] **Step 2: Mark online evaluation copy** in `index.html` for the submission format, criteria, and example callout.
- [ ] **Step 3: Mark the three-step teaser flow** in `teaser.html` so its first step is online recruitment and its copy matches the canonical stages.

### Task 3: Parse Markdown and build both posters

**Files:**
- Modify: `scripts/build_public.py`

**Interfaces:**
- Add `parse_program_fields(path: Path) -> dict[str, str]` that reads only the `## poster-fields` section and returns trimmed key/value pairs.
- Add `inject_program_fields(source: str, fields: dict[str, str]) -> str` that replaces the text content of elements carrying `data-program-key` while preserving tags and attributes.

- [ ] **Step 1: Add parser tests as executable checks** inside the script for missing-field and multiline-value behavior using standard-library assertions.
- [ ] **Step 2: Implement `parse_program_fields`** with UTF-8 reading, section boundaries, first-colon splitting, and clear `ValueError` messages for malformed lines.
- [ ] **Step 3: Implement `inject_program_fields`** using an HTML parser from the standard library or a constrained tag replacement that handles the existing marked elements safely; HTML-escape field text before insertion.
- [ ] **Step 4: Apply injection** to both root sources before stripping editor/review sections, and copy the applicant example Markdown into `docs/` for public access.
- [ ] **Step 5: Run `python scripts/build_public.py`** and verify it prints the build success message.

### Task 4: Verify public outputs and editability

**Files:**
- Modify: `README.md` with the new source-of-truth workflow and public example link
- Generated: `docs/index.html`, `docs/teaser.html`, `docs/content/online-evaluation-submission-example.md`

- [ ] **Step 1: Search generated HTML** for `온라인 모집`, `온라인 평가`, `1장 이미지`, and `300자`.
- [ ] **Step 2: Confirm removed internal content** with searches showing no `공고 확정·홍보 준비`, `contenteditable`, `app.js`, or `review-panel` in generated pages.
- [ ] **Step 3: Confirm both pages contain the same online-evaluation format and first flow stage.**
- [ ] **Step 4: Open the local server or use a static HTML check** to confirm the generated links and Markdown example are reachable.
- [ ] **Step 5: Run `git diff --check` and `git status --short` before handoff.**
