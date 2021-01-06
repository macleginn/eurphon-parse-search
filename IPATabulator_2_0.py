from IPAParser_2_0 import parse_consonant, parse_vowel
from io import StringIO
from itertools import product

SERIES_FORMING_FEATURES = {'pre-glottalised', 'pre-aspirated', 'pre-nasalised', 'pre-labialised', 'pharyngealised', 'nasalised', 'labialised', 'velarised', 'faucalised', 'palatalised', 'half-long', 'long', 'overlong', 'creaky voiced', 'breathy voiced', 'lateral-released', 'rhotic', 'advanced-tongue-root', 'retracted-tongue-root'}

CONS_ROW_NAMES = ['stop', 'implosive', 'trill', 'tap', 'lateral tap', 'fricative', 'affricate', 'lateral fricative', 'lateral affricate', 'nasal', 'approximant', 'lateral approximant']
CONS_COL_NAMES = ['bilabial', 'labio-velar', 'labio-palatal', 'labio-dental', 'dental', 'alveolar', 'postalveolar', 'hissing-hushing', 'retroflex', 'alveolo-palatal', 'palatal', 'palatal-velar', 'velar', 'uvular', 'pharyngeal', 'glottal', 'epiglottal']

VOW_ROW_NAMES = ['close', 'near-close', 'close-mid', 'mid', 'open-mid', 'near-open', 'open']
VOW_COL_NAMES = ['front', 'near-front', 'central', 'near-back', 'back']


def is_subset(list1, list2):
    for el in list1:
        if el not in list2:
            return False
    return True


def row_not_empty(row):
    # Returns true if at least one element
    # in the row except for the rowname,
    # which comes first, is not None 
    for el in row[1:]:
        if el != None:
            return True
    return False


def transpose(arr):
    # Array must be non-empty and not ragged,
    # and its elements must be non-empty arrays
    # as well. 
    new_arr = [
        [None for el in arr] for el in arr[0]
    ]
    for i in range(len(arr[0])):
        for j in range(len(arr)):
            new_arr[i][j] = arr[j][i]
    return new_arr


def delete_empty_rows_and_cols(table):
    # Delete empty rows then rotate, repeat,
    # and rotate back. 
    tmp = [ el for el in table if row_not_empty(el) ]
    tmp = transpose(tmp)
    tmp = [ el for el in tmp if row_not_empty(el) ]
    return transpose(tmp)


def remove_none(s):
    if s is None:
        return ''
    else:
        return s


def write_list(list_header, segment_arr, out_stream):
    out_stream.write(f'<h4>{list_header}</h4>\n')
    out_stream.write(f'<p class="ipa-listing">/{ "/, /".join(segment_arr) }/</p>\n')


def write_table(table, out_stream):
    out_stream.write('<table class="ipa-chart">\n')
    for r in table:
        out_stream.write('<tr>\n')
        out_stream.write(
            ''.join(
                map(
                    lambda x: f'<td>{remove_none(x)}</td>',
                    r)))
        out_stream.write('\n')
        out_stream.write('\n</tr>\n')
    out_stream.write('</table>\n')


def draw_table_consonants(table_header, parse_dict, out_stream):
    out_stream.write(f'<h4>{table_header}</h4>\n')
    # Create and fill a table with all features than 
    # delete empty rows and columns.
    rownames = [el for el in CONS_ROW_NAMES]
    colnames = [el for el in CONS_COL_NAMES]
    full_table = [[''] + colnames]
    full_table.extend([
        [rn]+[None for cn in colnames] for rn in rownames
    ])
    rowname_idx = {
        rowname: i+1 for i, rowname in enumerate(rownames)
    }
    colname_idx = {
        colname: i+1 for i, colname in enumerate(colnames)
    }
    for v in parse_dict.values():
        manner = v['manner']
        place = v['place']
        # Nasal stops are nasals for the
        # sake of the table. 
        if manner == 'stop' and v['nasal']:
            manner = 'nasal'
        # Lateral fricatives, affricates, taps, and
        # approximants are their own thing
        if manner in ['fricative',
                      'affricate',
                      'approximant',
                      'tap'] and v['lateral']:
            manner = f'lateral {manner}'
        # Interdental fricatives are dental
        # for the sake of the table
        if place == 'interdental':
            place = 'dental'
        i = rowname_idx[manner]
        j = colname_idx[place]
        if full_table[i][j] == None:
            full_table[i][j] = v['glyph']
        else:
            full_table[i][j] = full_table[i][j] + (', ' + v['glyph'])
    reduced_table = delete_empty_rows_and_cols(full_table)
    write_table(reduced_table, out_stream)


