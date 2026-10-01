"""Stamp stylesheet links with a content hash so browsers fetch changed CSS.

Run after editing any CSS in docs/:  python tools/stamp_css.py
tests/test_site.py fails while a stamp is stale.
"""
from hashlib import sha256
from pathlib import Path
import re

DOCS = Path(__file__).resolve().parents[1] / 'docs'
LINK = re.compile(r'(<link rel="stylesheet" href=")([^"?]+\.css)(?:\?v=[0-9a-f]+)?(")')


def css_version(css: Path) -> str:
    return sha256(css.read_bytes()).hexdigest()[:8]


def stamp(page: Path) -> str:
    source = page.read_text(encoding='utf-8')
    return LINK.sub(lambda m: f'{m[1]}{m[2]}?v={css_version((page.parent / m[2]).resolve())}{m[3]}', source)


if __name__ == '__main__':
    for page in sorted(DOCS.rglob('*.html')):
        stamped = stamp(page)
        if stamped != page.read_text(encoding='utf-8'):
            page.write_text(stamped, encoding='utf-8')
            print('stamped', page.relative_to(DOCS))
