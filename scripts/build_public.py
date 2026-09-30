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
<meta name="description" content="KAIST 증강현실연구센터(ARRC) 2026–2027 Winter Research Talent Program 안내. AR/XR로 돕는 1:1 대면 대화를 탐구하는 단계형 연구경험 프로그램.">
<title>KAIST ARRC · Winter Research Talent Program</title>
<link rel="stylesheet" href="../styles.css">
<style>body{padding:24px 0}@media(max-width:700px){body{padding:10px 0}}@media print{body{padding:0}}</style>
</head><body>
<nav class="poster-versions no-print" aria-label="포스터 버전"><span>WINTER RESEARCH TALENT PROGRAM</span><div><a href="../">01 홍보형</a><a href="./" aria-current="page">02 상세형</a></div></nav>
<main>
''' + re.sub(r'((?:href|src)=")(assets/|content/)', r'\1../\2', poster) + '\n</main></body></html>\n'
details_output = output / 'details'
details_output.mkdir(parents=True, exist_ok=True)
(details_output / 'index.html').write_text(page, encoding='utf-8')
for name in ('styles.css', 'teaser.html', 'teaser.css'):
    if name == 'teaser.html':
        teaser = inject_program_fields((root / name).read_text(encoding='utf-8'), fields)
        teaser = teaser.replace('href="index.html"', 'href="details/"').replace('href="teaser.html"', 'href="./"')
        (output / 'index.html').write_text(teaser, encoding='utf-8')
        # Retain the former promotional URL for existing links.
        (output / name).write_text(teaser, encoding='utf-8')
    else:
        shutil.copy2(root / name, output / name)
for name in ('kaist-logo.png', 'arrc-logo.png', 'symbiotic-air-face-to-face.png'):
    shutil.copy2(root / 'assets' / name, output / 'assets' / name)
# Publish only the concept references linked from the posters, preserving originals.
reference_names = (
    '29405226-2EC3-4148-92DE-F0D3CD0B64FE.png',
    'iOS 이미지 (4).jpg',
    '7C35FF8E-DB95-42DA-A416-F18C9A2E47D7.png',
)
reference_output = output / 'assets' / 'air4bts_woo'
reference_output.mkdir(parents=True, exist_ok=True)
for name in reference_names:
    shutil.copy2(root / 'assets' / 'air4bts_woo' / name, reference_output / name)
# The original poster remains an editor reference, not a public branding asset.
(output / 'assets/poster-reference.jpg').unlink(missing_ok=True)
(output / '.nojekyll').touch()
assert 'contenteditable' not in page
assert 'app.js' not in page
assert 'review-panel' not in page
assert '온라인 모집' in page
print('Built read-only public poster in docs/')
