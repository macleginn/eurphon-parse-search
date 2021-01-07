import json
import base64

from flask import Flask, request, make_response, jsonify
from pprint import pprint

import query_processor as qp
from dbprocessing import *
from formatter import get_homepage, get_language_page
from tests import consonant_parsing_test, vowel_parsing_test

# import prepare_parse_cache
# import prepare_inventory_file


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
        query_phoible = 'phoible' in POST_data
        restrictor_dict = {}
        if 'phylum' in POST_data:
            restrictor_dict['phylum'] = POST_data['phylum']
        elif 'genus' in POST_data:
            restrictor_dict['genus'] = POST_data['genus']
        try:
            query = qp.parse_query(query_string)
            try:
                result = qp.apply_query_and_filter(
                    query, restrictor_dict, query_phoible)
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
        resp = make_response(get_language_page(lang_dict), 200)
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
    resp = make_response(get_homepage(), 200)
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
# @app.route('/css', methods=['GET'])
# def css_handler():
#     with open('assets/style.css', 'r') as inp:
#         CSS_RESPONSE = make_response(inp.read())
#         populate_headers_css(CSS_RESPONSE)
#         return CSS_RESPONSE


# Initialise data caches beforehand
# prepare_inventory_file.prepare_eurphon()
# prepare_inventory_file.prepare_phoible()
# prepare_parse_cache.prepare_eurphon()
# prepare_parse_cache.prepare_phoible()
