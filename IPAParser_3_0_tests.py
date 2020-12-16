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
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('y').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close','backness': 'front','rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɨ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ʉ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'central', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɯ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('u').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɪ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_close', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ʏ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_close', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ʊ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('e').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ø').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɘ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɵ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'central', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɤ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('o').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close_mid', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('e̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ø̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ə').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɤ̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('o̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'mid', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɛ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('œ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɜ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɞ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'central', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ʌ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɔ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open_mid', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('æ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_open', 'backness': 'front', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɐ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'near_open', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɶ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'front', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɑ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'back', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ɒ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('a').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ä').as_dict(),
            parser.parse('a').as_dict())

    def test_diphthongs(self):
        self.assertEqual(
            parser.parse('ai').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('aj').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('au').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('aw').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ia').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ja').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ua').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('wa').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        
    def test_triphthongs(self):
        self.assertEqual(
            parser.parse('iau').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': True,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('jau').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': True,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('iaw').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': True,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': set()
            })

    def test_diacritics(self):
        self.assertEqual(
            parser.parse('ia:w').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': True,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'long', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ajˑ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': True, 'triphthong': False,
                'height': None, 'backness': None, 'rounded': None,
                'length': 'half_long', 'phonation': 'modal',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ü').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'centralised'}
            })
        self.assertEqual(
            parser.parse('u̯').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'non_syllabic'}
            })
        self.assertEqual(
            parser.parse('u̥').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'voiceless'}
            })
        self.assertEqual(
            parser.parse('u̝').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'raised'}
            })
        self.assertEqual(
            parser.parse('u̞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'lowered'}
            })
        self.assertEqual(
            parser.parse('u̟').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'advanced'}
            })
        self.assertEqual(
            parser.parse('u̠').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'retracted'}
            })
        self.assertEqual(
            parser.parse('u̹').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'more_rounded'}
            })
        self.assertEqual(
            parser.parse('u̜').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'less_rounded'}
            })
        self.assertEqual(
            parser.parse('ṳ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'breathy_voice',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('ṵ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'creaky_voice',
                'additional_articulations': set()
            })
        self.assertEqual(
            parser.parse('u̘').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'atr'}
            })
        self.assertEqual(
            parser.parse('u̙').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'rtr'}
            })
        self.assertEqual(
            parser.parse('u˞').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'rhotacised'}
            })
        self.assertEqual(
            parser.parse('u̽').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'mid_centralised'}
            })
        self.assertEqual(
            parser.parse('ũ').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'close', 'backness': 'back', 'rounded': True,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'nasalised'}
            })
        self.assertEqual(
            parser.parse('ä̃').as_dict(),
            {
                'apical_vowel': False, 'diphthong': False, 'triphthong': False,
                'height': 'open', 'backness': 'central', 'rounded': False,
                'length': 'short', 'phonation': 'modal',
                'additional_articulations': {'nasalised'}
            })

    def test_apical_vowels(self):
        pass
    

if __name__ == '__main__':
    unittest.main()