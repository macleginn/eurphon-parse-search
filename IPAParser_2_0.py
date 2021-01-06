from sys import argv, stderr
from pprint import pprint

MAIN_GLYPHS_CONS = {
    'ⱱ', #\u2c71
    'β', #\u03b2
    'θ', #\u03b8
    'χ', #\u03c7
    'ᴅ', #\u1d05
    'ᶑ', #\u1d91
    'ʙ', #\u0299
    'ʛ', #\u029
    'ʝ', #\u029d
    'ʟ', #\u029f
    'ʡ', #\u02a1
    'ʐ', #\u0290
    'ʑ', #\u0291
    'ʒ', #\u0292
    'ʔ', #\u0294
    'ʕ', #\u0295
    'ʋ', #\u028
    'ʍ', #\u028d
    'ʎ', #\u028e
    'ɸ', #\u0278
    'ɹ', #\u0279
    'ɺ', #\u027a
    'ɻ', #\u027
    'ɽ', #\u027d
    'ɾ', #\u027e
    'ʀ', #\u0280
    'ʁ', #\u0281
    'ʂ', #\u0282
    'ʃ', #\u0283
    'ʄ', #\u0284
    'ʈ', #\u0288
    'ɰ', #\u0270
    'ɱ', #\u0271
    'ɲ', #\u0272
    'ɳ', #\u0273
    'ɴ', #\u0274
    'ɫ', #\u026
    'ɬ', #\u026c
    'ɭ', #\u026d
    'ɮ', #\u026e
    'ɥ', #\u0265
    'ɦ', #\u0266
    'ɧ', #\u0267
    'ɟ', #\u025f
    'ɠ', #\u0260
    'ɡ', #\u0261
    'g', #g
    'ɢ', #\u0262
    'ɣ', #\u0263
    'ɓ', #\u0253
    'ɕ', #\u0255
    'ɖ', #\u0256
    'ɗ', #\u0257
    'z', #z
    'ç', #\xe7
    'ð', #\xf0
    'ø', #\xf8
    'ħ', #\u0127
    'ŋ', #\u014
    'b', #b
    'c', #c
    'd', #d
    'f', #f
    'h', #h
    'j', #j
    'k', #k
    'l', #l
    'm', #m
    'n', #n
    'p', #p
    'q', #q
    'r', #r
    's', #s
    't', #t
    'v', #v
    'w', #w
    'x', #x
    'ʢ', #\u02a2
    'ʜ', #\u029c
    'ŝ', #\u015d
    'ẑ'  #\u1e91
}

# TODO: add escape seqs for vowel main glyphs

MAIN_GLYPHS_VOWS = {
    'ɿ': {
        'apical vowel': True
    },
    'ʅ': {
        'apical vowel': True
    },
    'ʮ': {
        'apical vowel': True
    },
    'ʯ': {
        'apical vowel': True
    },
    'z': {
        'apical vowel': True
    },
    'a': {
        'height': 'open',
        'backness': 'central',
        'rounded': False
    },
    'a\u0308': {
        'height': 'open',
        'backness': 'central',
        'rounded': False
    }, # ä
    'e': {
        'height': 'close-mid',
        'backness': 'front',
        'rounded': False
    },
    'e\u031e': {
        'height': 'mid',
        'backness': 'front',
        'rounded': False
    }, # e̞
    'i': {
        'height': 'close',
        'backness': 'front',
        'rounded': False,
    },
    'o': {
        'height': 'close-mid',
        'backness': 'back',
        'rounded': True,
    },
    'o\u031e': {
        'height': 'mid',
        'backness': 'back',
        'rounded': True,
    }, # o̞
    'u': {
        'height': 'close',
        'backness': 'back',
        'rounded': True,
    },
    'y': {
        'height': 'close',
        'backness': 'front',
        'rounded': True,
    },
    'æ': {
        'height': 'near-open',
        'backness': 'front',
        'rounded': False,
    },
    'ø': {
        'height': 'close-mid',
        'backness': 'front',
        'rounded': True,
    },
    'ø\u031e': {
        'height': 'mid',
        'backness': 'front',
        'rounded': True,
    }, # ø̞
    'œ': {
        'height': 'open-mid',
        'backness': 'front',
        'rounded': True,
    },
    'ɐ': {
        'height': 'near-open',
        'backness': 'central',
        'rounded': False,
    },
    'ɑ': {
        'height': 'open',
        'backness': 'back',
        'rounded': False,
    },
    'ɒ': {
        'height': 'open',
        'backness': 'back',
        'rounded': True,
    },
    'ɒ\u0308': {
        'height': 'open',
        'backness': 'central',
        'rounded': True,
    }, # ɒ̈
    'ɔ': {
        'height': 'open-mid',
        'backness': 'back',
        'rounded': True,
    },
    'ɘ': {
        'height': 'close-mid',
        'backness': 'central',
        'rounded': False,
    },
    'ə': {
        'height': 'mid',
        'backness': 'central',
        'rounded': False,
    },
    'ɛ': {
        'height': 'open-mid',
        'backness': 'front',
        'rounded': False,
    },
    'ɜ': {
        'height': 'open-mid',
        'backness': 'central',
        'rounded': False,
    },
    'ɞ': {
        'height': 'open-mid',
        'backness': 'central',
        'rounded': True,
    },
    'ɤ': {
        'height': 'close-mid',
        'backness': 'back',
        'rounded': False,
    },
    'ɤ\u031e': {
        'height': 'mid',
        'backness': 'back',
        'rounded': False,
    }, # ɤ̞
    'ɨ': {
        'height': 'close',
        'backness': 'central',
        'rounded': False,
    },
    'ɨ\u031e': {
        'height': 'near-close',
        'backness': 'central',
        'rounded': False,
    }, # ɨ̞
    'ɪ': {
        'height': 'near-close',
        'backness': 'front',
        'rounded': False,
    },
    'ɯ': {
        'height': 'close',
        'backness': 'back',
        'rounded': False,
    },
    'ɯ\u031e': {
        'height': 'near-close',
        'backness': 'back',
        'rounded': False,
    }, # ɯ̞
    'ɵ': {
        'height': 'close-mid',
        'backness': 'central',
        'rounded': True,
    },
    'ɶ': {
        'height': 'open',
        'backness': 'front',
        'rounded': True,
    },
    'ʉ': {
        'height': 'close',
        'backness': 'central',
        'rounded': True,
    },
    'ʉ\u031e': {
        'height': 'near-close',
        'backness': 'central',
        'rounded': True,
    }, # ʉ̞
    'ʊ': {
        'height': 'near-close',
        'backness': 'back',
        'rounded': True,
    },
    'ʌ': {
        'height': 'open-mid',
        'backness': 'back',
        'rounded': False,
    },
    'ʏ': {
        'height': 'near-close',
        'backness': 'front',
        'rounded': True,
    },
}

