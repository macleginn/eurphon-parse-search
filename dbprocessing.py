import sqlite3
import csv

from io import StringIO
from unicodedata import normalize

DBPATH = 'europhon.sqlite'
BASE_URL = 'https://eurphon.info'
# BASE_URL = 'http://127.0.0.1:11000'
ISO_URL = 'https://iso639-3.sil.org/code'
GLOTTOLOG_URL = 'https://glottolog.org/resource/languoid/id'


# Helper routines

def name_to_str(lang_name, alternate_names):
    """When applicable, adds alternate names to the name
    of a language, genus, or phylum"""
    if alternate_names:
        return normalize('NFC', f'{lang_name} ({alternate_names})')
    else:
        return normalize('NFC', lang_name)


# Database access routines


def get_url_for_iso(iso):
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        try:
            lang_id = cursor.execute(
                f'''
                SELECT `id`
                FROM `languages`
                WHERE `iso_code` = "{iso}"
                ''').fetchone()[0]
        except:
            return 'ISO code not found'
        return f'http://eurphon.info/languages/html?lang_id={lang_id}'


def get_iso_link(iso_code):
    if iso_code == None:
        return ''
    else:
        return f'<a href="{ISO_URL}/{iso_code}">{iso_code}</a>'


def dump_table_to_csv(table_name):
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        table_names = [
            el[1] for el in cursor.execute(
                f'PRAGMA table_info(`{table_name}`)'
            ).fetchall()]
        csv_stream = StringIO()
        csv_writer = csv.writer(csv_stream, delimiter='\t')
        csv_writer.writerow(table_names)
        for record in cursor.execute(
            f'SELECT * FROM `{table_name}`'):
            csv_writer.writerow(record)
    return csv_stream.getvalue()


def get_phyla_dict():
    phyla_dict = {}
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        for (phylum_id, name, glottocode, alternate_names) in cursor.execute(
            'SELECT * FROM `phyla`'
        ):
            phyla_dict[phylum_id] = {
                'name': name_to_str(name, alternate_names),
                'glottocode': glottocode
            }
    return phyla_dict


def get_phylogenetic_tree():
    phylo_tree = {}
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        for (phylum_id, phylum_name, phylum_alternate_names) in cursor.execute(
            'SELECT `id`, `name`, `alternate_names` FROM `phyla`'
        ):
            phylo_tree[phylum_id] = {
                'name': phylum_name,
                'alternate_names': phylum_alternate_names,
                'genera': {}
            }
            cursor_nested = connection.cursor()
            for (genus_id, genus_name, genus_alternate_names) in cursor_nested.execute(
                f'''
                SELECT `id`, `name`, `alternate_names`
                FROM `genera`
                WHERE `phylum_id` = {phylum_id}
                '''
            ):
                phylo_tree[phylum_id]['genera'][genus_id] = {
                    'name': genus_name,
                    'alternate_names': genus_alternate_names
                }
    return phylo_tree


def get_genera_for_phylum(phylum_id):
    genus_arr = []
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        for (genus_id, name, glottocode, alternate_names) in cursor.execute(
            '''SELECT `id`, `name`, `glottocode`, `alternate_names`
            FROM `genera`
            WHERE `phylum_id` = ?
            ''',
            (phylum_id,)
        ):
            genus_arr.append({
                'id': genus_id,
                'name': name_to_str(name, alternate_names),
                'glottocode': glottocode
            })
    genus_arr.sort(key = lambda x: x['name'])
    return genus_arr


def get_all_langs(with_dialects=False):
    langs_arr = []
    if with_dialects:
        numeric_bool = 1
    else:
        numeric_bool = 0
    # The value of numeric_bool is set here,
    # no chance of an injection.
    stmt = f'''SELECT `id`, `name`, `alternate_names`, `latitude`, `longitude`
    FROM `languages`
    WHERE `dialect` = {numeric_bool}'''
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        for (lang_id, name, alternate_names, lat, lon) in cursor.execute(stmt):
            langs_arr.append({
                'id': lang_id,
                'name': name_to_str(name, alternate_names),
                'lat': lat,
                'lon': lon
                })
    langs_arr.sort(key = lambda x: x['name'])
    return langs_arr


