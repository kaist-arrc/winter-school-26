"""Build the read-only GitHub Pages site from the editable source."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
source = (root / 'index.html').read_text()
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
<meta name="description" content="KAIST KI-ARRC 2026–2027 Winter Research Talent Program 운영계획(안). 온라인 아이디어 제안에서 현장 해커톤, 인턴 연구로 이어지는 단계형 연구경험 프로그램.">
<title>KAIST ARRC · Winter Research Talent Program</title>
<link rel="stylesheet" href="styles.css">
<style>body{padding:24px 0} @media(max-width:700px){body{padding:10px 0}} @media print{body{padding:0}}</style>
</head><body><main>
''' + poster + '\n</main></body></html>\n'
(output / 'index.html').write_text(page)
shutil.copy2(root / 'styles.css', output / 'styles.css')
shutil.copy2(root / 'assets/poster-reference.jpg', output / 'assets/poster-reference.jpg')
(output / '.nojekyll').touch()
assert 'contenteditable' not in page
assert 'app.js' not in page
assert 'review-panel' not in page
print('Built read-only public poster in docs/')
