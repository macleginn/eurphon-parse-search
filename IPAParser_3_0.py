from dataclasses import dataclass
from typing import List, Set, Union
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
    backness: Backness
    rounded: bool
    length: Length
    phonation: Phonation
    # Needed for tabulation; also pre-labialised vowels are sometimes posited.
    pre_features: Set[AdditionalArticulation]
    additional_articulations: Set[AdditionalArticulation]


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
    def vowel(
        self, 
        pre_features: List[AdditionalArticulation], 
        core: Union[VowelAtom, Diphthong, Triphthong]
    ):
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

    def diphthong(
        self, 
        onset: Union[OnsetCoda, VowelAtom], 
        coda: Union[OnsetCoda, VowelAtom]
    ):
        return Diphthong(onset, coda)

    def triphthong(
        self,
        onset: Union[OnsetCoda, VowelAtom],
        middle_element: VowelAtom,
        coda: Union[OnsetCoda, VowelAtom]
    ):
        return Triphthong(onset, middle_element, coda)

    def vowel_atom(
        self,
        vowel_glyph: Union[ApicalVowel, RegularVowel],
        post_features: List[Union[AdditionalArticulation, Length, Phonation, Voice, Place]]
    ):
        return VowelAtom(vowel_glyph, set(post_features))

    def onset_coda(
        self,
        wj: Union[WElement, JElement],
        post_features: List[Union[AdditionalArticulation, Length, Phonation, Voice, Place]]
    ):
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
        return AdditionalArticulation.MID_CETNRALISED
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