def get_langs_for_genus(genus_id, with_dialects=False):
    langs_dict = {}
    stmt = f'''SELECT `id`, `name`, `alternate_names`
    FROM `languages`
    WHERE `dialect` = {int(with_dialects)} AND `genus_id` = ?'''
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        for (lang_id, name, alternate_names) in cursor.execute(
            stmt,
            (genus_id,)):
            langs_dict[lang_id] = {
                'name': name,
                'alternate_names': alternate_names
                }
    return langs_dict


# TODO: convert into returning a dict
def get_langs_for_phylum(phylum_id, with_dialects=False):
    langs_arr = []
    stmt = f'''SELECT `id`, `name`, `alternate_names`
    FROM `languages`
    WHERE `dialect` = {int(with_dialects)} AND `phylum_id` = ?'''
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        for (lang_id, name, alternate_names) in cursor.execute(
            stmt,
            (phylum_id,)):
            langs_arr.append({
                'id': lang_id,
                'name': name_to_str(name, alternate_names)
                })
    langs_arr.sort(key = lambda x: x['name'])
    return langs_arr


def get_field_by_id(table_name, field_name, entity_id):
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        return cursor.execute(
            f'''
            SELECT `{field_name}` FROM `{table_name}`
            WHERE `id` = {entity_id}
            '''
        ).fetchone()[0]


def get_field_by_foreign_id(table_name,
                            field_name,
                            foreign_id_column,
                            foreign_id):
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        return cursor.execute(
            f'''
            SELECT `{field_name}` FROM `{table_name}`
            WHERE `{foreign_id_column}` = {foreign_id}
            '''
        ).fetchone()[0]


def get_language_dict(lang_id):
    lang_dict = {
        'id': lang_id
    }
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        (
            name,
            alternate_names,
            phylum_id,
            genus_id,
            lat,
            lon,
            iso_code,
            source,
            contributor_id,
            is_dialect,
            head_dialect,
            comments
        ) = cursor.execute(
            '''
            SELECT `name`,
                   `alternate_names`,
                   `phylum_id`,
                   `genus_id`,
                   `latitude`,
                   `longitude`,
                   `iso_code`,
                   `source`,
                   `contributor_id`,
                   `dialect`,
                   `head_dialect`,
                   `comments`
            FROM `languages`
            WHERE `id` = ?
            ''',
            (lang_id,)
        ).fetchone()
        phylum = get_field_by_id('phyla', 'name', phylum_id)
        genus = get_field_by_id('genera', 'name', genus_id)
        contributor_name, contributor_email = cursor.execute(
            '''
            SELECT `name`, `email`
            FROM `contributors`
            WHERE `id` = ?
            ''',
            (contributor_id,)
        ).fetchone()
        lang_dict.update({
            'name': name,
            'alternate_names': alternate_names,
            'phylum': phylum,
            'genus': genus,
            'lat': lat,
            'lon': lon,
            'iso_code': iso_code,
            'source': source,
            'comments': comments,
            'contributor_name': contributor_name,
            'contributor_email': contributor_email
        })
        lang_dict['consonants'] = [
            el[0] for el in cursor.execute(
                '''
                SELECT `ipa`
                FROM `segments`
                WHERE `language_id` = ? AND `is_consonant` = 1
                ''',
                (lang_id,))
        ]
        lang_dict['vowels'] = [
            el[0] for el in cursor.execute(
                '''
                SELECT `ipa`
                FROM `segments`
                WHERE `language_id` = ? AND `is_consonant` = 0
                ''',
                (lang_id,))
        ]
        lang_dict['tones'] = [
            el[0] for el in cursor.execute(
                '''
                SELECT `tone`
                FROM `tones`
                WHERE `language_id` = ?
                ''',
                (lang_id,))
        ]
        try:
            lang_dict['initial_clusters'] = get_field_by_foreign_id(
                'initial_clusters',
                'initial_cluster',
                'language_id',
                lang_id)
        except:
            lang_dict['initial_clusters'] = ''
        try:
            lang_dict['finals'] = get_field_by_foreign_id(
                'finals',
                'final',
                'language_id',
                lang_id)
        except:
            lang_dict['finals'] = ''
        try:
            lang_dict['syllabic_templates'] = get_field_by_foreign_id(
                'syllabic_templates',
                'template',
                'language_id',
                lang_id)
        except:
            lang_dict['syllabic_templates'] = ''
        if is_dialect:
            head_dialect_name = get_field_by_id(
                'languages',
                'name',
                head_dialect)
        else:
            head_dialect_name = ''
        lang_dict.update({
            'is_dialect': bool(is_dialect),
            'head_dialect_id': head_dialect,
            'head_dialect_name': head_dialect_name
        })
        return lang_dict


