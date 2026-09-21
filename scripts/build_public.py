"""Build the read-only GitHub Pages site from the editable source."""
from pathlib import Path
import shutil
import html
import re


def parse_program_fields(path: Path) -> dict[str, str]:
    """Read the simple key/value section used as the poster copy source."""
    lines = path.read_text(encoding='utf-8').splitlines()
    try:
        start = lines.index('## poster-fields') + 1
    except ValueError as exc:
        raise ValueError(f'Missing ## poster-fields in {path}') from exc
    fields: dict[str, str] = {}
    for line in lines[start:]:
        if line.startswith('## '):
            break
        if not line.strip():
            continue
        if ':' not in line:
            raise ValueError(f'Malformed poster field: {line!r}')
        key, value = line.split(':', 1)
        key, value = key.strip(), value.strip()
        if not key:
            raise ValueError(f'Empty poster field key: {line!r}')
        fields[key] = value.replace('\\n', '\n')
    return fields


def inject_program_fields(source: str, fields: dict[str, str]) -> str:
    """Replace text inside elements marked with data-program-key."""
    for key, value in fields.items():
        if f'data-program-key="{key}"' not in source and f"data-program-key='{key}'" not in source:
            continue
        pattern = re.compile(
            rf'(<(?P<tag>[A-Za-z][\w:-]*)\b[^>]*data-program-key=["\']{re.escape(key)}["\'][^>]*>).*?(</(?P=tag)>)',
            re.DOTALL,
        )
        replacement = html.escape(value).replace('\n', '<br>')
        source, count = pattern.subn(lambda match: match.group(1) + replacement + match.group(3), source, count=1)
        if count != 1:
            raise ValueError(f'No unique data-program-key target found for {key!r}')
    return source

root = Path(__file__).resolve().parent.parent
fields = parse_program_fields(root / 'content' / 'program.md')
source = inject_program_fields((root / 'index.html').read_text(encoding='utf-8'), fields)
poster = source.split('<section id="poster-panel" role="tabpanel" aria-labelledby="tab-poster">', 1)[1].split('<section id="review-panel"', 1)[0]
# The panel wrapper closes immediately after the poster article.
poster = poster.rsplit('</section>', 1)[0]
output = root / 'docs'
(output / 'assets').mkdir(parents=True, exist_ok=True)
page = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#093c76">
<meta name="description" content="KAIST 증강현실연구센터(ARRC) 2026–2027 Winter Research Talent Program 운영계획(안). AR/XR로 돕는 1:1 대면 대화를 탐구하는 단계형 연구경험 프로그램.">
<title>[작업 중] KAIST ARRC · Winter Research Talent Program</title>
<link rel="stylesheet" href="styles.css">
<style>body{padding:24px 0}.work-notice{max-width:1100px;margin:0 auto 18px;padding:16px 20px;border:1px solid #e2c785;border-left:4px solid #b58328;border-radius:5px;background:#fff8e8;color:#654b1c}.work-notice strong{display:block;font-size:16px;margin-bottom:5px}.work-notice p{margin:0;font-size:12px;line-height:1.8}@media(max-width:1136px){.work-notice{margin-left:18px;margin-right:18px}}@media(max-width:700px){body{padding:10px 0}.work-notice{margin:0 10px 12px;padding:12px 14px}}@media print{body{padding:0}.work-notice{margin:0 0 5mm;break-inside:avoid}}</style>
</head><body>
<nav class="poster-versions no-print" aria-label="포스터 버전"><span>WINTER RESEARCH TALENT PROGRAM</span><div><a href="teaser.html">01 홍보형</a><a href="index.html" aria-current="page">02 상세형</a></div></nav>
<main>
<aside class="work-notice" aria-label="작업 중 안내"><strong>작업 중인 초안입니다 · Work in progress</strong><p>추석 연휴 전 공고 확정을 목표로 프로그램 내용을 검토·수정하고 있습니다. 일정, 지원자격, 선발방식 및 지원 내용은 확정되지 않았으며 변경될 수 있습니다. 이 페이지는 최종 모집 공고가 아닙니다.</p></aside>
''' + poster + '\n</main></body></html>\n'
(output / 'index.html').write_text(page, encoding='utf-8')
for name in ('styles.css', 'teaser.html', 'teaser.css'):
    if name == 'teaser.html':
        teaser = inject_program_fields((root / name).read_text(encoding='utf-8'), fields)
        (output / name).write_text(teaser, encoding='utf-8')
    else:
        shutil.copy2(root / name, output / name)
for name in ('kaist-logo.png', 'arrc-logo.png'):
    shutil.copy2(root / 'assets' / name, output / 'assets' / name)
output_content = output / 'content'
output_content.mkdir(parents=True, exist_ok=True)
shutil.copy2(root / 'content' / 'online-evaluation-submission-example.md', output_content / 'online-evaluation-submission-example.md')
shutil.copy2(root / 'content' / 'online-evaluation-example.svg', output_content / 'online-evaluation-example.svg')
# The original poster remains an editor reference, not a public branding asset.
(output / 'assets/poster-reference.jpg').unlink(missing_ok=True)
(output / '.nojekyll').touch()
assert 'contenteditable' not in page
assert 'app.js' not in page
assert 'review-panel' not in page
assert '온라인 모집' in page
print('Built read-only public poster in docs/')
