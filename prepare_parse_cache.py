# TODO: run this as a procedure when the query engines starts.

import os
import json
import sqlite3
import pandas as pd
from IPAParser_3_0 import IPAParser

parser = IPAParser()


def prepare_eurphon():
    parses_cache = {}
    conn = sqlite3.connect(os.path.join('data', 'europhon.sqlite'))
    cursor = conn.cursor()
    for (segment,) in cursor.execute('SELECT DISTINCT ipa FROM segments'):
        segment = segment.replace('(', '').replace(')', '')
        if segment not in parses_cache:
            parses_cache[segment] = parser.parse(segment).as_list()
    with open('parses_cache.json', 'w', encoding='utf-8') as out:
        json.dump(parses_cache, out, indent=2, ensure_ascii=False)


def prepare_phoible():
    parses_cache = {}
    d = pd.read_csv(os.path.join('data', 'phoible.csv'), low_memory=False)
    d = d.loc[d.SegmentClass != 'tone']
    segments_table = d[['Phoneme', 'click']].drop_duplicates()
    for row in segments_table.itertuples():
        if '+' in row.click:
            parses_cache[row.Phoneme] = ['click', 'consonant']
        else:
            segment = row.Phoneme.split('|')[0]
            if segment not in parses_cache:
                try:
                    parses_cache[segment] = parser.parse(segment).as_list()
                except:
                    print(f'Failed to parse /{segment}/')
                    continue
    with open('parses_cache_phoible.json', 'w', encoding='utf-8') as out:
        json.dump(parses_cache, out, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    prepare_eurphon()
    prepare_phoible()
