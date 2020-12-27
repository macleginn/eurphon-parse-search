from copy import deepcopy
from dataclasses import dataclass
from typing import List, Set, Union
from unicodedata import normalize

from lark import Transformer, Lark

from enums import AdditionalArticulation, Place, Height, Backness
from enums import Length, Phonation, Voice, Manner
from enums import s, n
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
    # Apical vowels have a place. It is stored in this field.
    backness: Union[Backness, Place]
    rounded: bool
    length: Length
    phonation: Phonation
    # Needed for tabulation; also pre-labialised vowels are sometimes posited.
    pre_features: Set[AdditionalArticulation]
    additional_articulations: Set[AdditionalArticulation]

    def as_dict(self):
        """
        n or s stringification is used on nullable
        and non-nullable enum-encoded features respectively.
        """
        return {
            'type': 'vowel',
            'apical_vowel': self.apical_vowel,
            'diphthong': self.diphthong,
            'triphthong': self.triphthong,
            'height': n(self.height),
            'backness': n(self.backness),
            'rounded': self.rounded,
            'length': s(self.length),
            'phonation': s(self.phonation),
            'additional_articulations': set(s(f) for f in self.pre_features) |
            set(s(f) for f in self.additional_articulations)
        }

    def as_list(self):
        result = [s(self.length), s(self.phonation)] +\
            [s(f) for f in self.pre_features] +\
            [s(f) for f in self.additional_articulations]

        if self.height is not None:
            result.append(s(self.height))
        if self.backness is not None:
            result.append(s(self.backness))
        if not (self.diphthong or self.triphthong):
            if self.rounded:
                result.append('rounded')
            else:
                result.append('unrounded')
        if self.diphthong:
            result.append('diphthong')
        elif self.triphthong:
            result.append('triphthong')
        else:
            result.append('monophthong')

        if self.apical_vowel:
            result.append('apical')
        result.append('vowel')
        return result

    def as_set(self):
        return set(self.as_list())


@ dataclass
class ConsonantParse:
    place: Place
    manner: Manner
    voice: Voice
    length: Length
    lateral: bool
    nasal: bool
    implosive: bool
    pre_features: Set[AdditionalArticulation]
    additional_articulations: Set[AdditionalArticulation]

    def as_dict(self):
        return {
            'type': 'consonant',
            'place': s(self.place),
            'manner': s(self.manner),
            # Glottals and epiglottals do not have voice.
            'voice': n(self.voice),
            'length': s(self.length),
            'lateral': self.lateral,
            'nasal': self.nasal,
            'implosive': self.implosive,
            'additional_articulations': set(s(f) for f in self.pre_features) |
            set(s(f) for f in self.additional_articulations)
        }

    def as_list(self):
        result = [s(self.length)]
        if self.voice is not None:
            result.append(s(self.voice))
        result.extend(
            [s(f) for f in self.pre_features] +
            [s(f) for f in self.additional_articulations]
        )
        if self.lateral:
            result.append('lateral')
        if self.nasal:
            result.append('nasal')
        if self.implosive:
            result.append('implosive')
        result.extend([
            s(self.place),
            s(self.manner)
        ])
        result.append('consonant')
        return result

    def as_set(self):
        return set(self.as_list())