# Manners for consonants

PLOSIVES = {'b', 'c', 'd', 'g', 'ɡ', 'k', 'p', 'q', 't', 'ɖ', 'ɟ', 'ɢ', 'ʈ', 'ʔ', 'ʡ'}
IMPLOSIVES = {'ɓ', 'ɗ', 'ɠ', 'ʄ', 'ʛ', 'ᶑ'}
NASALS = {'m', 'n', 'ŋ', 'ɱ', 'ɲ', 'ɳ', 'ɴ'}
TRILLS = {'r', 'ʀ', 'ʙ', 'ʢ', 'ʜ'}
TAPS = {'ɽ', 'ɾ', 'ⱱ'}
LATERAL_TAPS = {'ɺ'}
FRICATIVES = {'f', 'h', 's', 'v', 'x', 'z', 'ç', 'ð', 'ħ', 'ɕ', 'ɣ', 'ɦ', 'ɸ', 'ʁ', 'ʂ', 'ʃ', 'ʐ', 'ʑ', 'ʒ', 'ʕ', 'ʝ', 'β', 'θ', 'χ', 'ƺ', 'ʓ', 'ɧ', 'ŝ', 'ẑ'}
LATERAL_FRICATIVES = {'ɬ', 'ɮ'}
APPROXIMANTS = {'j', 'w', 'ɥ', 'ɰ', 'ɹ', 'ɻ', 'ʋ', 'ʍ'}
LATERAL_APPROXIMANTS = {'l', 'ɫ', 'ɭ', 'ʎ', 'ʟ'}

# Places for consonants

BILABIAL = {'b', 'm', 'p', 'ɸ', 'ʙ', 'β', 'ɓ'}
LABIAL_VELAR = {'w', 'ʍ'}
LABIAL_PALATAL = {'ɥ'}
LABIODENTAL = {'f', 'v', 'ɱ', 'ʋ', 'ⱱ'}
INTERDENTAL = {'ð', 'θ'}
ALVEOLAR = {'ɗ', 'ɹ', 'ɾ', 'ɮ', 'ɬ', 'r', 't', 'n', 'ɫ', 'l', 'd', 's', 'z', 'ɺ'}
POSTALVEOLAR = {'ʃ', 'ʒ'}
HISSING_HUSHING = {'ŝ', 'ẑ'}
RETROFLEX = {'ɖ', 'ɭ', 'ɳ', 'ɻ', 'ɽ', 'ʂ', 'ʈ', 'ʐ', 'ᶑ'}
ALVEOLO_PALATAL = {'ɕ', 'ʑ'}
PALATAL = {'c', 'j', 'ç', 'ɟ', 'ɲ', 'ʎ', 'ʝ', 'ʄ'}
PALATAL_VELAR = {'ɧ'}
VELAR = {'g', 'ɡ', 'k', 'x', 'ŋ', 'ɣ', 'ɰ', 'ʟ', 'ɠ'}
UVULAR = {'q', 'ɢ', 'ɴ', 'ʀ', 'ʁ', 'χ', 'ʛ'}
PHARYNGEAL = {'ħ', 'ʕ'}
GLOTTAL = {'ʔ', 'h', 'ɦ'}
EPIGLOTTAL = {'ʜ', 'ʢ', 'ʡ'}

