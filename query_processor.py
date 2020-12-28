import sqlite3
import json
import io

from collections import defaultdict
from typing import Set
from unicodedata import normalize
from dataclasses import dataclass

from QueryParser import query_parser, QueryTransformer, ASTNode, OrNode, AndNode, NotNode
from QueryParser import EqFeature, EqPhoneme, EqFeatures
from helpers import get_count_for_features, get_all_language_ids, check_eq

#
# Globals
#

USAGE_short = """Usage:

python query_processor.py query [phylum=family-list|genus=group-list]

or

python query_processor.py help
"""

USAGE = '''
Usage
=====

python query_processor.py query [phylum=family-list|genus=group-list]

returns the list of languages satisfying the query.

python query_processor.py list-features

lists all consonant and vowel features that can be used in a query.

python query_processor.py list-phyla

lists all languages families found in the database.

python query_processor.py genus-tree

prints a tree of all language groups found in the database organised
by language family.

Query types
===========

1. Presence/absence for segments and feature bundles:
   "+ /p/" (languages that have /p/), "- labio-dental fricative"
   (languages without labio-dental fricatives), &c.

2. Count queries for segments and feature bundles:
   "> 4 bilabial consonant" (languages with more than 4 bilabial consonants),
   "= 3 plosive" (languages with exactly 3 plosives), &c.
   Supported comparison operators: =, <, >, <=, >=.

3. Comparison queries for feature bundles:
   "> bilabial consonant, dental consonant" (languages with more bilabial
   consonants than dental consonants), &c. The same comparison operators
   are supported as above. Note that elements of feature lists are separated
   by spaces, while the two lists are separated by a comma.

Complex queries
===============

Queries can be negated using "not" and combined using "and" and "or".

Operator-precedence order: not > and > or.

Use parentheses for nested queries and clarity.

An example complex query:

not (
    >= bilabial plosive, labio-dental fricative
    or
    <= bilabial plosive, labio-dental fricative
) or
+ /p/ and > 4 approximant

Restricting the search by phyla or genera
=========================================

It is possible to apply queries only to languages from particular
language families or groups. Examples:

python query_processor.py "- /p/" "phylum=Indo-European,Austronesian"
python query_processor.py "< nasal consonant, lateral consonant" "genus=Avar-Andi"

'''


@dataclass
class Language:
    iso: str
    name: str
    phylum: str
    genus: str


db_connection = sqlite3.connect('europhon.sqlite')
meta = {
    language_id: Language(iso, language_name, phylum, genus)
    for language_id, iso, language_name, phylum, genus
    in db_connection.execute(
        """
            SELECT 
                languages.id, languages.`iso_code`, languages.name, 
                phyla.name, genera.name
            FROM languages 
                LEFT JOIN phyla ON
                    languages.phylum_id = phyla.id
                LEFT JOIN genera ON
                    languages.genus_id = genera.id
            """)
}
query_transformer = QueryTransformer()


def apply_query(query: ASTNode, db_connection: sqlite3.Connection) -> Set[int]:
    """
    Recursively applies the query transformed into an ASTNode to the inventories
    stored in the database and returns a set of inventory ids.
    """
    if type(query) == OrNode:
        return apply_query(query.lhs, db_connection) | apply_query(query.rhs, db_connection)
    elif type(query) == AndNode:
        return apply_query(query.lhs, db_connection) & apply_query(query.rhs, db_connection)
    elif type(query) == NotNode:
        return get_all_language_ids(db_connection) - apply_query(query.query, db_connection)
    elif type(query) == EqPhoneme:
        return apply_eq_phoneme(query, db_connection)
    elif type(query) == EqFeature:
        return apply_eq_feature(query, db_connection)
    elif type(query) == EqFeatures:
        return apply_eq_features(query, db_connection)
    else:
        raise NotImplementedError(
            f'The query type is not recognised: {type(query)}')


def apply_eq_phoneme(query: EqPhoneme, db_connection: sqlite3.Connection):
    result = set()
    test_segment = normalize('NFD', query.phoneme)
    for language_id in get_all_language_ids(db_connection):
        segment_count = 0
        for (segment,) in db_connection.execute(
            'SELECT ipa FROM segments WHERE `language_id` = ?',
            (language_id,)
        ):
            if segment == test_segment:
                segment_count += 1
                # We expect to see each segment only once
                # in an inventory.
                break
        diff = segment_count - query.number
        if check_eq(diff, query.op):
            result.add(language_id)
    return result


def apply_eq_feature(query: EqFeature, db_connection: sqlite3.Connection):
    result = set()
    # A search optimisation: only check the subset once for each segment.
    hit_tmp = {}
    for language_id in get_all_language_ids(db_connection):
        diff = get_count_for_features(
            language_id,
            query.features,
            db_connection,
            hit_tmp) - query.number
        if check_eq(diff, query.op):
            result.add(language_id)
    return result


