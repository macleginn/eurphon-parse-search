import json
import base64

from flask import Flask, request, make_response, jsonify
from pprint import pprint
from io import StringIO

import query_processor as qp
from dbprocessing import *
from IPATabulator_2_0 import get_html_for_consonants, get_html_for_vowels
from tests import consonant_parsing_test, vowel_parsing_test


def allow_origin(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'


def populate_headers_json(resp):
    resp.headers['Content-Type'] = 'application/json'
    allow_origin(resp)


def populate_headers_plain(resp):
    resp.headers['Content-Type'] = 'text/plain'
    allow_origin(resp)


def populate_headers_css(resp):
    resp.headers['Content-Type'] = 'text/css'
    allow_origin(resp)


def populate_headers_html(resp):
    resp.headers['Content-Type'] = 'text/html'
    allow_origin(resp)


def populate_headers_csv(resp, filename):
    resp.headers['Content-Type'] = 'text/csv'
    resp.headers['Content-Disposition'] = f'attachment; filename="{filename}.tsv"'
    allow_origin(resp)


app = Flask(__name__)


# In order to secure the database, we do not permit
# deletes or edits over the API.

@app.route('/dump/<table>', methods=['GET'])
def dumper(table):
    try:
        resp = make_response(dump_table_to_csv(table), 200)
    except:
        resp = make_response(
            'Failed to dump the table. Is the name correct?', 500)
        populate_headers_plain(resp)
        return resp
    populate_headers_csv(resp, table)
    return resp


@app.route('/query/<action>', methods=['GET', 'POST'])
def query_handler(action):
    "A web wrapper around query_processor.py."
    if action == 'usage':
        resp = make_response(qp.USAGE, 200)
        populate_headers_plain(resp)
    elif action == 'list-phyla':
        resp = make_response(qp.print_phyla(), 200)
        populate_headers_plain(resp)
    elif action == 'genus-tree':
        resp = make_response(qp.print_genus_tree(), 200)
        populate_headers_plain(resp)
    elif action == 'query':
        POST_data = json.loads(request.get_data())
        if 'query_string' not in POST_data:
            resp = make_response('No query provided', 400)
            populate_headers_plain(resp)
        query_string = POST_data['query_string']
        restrictor_dict = {}
        if 'phylum' in POST_data:
            restrictor_dict['phylum'] = POST_data['phylum']
        elif 'genus' in POST_data:
            restrictor_dict['genus'] = POST_data['genus']
        try:
            query = qp.parse_query(query_string)
            try:
                result = qp.apply_query_and_filter(query, restrictor_dict)
                resp = make_response(jsonify(result), 200)
                populate_headers_json(resp)
            except Exception as e:
                resp = make_response(f'Internal error: {e}', 500)
                populate_headers_plain(resp)
        except Exception as e:
            resp = make_response(
                f'Bad query: {query_string}\n\nParser output: {e}', 400)
            populate_headers_plain(resp)
    return resp


@app.route('/phyla/<action>', methods=['GET', 'POST'])
def phyla_handler(action):
    # TODO: authentication
    if action == 'all':
        phyla_dict = get_phyla_dict()
        resp = make_response(jsonify(phyla_dict), 200)
        populate_headers_json(resp)
        return resp
    elif action == 'tree':
        phyla_tree = get_phylogenetic_tree()
        resp = make_response(jsonify(phyla_tree), 200)
        populate_headers_json(resp)
        return resp
    elif action == 'add':
        data = request.json
        pprint(data)
        resp = make_response('Success', 200)
        populate_headers_plain(resp)
        return resp
    else:
        resp = make_response('Wrong action', 400)
        populate_headers_plain(resp)
        return resp


@app.route('/genera/<action>', methods=['GET', 'POST'])
def genera_handler(action):
    # TODO: authentication
    if action == 'byphylum':
        if 'phylum_id' not in request.args:
            resp = make_response('No phylum ID provided', 400)
            populate_headers_plain(resp)
            return resp
        phylum_id = request.args.get('phylum_id')
        genus_array = get_genera_for_phylum(phylum_id)
        resp = make_response(jsonify(genus_array), 200)
        populate_headers_json(resp)
        return resp
    elif action == 'add':
        data = request.json
        pprint(data)
        resp = make_response('Success', 200)
        populate_headers_plain(resp)
        return resp
    else:
        resp = make_response('Wrong action', 400)
        populate_headers_plain(resp)
        return resp


@app.route('/contributors', methods=['GET'])
def contributor_handler():
    resp = get_all_contributors()
    resp = make_response(jsonify(resp), 200)
    populate_headers_json(resp)
    return resp


@app.route('/languages/<action>', methods=['POST', 'GET'])
def language_handler(action):
    # TODO: authentication
    if action == 'all':
        if 'with_dialects' not in request.args:
            with_dialects = False
        else:
            with_dialects = True
        lang_dict = get_all_langs(with_dialects)
        resp = jsonify(lang_dict)
        populate_headers_json(resp)
        return resp
    elif action == 'byphylum':
        if 'phylum_id' not in request.args:
            resp = make_response('No phylum ID provided', 400)
            populate_headers_plain(resp)
            return resp
        phylum_id = request.args.get('phylum_id')
        lang_array = get_langs_for_phylum(phylum_id)
        resp = make_response(jsonify(lang_array))
        populate_headers_json(resp)
        return resp
    elif action == 'bygenus':
        if 'genus_id' not in request.args:
            resp = make_response('No genus ID provided', 400)
            populate_headers_plain(resp)
            return resp
        genus_id = request.args.get('genus_id')
        lang_array = get_langs_for_genus(genus_id)
        resp = make_response(jsonify(lang_array))
        populate_headers_json(resp)
        return resp
    elif action == 'json':
        if 'lang_id' not in request.args:
            resp = make_response('No language ID provided', 400)
            populate_headers_plain(resp)
            return resp
        resp = make_response(
            jsonify(
                get_language_dict(request.args['lang_id'])), 200)
        populate_headers_json(resp)
        return resp
    # TODO: add ISO codes and glottocodes
    elif action == 'html':
        if 'lang_id' not in request.args:
            resp = make_response('No language ID provided', 400)
            populate_headers_plain(resp)
            return resp
        lang_dict = get_language_dict(request.args['lang_id'])
        consonants_html = get_html_for_consonants(lang_dict['consonants'])
        vowels_html = get_html_for_vowels(lang_dict['vowels'])
        out_stream = StringIO()
        out_stream.write(f'<h3>Consonants</h3>\n{consonants_html}')
        out_stream.write(f'<h3>Vowels</h3>\n{vowels_html}')
        if lang_dict['tones']:
            out_stream.write(
                f'<h3>Tones</h3>\n<p class="ipa-listing">{", ".join(lang_dict["tones"])}</p>\n')
        if lang_dict['initial_clusters']:
            out_stream.write(
                f'<h3>Licit initial clusters</h3>\n<p class="ipa-listing">{lang_dict["initial_clusters"]}</p>\n')
        if lang_dict['finals']:
            out_stream.write(
                f'<h3>Licit finals</h3>\n<p class="ipa-listing">{lang_dict["finals"]}</p>\n')
        if lang_dict['syllabic_templates']:
            out_stream.write(
                f'<h3>Licit syllabic templates</h3>\n<p class="ipa-listing">{lang_dict["syllabic_templates"]}</p>\n')
        if lang_dict['comments']:
            comments_section = f'''<p>Comments: {lang_dict['comments']}</p>'''
        else:
            comments_section = ''
        resp = make_response(f'''
<html>
<head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Serif:400,400i,700,700i" rel="stylesheet">
    <link href="{BASE_URL}/css" rel="stylesheet">
    <title>EURPhon: {lang_dict['name']}</title>
</head>
<body>
<a href="{BASE_URL}">&lt;&lt;&lt; Home page</a>
<h2>{name_to_str(lang_dict['name'], lang_dict['alternate_names'])}</h2>
<div id="lang-card">
<p>Phylum: {lang_dict['phylum']}</p>
<p>Genus: {lang_dict['genus']}</p>
<p>Lat/lon: {lang_dict['lat']}, {lang_dict['lon']}</p>
<p>ISO code: {get_iso_link(lang_dict['iso_code'])}</p>
</div>
<div id="tables">
{out_stream.getvalue()}
</div>
<p>Source: {lang_dict['source']}</p>
{comments_section}
<p>Contributed by: {lang_dict['contributor_name']} ({lang_dict['contributor_email']})</p>
</body>
</html>''', 200)
        populate_headers_html(resp)
        return resp
    elif action == 'add':
        POST_data = json.loads(request.data)
        # try:
        # pprint(POST_data)
        add_language_data(POST_data)
        resp = make_response('Language added', 200)
        populate_headers_plain(resp)
        # except:
        #     resp = make_response('Error')
        #     populate_headers_500(resp)
        return resp
    else:
        resp = make_response('Wrong action', 400)
        populate_headers_plain(resp)
        return resp


@app.route('/', methods=['GET'])
def homepage_handler():
    warning = '<div style="width: 100%; border: 2px solid brown; border-radius: 5px; padding: 5px;">This is a pre-release version of the database. It only displays a tree of languages and their inventories. Please see <a href="http://eurasianphonology.info">the current stable version</a> for search, maps, and language-group reports.</div>\n'
    header = '<h1>The Database of Eurasian Phonological Inventories (pre-release version)</h1>\n'
    footer = '<div style="position: fixed; bottom: 0; background-color: beige; padding: 5px;">Please cite the original source as well as <a href="https://www.degruyter.com/view/j/lingvan.2018.4.issue-1/lingvan-2017-0050/lingvan-2017-0050.xml">this paper</a> if you use the data in your research.</div>'

    main_content = get_language_tree()

    resp = make_response(f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Serif:400,400i,700,700i" rel="stylesheet">
    <link href="{BASE_URL}/css" rel="stylesheet">
    <title>The Database of Eurasian Phonological Inventories (pre-release version)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    {warning}
    {header}
    {main_content}
    {footer}
</body>
</html>
''', 200)
    populate_headers_html(resp)
    return resp


@app.route('/downloads', methods=['GET'])
def downloads_handler():
    with open('assets/download_template.html', 'r') as inp:
        html_template = inp.read()
    with open('assets/dbdiagram.png', 'rb') as inp:
        img_base64 = base64.b64encode(inp.read())
    resp = make_response(html_template.format(
        base_url=BASE_URL,
        database_img_src=img_base64.decode()), 200)
    populate_headers_html(resp)
    return resp

# This handler takes a list of glyphs
# as input and returns a list of glyphs
# it couldn't parse. An empty result
# signifies success.


@app.route('/validation/<action>', methods=['POST'])
def validation_handler(action):
    if action == 'consonants':
        result = []
        consonant_arr = json.loads(request.data)
        for el in consonant_arr:
            if not consonant_parsing_test(el):
                result.append(el)
        resp = make_response(jsonify(result))
        populate_headers_json(resp)
        return resp
    elif action == 'vowels':
        result = []
        vowel_arr = json.loads(request.data)
        for el in vowel_arr:
            if not vowel_parsing_test(el):
                result.append(el)
        resp = make_response(jsonify(result))
        populate_headers_json(resp)
        return resp
    else:
        resp = make_response(f'Wrong action: {action}', 400)
        populate_headers_plain(resp)
        return resp


# A hack for serving CSS over https
# TODO: refactor
@app.route('/css', methods=['GET'])
def css_handler():
    with open('assets/style.css', 'r') as inp:
        CSS_RESPONSE = make_response(inp.read())
        populate_headers_css(CSS_RESPONSE)
        return CSS_RESPONSE
