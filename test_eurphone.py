import sqlite3
from lark.exceptions import UnexpectedCharacters
import IPAParser_3_0

parser = IPAParser_3_0.IPAParser()

conn = sqlite3.connect('europhon.sqlite')
cursor = conn.cursor()

print('Testing vowels...')
vowel_type_n = 0
for (vowel,) in cursor.execute(
    '''
    SELECT DISTINCT ipa FROM segments
    WHERE `is_consonant` = 0
    '''
):
    vowel = vowel.replace('(', '').replace(')', '')
    try:
        parser.parse(vowel)
    except UnexpectedCharacters as e:
        print(vowel, e)
        input()
    except Exception as e:
        print(f'Other error: {vowel} {e}')
        input()
    vowel_type_n += 1
else:
    print(f'Success: {vowel_type_n} vowel types parsed.')