def get_tables_consonants(parse_dict, out_stream):
    if parse_dict:
        # Extract the base series
        # We need to separate additional articulations into
        # those that place consonants in different tables
        # and those that don't.
        base_series = {
            k: v for k, v in parse_dict.items() if v['length'] == 'short' \
                and not list(
                    filter(
                        lambda x: x in SERIES_FORMING_FEATURES,
                        v['additional articulations'] + \
                        v['pre-features']))
        }
        if base_series:
            draw_table_consonants('Basic short series', base_series, out_stream)
        # Find other series
        len_add_art_combs = {}
        for k, v in parse_dict.items():
            aa_of_interest = [
                el for el in sorted(v['additional articulations'] + \
                                    v['pre-features']) \
                    if el in SERIES_FORMING_FEATURES
            ]
            laa = (v['length'], tuple(aa_of_interest))
            if laa not in len_add_art_combs:
                len_add_art_combs[laa] = {}
            len_add_art_combs[laa].update({ k: v })
        try:
            del len_add_art_combs[('short', tuple())]
        except ValueError:
            pass
        if len_add_art_combs:
            for laa, new_series in len_add_art_combs.items():
                length, aas = laa
                header = f'{length.capitalize()} {" ".join(aas)} series'
                draw_table_consonants(header, new_series, out_stream)


def draw_table_vowels(table_header, parse_dict, out_stream):
    out_stream.write(f'<h4>{table_header}</h4>\n')
    # Create and fill a table with all features than 
    # delete empty rows and columns.
    rownames = [el for el in VOW_ROW_NAMES]
    colnames = [el for el in VOW_COL_NAMES]
    full_table = [[''] + colnames]
    full_table.extend([
        [rn]+[None for cn in colnames] for rn in rownames
    ])
    rowname_idx = {
        rowname: i+1 for i, rowname in enumerate(rownames)
    }
    colname_idx = {
        colname: i+1 for i, colname in enumerate(colnames)
    }
    for v in parse_dict.values():
        i = rowname_idx[v['height']]
        j = colname_idx[v['backness']]
        if full_table[i][j] == None:
            full_table[i][j] = v['glyph']
        else:
            full_table[i][j] = full_table[i][j] + (', ' + v['glyph'])
    reduced_table = delete_empty_rows_and_cols(full_table)
    write_table(reduced_table, out_stream)


def get_tables_vowels(parse_dict, out_stream):
    if parse_dict:
        # Separate apical vowels and polyphthongs
        apical_vowels = []
        diphthongs = []
        triphthongs = []
        keys_for_deletion = []
        for k, v in parse_dict.items():
            if v['apical vowel']:
                apical_vowels.append(v['glyph'])
                keys_for_deletion.append(k)
            elif v['diphthong']:
                diphthongs.append(v['glyph'])
                keys_for_deletion.append(k)
            elif v['triphthong']:
                triphthongs.append(v['glyph'])
                keys_for_deletion.append(k)
        for k in keys_for_deletion:
            del parse_dict[k]

        # The respective segments will be written
        # to the stream at the end.

        base_series = {
            k: v for k, v in parse_dict.items() if v['length'] == 'short' \
                and not list(
                    filter(
                        lambda x: x in SERIES_FORMING_FEATURES,
                        v['additional articulations'] + \
                        v['pre-features']))
        }
        if base_series:
            draw_table_vowels('Basic short series', base_series, out_stream)
        # Find other series
        len_add_art_combs = {}
        for k, v in parse_dict.items():
            aa_of_interest = [
                el for el in sorted(v['additional articulations'] + \
                                    v['pre-features']) \
                    if el in SERIES_FORMING_FEATURES
            ]
            laa = (v['length'], tuple(aa_of_interest))
            if laa not in len_add_art_combs:
                len_add_art_combs[laa] = {}
            len_add_art_combs[laa].update({ k: v })
        try:
            del len_add_art_combs[('short', tuple())]
        except KeyError:
            pass
        if len_add_art_combs:
            for laa, new_series in len_add_art_combs.items():
                length, aas = laa
                header = f'{length.capitalize()} {" ".join(aas)} series'
                draw_table_vowels(header, new_series, out_stream)

        if apical_vowels:
            write_list('Apical vowels', apical_vowels, out_stream)
        if diphthongs:
            write_list('Diphthongs', diphthongs, out_stream)
        if triphthongs:
            write_list('Triphthongs', triphthongs, out_stream)


def dump_unparsed(unparsed_arr, out_stream):
    if unparsed_arr:
        out_stream.write('Segments with unrecognised features: /')
        out_stream.write('/, /'.join(unparsed_arr))
        out_stream.write('/')


def get_html_for_consonants(cons_list):
    unparsed = []
    parsed = {}
    for c in cons_list:
        try:
            parsed[c] = parse_consonant(c)
        except ValueError:
            unparsed.append(c)
    with StringIO() as html_stream:
        get_tables_consonants(parsed, html_stream)
        dump_unparsed(unparsed, html_stream)
        return html_stream.getvalue()


def get_html_for_vowels(vow_list):
    unparsed = []
    parsed = {}
    for v in vow_list:
        try:
            parsed[v] = parse_vowel(v)
        except ValueError:
            unparsed.append(v)
    with StringIO() as html_stream:
        get_tables_vowels(parsed, html_stream)
        dump_unparsed(unparsed, html_stream)
        return html_stream.getvalue()