def apply_eq_features(query: EqFeatures, db_connection: sqlite3.Connection):
    result = set()
    # Two caches for two sets of features.
    hit_tmp1 = {}
    hit_tmp2 = {}
    for language_id in get_all_language_ids(db_connection):
        lhs_count = get_count_for_features(
            language_id, query.features_1, db_connection, hit_tmp1)
        rhs_count = get_count_for_features(
            language_id, query.features_2, db_connection, hit_tmp2)
        diff = lhs_count - rhs_count
        if check_eq(diff, query.op):
            result.add(language_id)
    return result


# def parse_and_apply(query, parser, db_connection):
#     tree = parser.parse(query)

#
# UI functions
#

def print_features():
    with open(f'parses_cache.json', 'r', encoding='utf-8') as inp:
        parses = json.load(inp)
    consonant_features = set()
    vowel_features = set()
    for feature_list in parses.values():
        if 'consonant' in feature_list:
            consonant_features.update(feature_list)
        else:
            vowel_features.update(feature_list)
    consonant_features.discard('consonant')
    vowel_features.discard('vowel')

    with io.StringIO() as out:
        print('"vowel" and "consonant" can be used as features.', file=out)
        print('', file=out)
        print('Vowel features', file=out)
        print('==============', file=out)
        print(', '.join(sorted(vowel_features)), file=out)
        print('', file=out)
        print('Consonant features', file=out)
        print('==================', file=out)
        print(', '.join(sorted(consonant_features)), file=out)
        return out.getvalue()


def print_phyla():
    phyla = sorted(row[0] for row
                   in db_connection.execute("SELECT name FROM phyla"))
    return '\n'.join(phyla)


def print_genus_tree():
    tree = defaultdict(list)
    for phylum_id, phylum in db_connection.execute(
        "SELECT id, name FROM phyla"
    ):
        tree[phylum] = sorted(row[0] for row in db_connection.execute(
            "SELECT name FROM genera WHERE `phylum_id` = ?",
            (phylum_id,)))
    with io.StringIO() as out:
        for phylum in sorted(tree):
            print(phylum, file=out)
            for genus in tree[phylum]:
                print('\t' + genus, file=out)
        return out.getvalue()


def parse_query(query_string):
    "We separate this bit into a separate function to catch Lark exceptions."
    return query_parser.parse(query_string)


def apply_query_and_filter(query_tree, restrictor_dict={}):
    # Transforming the query after successfully
    # parsing it should be safe.
    query = query_transformer.transform(query_tree)
    result = apply_query(query, db_connection)
    if 'phylum' in restrictor_dict:
        phyla = restrictor_dict['phylum']
        result = list(
            filter(lambda lang_id: meta[lang_id].phylum in phyla, result))
    elif 'genus' in restrictor_dict:
        genera = restrictor_dict['genus']
        result = list(
            filter(lambda lang_id: meta[lang_id].genus in genera, result))
    result = {
        lang_id: f'{meta[lang_id].name} ({meta[lang_id].iso})'
        for lang_id in result
    }
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(USAGE_short)
        sys.exit()
    elif sys.argv[1] in {'-h', 'help', '--help', '-help'}:
        print(USAGE)
        sys.exit()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'list-features':
            print(print_features(), end='')
            sys.exit()
        elif sys.argv[1] == 'list-phyla':
            print(print_phyla())
            sys.exit()
        elif sys.argv[1] == 'genus-tree':
            print(print_genus_tree(), end='')
            sys.exit()

    try:
        raw_query = query_parser.parse(sys.argv[1])
    except Exception as e:
        print(
            f'Bad query: {sys.argv[1]}\n\nQuery-parser output: {e}', file=sys.stderr)
        sys.exit(1)
    query_transformer = QueryTransformer()
    print(raw_query.pretty())
    query = query_transformer.transform(raw_query)
    print(query, '\n')

    result = apply_query(query, db_connection)

    # Filter by phylum or genus when applicable
    if len(sys.argv) > 2:
        phyla = None
        genera = None
        restrictor = sys.argv[2]
        if not (
            restrictor.startswith('phylum=')
            or restrictor.startswith('genus=')
        ):
            print(USAGE_short)
            sys.exit(1)
        if restrictor.startswith('phylum'):
            phyla = restrictor.split('=')[1].split(',')
            result = list(
                filter(lambda lang_id: meta[lang_id].phylum in phyla, result))
        else:
            genera = restrictor.split('=')[1].split(',')
            result = list(
                filter(lambda lang_id: meta[lang_id].genus in genera, result))

    # Format the output
    result = list(
        map(lambda lang_id: f'{meta[lang_id].name} ({meta[lang_id].iso})', result))
    print(result)
