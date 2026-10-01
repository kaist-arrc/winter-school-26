"""Checks for the published site in docs/.  Run: python -m unittest discover tests"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
sys.path.insert(0, str(ROOT / 'tools'))
from stamp_css import stamp  # noqa: E402

PAGES = sorted(DOCS.rglob('*.html'))


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.add(values['id'])
        for key in ('href', 'src'):
            if values.get(key):
                self.targets.append(values[key])


def parse(page: Path) -> Links:
    parser = Links()
    parser.feed(page.read_text(encoding='utf-8'))
    return parser


def local_file(page: Path, link: str) -> Path | None:
    target = urlsplit(link)
    if target.scheme or target.netloc or not target.path:
        return None
    path = (page.parent / unquote(target.path)).resolve()
    return path / 'index.html' if link.split('#')[0].split('?')[0].endswith('/') or path.is_dir() else path


class SiteTests(unittest.TestCase):
    def test_local_links_and_images_exist(self):
        for page in PAGES:
            for link in parse(page).targets:
                path = local_file(page, link)
                if path is not None:
                    self.assertTrue(path.is_file(), f'{page.relative_to(DOCS)} → {link}')

    def test_concept_links_reach_their_sections(self):
        for route in ('index.html', 'details/index.html'):
            page = DOCS / route
            links = [t for t in parse(page).targets if 'concepts/' in t]
            self.assertEqual(len(links), 3, route)
            for link in links:
                self.assertIn(urlsplit(link).fragment, parse(local_file(page, link)).ids, link)

    def test_css_version_stamps_are_current(self):
        for page in PAGES:
            self.assertEqual(stamp(page), page.read_text(encoding='utf-8'),
                             f'{page.relative_to(DOCS)}: run python tools/stamp_css.py')

    def test_award_is_prominent_and_names_both_tracks(self):
        for route in ('index.html', 'details/index.html'):
            page = (DOCS / route).read_text(encoding='utf-8')
            award = re.search(r'<aside class="internship-award".*?</aside>', page, re.S)
            self.assertIsNotNone(award, route)
            for text in ('KAIST ARRC 연구 인턴십 기회', '해커톤 우수 참가자 선정 시 제공', 'ARRC 센터상', '산업체 선정상', '부상'):
                self.assertIn(text, award.group(), route)
            self.assertNotIn('260만원', page)
            self.assertLess(award.start(), page.index('30,000원'), route)

    def test_old_teaser_url_redirects_home(self):
        self.assertIn('url=./', (DOCS / 'teaser.html').read_text(encoding='utf-8'))

    def test_no_editor_leftovers(self):
        for page in PAGES:
            source = page.read_text(encoding='utf-8')
            for marker in ('contenteditable', 'app.js', 'review-panel', 'data-edit', 'data-program-key'):
                self.assertNotIn(marker, source, page.relative_to(DOCS))


if __name__ == '__main__':
    unittest.main()