# Voiced segs

VOICED = {'b', 'd', 'g', 'ɡ', 'j', 'l', 'm', 'n', 'r', 'v', 'w', 'z', 'ð', 'ŋ', 'ɓ', 'ᶑ', 'ɖ', 'ɗ', 'ɟ', 'ɠ', 'ɢ', 'ɣ', 'ɥ', 'ɦ', 'ɭ', 'ɮ', 'ɰ', 'ɱ', 'ɲ', 'ɳ', 'ɴ', 'ɹ', 'ɺ', 'ɻ', 'ɽ', 'ɾ', 'ʀ', 'ʁ', 'ʄ', 'ʎ', 'ʐ', 'ʑ', 'ʒ', 'ʙ', 'ʛ', 'ʝ', 'ʟ', 'ʢ', 'β', 'ɫ', 'ʓ', 'ʕ', 'ⱱ', 'ʋ', 'ẑ'}

# Reference data structures for vowels.
# Not used in actual parsing at the moment:
# we simply check all possible glyphs

# Vowels by height

CLOSE = {'i', 'u', 'y', 'ɨ', 'ɯ', 'ʉ'}
NEAR_CLOSE = {'ɪ', 'ɪ\u0308', 'ʊ', 'ʊ\u0308', 'ʏ', 'ɨ\u031e', 'ʉ\u031e'}
CLOSE_MID = {'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o'}
MID = {'e\u031e', 'ø\u031e', 'ə', 'ɚ', 'ɤ\u031e', 'o\u031e'}
OPEN_MID = {'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ'}
NEAR_OPEN = {'æ', 'ɐ'}
OPEN = {'a', 'ɶ', 'a\u0308', 'ɒ\u0308', 'ɑ', 'ɒ'}

# Vowels by backness

FRONT = {
    'i', 'y',
    'e', 'ø',
    'e\u031e', 'ø\u031e',
    'ɛ', 'œ',
    'æ',
    'ɶ'
}
NEAR_FRONT = {'ɪ', 'ʏ'}
CENTRAL = {
    'ɨ',  'ʉ',
    'ɨ\u031e', 'ʉ\u031e',
    'ɪ\u0308', 'ʊ\u0308',
    'ə', 'ɵ',
    'ɘ', 'ɚ',
    'ɜ', 'ɞ',
    'ɐ',
    'ä', 'ɒ\u0308'
    'a' # Ignoring the IPA guidelines
        # because everybody does.
}
NEAR_BACK = {'ɯ\u031e', 'ʊ'}
BACK = {
    'ɯ', 'u',
    'ɤ', 'o',
    'ɤ\u031e', 'o\u031e',
    'ʌ', 'ɔ',
    'ɑ', 'ɒ'
}


def get_CP():
    """Creates an empty consonant parse dict."""
    return {
        'place': None,
        'manner': None,
        'voice': None,
        'length': None,
        'lateral': None,
        'nasal': None,
        'doubly articulated': None,
        'glyph': None,
        'implosive': None,
        'click': None,
        'pre-features': [],
        'additional articulations': []
    }


def cp_to_set(cp_dict):
    """
    Converts a parse dictionary to a set for filtering.
    """

    if cp_dict['click']:
        return { 'click' }

    result = set()

    if cp_dict['lateral']:
        result.add('lateral')
    elif cp_dict['nasal']:
        result.add('nasal')

    result.add(cp_dict['place'])
    result.add(cp_dict['manner'])
    result.add(cp_dict['voice'])
    result.add(cp_dict['length'])

    if cp_dict['doubly articulated']:
        result.add('doubly_articulated')
    if cp_dict['implosive']:
        result.add('implosive')

    for feature in cp_dict['pre-features']:
        result.add(feature)
    for feature in cp_dict['additional articulations']:
        result.add(feature)

    return result
        


def get_WP():
    '''Creates an empty vowel parse dict.'''
    return {
        'apical vowel': None,
        'glyph': None,
        'diphthong': None,
        'triphthong': None,
        'height': None,
        'backness': None,
        'rounded': None,
        'length': None,
        'additional articulations': [], # Including nasalisation
                                        # and phonation. 
        'pre-features': [] # Needed for tabulation;
                           # also pre-labialised vowels
                           # are sometimes posited. 
    }

