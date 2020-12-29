import sqlite3
import json

import IPAParser_3_0


PARSER = IPAParser_3_0.IPAParser()
with open('parses_cache.json', 'r', encoding='utf-8') as inp:
    PARSES_CACHE = json.load(inp)


def get_all_language_ids(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()
    return set(el[0] for el in cursor.execute("SELECT id FROM languages").fetchall())


def get_consonants_for_language(language_id: int, db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()
    return set(el[0].replace('(', '').replace(')', '') for el in cursor.execute(
        """
        SELECT ipa FROM segments
        WHERE `is_consonant` = 1
        AND `language_id` = ?
        """,
        (language_id,)
    ).fetchall())


def get_vowels_for_language(language_id: int, db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()
    return set(el[0].replace('(', '').replace(')', '') for el in cursor.execute(
        """
        SELECT ipa FROM segments
        WHERE `is_consonant` = 0
        AND `language_id` = ?
        """,
        (language_id,)
    ).fetchall())


def supply_defaults(parse_set):
    """
    Excludes nasals, laterals, and implosives from the search
    if they are not mentioned explicitely.
    """
    if 'lateral' not in parse_set:
        parse_set.add('non-lateral')
    if 'nasal' not in parse_set:
        parse_set.add('oral')
    if 'implosive' not in parse_set:
        parse_set.add('non-implosive')


def get_parse(segment):
    if segment in PARSES_CACHE:
        # Do not touch the cache itself.
        tmp = set(el for el in PARSES_CACHE[segment])
    else:
        tmp = PARSER.parse(segment).as_set()
    supply_defaults(tmp)
    return tmp


def get_count_for_features(language_id, features, db_connection, hit_tmp):
    features = set(el for el in features)
    supply_defaults(features)
    consonants = get_consonants_for_language(language_id, db_connection)
    vowels = get_vowels_for_language(language_id, db_connection)
    hit_count = 0
    for segment in consonants | vowels:
        if segment not in hit_tmp:
            hit_tmp[segment] = features.issubset(get_parse(segment))
        if hit_tmp[segment]:
            hit_count += 1
    return hit_count


def check_eq(diff, op):
    if op == '=':
        return diff == 0
    elif op == '<':
        return diff < 0
    elif op == '<=':
        return diff <= 0
    elif op == '>':
        return diff > 0
    elif op == '>=':
        return diff >= 0
    else:
        raise NotImplementedError(f'Comparison operator not recognised: {op}')