#
# Global variables that hold parts of affricates
# for closer inspection
#
affricates_first = None
affricate_second = None


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

    #
    # Vowels
    #

    def vowel(self, params):
        *pre_features, core = params
        if type(core) == Diphthong:
            tmp = VowelParse(False, True, False, None, None, None,
                             Length.SHORT, Phonation.MODAL_VOICE,
                             set(pre_features), set())
        elif type(core) == Triphthong:
            tmp = VowelParse(False, False, True, None, None, None,
                             Length.SHORT, Phonation.MODAL_VOICE,
                             set(pre_features), set())
        else:
            if type(core.glyph) == ApicalVowel:
                tmp = VowelParse(True, False, False, None,
                                 core.glyph.place, core.glyph.rounded,
                                 Length.SHORT, Phonation.MODAL_VOICE,
                                 set(pre_features), set())
            else:
                tmp = VowelParse(False, False, False,
                                 core.glyph.height, core.glyph.backness, core.glyph.rounded,
                                 Length.SHORT, Phonation.MODAL_VOICE,
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

    #
    # Consonants
    #

    def consonant(self, params):
        *pre_features, consonant_core = params
        tmp = ConsonantParse(
            consonant_core.glyph.place,
            consonant_core.glyph.manner,
            consonant_core.glyph.voice,
            Length.SHORT,
            consonant_core.glyph.lateral,
            consonant_core.glyph.nasal,
            consonant_core.glyph.implosive,
            set(pre_features),
            set())
        add_post_features_to_consonant(tmp, consonant_core.post_features)
        return tmp

    def simple_consonant(self, params):
        core, *post_features = params
        return ConsonantCore(core, set(post_features))

    stop = simple_consonant
    fricative = simple_consonant
    approximant = simple_consonant
    tap = simple_consonant
    trill = simple_consonant

    def affricate(self, params: List[ConsonantCore]):
        stop_part, fricative_part = params
        # Set the global variables, so that the user
        # could have a full picture of the affricate components
        global affricates_first
        affricates_first = stop_part
        global affricate_second
        affricate_second = fricative_part
        # The fricative part determines the parse.
        affricate_glyph = deepcopy(fricative_part.glyph)
        affricate_glyph.manner = Manner.AFFRICATE
        return ConsonantCore(affricate_glyph, set.union(
            stop_part.post_features,
            fricative_part.post_features
        ))

    # Atomic consonants

    # Plosives
    def voiceless_bilabial_plosive(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_bilabial_plosive(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.PLOSIVE, Voice.VOICED)

    def voiceless_alveolar_plosive(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_alveolar_plosive(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.PLOSIVE, Voice.VOICED)

    def voiceless_retroflex_plosive(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_retroflex_plosive(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.PLOSIVE, Voice.VOICED)

    def voiceless_palatal_plosive(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_palatal_plosive(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.PLOSIVE, Voice.VOICED)

    def voiceless_velar_plosive(self, _):
        return SimpleConsonant(Place.VELAR, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_velar_plosive(self, _):
        return SimpleConsonant(Place.VELAR, Manner.PLOSIVE, Voice.VOICED)

    def voiceless_uvular_plosive(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_uvular_plosive(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.PLOSIVE, Voice.VOICED)

    def epiglottal_plosive(self, _):
        return SimpleConsonant(Place.EPIGLOTTAL, Manner.PLOSIVE, None)

    def glottal_stop(self, _):
        return SimpleConsonant(Place.GLOTTAL, Manner.PLOSIVE, None)

    def voiceless_labial_alveolar_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_ALVEOLAR, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_labial_alveolar_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_ALVEOLAR, Manner.PLOSIVE, Voice.VOICED)

    def voiceless_labial_velar_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_VELAR, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_labial_velar_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_VELAR, Manner.PLOSIVE, Voice.VOICED)

    def voiceless_uvular_epiglottal_plosive(self, _):
        return SimpleConsonant(Place.UVULAR_EPIGLOTTAL, Manner.PLOSIVE, Voice.VOICELESS)

    def voiced_bilabial_nasal_plosive(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiced_labiodental_nasal_plosive(self, _):
        return SimpleConsonant(Place.LABIODENTAL, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiced_alveolar_nasal_plosive(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiced_retroflex_nasal_plosive(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiced_palatal_nasal_plosive(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiced_velar_nasal_plosive(self, _):
        return SimpleConsonant(Place.VELAR, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiced_uvular_nasal_plosive(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiceless_labial_alveolar_nasal_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_ALVEOLAR, Manner.PLOSIVE, Voice.VOICELESS, nasal=True)

    def voiced_labial_alveolar_nasal_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_ALVEOLAR, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiced_labial_velar_nasal_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_VELAR, Manner.PLOSIVE, Voice.VOICED, nasal=True)

    def voiceless_labial_velar_nasal_plosive(self, _):
        return SimpleConsonant(Place.LABIAL_VELAR, Manner.PLOSIVE, Voice.VOICELESS, nasal=True)

    def voiced_bilabial_implosive(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.PLOSIVE, Voice.VOICED, implosive=True)

    def voiced_alveolar_implosive(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.PLOSIVE, Voice.VOICED, implosive=True)

    def voiced_retroflex_implosive(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.PLOSIVE, Voice.VOICED, implosive=True)

    def voiced_palatal_implosive(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.PLOSIVE, Voice.VOICED, implosive=True)

    def voiced_velar_implosive(self, _):
        return SimpleConsonant(Place.VELAR, Manner.PLOSIVE, Voice.VOICED, implosive=True)

    def voiced_uvular_implosive(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.PLOSIVE, Voice.VOICED, implosive=True)

    def voiced_labial_velar_implosive(self, _):
        return SimpleConsonant(Place.LABIAL_VELAR, Manner.PLOSIVE, Voice.VOICED, implosive=True)

    # Fricatives
    def voiceless_bilabial_fricative(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_bilabial_fricative(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_labiodental_fricative(self, _):
        return SimpleConsonant(Place.LABIODENTAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_labiodental_fricative(self, _):
        return SimpleConsonant(Place.LABIODENTAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_interdental_fricative(self, _):
        return SimpleConsonant(Place.INTERDENTAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_interdental_fricative(self, _):
        return SimpleConsonant(Place.INTERDENTAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_alveolar_fricative(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_alveolar_fricative(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_hissing_hushing_fricative(self, _):
        return SimpleConsonant(Place.HISSING_HUSHING, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_hissing_hushing_fricative(self, _):
        return SimpleConsonant(Place.HISSING_HUSHING, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_postalveolar_fricative(self, _):
        return SimpleConsonant(Place.POSTALVEOLAR, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_postalveolar_fricative(self, _):
        return SimpleConsonant(Place.POSTALVEOLAR, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_alveolo_palatal_fricative(self, _):
        return SimpleConsonant(Place.ALVEOLO_PALATAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_alveolo_palatal_fricative(self, _):
        return SimpleConsonant(Place.ALVEOLO_PALATAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_retroflex_fricative(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_retroflex_fricative(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_palatal_fricative(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_palatal_fricative(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_velar_fricative(self, _):
        return SimpleConsonant(Place.VELAR, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_velar_fricative(self, _):
        return SimpleConsonant(Place.VELAR, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_palatal_velar_fricative(self, _):  # ɧ
        return SimpleConsonant(Place.PALATAL_VELAR, Manner.FRICATIVE, Voice.VOICELESS)

    def voiceless_uvular_fricative(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_uvular_fricative(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_pharyngeal_fricative(self, _):
        return SimpleConsonant(Place.PHARYNGEAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_pharyngeal_fricative(self, _):
        return SimpleConsonant(Place.PHARYNGEAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_glottal_fricative(self, _):
        return SimpleConsonant(Place.GLOTTAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_glottal_fricative(self, _):
        return SimpleConsonant(Place.GLOTTAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_epiglottal_fricative(self, _):
        return SimpleConsonant(Place.EPIGLOTTAL, Manner.FRICATIVE, Voice.VOICELESS)

    def voiced_epiglottal_fricative(self, _):
        return SimpleConsonant(Place.EPIGLOTTAL, Manner.FRICATIVE, Voice.VOICED)

    def voiceless_alveolar_lateral_fricative(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.FRICATIVE, Voice.VOICELESS, lateral=True)

    def voiced_alveolar_lateral_fricative(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.FRICATIVE, Voice.VOICED, lateral=True)

    def voiceless_retroflex_lateral_fricative(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.FRICATIVE, Voice.VOICELESS, lateral=True)

    def voiced_retroflex_lateral_fricative(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.FRICATIVE, Voice.VOICED, lateral=True)

    def voiceless_palatal_lateral_fricative(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.FRICATIVE, Voice.VOICELESS, lateral=True)

    def voiced_palatal_lateral_fricative(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.FRICATIVE, Voice.VOICED, lateral=True)

    def voiceless_velar_lateral_fricative(self, _):
        return SimpleConsonant(Place.VELAR, Manner.FRICATIVE, Voice.VOICELESS, lateral=True)

    def voiced_velar_lateral_fricative(self, _):
        return SimpleConsonant(Place.VELAR, Manner.FRICATIVE, Voice.VOICED, lateral=True)

    # Approximants
    def voiceless_interdental_approximant(self, _):
        return SimpleConsonant(Place.INTERDENTAL, Manner.APPROXIMANT, Voice.VOICELESS)

    def voiced_interdental_approximant(self, _):
        return SimpleConsonant(Place.INTERDENTAL, Manner.APPROXIMANT, Voice.VOICED)

    def voiceless_bilabial_approximant(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.APPROXIMANT, Voice.VOICELESS)

    def voiced_bilabial_approximant(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_labiodental_approximant(self, _):
        return SimpleConsonant(Place.LABIODENTAL, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_alveolar_approximant(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_retroflex_approximant(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_palatal_approximant(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_velar_approximant(self, _):
        return SimpleConsonant(Place.VELAR, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_uvular_approximant(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_alveolar_lateral_approximant(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.APPROXIMANT, Voice.VOICED, lateral=True)

    def voiced_retroflex_lateral_approximant(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.APPROXIMANT, Voice.VOICED, lateral=True)

    def voiced_palatal_lateral_approximant(self, _):
        return SimpleConsonant(Place.PALATAL, Manner.APPROXIMANT, Voice.VOICED, lateral=True)

    def voiced_velar_lateral_approximant(self, _):
        return SimpleConsonant(Place.VELAR, Manner.APPROXIMANT, Voice.VOICED, lateral=True)

    def voiced_uvular_lateral_approximant(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.APPROXIMANT, Voice.VOICED, lateral=True)

    def voiceless_labio_velar_approximant(self, _):
        return SimpleConsonant(Place.LABIAL_VELAR, Manner.APPROXIMANT, Voice.VOICELESS)

    def voiced_labio_velar_approximant(self, _):
        return SimpleConsonant(Place.LABIAL_VELAR, Manner.APPROXIMANT, Voice.VOICED)

    def voiced_labio_palatal_approximant(self, _):
        return SimpleConsonant(Place.LABIAL_PALATAL, Manner.APPROXIMANT, Voice.VOICED)

    # Taps

    def voiced_labiodental_tap(self, _):
        return SimpleConsonant(Place.LABIODENTAL, Manner.TAP, Voice.VOICED)

    def voiced_alveolar_tap(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.TAP, Voice.VOICED)

    def voiced_alveolar_lateral_tap(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.TAP, Voice.VOICED, lateral=True)

    def voiced_retroflex_tap(self, _):
        return SimpleConsonant(Place.RETROFLEX, Manner.TAP, Voice.VOICED)

    # Trills

    def voiced_alveolar_trill(self, _):
        return SimpleConsonant(Place.ALVEOLAR, Manner.TRILL, Voice.VOICED)

    def voiced_bilabial_trill(self, _):
        return SimpleConsonant(Place.BILABIAL, Manner.TRILL, Voice.VOICED)

    def voiced_uvular_trill(self, _):
        return SimpleConsonant(Place.UVULAR, Manner.TRILL, Voice.VOICED)

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

    def voiced(self, _):
        return Voice.VOICED

    def creaky_voiced(self, _):
        return Phonation.CREAKY_VOICE

    def ingressive(self, _):
        return AdditionalArticulation.INGRESSIVE

    def rhotacised(self, _):
        return AdditionalArticulation.RHOTACISED

    def strong_articulation(self, _):
        return AdditionalArticulation.STRONG_ARTICULATION

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

    def ejective(self, _):
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

    def tenuis(self, _):
        return AdditionalArticulation.TENUIS

    def linguo_labial(self, _):
        return AdditionalArticulation.LINGUO_LABIAL

#
# Helper functions
#


def add_post_features_to_vowel(parse: VowelParse, features):
    for f in features:
        if type(f) == Length:
            parse.length = f
        elif type(f) == Phonation:
            parse.phonation = f
        else:
            if f == AdditionalArticulation.NON_SYLLABIC and\
                    (parse.diphthong or parse.triphthong):
                continue
            parse.additional_articulations.add(f)


def add_post_features_to_consonant(parse: ConsonantParse, features):
    for f in features:
        if type(f) == Length:
            parse.length = f
        elif type(f) == Place:
            parse.place = f
        elif type(f) == Voice:
            if (
                parse.voice == Voice.VOICED
                and f == Voice.VOICELESS
                and parse.manner in {Manner.PLOSIVE, Manner.AFFRICATE}
                and not parse.nasal
            ):
                parse.voice = Voice.DEVOICED
            else:
                parse.voice = f
        else:
            parse.additional_articulations.add(f)


#
# A replacement dictionary for handling ambiguous
# and non-decomposable sequences.
#

replacement_dict = {
    # A special symbol for double length
    # to resolve ambiguity
    '::': '=',
    'ːː': '=',
    'ː:': '=',
    ':ː': '=',

    # Vowel height or backness denoted by a diacritic
    'e\u031e': 'E1',
    'o\u031e': 'O1',
    'ø\u031e': 'O2',
    'ɒ\u0308': 'A1',
    'ɤ\u031e': 'Y1',
    'ɨ\u031e': 'I1',
    'ɯ\u031e': 'W1',
    'ʉ\u031e': 'U1',

    # Approximants denoted as fricatives with a "lowered" diacritic
    'θ\u031e': 'D1',
    'ð\u031e': 'D2',
    'ɸ\u031e': 'V1',
    'β\u031e': 'V2',
    'ʁ\u031e': 'R1',

    # Fricatives denoted as approximants with a
    # "raised"/"frictionalised" diacritic
    '\u026d\u030a\u031d': 'L1',
    '\u026d\u031d\u030a': 'L1',
    '\u026d\u031d': 'L11',
    '\u028e\u031d\u030a': 'L2',
    '\u028e\u030a\u031d': 'L2',
    '\u028e\u031d': 'L22',
    '\u029f\u031d\u030a': 'L3',
    '\u029f\u030a\u031d': 'L3',
    '\u029f\u031d': 'L4',
    '\u029f\u0353': 'L4',

    # Hissing-hushing fricatives
    's\u0302': 'S1',
    'z\u0302': 'Z1',

    # Misc
    'ɚ': 'ə\u02de',
    'g': 'ɡ',
    'ɫ': 'lˠ',
    'ʟ\u0320': 'L5',
    'c\u0327': '\xe7',  # Denormalise decomposed /ç/

    # Redundant encoding of features in PHOIBLE
    'n̠d̠': 'nd',
    'n̠t̠': 'nt',
    'n̤d̤z̤': 'nd̤z̤',
    'n̠d̠ʒ': 'ndʒ',
    'd̠ʒ': 'dʒ',
    'n̠̤d̠̤ʒ': 'nd̤ʒ',
    'n̠̊t̠ʃ': 'ntʃ',
    'n̠t̠ʃ': 'ntʃ',
    't̠ʃ': 'tʃ',
    'n̤d̤ɮ̤': 'nd̤ɮ̤',
    'n̪t̪': 'nt̪',
    'n̪d̪': 'nd̪',
    'n̤d̤': 'nd̤',
    'm̤b̤': 'mb̤',
    'n̤ɡ̤': 'nɡ̤',
    'ŋ̤ɡ̤': 'ŋɡ̤',
    'm̤b̤v̤': 'mb̤v̤',
    'ɲ̤ɟ̤': 'ɲɟ̤',
    'm̊p': 'mp',
    'm̤pʰ': 'mpʰ',
    'n̤tʰ': 'ntʰ',
    'ŋ̤kʰ': 'ŋkʰ',
    'ɲ̤cʰ': 'ɲcʰ',
    'ŋɡmb': 'ŋɡb',
    'ŋmkp': 'ŋkp',
    'ȵ': 'ɲ',
    'ɲ̟dʑ': 'ɲdʑ',
    'ɲ̟tɕʰ': 'ɲtɕʰ',
    'ʆ': 'ʃʲ',
    'ʓ': 'ʒʲ',
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
        # Replace single glyphs for uniformity.
        result = result.replace('\u02d4', '\u031d')   # Raised
        result = result.replace('\u0325', '\u030a')   # Voiceless
        # Replace glyph combinations
        for k, v in replacement_dict.items():
            result = result.replace(k, v)
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
    if type(result) == ConsonantParse and result.manner == Manner.AFFRICATE:
        print('Affricate components:')
        print('First part:', affricates_first.as_set())
        print('Second part:', affricate_second.as_set())
    print()
    print('Parse as a (space-joined) list:')
    pprint(' '.join(result.as_list()))