def get_lang_link(lang_id, name, alternate_names, is_a_dialect=False):
    if is_a_dialect:
        style_element = ' style="font-style: italic;"'
    else:
        style_element = ''
    if alternate_names:
        return normalize(
            'NFC', 
            f'<a{style_element} class="lang-link" href="{BASE_URL}/languages/html?lang_id={lang_id}">{name} ({alternate_names})</a>')
    else:
        return normalize(
            'NFC', 
            f'<a{style_element} class="lang-link" href="{BASE_URL}/languages/html?lang_id={lang_id}">{name}</a>')


def get_lang_link_w_dialects(lang_id, name, alternate_names):
    # Check if language has dialects
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        dialect_count = cursor.execute(
            f'''
            SELECT COUNT(`id`)
            FROM `languages`
            WHERE `head_dialect` = {lang_id}
            AND `deprecated` = 0
            '''
        ).fetchone()[0]
        if dialect_count == 0:
            dialect_str = ''
        else:
            tmp = []
            for dialect_id, dialect_name, dialect_alternate_names in cursor.execute(
                    f'''
                    SELECT `id`, `name`, `alternate_names`
                    FROM `languages`
                    WHERE `head_dialect` = {lang_id}
                    '''
                ):
                tmp.append(
                    get_lang_link(dialect_id,
                                  dialect_name,
                                  dialect_alternate_names,
                                  True))
            dialect_str = f' [{", ".join(tmp)}]'
    return get_lang_link(lang_id, name, alternate_names) + dialect_str
    

def get_lang_links(lang_list):
    '''Lang list contains tuple of the form
    (id, name, alternate_names).'''
    return ', '.join(get_lang_link_w_dialects(*el) for el in lang_list)


# TODO: print alternate names for phyla and genera
# TODO: add a version without dialects
def get_language_tree(with_dialects=True):
    out_stream = StringIO()
    out_stream.write('<ul>\n')
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        phyla_arr = [
            el for el in cursor.execute(
                '''
                SELECT `id`, `name`, `alternate_names`
                FROM `phyla`
                '''
            )]
        phyla_arr.sort(key = lambda x: x[1])
        for phylum_id, phylum_name, phylum_alternate_names in phyla_arr:
            language_count = cursor.execute(
                f'''
                SELECT COUNT(`name`)
                FROM `languages`
                WHERE `phylum_id` = {phylum_id}
                '''
                ).fetchone()[0]
            if language_count == 0:
                continue
            phylum_full_name = name_to_str(phylum_name, phylum_alternate_names)
            out_stream.write(f'<li>{normalize("NFC", phylum_full_name)}\n<ul>\n')
            genera_arr = [
                el for el in cursor.execute(
                    f'''
                    SELECT `name`, `id`
                    FROM `genera`
                    WHERE `phylum_id` = {phylum_id}
                    '''
                )
            ]
            genera_arr.sort()
            # TODO: cleanup genera without languages
            if len(genera_arr) == 1 and genera_arr[0][0] == 'Ungrouped':
                # Don't use any genera labels
                lang_arr = [
                    el for el in cursor.execute(
                        f'''
                        SELECT `id`, `name`, `alternate_names`
                        FROM `languages`
                        WHERE `phylum_id` = {phylum_id} 
                            AND `genus_id` = {genera_arr[0][1]}
                            AND `dialect` = 0
                            AND `deprecated` = 0
                        ''')]
                if lang_arr:
                    lang_arr.sort(key = lambda x: x[1])
                    lang_string = get_lang_links(lang_arr)
                    out_stream.write(f'<li>{lang_string}</li>\n')
            else:
                for g_name, genus_id in genera_arr:
                    lang_arr = [
                        el for el in cursor.execute(
                            f'''
                            SELECT `id`, `name`, `alternate_names`
                            FROM `languages`
                            WHERE `phylum_id` = {phylum_id} 
                                AND `genus_id` = {genus_id}
                                AND `dialect` = 0
                                AND `deprecated` = 0
                            ''')]
                    if lang_arr:
                        out_stream.write(f'<li><span style="font-variant: small-caps;">{normalize("NFC", g_name)}</span>: ')
                        lang_arr.sort(key = lambda x: x[1])
                        lang_string = get_lang_links(lang_arr)
                        out_stream.write(f'{lang_string}')
                        out_stream.write('</li>\n')
            out_stream.write('</ul>\n')
            out_stream.write('</li>\n')
    out_stream.write('</ul>\n')
    return out_stream.getvalue()