PRE_MODIFIERS = {
    #ʰt / ʱd
    '\u02b0': 'pre-aspirated',
    'ʱ':      'pre-aspirated',
    #ˀj / ʼj
    '\u02c0': 'pre-glottalised',
    'ʼ':      'pre-glottalised',
    #ⁿd
    '\u207f': 'pre-nasalised',
    #ʷd
    'ʷ':      'pre-labialised',
}

POST_MODIFIERS = {
    # Universal modifiers
    #aː
    '\u02d0': 'long',
    #aˑ
    '\u02d1': 'half-long',
    #aˤ
    '\u02e4': 'pharyngealised',
    #ã
    '\u0303': 'nasalised',
    #ă
    '\u0306': 'shortened',
    #a̝
    '\u031d': 'raised',
    #a̞      
    '\u031e': 'lowered',
    #a̟
    '\u031f': 'advanced',
    #a̠
    '\u0320': 'retracted', 
    #a̤
    '\u0324': 'breathy voiced',
    #ḁ
    '\u0325': 'voiceless',
    #å
    '\u030a': 'voiceless',
    #a̰
    '\u0330': 'creaky voiced',
    #a↓
    '\u2193': 'ingressive',

    # Vocalic modifiers
    #a˞
    '\u02de': 'rhotacised',
    #a͈
    '\u0348': 'faucalised',
    #ä
    '\u0308': 'centralised',
    #a̘
    '\u0318': 'ATR',
    #a̙
    '\u0319': 'RTR',
    #a̜
    '\u031c': 'less rounded',
    #a̹
    '\u0339': 'more rounded',
    #a̯
    '\u032f': 'non-syllabic',
    # a̽
    '\u033d': 'mid-centralised',

    # Consonantal modifiers
    #aʰ
    '\u02b0': 'aspirated',
    #aʱ
    '\u02b1': 'aspirated',
    #aʲ
    '\u02b2': 'palatalised',
    #aʷ
    '\u02b7': 'labialised',
    #t’ / tʼ 
    '\u2019': 'ejective',
    '\u02bc': 'ejective',
    #dˀ
    '\u02c0': 'glottalised',
    #lˠ / l̴
    '\u02e0': 'velarised',
    '\u0334': 'velarised',
    #dˡ
    '\u02e1': 'lateral released',
    #a̚
    '\u031a': 'unreleased',
    #a̩
    '\u0329': 'syllabic',
    #a̪
    '\u032a': 'dental',
    #a͇
    '\u0347': 'alveolar',
    #a̺
    '\u033a': 'apical',
    #a̻
    '\u033b': 'laminal',
    #a͉
    '\u0349': 'weakly articulated',
    #aᶣ
    '\u1da3': 'labio-palatalised',
    #aⁿ
    '\u207f': 'nasal released',
    #tˢ / dᶻ
    '\u02e2': 'affricated',
    '\u1dbb': 'affricated'
}

# A global variable keeping track of the original
# form of the phoneme of interest, so that it be
# accessible to all functions in the pipeline.
CURRENT_P = ''

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def separate_main_glyphs(phon):
    """Assumes that pre-features and additional articulation
    have been taken care of. Failes otherwise."""
    core_els = []
    for el in phon:
        try:
            if el in MAIN_GLYPHS_CONS:
                core_els.append([el, []])
            else:
                core_els[-1][1].append(el)
        except:
            raise ValueError("Problematic glyph %s in phoneme: %s" % (el, CURRENT_P))
    return core_els

def update_parse(old_parse, new_parse):
    """Attempts to extend extendable attributes and set unset ones.
    Doesn't resolve conflicts and fails instead."""
    for k, v in new_parse.items():
        if k not in old_parse:
            raise KeyError("Wrong feature name: %s" % k)
        else:
            if not (isinstance(v, str) or isinstance(v, bool)):
                raise ValueError('All values in new_parse must be strings or booleans.')
            if old_parse[k] is None:
                old_parse[k] = v
            else:
                try:
                    old_parse[k].append(v)
                except AttributeError:
                    print('The feature "%s" in %s is already set with value "%s" and cannot be extended.' % (k, CURRENT_P, str(old_parse[k])))
                    raise

