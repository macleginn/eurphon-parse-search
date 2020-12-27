# TODO: run this as a procedure when the query engines starts.

import os
import json
import sqlite3

from IPAParser_3_0 import IPAParser

parses_cache = {}

conn = sqlite3.connect('europhon.sqlite')
cursor = conn.cursor()
parser = IPAParser()
for (segment,) in cursor.execute('SELECT DISTINCT ipa FROM segments'):
    segment = segment.replace('(', '').replace(')', '')
    if segment not in parses_cache:
        parses_cache[segment] = parser.parse(segment).as_list()
with open('parses_cache.json', 'w', encoding='utf-8') as out:
    json.dump(parses_cache, out, indent=2, ensure_ascii=False)
