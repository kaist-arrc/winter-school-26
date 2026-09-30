"""Check the published posters keep the award prominent and conditional."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PosterAwardTests(unittest.TestCase):
    def test_award_precedes_fees_on_both_posters(self):
        for route in ('docs/index.html', 'docs/details/index.html'):
            with self.subTest(route=route):
                page = (ROOT / route).read_text(encoding='utf-8')
                award = re.search(r'<aside class="internship-award".*?</aside>', page, re.S)
                self.assertIsNotNone(award, 'Dedicated internship award area is missing')
                self.assertIn('KAIST ARRC 연구 인턴십 기회', award.group())
                self.assertIn('260만원 상당', award.group())
                self.assertIn('해커톤 우수 참가자 선정 시 제공', award.group())
                self.assertLess(award.start(), page.index('data-program-key="registration-title"'))
                self.assertIn('30,000원', page)
                self.assertIn('150,000원', page)


if __name__ == '__main__':
    unittest.main()
