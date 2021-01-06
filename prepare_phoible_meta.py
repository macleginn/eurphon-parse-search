import json
import os
import math
import pandas as pd

phoible = pd.read_csv(os.path.join('data', 'phoible.csv'), low_memory=False)
with open('inventories_phoible.json', 'r', encoding='utf-8') as inp:
    inventories_dict = json.load(inp)
inventory_id_to_gltc = {
    str(inventory_id): glottocode
    for inventory_id, glottocode in zip(phoible.InventoryID, phoible.Glottocode)
}

glottolog_geo = pd.read_csv(os.path.join(
    'data', 'languages_and_dialects_geo.csv'))
glottolog_geo.index = glottolog_geo.glottocode
glottolog_meta = pd.read_csv(os.path.join('data', 'languoid.csv'))
glottolog_meta.index = glottolog_meta.id

phoible_meta = {}
for inventory_id in inventories_dict:
    gltc = inventory_id_to_gltc[inventory_id]
    # Otherwise seems to conflict with the inbuilt 'name' field
    name = glottolog_meta.loc[gltc]['name']

    family_id = glottolog_meta.loc[gltc].family_id
    parent_id = glottolog_meta.loc[gltc].parent_id
    phylum = glottolog_meta.loc[family_id]['name'] if not pd.isnull(
        family_id) else 'Isolate'
    genus = glottolog_meta.loc[parent_id]['name'] if not pd.isnull(
        parent_id) else 'Ungrouped'

    # Normalise different kinds of missing values
    latitude = glottolog_geo.loc[gltc].latitude if (
        gltc in glottolog_geo.index and not math.isnan(glottolog_geo.loc[gltc].latitude)) else None
    longitude = glottolog_geo.loc[gltc].longitude if (
        gltc in glottolog_geo.index and not math.isnan(glottolog_geo.loc[gltc].longitude)) else None

    phoible_meta[inventory_id] = {
        'name': name,
        'glottocode': gltc,
        'phylum': phylum,
        'genus': genus,
        'latitude': latitude,
        'longitude': longitude
    }
with open(f'phoible_meta.json', 'w', encoding='utf-8') as out:
    json.dump(phoible_meta, out, indent=2, ensure_ascii=False)
