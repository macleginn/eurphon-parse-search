import json
import sqlite3
from collections import defaultdict


def do_the_thing():
    db_connection = sqlite3.connect('europhon.sqlite')
    cursor = db_connection.cursor()

    all_lang_ids = set()
    for row in cursor.execute("SELECT id FROM languages"):
        all_lang_ids.add(row[0])
    inventories = defaultdict(list)
    for segment, language_id in cursor.execute("SELECT ipa, `language_id` FROM segments"):
        if language_id in all_lang_ids:
            inventories[language_id].append(segment)

    with open('inventories.json', 'w', encoding='utf-8') as out:
        json.dump(inventories, out, indent=2, ensure_ascii=False)