def parse_single_glyph(g):
    parse = get_CP()

    # Already taken care of
    del parse['glyph']

    # Clicks will not be passed to this function for now
    del parse['click']

    # Cannot infer length without diacritics
    del parse['length']

    # Check for portmanteau glyphs with additional articulations
    if g == 'ɫ':
        update_parse(parse, { 'additional articulations': 'velarised' })

    # 1. Manner: must fill manner, lateral, and nasal:
    if g in PLOSIVES:
        update_parse(parse, { 'manner': 'stop' })
    elif g in IMPLOSIVES:
        update_parse(parse, { 'manner': 'stop' })
        update_parse(parse, { 'implosive': True })
    elif g in NASALS:
        update_parse(parse, { 'manner': 'stop' })
        update_parse(parse, { 'nasal': True })
    elif g in TRILLS:
        update_parse(parse, { 'manner': 'trill' })
    elif g in TAPS:
        update_parse(parse, { 'manner': 'tap' })
    elif g in LATERAL_TAPS:
        update_parse(parse, { 'manner': 'tap' })
        update_parse(parse, { 'lateral': True })
    elif g in FRICATIVES:
        update_parse(parse, { 'manner': 'fricative' })
    elif g in LATERAL_FRICATIVES:
        update_parse(parse, { 'manner': 'fricative' })
        update_parse(parse, { 'lateral': True })
    elif g in APPROXIMANTS:
        update_parse(parse, { 'manner': 'approximant' })
    elif g in LATERAL_APPROXIMANTS:
        update_parse(parse, { 'manner': 'approximant' })
        update_parse(parse, { 'nasal': False })
        update_parse(parse, { 'lateral': True })
    else:
        raise ValueError("Unrecognised glyph: %s" % g)
    
    # Fill the defaults
    if parse['nasal']     is None: parse['nasal']     = False
    if parse['lateral']   is None: parse['lateral']   = False
    if parse['implosive'] is None: parse['implosive'] = False

    # 2. Place
    if g in BILABIAL:
        update_parse(parse, { 'place': 'bilabial' })
    elif g in LABIAL_VELAR:
        update_parse(parse, { 'place': 'labio-velar' })
        update_parse(parse, { 'doubly articulated': True })
    elif g in LABIAL_PALATAL:
        update_parse(parse, { 'place': 'labio-palatal' })
        update_parse(parse, { 'doubly articulated': True })
    elif g in LABIODENTAL:
        update_parse(parse, { 'place': 'labio-dental' })
    elif g in INTERDENTAL:
        update_parse(parse, { 'place': 'interdental' })
    elif g in ALVEOLAR:
        update_parse(parse, { 'place': 'alveolar' })
    elif g in POSTALVEOLAR:
        update_parse(parse, { 'place': 'postalveolar' })
    elif g in RETROFLEX:
        update_parse(parse, { 'place': 'retroflex' })
    elif g in HISSING_HUSHING:
        update_parse(parse, { 'place': 'hissing-hushing' })
    elif g in ALVEOLO_PALATAL:
        update_parse(parse, { 'place': 'alveolo-palatal' })
    elif g in PALATAL:
        update_parse(parse, { 'place': 'palatal' })
    elif g in PALATAL_VELAR:
        update_parse(parse, { 'place': 'palatal-velar' })
        update_parse(parse, { 'doubly articulated': True })
    elif g in VELAR:
        update_parse(parse, { 'place': 'velar' })
    elif g in UVULAR:
        update_parse(parse, { 'place': 'uvular' })
    elif g in PHARYNGEAL:
        update_parse(parse, { 'place': 'pharyngeal' })
    elif g in GLOTTAL:
        update_parse(parse, { 'place': 'glottal' })
    elif g in EPIGLOTTAL:
        update_parse(parse, { 'place': 'epiglottal' })
    else:
        raise ValueError("Unrecognised glyph: %s" % g)

    if parse['doubly articulated'] is None: parse['doubly articulated'] = False

    # 3. Voice
    # May be overriden due to diacritics later
    if g in VOICED:
        update_parse(parse, { 'voice': 'voiced' })
    else:
        update_parse(parse, { 'voice': 'voiceless' })

    return parse

def is_affricate(glyph_list):
    return (glyph_list[0][0] in set.union(PLOSIVES, IMPLOSIVES) and glyph_list[1][0] in set.union(FRICATIVES, LATERAL_FRICATIVES)) or (glyph_list[0][0] + glyph_list[1][0] in {'ɖɽ', 'ʈɽ', 'ʈɹ', 'ʈr'})

