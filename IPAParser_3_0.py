from copy import deepcopy
from dataclasses import dataclass
from typing import List, Set, Union
from unicodedata import normalize

from lark import Transformer, Lark

from enums import AdditionalArticulation, Place, Height, Backness
from enums import Length, Phonation, Voice, Manner
from segment_types import *

# 
# The output types for the parser.
# 

@dataclass
class VowelParse:
    apical_vowel: bool
    diphthong: bool
    triphthong: bool
    height: Height
    backness: Union[Backness, Place]  # Apical vowels have a place.
    rounded: bool
    length: Length
    phonation: Phonation
    # Needed for tabulation; also pre-labialised vowels are sometimes posited.
    pre_features: Set[AdditionalArticulation]
    additional_articulations: Set[AdditionalArticulation]

    def as_dict(self):
        return {
            'apical_vowel': self.apical_vowel,
            'diphthong': self.diphthong,
            'triphthong': self.triphthong,
            'height': self.height.name.lower() if self.height is not None else None,
            'backness': self.backness.name.lower() if self.backness is not None else None,
            'rounded': self.rounded,
            'length': self.length.name.lower() if self.length is not None else None,
            'phonation': self.phonation.name.lower() if self.phonation is not None else None,
            'additional_articulations': set(
                f.name.lower() for f in self.pre_features
            ).union(set(
                f.name.lower() for f in self.additional_articulations))
        }


@dataclass
class ConsonantParse:
    place: Place
    manner: Manner
    voice: Voice
    length: Length
    lateral: bool
    nasal: bool
    doubly_articulated: bool
    implosive: bool
    click: bool
    pre_features: Set[AdditionalArticulation]
    additional_articulations: Set[AdditionalArticulation]


# 
# Classes and helper functions needed to manipulate
# the output of the Lark parser
# 

