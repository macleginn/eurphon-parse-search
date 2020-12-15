import sqlite3
from typing import List

from parser import parser, ASTNode, OrNode, AndNode, NotNode
from parser import EqFeature, EqPhoneme, EqFeatures
from helpers import get_count_for_features, get_all_language_ids, check_eq


def apply_query(query: ASTNode, db_connection: sqlite3.Connection) -> List[int]:
    """
    Recursively applies the query transformed into an ASTNode to the inventories
    stored in the database and returns a set of inventory ids.
    """
    if type(query) == OrNode:
        return set.union(
            apply_query(query.lhs, db_connection),
            apply_query(query.rhs, db_connection)
        )
    elif type(query) == AndNode:
        return set.intersection(
            apply_query(query.lhs, db_connection),
            apply_query(query.rhs, db_connection)
        )
    elif type(query) == NotNode:
        return get_all_language_ids(db_connection) - apply_query(query.query, db_connection)
    elif type(query) == EqFeature:
        return apply_eq_feature(query, db_connection)
    elif type(query) == EqPhoneme:
        # return apply_eq_phoneme(query, db_connection)
        pass
    elif type(query) == EqFeatures:
        # return apply_eq_features(query, db_connection)
        pass
    else:
        raise NotImplementedError(f'The query type is not recognised: {type(query)}')


def apply_eq_feature(query: EqFeature, db_connection: sqlite3.Connection):
    result = set()
    for language_id in get_all_language_ids(db_connection):
        diff = get_count_for_features(
            language_id, 
            query.features,
            db_connection) - query.number
        if check_eq(diff, query.op):
            result.add(language_id)
    return result



# def parse_and_apply(query, parser, db_connection):
#     tree = parser.parse(query)


conn = sqlite3.connect('eurphon.sqlite')

