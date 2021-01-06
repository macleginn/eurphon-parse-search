import os
import json
import sqlite3
from collections import defaultdict
from unicodedata import normalize
import pandas as pd
from IPAParser_3_0 import IPAParser

parser = IPAParser()


def prepare_eurphon():
    db_connection = sqlite3.connect(os.path.join('data', 'europhon.sqlite'))
    cursor = db_connection.cursor()

    all_lang_ids = set()
    for row in cursor.execute("SELECT id FROM languages"):
        all_lang_ids.add(row[0])
    inventories = defaultdict(list)
    for segment, language_id in cursor.execute("SELECT ipa, `language_id` FROM segments"):
        if language_id in all_lang_ids:
            inventories[language_id].append(
                normalize('NFD', segment))

    with open('inventories.json', 'w', encoding='utf-8') as out:
        json.dump(inventories, out, indent=2, ensure_ascii=False)


def prepare_phoible():
    d = pd.read_csv(os.path.join('data', 'phoible.csv'), low_memory=False)
    d = d.loc[d.SegmentClass != 'tone']
    inventories = defaultdict(list)

    # Discard inventories where not all segments can be parsed
    parse_memo = set()
    unparsable_memo = set()
    discarded_inventories = set()
    for inventory_id in d.InventoryID.unique():
        chunk = d.loc[d.InventoryID == inventory_id]
        if not inventory_parseable(chunk, parse_memo, unparsable_memo):
            discarded_inventories.add(inventory_id)
    print(f'{len(discarded_inventories)} problematic inventories discarded')

    # Select one inventory per language
    for glottocode in d.Glottocode.unique():
        inventory_ids = list(
            d.loc[d.Glottocode == glottocode].InventoryID.unique())
        # By default select the inventory with the biggest id
        candidates = list(filter(lambda iid: iid not in discarded_inventories,
                                 sorted(inventory_ids, reverse=True)))
        if not candidates:
            continue
        inventory_id = candidates[0]
        for row in d.loc[d.InventoryID == inventory_id].itertuples():
            if row.click == '-':
                segment = row.Phoneme.split('|')[0]
            else:
                segment = row.Phoneme
            inventories[int(inventory_id)].append(normalize('NFD', segment))
    with open('inventories_phoible.json', 'w', encoding='utf-8') as out:
        json.dump(inventories, out, indent=2, ensure_ascii=False)


def inventory_parseable(phoible_chunk, parse_memo, unparsable_memo):
    for row in phoible_chunk.itertuples():
        if '+' in row.click:
            continue
        segment = row.Phoneme.split('|')[0]
        if segment in parse_memo:
            continue
        elif segment in unparsable_memo:
            return False
        try:
            parser.parse(segment)
            parse_memo.add(segment)
        except:
            print(f'Failed to parse /{segment}/')
            unparsable_memo.add(segment)
            return False
    return True


if __name__ == "__main__":
    prepare_eurphon()
    prepare_phoible()