def parse_affricate(glyph_list, parse):
    update_parse(parse, { 'manner': 'affricate' })
    update_parse(parse, { 'doubly articulated': False })
    update_parse(parse, { 'nasal': False })
    p1 = parse_single_glyph(glyph_list[0][0])
    p2 = parse_single_glyph(glyph_list[1][0])
    update_parse(parse, { 'implosive': p1['implosive'] })
    # Place of an affricate is governed by the fricative part
    # unless this is a retroflex affricate.
    # /ps/ and /bz/ are treated as special cases.
    if p1['place'] == 'retroflex':
        update_parse(parse, { 'place': p1['place'] })
    elif p1['place'] == 'bilabial' and p2['place'] in { 'alveolar', 'dental' }:
        update_parse(parse, { 'place': 'labio-coronal' })
    else:
        # You can only impose dental place on alveolar
        # or labiodental segments. The update will be succesful
        # only if the place is not set yet, which should be
        # the case if the input is valid.
        if parse['place'] != 'dental':
            update_parse(parse, { 'place': p2['place'] })
        # If the place is already set as dental, check
        # that it is imposed on the segment of a correct type.
        elif p2['place'] not in {'alveolar', 'interdental'}:
            raise ValueError('Incompatible place features: %s' % parse['glyph'])
    # Features of the first item will be ignored,
    # except for breathy voice in voiced affricates.
    # Implosive affricates are considered unlikely
    # until good proof of their existence.
    update_parse(parse, { 'lateral': p2['lateral'] })
    if parse['voice'] == 'voiceless' and p2['voice'] == 'voiced':
        parse['voice'] = 'unvoiced'
    else:
        update_parse(parse, { 'voice': p2['voice'] })
    for g in glyph_list[0][1]:
        if g not in POST_MODIFIERS:
            raise ValueError('Unrecognised modifier or a diacritic: \u25cc%s' % g)
        elif POST_MODIFIERS[g] == 'breathy voiced':
            update_parse(parse, { 'additional articulations': 'breathy voiced' })

def is_bifocal(glyph_list):
    return (glyph_list[0][0] in VELAR and glyph_list[1][0] in BILABIAL) or (glyph_list[0][0] in BILABIAL and glyph_list[1][0] in VELAR)

def parse_bifocal(glyph_list, parse):
    update_parse(parse, { 'doubly articulated': True })
    update_parse(parse, { 'place': 'labio-velar' })
    update_parse(parse, { 'manner': 'stop' })
    update_parse(parse, { 'lateral': False })
    s = glyph_list[0][0] + glyph_list[1][0]
    if s in {'ɡb', 'ɠɓ', 'ŋm'}:
        if parse['voice'] is None:
            update_parse(parse, { 'voice': 'voiced' })
    else:
        update_parse(parse, { 'voice': 'voiceless' })
    if s == 'ɠɓ':
        update_parse(parse, { 'implosive': True })
    elif s == 'ŋm':
        update_parse(parse, { 'nasal': True })
    # Fill the defaults
    if parse['implosive'] is None:
        update_parse(parse, { 'implosive': False })
    if parse['nasal'] is None:
        update_parse(parse, { 'nasal': False })

def parse_double_glyph(phon, feat_dict):
    glyph_list = separate_main_glyphs(phon)
    if is_bifocal(glyph_list):
        parse_bifocal(glyph_list, feat_dict)
    elif glyph_list[0][0] in NASALS:
        update_parse(feat_dict, { 'pre-features': 'pre-nasalised'})
        phon = phon[1:]
        # Ignore all the modifiers for the prenasalisation
        while phon[0] not in MAIN_GLYPHS_CONS:
            phon = phon[1:]
        extract_core_features(phon, feat_dict)
    elif glyph_list[-1][0] in { 'h', 'ɦ' }:
        update_parse(feat_dict, { 'additional articulations': 'aspirated' })
        extract_core_features(phon[:-1], feat_dict)
    elif is_affricate(glyph_list):
        parse_affricate(glyph_list, feat_dict)
    elif glyph_list[0][0] == 'ʔ':
        update_parse(feat_dict, { 'pre-features': 'pre-glottalised' })
        extract_core_features(phon[1:], feat_dict)
    elif glyph_list[-1][0] == 'r':
        update_parse(feat_dict, { 'additional articulations': 'trilled released' })
        extract_core_features(phon[:-1], feat_dict)
    elif glyph_list[-1][0] == 'ʔ':
        update_parse(feat_dict, { 'additional articulations': 'glottalised' })
        extract_core_features(phon[:-1], feat_dict)
    elif glyph_list[-1][0] == 'ɾ':
        update_parse(feat_dict, { 'additional articulations': 'flapped' })
        extract_core_features(phon[:-1], feat_dict)
    elif glyph_list[-1][0] in NASALS:
        update_parse(feat_dict, { 'additional articulations': 'nasal released' })
        extract_core_features(phon[:-1], feat_dict)
    elif glyph_list[-1][0] in LATERAL_APPROXIMANTS:
        update_parse(feat_dict, { 'additional articulations': 'lateral released' })
        extract_core_features(phon[:-1], feat_dict)
    else:
        raise ValueError("Can't parse the string: %s" % phon)

