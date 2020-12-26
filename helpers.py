import sqlite3
# TODO: implement parse_vowel using Lark
from IPAParser_2_0 import parse_vowel, parse_consonant


def get_all_language_ids(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()
    return set(cursor.execute("SELECT id FROM languages").fetchall())


def get_consonants_for_language(language_id: int, db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()
    return set(cursor.execute(
        """
        SELECT ipa FROM segments
        WHERE `is_consonant` = 1
        AND `language_id` = ?
        """,
        (language_id,)
    ).fetchall())


def get_vowels_for_language(language_id: int, db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()
    return set(cursor.execute(
        """
        SELECT ipa FROM segments
        WHERE `is_consonant` = 0
        AND `language_id` = ?
        """,
        (language_id,)
    ).fetchall())


def satisfies_consonants(feature_dict, features):
    return True


def satisfies_vowels(feature_dict, features):
    return False


def get_count_for_features(language_id, features, db_connection):
    consonants = get_consonants_for_language(language_id, db_connection)
    vowels = get_vowels_for_language(language_id, db_connection)
    hit_count = 0
    for c in consonants:
        feature_dict = parse_consonant(c)
        if satisfies_consonants(feature_dict, features):
            hit_count += 1
    for v in vowels:
        feature_dict = parse_vowel(v)
        if satisfies_vowels(feature_dict, features):
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