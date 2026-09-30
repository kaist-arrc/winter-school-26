"""Build the read-only GitHub Pages site from the editable source."""
from pathlib import Path
import shutil
import html
import re


def add_social_metadata(source: str, route: str) -> str:
    """Use each page's title and description for server-readable share previews."""
    base = 'https://kaist-arrc.github.io/winter-school-26/'
    title = re.search(r'<title>(.*?)</title>', source).group(1)
    description = re.search(r'<meta name="description" content="([^"]*)">', source).group(1)
    image = base + 'assets/og-image.png'
    alt = 'XR·AI로, 사람과 사람을 더 가깝게. KAIST 해커톤 11월 21–22일, 신청 마감 11월 6일.'
    metadata = f'''<link rel="canonical" href="{base}{route}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="KAIST ARRC">
<meta property="og:title" content="{html.escape(html.unescape(title), quote=True)}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{base}{route}">
<meta property="og:image" content="{image}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(html.unescape(title), quote=True)}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">
<meta name="twitter:image:alt" content="{alt}">
'''
    return source.replace('</head>', metadata + '</head>', 1)


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
''' + re.sub(r'((?:href|src)=")(assets/|content/|concepts/)', r'\1../\2', poster) + '\n</main></body></html>\n'
details_output = output / 'details'
details_output.mkdir(parents=True, exist_ok=True)
(details_output / 'index.html').write_text(add_social_metadata(page, 'details/'), encoding='utf-8')
for name in ('styles.css', 'teaser.html', 'teaser.css'):
    if name == 'teaser.html':
        teaser = inject_program_fields((root / name).read_text(encoding='utf-8'), fields)
        teaser = teaser.replace('href="index.html"', 'href="details/"').replace('href="teaser.html"', 'href="./"')
        teaser = add_social_metadata(teaser, '')
        (output / 'index.html').write_text(teaser, encoding='utf-8')
        # Retain the former promotional URL for existing links.
        (output / name).write_text(teaser, encoding='utf-8')
    else:
        shutil.copy2(root / name, output / name)
for name in ('kaist-logo.png', 'arrc-logo.png', 'symbiotic-air-face-to-face.png', 'og-image.png'):
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
# Publish the text-first concept guide and its explicitly curated illustrations.
concept_output = output / 'concepts'
concept_output.mkdir(parents=True, exist_ok=True)
concept_page = (root / 'concepts' / 'index.html').read_text(encoding='utf-8')
(concept_output / 'index.html').write_text(add_social_metadata(concept_page, 'concepts/'), encoding='utf-8')
shutil.copy2(root / 'concepts' / 'concepts.css', concept_output / 'concepts.css')
illustration_names = (
    'air-observer', 'experience-scenes', 'bts-context', 'human-ai',
    'replay-workshop', 'transfer-workshop', 'paces-everyday',
)
illustration_output = output / 'assets' / 'concept-illustrations'
illustration_output.mkdir(parents=True, exist_ok=True)
for name in illustration_names:
    shutil.copy2(root / 'assets' / 'concept-illustrations' / f'{name}.webp', illustration_output / f'{name}.webp')
# The original poster remains an editor reference, not a public branding asset.
(output / 'assets/poster-reference.jpg').unlink(missing_ok=True)
(output / '.nojekyll').touch()
assert 'contenteditable' not in page
assert 'app.js' not in page
assert 'review-panel' not in page
assert '온라인 모집' in page
print('Built read-only public poster in docs/')
