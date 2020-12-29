# Search tutorial

## Introduction

Unlike Henning Reetz’s [Simple UPSID interface](http://web.phonetik.uni-frankfurt.de/upsid.html), this interface is exclusively text based. This introduces some complexity, but it also makes it possible to go beyond rigid search options any fixed interface can offer.

The query language implemented in the interface contains two basic query types—count queries and comparison queries–and allows the user to combine them in a flexible way through logical operators. (If you are comfortable with reading CFGs, all you need to know can be find in the very short [grammar](https://github.com/macleginn/eurphon-parse-search/blob/master/search_grammar.lark), from which the query parser is constructed on the fly using [Lark](https://lark-parser.readthedocs.io/en/latest/).)

We will describe the basic queries first and then show how to combine them into more complex ones.

## Basic queries

### Count queries

The general form of a count query is `operator number features` or `operator number /phoneme/`, where

* `operator` is one of `=, <, >, <=, >=`,
* `number` is a non-negative integer,
* `features` are one or more space-separated IPA features (see the full list at the end of the page), each optionally preceded by `^`, and
* `phoneme` is an individual segment described in standard IPA notation (https://ipa.typeit.org/full/ is used as a reference input system).

For example, a query asking for languages without lateral segments looks like `= 0 lateral` and a query to ask for languages with more than five voiceless affricates is `> 5 voiceless affricate`. Each feature can be turned into its complement by using `^`. Thus, the query `> 5 ^pre-nasalised voiced plosive` will return languages that have more than 5 oral plosives that are not pre-nasalised.

The order of features does not matter. Some features (e.g., `nasalised`) are shared between vowels and consonants, and the words `vowel` and `consonant` can be used for disambiguation.

Diphthongs, triphthongs, and click consonants have features `diphthong`/`triphthong` and `click` respectively assigned to them. Monophthong vowels have a feature `monophthong`, and non-click consonants have a feature `non-click`. Use these features to explicitly query for monophthong vowels and non-click consonants (the same goal can be achieved using `^diphthong ^triphthong vowel` and `^click consonant` respectively).

Note that negative values are supplied by default for `lateral` and `nasal` features. I.e., a query `= 0 voiced bilabial plosive` will ignore the presence of /m/ (voiced _nasal_ bilabial plosive) in an inventory, but will not return languages with /b/. Likewise, a query `= 0 approximant` will skip languages with /w/ and /j/, but will ignore the presence of /l/ (voiced _lateral_ alveolar approxumant).

To make it easier to look for presence and absence of feature bundles and phonemes, two shortcuts are provided: `+`, equivalent to `> 0`, and `-`, equivalent to `= 0`. E.g., a query for languages without /p/ looks like `- /p/`.

Note that phoneme-based queries look for a symbol-by-symbol match. Thus, a language with /b, pʰ, pʼ/ will still satisfy the `- /p/` query and `+ /ɫ/` will not retrieve languages where this segments is denoted by /lˠ/.

### Comparison queries

Comparison queries make it possible to search for languages that have more or fewer segments of some kind compared to some other kind of segments. The basic form of the query is `operator features, features`, where `operator` and `features` have the same form as above.

For example, languages with more vowels than consonants can be retrieved using `> vowel, consonant` and languages with the same number of monophthong vowels and diphthongs can be queried by `= monophthong, diphthong` (use `= monophthong vowel, ^monophthong vowel` if you want to count all polyphthongs).

## Combining queries

Sometimes basic queries are not enough. For example, in order to make basic queries simpler, the query language does not allow for querying nasal and oral consonants simultaneously. Therefore, in order to look for languages without both oral and nasal bilabial plosives it is necessary to combine two queries: `- nasal bilabial plosive and - bilabial plosive` (or, more explicitly `- nasal bilabial plosive and - ^nasal bilabial plosive`). This is also helpful to work around variations in IPA notation, e.g. `+ /g/ or + /ɡ/` (both the special /ɡ/ symbol and the basic Latin /g/ are officially recognised as part of IPA).

Three logical operators are supported (in the order of decreasing tightness):

* `not` (return the complement of the query)
* `and` (return the intersection of two queries)
* `or` (return the union of two queries)

Parentheses can be used for clarity or to override the operator precedence order. Thus, `- /p/ and - /b/ or - /t/ and - /d/` is equivalent to `(- /p/ and - /b/) or (- /t/ and - /d/)` (`and` binds more tightly than `or`), but `- /p/ or - /b/ and - /t/ or - /d/` is not equivalent to `(- /p/ or - /b/) and (- /t/ or - /d/)`, but is instead equivalent to `- /p/ or (- /b/ and - /t/) or - /d/`.

`not` binds the most tightly, so it is necessary to use parentheses to invert any complex query.

An example compound query:

```
not (
    (- /p/ or - /t/ or - /k/)
    and
    (- /b/ or - /d/ or - /g/)
) or
    > 10 voiced affricate
```
<br/>
<br/>
Any redundant whitespace is ignored.

## Features

Canonical feature names are listed in the British orthography, but `ize`-spellings are supported as well. Note that not all possible features are listed for consonants and vowels but only those found in the database (see the [complete list](https://github.com/macleginn/eurphon-parse-search/blob/master/ipa_parse_grammar.lark) in the parser grammar). E.g., all types of additional articulations are theoretically possible with both consonants and vowels.

### Vowel features

advanced, alveolar, apical, atr, back, breathy-voice, central, centralised, close, close-mid, creaky-voice, diphthong, front, half-long, less-rounded, long, lowered, mid, mid-centralised, modal-voice, monophthong, more-rounded, nasalised, near-close, near-open, non-syllabic, open, open-mid, overlong, pharyngealised, postalveolar, raised, retracted, rhotacised, rounded, rtr, short, shortened, triphthong, unrounded, velarised, voiceless

### Consonant features

advanced, affricate, affricated, alveolar, alveolo-palatal, apical, approximant, aspirated, bilabial, breathy-voice, dental, devoiced, ejective, epiglottal, fricative, glottal, glottalised, hissing-hushing, implosive, interdental, labial-palatal, labial-velar, labialised, labiodental, laminal, lateral, less-rounded, long, lowered, nasal, nasalised, overlong, palatal, palatal-velar, palatalised, pharyngeal, pharyngealised, plosive, postalveolar, pre-aspirated, pre-glottalised, pre-labialised, pre-nasalised, raised, retracted, retroflex, rhotacised, rtr, short, syllabic, tap, trill, uvular, velar, velarised, voiced, voiceless
