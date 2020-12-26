from dataclasses import dataclass
from typing import List, Set, Union
from enums import AdditionalArticulation, Place, Manner, Voice, Height, Backness, s, n


#
# Classes encapsulating properties of different
# vowel types.
#


@dataclass
class ApicalVowel:
    place: Place
    rounded: bool


@dataclass
class RegularVowel:
    height: Height
    backness: Backness
    rounded: bool


class VowelAtom:
    def __init__(
        self,
        glyph: Union[ApicalVowel, RegularVowel],
        post_features: Set[AdditionalArticulation]
    ):
        self.glyph = glyph
        self.post_features = post_features


# TODO: Add some kind of glyph to the next two types.
class WGlyph:
    def __init__(self):
        pass


class WElement:
    def __init__(self):
        self.glyph = WGlyph()


class JGlyph:
    def __init__(self):
        pass


class JElement:
    def __init__(self):
        self.glyph = JGlyph()


class OnsetCoda:
    def __init__(
        self,
        initial: Union[WElement, JElement],
        post_features: List[AdditionalArticulation]
    ):
        # We don't use the initial in any way for now.
        self.glyph = initial.glyph
        self.post_features = set(post_features)


class Diphthong:
    def __init__(
        self,
        onset: Union[OnsetCoda, VowelAtom],
        coda: Union[OnsetCoda, VowelAtom]
    ):
        self.onset = onset.glyph
        self.coda = coda.glyph
        self.post_features = set()
        for f in onset.post_features:
            self.post_features.add(f)
        for f in coda.post_features:
            self.post_features.add(f)


class Triphthong:
    def __init__(
        self,
        onset: Union[OnsetCoda, VowelAtom],
        middle_element: VowelAtom,
        coda: Union[OnsetCoda, VowelAtom]
    ):
        self.post_features = set()
        for f in onset.post_features:
            self.post_features.add(f)
        for f in middle_element.post_features:
            self.post_features.add(f)
        for f in coda.post_features:
            self.post_features.add(f)


#
# Classes encapsulating properties
# of different consonant types.
#


@dataclass
class SimpleConsonant:
    place: Place
    manner: Manner
    voice: Voice
    nasal: bool = False
    lateral: bool = False
    implosive: bool = False


class ConsonantCore:
    def __init__(
        self,
        glyph: SimpleConsonant,
        post_features: Set[AdditionalArticulation]
    ):
        self.glyph = glyph
        self.post_features = post_features

    def as_dict(self):
        return {
            'place': s(self.glyph.place),
            'manner': s(self.glyph.manner),
            'voice': s(self.glyph.voice),
            'additional_articulations': set(s(el) for el in self.post_features)
        }

    def as_set(self):
        return set([
            s(self.glyph.place),
            s(self.glyph.manner),
            s(self.glyph.voice)
        ]) | set(s(el) for el in self.post_features)