def get_all_contributors():
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        contributors_dict = {}
        for contr_id, name, email in cursor.execute(
            '''
            SELECT `id`, `name`, `email`
            FROM `contributors`
            '''
            ):
            contributors_dict[contr_id] = {
                'name': name,
                'email': email
            }
        return contributors_dict


def add_language_data(data):
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()

        # Add a new language; abort if
        # the combination of the name and
        # phylum and genus ids is not unique.
        test_count = cursor.execute(
            '''
            SELECT COUNT(`id`)
            FROM `languages`
            WHERE `name` = ?
                AND `phylum_id` = ?
                AND `genus_id` = ?
            ''',
            (data['name'], data['phylum_id'], data['genus_id'])
        ).fetchone()[0]
        if test_count != 0:
            raise ValueError(
                f"This combination of language name ({data['name']}), phylum id ({data['phylum_id']}), and genus_id ({data['genus_id']}) already exists in the database")

        cursor.execute(
            '''
            INSERT INTO `languages`
            (
                `name`,
                `iso_code`,
                `glottocode`,
                `phylum_id`,
                `genus_id`,
                `contributor_id`,
                `source`,
                `comments`,
                `dialect`,
                `latitude`,
                `longitude`,
                `head_dialect`,
                `alternate_names`
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''',
            (
                data['name'],
                data['iso_code'],
                data['glottocode'],
                data['phylum_id'],
                data['genus_id'],
                data['contributor_id'],
                data['source'],
                data['comments'],
                data['is_dialect'],
                data['lat'],
                data['lon'],
                data['head_dialect_id'],
                data['alternate_names']
            ))

        new_lang_id = cursor.execute(
            '''
            SELECT `id`
            FROM `languages`
            WHERE `name` = ?
                AND `phylum_id` = ?
                AND `genus_id` = ?
            ''',
            (data['name'], data['phylum_id'], data['genus_id'])
        ).fetchone()[0]

        # Add obligatory stuff for the new language
        for cons in data['consonants']:
            cursor.execute(
                '''
                INSERT INTO `segments`
                (`language_id`, `ipa`, `is_consonant`)
                VALUES (?,?,?)
                ''',
                (new_lang_id, cons, 1))
        for vow in data['vowels']:
            cursor.execute(
                '''
                INSERT INTO `segments`
                (`language_id`, `ipa`, `is_consonant`)
                VALUES (?,?,?)
                ''',
                (new_lang_id, vow, 0))
        
        # Add optional elements
        if data['tones']:
            for tone in data['tones']:
                cursor.execute(
                    '''
                    INSERT INTO `tones`
                    (`language_id`, `tone`)
                    VALUES (?,?)
                    ''',
                    (new_lang_id, tone))
        if data['initial_clusters']:
            cursor.execute(
                'INSERT INTO `initial_clusters` (`language_id`, `initial_cluster`) VALUES (?,?)',
                (new_lang_id, data['initial_clusters']))
        if data['finals']:
            cursor.execute(
                'INSERT INTO `finals` (`language_id`, `final`) VALUES (?,?)', 
                (new_lang_id, data['finals']))
        if data['syllabic_templates']:
            cursor.execute(
                'INSERT INTO `syllabic_templates` (`language_id`, `template`) VALUES (?,?)',
                (new_lang_id, data['syllabic_templates']))
        connection.commit()
