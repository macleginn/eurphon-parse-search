import unittest
from IPAParser_3_0 import IPAParser


parser = IPAParser()


class TestVowelParsing(unittest.TestCase):

    def test_plain_vowels(self):
        self.assertEqual(
            parser.parse('i').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('y').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close','backness': 'front','rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɨ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ʉ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'central', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɯ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('u').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɪ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_close', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ʏ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_close', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ʊ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('e').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ø').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɘ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɵ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'central', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɤ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('o').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('e̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ø̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ə').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɤ̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('o̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɛ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('œ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɜ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɞ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'central', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ʌ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɔ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('æ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_open', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɐ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_open', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɶ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɑ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ɒ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('a').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set(),
            })
        self.assertEqual(
            parser.parse('ä').as_dict(),
            parser.parse('a').as_dict())

    def test_diphthongs(self):
        pass

    def test_triphthongs(self):
        pass

    def test_diacritics(self):
        pass
    

if __name__ == '__main__':
    unittest.main()