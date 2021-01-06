import sqlite3
import json

import IPAParser_3_0

PARSER = IPAParser_3_0.IPAParser()

with open('parses_cache.json', 'r', encoding='utf-8') as inp:
    PARSES_CACHE = json.load(inp)
with open('parses_cache_phoible.json', 'r', encoding='utf-8') as inp:
    PARSES_CACHE_PHOIBLE = json.load(inp)
with open('inventories_phoible.json', 'r', encoding='utf-8') as inp:
    INVENTORIES_PHOIBLE = json.load(inp)


def get_all_language_ids(db_connection: sqlite3.Connection, query_phoible=False):
    if query_phoible:
        return set(INVENTORIES_PHOIBLE)
    else:
        cursor = db_connection.cursor()
        return set(el[0] for el in cursor.execute("SELECT id FROM languages").fetchall())


def get_parse(segment):
    if segment in PARSES_CACHE:
        return set(el for el in PARSES_CACHE[segment])
    else:
        return PARSER.parse(segment).as_set()


#
# Slow legacy code; replaced with Go binaries
#

# def get_consonants_for_language(language_id: int, db_connection: sqlite3.Connection):
#     cursor = db_connection.cursor()
#     return set(el[0].replace('(', '').replace(')', '') for el in cursor.execute(
#         """
#         SELECT ipa FROM segments
#         WHERE `is_consonant` = 1
#         AND `language_id` = ?
#         """,
#         (language_id,)
#     ).fetchall())


# def get_vowels_for_language(language_id: int, db_connection: sqlite3.Connection):
#     cursor = db_connection.cursor()
#     return set(el[0].replace('(', '').replace(')', '') for el in cursor.execute(
#         """
#         SELECT ipa FROM segments
#         WHERE `is_consonant` = 0
#         AND `language_id` = ?
#         """,
#         (language_id,)
#     ).fetchall())


# def get_count_for_features(language_id, features, db_connection, hit_tmp):

#     pos_features = set(el[1] for el in features if el[0] == '+')
#     neg_features = set(el[1] for el in features if el[0] == '-')
#     if 'approximant' in pos_features and 'lateral' not in pos_features:
#         neg_features.add('lateral')
#     if 'plosive' in pos_features and 'nasal' not in pos_features:
#         neg_features.add('nasal')
#     consonants = get_consonants_for_language(language_id, db_connection)
#     vowels = get_vowels_for_language(language_id, db_connection)
#     hit_count = 0
#     for segment in consonants | vowels:
#         if segment not in hit_tmp:
#             parse = get_parse(segment)
#             hit_tmp[segment] = pos_features.issubset(parse) and\
#                 not neg_features & parse
#         if hit_tmp[segment]:
#             hit_count += 1
#     return hit_count


# def check_eq(diff, op):
#     if op == '=':
#         return diff == 0
#     elif op == '<':
#         return diff < 0
#     elif op == '<=':
#         return diff <= 0
#     elif op == '>':
#         return diff > 0
#     elif op == '>=':
#         return diff >= 0
#     else:
#         raise NotImplementedError(f'Comparison operator not recognised: {op}')