def extract_core_features(phon, feat_dict):
    glyph_list = separate_main_glyphs(phon)
    # TODO: can we treat all 3+ sequences in a unified way?
    if len(glyph_list) >= 4:
        if glyph_list[0][0] + glyph_list[1][0] == 'ŋm':
            update_parse(feat_dict, { 'pre-features': 'pre-nasalised' })
            extract_core_features(phon[2:], feat_dict)
        elif glyph_list[0][0] in NASALS:
            update_parse(feat_dict, { 'pre-features': 'pre-nasalised' })
            phon = phon[1:]
            # Ignore all the modifiers for the prenasalisation
            while phon[0] not in MAIN_GLYPHS_CONS:
                phon = phon[1:]
            extract_core_features(phon, feat_dict)
        else:
            raise ValueError('Unrecognised long sequence: %s' % phon)
    elif len(glyph_list) == 3:
        if glyph_list[0][0] in NASALS:
            update_parse(feat_dict, { 'pre-features': 'pre-nasalised' })
            phon = phon[1:]
            # Ignore all the modifiers for the prenasalisation
            while phon[0] not in MAIN_GLYPHS_CONS:
                phon = phon[1:]
            extract_core_features(phon, feat_dict)
        elif glyph_list[2][0] in TRILLS:
            update_parse(feat_dict, { 'additional articulations': 'trilled released' })
            extract_core_features(phon[:-1], feat_dict)
        elif glyph_list[2][0] in TAPS:
            update_parse(feat_dict, { 'additional articulations': 'flapped' })
            extract_core_features(phon[:-1], feat_dict)
        elif glyph_list[2][0] in {'h', 'ɦ'}:
            update_parse(feat_dict, { 'additional articulations': 'aspirated' })
            extract_core_features(phon[:-1], feat_dict)
        else:
            raise ValueError('Unrecognised 3-glyph sequence: %s' % phon)
    elif len(glyph_list) == 2:
        parse_double_glyph(phon, feat_dict)
    elif len(glyph_list) == 1:
        base_parse = parse_single_glyph(glyph_list[0][0])
        # The modifiers should've been chopped off by now.
        # If this hasn't happened, something went wrong.
        for el in glyph_list[0][1]:
            if el not in POST_MODIFIERS:
                raise ValueError('Unrecognised modifier or diacritic: \u25cc%s in the phoneme %s' % (el, phon))
        # Resolve possible conflicts
        if feat_dict['voice'] == 'voiceless' and base_parse['voice'] == 'voiced':
            if not (base_parse['lateral'] or base_parse['nasal'] or base_parse['implosive']):
                feat_dict['voice'] = 'unvoiced'
            del base_parse['voice']
        elif feat_dict['voice'] == 'voiceless' and base_parse['voice'] == 'voiceless':
            # eprint('Redundant voicelessness: %s' % CURRENT_P)
            del base_parse['voice']
        # Can impose dental place on alveolar or interdental segments.
        # Otherwise will fail in the update phase.
        # TODO: bring the error message in line with the better one
        # in parse_affricate.
        if feat_dict['place'] == 'dental' and base_parse['place'] in {'alveolar', 'interdental'}:
            del base_parse['place']
        for k,v in base_parse.items():
            if k == 'pre-features' or k == 'additional articulations':
                for el in v:
                    update_parse(feat_dict, { k: el })
            else:
                update_parse(feat_dict, { k: v })
    else:
        raise ValueError("No main glyphs found: %s" % phon)


def parse_consonant(phon):
    global CURRENT_P
    CURRENT_P = phon
    # Separate clicks
    # TODO: actually parse them
    for el in ['ǀ', 'ǁ', 'ǂ', 'ǃ', 'ʘ']:
        if el in phon: return { 'click': True,
                                'glyph': phon }

    # Remove ignored diacritics. Disregard borrowed/marginal status
    # TODO: check for eventual duplicates at some point
    phon = phon.strip(' ()<>').replace('\u0353', '').replace('\u032c', '')
    parse = get_CP()
    update_parse(parse, { 'click': False })
    update_parse(parse, { 'glyph': phon })

    # Extract pre-features
    while True:
        if phon[0] not in PRE_MODIFIERS: break
        update_parse(parse, { 'pre-features': PRE_MODIFIERS[phon[0]] })
        phon = phon[1:]

    # TODO: rewrite to accommodate overlong segments

    # Extract post-features
    while True:
        if phon[-1] not in POST_MODIFIERS: break
        if POST_MODIFIERS[phon[-1]] == 'voiceless':
            update_parse(parse, { 'voice': POST_MODIFIERS[phon[-1]] })
        elif POST_MODIFIERS[phon[-1]] == 'long':
            if parse['length'] is None:
                parse['length'] = 'long'
            elif parse['length'] == 'long':
                parse['length'] = 'overlong'
            else:
                raise ValueError('Incompatible length diacritics: %s' % phon)
        elif POST_MODIFIERS[phon[-1]] == 'half-long':
            if parse['length'] is None:
                parse['length'] = 'long'
            else:
                raise ValueError('Incompatible length diacritics: %s' % phon)
        elif POST_MODIFIERS[phon[-1]] == 'shortened':
            if parse['length'] is None:
                parse['length'] = 'shortened'
            else:
                raise ValueError('Incompatible length diacritics: %s' % phon)
        elif POST_MODIFIERS[phon[-1]] == 'dental':
            update_parse(parse, { 'place': 'dental' })
        elif POST_MODIFIERS[phon[-1]] == 'centralised':
            update_parse(parse, { 'additional articulations': 'breathy voiced' })
        elif POST_MODIFIERS[phon[-1]] == 'alveolar':
            pass
        else:
            update_parse(parse, { 'additional articulations': POST_MODIFIERS[phon[-1]] })
        phon = phon[:-1]

    # Do the rest
    extract_core_features(phon, parse)

    # Fill in the remaining defaults
    if parse['length'] is None:
        parse['length'] = 'short'

    # Sanity check
    for k,v in parse.items():
        if v is None:
            raise Exception('The value of the feature %s is not set for the phoneme %s' % (k, phon))

    return parse

