import sqlite3
from typing import Set

from parser import query_parser, QueryTransformer, ASTNode, OrNode, AndNode, NotNode
from parser import EqFeature, EqPhoneme, EqFeatures
from helpers import get_count_for_features, get_all_language_ids, check_eq


def apply_query(query: ASTNode, db_connection: sqlite3.Connection) -> Set[int]:
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
    # elif type(query) == EqPhoneme:
    #     # return apply_eq_phoneme(query, db_connection)
    #     pass
    # elif type(query) == EqFeatures:
    #     # return apply_eq_features(query, db_connection)
    #     pass
    else:
        raise NotImplementedError(
            f'The query type is not recognised: {type(query)}')


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


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2 or sys.argv[1] in {'-h', 'help', '--help', '-help'}:
        print(
            '''
Usage
=====
            
python query_processor.py query

returns the list of languages satisfying the query.

python query_processor.py list-features

lists all consonant and vowel features that can be used in a query.

Query types
===========

1. Presence/absence for segments and feature bundles: 
   "+ /p/", "- labio-dental fricative", &c.

2. Count queries for segments and feature bundles: 
   "> 4 bilabial consonant", "= 3 plosive", &c.
   Supported comparison operators: =, <, >, <=, >=.

3. Comparison queries for feature bundles: 
   "> bilabial consonant, dental consonant", &c. 
   The same comparison operators are supported as above.
   Note that elements of feature lists are separated by spaces,
   and the two lists are separated by a comma.

Complex queries
===============

Queries can be negated using "not" and combined using
"and" and "or".

Operator precedence order: not > and > or.

Use parentheses for nested queries and clarity. 

An example complex query:

not (
    >= bilabial plosive, labio-dental fricative 
    or 
    <= bilabial plosive, labio-dental fricative
) or
+ /p/ and > 4 approximant
'''
        )
    conn = sqlite3.connect('europhon.sqlite')
    raw_query = query_parser.parse(sys.argv[1])
    query_transformer = QueryTransformer()
    print(raw_query.pretty())
    print()
    query = query_transformer.transform(raw_query)
    print(query)
    print()
    print(apply_query(query, conn))
