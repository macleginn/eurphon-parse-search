from dataclasses import dataclass
from typing import List, Set, Union
from enums import AdditionalArticulation, Place, Height, Backness

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


class WElement:
    def __init__(self):
        pass


class JElement:
    def __init__(self):
        pass


class OnsetCoda:
    def __init__(
        self, 
        initial: Union[WElement, JElement], 
        post_features: List[AdditionalArticulation]
    ):
        # We don't use the initial in any way for now.
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
        for f in coda.post_features:
            self.post_features.add(f)