def parse_vowel(phon):
    global CURRENT_P
    CURRENT_P = phon

    # Remove ignored diacritics. Disregard borrowed/marginal status
    # TODO: check for eventual duplicates at some point
    phon = phon.strip(' ()<>').replace('\u0353', '').replace('\u032c', '')

    parse = get_WP()
    update_parse(parse, { 'glyph': phon })


    # Extract pre-features
    while True:
        if phon[0] not in PRE_MODIFIERS: break
        update_parse(parse, { 'pre-features': PRE_MODIFIERS[phon[0]] })
        phon = phon[1:]
    
    # Check for length; should be denoted
    # by the last glyph or last two glyphs
    # in the sequence.
    if phon.endswith('\u02d0\u02d0'):
        parse['length'] = 'overlong'
        phon = phon[:-2]
    elif phon[-1] == '\u02d0':
        parse['length'] = 'long'
        phon = phon[:-1]
    elif phon[-1] == 'u02d1':
        parse['length'] = 'half-long'
        phon = phon[-1]
    else:
        parse['length'] = 'short'

    # Extract additional articulations
    while True:
        if phon[-1] not in POST_MODIFIERS: break
        update_parse(parse, { 'additional articulations': POST_MODIFIERS[phon[-1]] })
        phon = phon[:-1]

    # Check for di- and triphthongs
    main_glyph_count = 0
    # Check for symbols for approximants
    # used to denote diphthongs and triphthongs
    for c in phon:
        if c in {'w', 'j', 'ɰ'}:
            main_glyph_count += 1
    for c in phon:
        if c in MAIN_GLYPHS_VOWS:
            main_glyph_count += 1
    if main_glyph_count == 0:
        raise ValueError(f'No main glyphs in {CURRENT_P}')
    elif main_glyph_count == 2:
        parse['diphthong'] = True
        return parse
    elif main_glyph_count == 3:
        parse['triphthong'] = True
        return parse

    parse['diphthong'] = False
    parse['triphthong'] = False

    try:
        update_parse(
            parse,
            MAIN_GLYPHS_VOWS[phon]
        )
    except KeyError:
        raise ValueError(f'Unrecognised main sequence in {CURRENT_P}')
    
    # Apical vowels are left unspecified
    if parse['apical vowel']:
        return parse
    else:
        parse['apical vowel'] = False

    for k, v in parse.items():
        if v == None:
            raise ValueError(f'The feature {k} is not set for phoneme {CURRENT_P}')

    return parse

def consonant_parse_to_string(parse):
    if parse['click']:
        return 'click'
    parse_arr = []
    fixed_order_or_skip = {'length', 'voice', 'nasal', 'lateral', 'place', 'manner', 'glyph'}
    parse_arr.append(parse['length'])
    parse_arr.append(parse['voice'])
    if parse['nasal']:
        parse_arr.append('nasal')
    elif parse['lateral']:
        parse_arr.append('lateral')
    parse_arr.append(parse['place'])
    parse_arr.append(parse['manner'])
    tail = []
    for k, v in parse.items():
        if k in fixed_order_or_skip:
            continue
        if isinstance(v, bool):
            if v:
                tail.append(k)
        elif isinstance(v, list):
            for el in v:
                tail.append(el)
        else:
            tail.append(v)
    return(' '.join(parse_arr + sorted(tail)))

pc = parse_consonant
pw = parse_vowel

if __name__ == '__main__':
    if len(argv) < 3:
        print("Please specify the segment to parse as a first argument and whether this is a consonant (c) or a vowel (v) as the second argument.")
    else:
        if argv[2] == 'c':
            pprint(parse_consonant(argv[1]))
        else:
            pprint(parse_vowel(argv[1]))
