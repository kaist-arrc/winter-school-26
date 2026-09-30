"""Exercise publication of the reconstructed concept references."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


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
            if key in values:
                self.targets.append(values[key])


class ConceptPublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, 'scripts/build_public.py'], cwd=ROOT, check=True)

    def test_poster_concept_links_resolve_to_published_sections(self):
        for route in ('index.html', 'details/index.html'):
            page = ROOT / 'docs' / route
            parser = Links()
            parser.feed(page.read_text(encoding='utf-8'))
            concept_links = [t for t in parser.targets if 'concepts/' in t]
            self.assertEqual(len(concept_links), 3, route)
            for link in concept_links:
                target = urlsplit(link)
                destination = (page.parent / unquote(target.path) / 'index.html').resolve()
                self.assertTrue(destination.is_file(), link)
                contents = Links()
                contents.feed(destination.read_text(encoding='utf-8'))
                self.assertIn(target.fragment, contents.ids, link)

    def test_concept_illustrations_and_styles_are_published(self):
        page = ROOT / 'docs/concepts/index.html'
        self.assertTrue(page.is_file())
        parser = Links()
        parser.feed(page.read_text(encoding='utf-8'))
        for link in parser.targets:
            target = urlsplit(link)
            if not target.scheme and target.path and not target.path.endswith('/'):
                self.assertTrue((page.parent / unquote(target.path)).resolve().is_file(), link)


if __name__ == '__main__':
    unittest.main()