class IPAQueryTransformer(Transformer):
    """
    This class guides the transformation
    of the Lark tree into a parse dictionary.
    IPA notation is not recursive, so there is
    no need for an AST.
    """
    def vowel(self, params):
        *pre_features, core = params
        if type(core) == Diphthong:
            tmp = VowelParse(False, True, False, None, None, None,
                Length.SHORT, Phonation.MODAL, 
                set(pre_features), set())
        elif type(core) == Triphthong:
            tmp = VowelParse(False, False, True, None, None, None,
                Length.SHORT, Phonation.MODAL,
                set(pre_features), set())
        else:
            if type(core.glyph) == ApicalVowel:
                tmp = VowelParse(True, False, False, None, 
                    core.glyph.place, core.glyph.rounded, 
                    Length.SHORT, None,
                    set(pre_features), set())
            else:
                tmp = VowelParse(False, False, False,
                    core.glyph.height, core.glyph.backness, core.glyph.rounded,
                    Length.SHORT, Phonation.MODAL,
                    set(pre_features), set())
        add_post_features_to_vowel(tmp, core.post_features)
        return tmp

    def diphthong(self, params):
        onset, coda = params
        return Diphthong(onset, coda)

    def triphthong(self, params):
        onset, middle_element, coda = params
        return Triphthong(onset, middle_element, coda)

    def vowel_atom(self, params):
        vowel_glyph, *post_features = params
        return VowelAtom(vowel_glyph, set(post_features))

    def onset_coda(self, params):
        wj, *post_features = params
        return OnsetCoda(wj, set(post_features))

    def w(self, _):
        return WElement()

    def j(self, _):
        return JElement()

    # Functions for atomic elements.

    # Apical vowels

    def alveolar_apical_vowel_unrounded(self, _):
        return ApicalVowel(Place.ALVEOLAR, False)
    def alveolar_apical_vowel_rounded(self, _):
        return ApicalVowel(Place.ALVEOLAR, True)
    def postalveolar_apical_vowel_unrounded(self, _):
        return ApicalVowel(Place.POSTALVEOLAR, False)
    def postalveolar_apical_vowel_rounded(self, _):
        return ApicalVowel(Place.POSTALVEOLAR, True)

    # Regular vowels

    def close_front_unrounded(self, _):
        return RegularVowel(Height.CLOSE, Backness.FRONT, False)
    def close_front_rounded(self, _):
        return RegularVowel(Height.CLOSE, Backness.FRONT, True)
    def close_central_unrounded(self, _):
        return RegularVowel(Height.CLOSE, Backness.CENTRAL, False)
    def close_central_rounded(self, _):
        return RegularVowel(Height.CLOSE, Backness.CENTRAL, True)
    def close_back_unrounded(self, _):
        return RegularVowel(Height.CLOSE, Backness.BACK, False)
    def close_back_rounded(self, _):
        return RegularVowel(Height.CLOSE, Backness.BACK, True)
    
    def near_close_front_unrounded(self, _):
        return RegularVowel(Height.NEAR_CLOSE, Backness.FRONT, False)
    def near_close_front_rounded(self, _):
        return RegularVowel(Height.NEAR_CLOSE, Backness.FRONT, True)
    def near_close_central_unrounded(self, _):
        return RegularVowel(Height.NEAR_CLOSE, Backness.CENTRAL, False)
    def near_close_central_rounded(self, _):
        return RegularVowel(Height.NEAR_CLOSE, Backness.CENTRAL, True)
    def near_close_back_unrounded(self, _):
        return RegularVowel(Height.NEAR_CLOSE, Backness.BACK, False)
    def near_close_back_rounded(self, _):
        return RegularVowel(Height.NEAR_CLOSE, Backness.BACK, True)
    
    def close_mid_front_unrounded(self, _):
        return RegularVowel(Height.CLOSE_MID, Backness.FRONT, False)
    def close_mid_front_rounded(self, _):
        return RegularVowel(Height.CLOSE_MID, Backness.FRONT, True)
    def close_mid_central_unrounded(self, _):
        return RegularVowel(Height.CLOSE_MID, Backness.CENTRAL, False)
    def close_mid_central_rounded(self, _):
        return RegularVowel(Height.CLOSE_MID, Backness.CENTRAL, True)
    def close_mid_back_unrounded(self, _):
        return RegularVowel(Height.CLOSE_MID, Backness.BACK, False)
    def close_mid_back_rounded(self, _):
        return RegularVowel(Height.CLOSE_MID, Backness.BACK, True)
    
    def mid_front_unrounded(self, _):
        return RegularVowel(Height.MID, Backness.FRONT, False)
    def mid_front_rounded(self, _):
        return RegularVowel(Height.MID, Backness.FRONT, True)
    def mid_central_unrounded(self, _):
        return RegularVowel(Height.MID, Backness.CENTRAL, False)
    def mid_back_unrounded(self, _):
        return RegularVowel(Height.MID, Backness.BACK, False)
    def mid_back_rounded(self, _):
        return RegularVowel(Height.MID, Backness.BACK, True)
    
    def open_mid_front_rounded(self, _):
        return RegularVowel(Height.OPEN_MID, Backness.FRONT, True)
    def open_mid_front_unrounded(self, _):
        return RegularVowel(Height.OPEN_MID, Backness.FRONT, False)
    def open_mid_central_unrounded(self, _):
        return RegularVowel(Height.OPEN_MID, Backness.CENTRAL, False)
    def open_mid_central_rounded(self, _):
        return RegularVowel(Height.OPEN_MID, Backness.CENTRAL, True)
    def open_mid_back_unrounded(self, _):
        return RegularVowel(Height.OPEN_MID, Backness.BACK, False)
    def open_mid_back_rounded(self, _):
        return RegularVowel(Height.OPEN_MID, Backness.BACK, True)
    
    def near_open_front_unrounded(self, _):
        return RegularVowel(Height.NEAR_OPEN, Backness.FRONT, False)
    def near_open_central_unrounded(self, _):
        return RegularVowel(Height.NEAR_OPEN, Backness.CENTRAL, False)
    
    def open_front_rounded(self, _):
        return RegularVowel(Height.OPEN, Backness.FRONT, True)
    def open_central_unrounded(self, _):
        return RegularVowel(Height.OPEN, Backness.CENTRAL, False)
    def open_central_rounded(self, _):
        return RegularVowel(Height.OPEN, Backness.CENTRAL, True)
    def open_back_unrounded(self, _):
        return RegularVowel(Height.OPEN, Backness.BACK, False)
    def open_back_rounded(self, _):
        return RegularVowel(Height.OPEN, Backness.BACK, True)

    # Functions for additional articulations
    def pre_aspirated(self, _):
        return AdditionalArticulation.PRE_ASPIRATED
    def pre_glottalised(self, _):
        return AdditionalArticulation.PRE_GLOTTALISED
    def pre_nasalised(self, _):
        return AdditionalArticulation.PRE_NASALISED
    def pre_labialised(self, _):
        return AdditionalArticulation.PRE_LABIALISED

    def overlong(self, _):
        return Length.OVERLONG
    def long(self, _):
        return Length.LONG
    def half_long(self, _):
        return Length.HALF_LONG
    def pharyngealised(self, _):
        return AdditionalArticulation.PHARYNGEALISED
    def nasalised(self, _):
        return AdditionalArticulation.NASALISED
    def shortened(self, _):
        return Length.SHORTENED
    def raised(self, _):
        return AdditionalArticulation.RAISED
    def lowered(self, _):
        return AdditionalArticulation.LOWERED
    def advanced(self, _):
        return AdditionalArticulation.ADVANCED
    def retracted(self, _):
        return AdditionalArticulation.RETRACTED
    def breathy_voiced(self, _):
        return Phonation.BREATHY_VOICE
    def voiceless(self, _):
        return Voice.VOICELESS
    def creaky_voiced(self, _):
        return Phonation.CREAKY_VOICE
    def ingressive(self, _):
        return AdditionalArticulation.INGRESSIVE
    def rhotacised(self, _):
        return AdditionalArticulation.RHOTACISED
    def faucalised(self, _):
        return AdditionalArticulation.FAUCALISED
    def centralised(self, _):
        return AdditionalArticulation.CENTRALISED
    def atr(self, _):
        return AdditionalArticulation.ATR
    def rtr(self, _):
        return AdditionalArticulation.RTR
    def less_rounded(self, _):
        return AdditionalArticulation.LESS_ROUNDED
    def more_rounded(self, _):
        return AdditionalArticulation.MORE_ROUNDED
    def non_syllabic(self, _):
        return AdditionalArticulation.NON_SYLLABIC
    def mid_centralised(self, _):
        return AdditionalArticulation.MID_CENTRALISED
    def aspirated(self, _):
        return AdditionalArticulation.ASPIRATED
    def palatalised(self, _):
        return AdditionalArticulation.PALATALISED
    def labialised(self, _):
        return AdditionalArticulation.LABIALISED
    def ejective (self, _):
        return AdditionalArticulation.EJECTIVE
    def glottalised(self, _):
        return AdditionalArticulation.GLOTTALISED
    def velarised(self, _):
        return AdditionalArticulation.VELARISED
    def lateral_released(self, _):
        return AdditionalArticulation.LATERAL_RELEASED
    def unreleased(self, _):
        return AdditionalArticulation.UNRELEASED
    def syllabic(self, _):
        return AdditionalArticulation.SYLLABIC
    def dental(self, _):
        return Place.DENTAL
    def alveolar(self, _):
        return Place.ALVEOLAR
    def apical(self, _):
        return AdditionalArticulation.APICAL
    def laminal(self, _):
        return AdditionalArticulation.LAMINAL
    def weakly_articulated(self, _):
        return AdditionalArticulation.WEAKLY_ARTICULATED
    def labio_palatalised(self, _):
        return AdditionalArticulation.LABIO_PALATALISED
    def nasal_released(self, _):
        return AdditionalArticulation.NASAL_RELEASED
    def affricated(self, _):
        return AdditionalArticulation.AFFRICATED
    def epilaryngeal_source(self, _):
        return AdditionalArticulation.EPILARYNGEAL_SOURCE
    def frictionalised(self, _):
        return AdditionalArticulation.FRICTIONALISED

