from io import StringIO

from IPATabulator_2_0 import get_html_for_consonants, get_html_for_vowels
from dbprocessing import BASE_URL, name_to_str, get_iso_link, get_language_tree


def get_homepage():
    warning = '<div style="width: 100%; border: 2px solid brown; border-radius: 5px; padding: 5px;">This is a pre-release version of the database. It only displays a tree of languages and their inventories. Please see <a href="http://eurasianphonology.info">the current stable version</a> for search, maps, and language-group reports.</div>\n'
    header = '''<h1>The Database of Eurasian Phonological Inventories</h1>
<div id="menu">
    <a href="https://eurphon.info">Home</a>
    <span>&nbsp;|&nbsp;</span>
    <a href="https://eurphon.info/about/">About</a>
    <span>&nbsp;|&nbsp;</span>
    <a href="https://eurphon.info/map/">Map</a>
    <span>&nbsp;|&nbsp;</span>
    <a href="https://eurphon.info/search/">Search</a>
    <span>&nbsp;|&nbsp;</span>
    <a href="https://eurphon.info/downloads">Download</a>
</div>'''
    footer = '<div style="position: fixed; bottom: 0; background-color: beige; padding: 5px;">Please cite the original source as well as <a href="https://www.degruyter.com/view/j/lingvan.2018.4.issue-1/lingvan-2017-0050/lingvan-2017-0050.xml">this paper</a> if you use the data in your research.</div>'

    main_content = get_language_tree()

    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Serif:400,400i,700,700i" rel="stylesheet">
    <link href="{BASE_URL}/static/style.css" rel="stylesheet">
    <title>The Database of Eurasian Phonological Inventories</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    {header}
    {main_content}
    {footer}
</body>
</html>
'''


def get_language_page(lang_dict):
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
    return f'''
<html>
<head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Serif:400,400i,700,700i" rel="stylesheet">
    <link href="{BASE_URL}/static/style.css" rel="stylesheet">
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
</html>'''
