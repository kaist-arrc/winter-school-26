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
<meta name="description" content="KAIST 증강현실연구센터(ARRC) 2026–2027 Winter Research Talent Program 운영계획(안). 온라인 아이디어 제안에서 현장 해커톤, 인턴 연구로 이어지는 단계형 연구경험 프로그램.">
<title>[작업 중] KAIST ARRC · Winter Research Talent Program</title>
<link rel="stylesheet" href="styles.css">
<style>body{padding:24px 0}.work-notice{max-width:1100px;margin:0 auto 18px;padding:16px 20px;border:1px solid #e2c785;border-left:4px solid #b58328;border-radius:5px;background:#fff8e8;color:#654b1c}.work-notice strong{display:block;font-size:16px;margin-bottom:5px}.work-notice p{margin:0;font-size:12px;line-height:1.8}@media(max-width:1136px){.work-notice{margin-left:18px;margin-right:18px}}@media(max-width:700px){body{padding:10px 0}.work-notice{margin:0 10px 12px;padding:12px 14px}}@media print{body{padding:0}.work-notice{margin:0 0 5mm;break-inside:avoid}}</style>
</head><body><main>
<aside class="work-notice" aria-label="작업 중 안내"><strong>작업 중인 초안입니다 · Work in progress</strong><p>현재 프로그램 내용을 검토·수정하고 있습니다. 일정, 지원자격, 선발방식 및 지원 내용은 확정되지 않았으며 변경될 수 있습니다. 이 페이지는 최종 모집 공고가 아닙니다.</p></aside>
''' + poster + '\n</main></body></html>\n'
(output / 'index.html').write_text(page)
shutil.copy2(root / 'styles.css', output / 'styles.css')
for name in ('kaist-logo.png', 'arrc-logo.png'):
    shutil.copy2(root / 'assets' / name, output / 'assets' / name)
# The original poster remains an editor reference, not a public branding asset.
(output / 'assets/poster-reference.jpg').unlink(missing_ok=True)
(output / '.nojekyll').touch()
assert 'contenteditable' not in page
assert 'app.js' not in page
assert 'review-panel' not in page
print('Built read-only public poster in docs/')