# 
# Helper functions
# 

def add_post_features_to_vowel(parse, features):
    for f in features:
        if type(f) == Length:
            parse.length = f
        elif type(f) == Phonation:
            parse.phonation = f
        else:
            parse.additional_articulations.add(f)


# 
# A replacement dictionary for handling ambiguous
# and non-decomposable sequences.
# 

replacement_dict = {
    'e\u031e': 'E1',
    'o\u031e': 'O1',
    'ø\u031e': 'O2',
    'ɒ\u0308': 'A1',
    'ɤ\u031e': 'Y1',
    'ɨ\u031e': 'I1',
    'ɯ\u031e': 'W1',
    'ʉ\u031e': 'U1',
    'ɚ': 'ə\u02de'
}


# 
# The exported class
# 

class IPAParser:
    def __init__(self):
        with open('ipa_parse_grammar.lark', 'r', encoding='utf-8') as inp:
            self.parser = Lark(inp.read(), start='segment')
        self.transformer = IPAQueryTransformer()

    def _preprocess(self, input_str):
        result = normalize('NFD', input_str.strip())
        for k, v in replacement_dict.items():
            result = result.replace(k,v)
        return result

    def parse(self, input_str):
        "Returns the parse of input_str as a ConsonantParse or VowelParse."
        return self.transformer.transform(
            self.parser.parse(
                self._preprocess(input_str)))
    
    def parse_no_transform(self, input_str):
        "Returns the raw Lark output."
        return self.parser.parse(
            self._preprocess(input_str))


# 
# A basic test; see IPAParser_3_0_test.py for 
# a more comprehensive test suite.
# 

if __name__ == "__main__":
    import sys
    from pprint import pprint
    input_segment = sys.argv[1]
    parser = IPAParser()
    parse_raw = parser.parse_no_transform(input_segment)
    result = parser.parse(input_segment)
    print(f'Input segment: [{input_segment}]\n')
    print('Lark parse tree:')
    print(parse_raw.pretty())
    print('Parse as a Python dictionary:')
    pprint(result.as_dict())