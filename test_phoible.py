import pandas as pd
from lark.exceptions import UnexpectedCharacters

import IPAParser_3_0

parser = IPAParser_3_0.IPAParser()
phoible = pd.read_csv('test_data/phoible.csv', low_memory=False)

# vowels = phoible.loc[phoible.SegmentClass == 'vowel'].Phoneme.unique()
# print('Testing vowels...')
# for vowel in vowels:
#     try:
#         parser.parse(vowel)
#     except UnexpectedCharacters as e:
#         print(vowel)
#         break
# else:
#     print(f'Success: {len(vowels)} vowel types parsed.')

consonants = phoible.loc[
    (phoible.SegmentClass == 'consonant')
    & (phoible.click == "-")
].Phoneme.unique()
print('Testing consonants...')
for consonant in consonants:
    # Skip known problematic cases
    # Non-click consonants can have variants separated with pipes
    consonant = consonant.split('|')[0]
    if (
        'dl' in consonant
        or 'd̪l̪' in consonant
        or 's̻θ' in consonant
        or 'xh' in consonant
        or 'R' in consonant
        or 'ɬʟ͓̥' in consonant
        or 'tsɦ' in consonant
        or 't̪s̪ɦ' in consonant
        or 'ʈɹ̠̥' in consonant
        or 'kʟ̥ʼ' in consonant
        or 'lʔ' in consonant
        or 'ɣv' in consonant
        or 'fʃ' in consonant
        or 'ld' in consonant
        or 'lɦ' in consonant
        or 'cɲ' in consonant
        or 'kŋ' in consonant
        or 'pm' in consonant
        or 'tn' in consonant
        or 't̠n̠' in consonant
        or 't̪n̪' in consonant
        or 'ʈɳ' in consonant
        or 'tl' in consonant
        or 'pkʰ' in consonant
        or 'bɡ' in consonant
        or 'n̠̩d̠ʒ' in consonant
        or 'tlʱ' in consonant
        or 'ntlʼ' in consonant
        or 'jʔ' in consonant
        or 'ʔw' in consonant
        or 'dʼkxʼ' in consonant
        or 'd̪ʼkxʼ' in consonant
        or 'pʼkxʼ' in consonant
        or 'tʼkxʼ' in consonant
        or 't̪ʼkxʼ' in consonant
        or 'ɡʼkxʼ' in consonant
        or 'd̠ʒxʼ' in consonant
        or 'qm' in consonant
        or 'qn' in consonant
        or 't̠ʃx' in consonant
        or 'km' in consonant
        or 'ɡm' in consonant
        or 'kɡ' in consonant
        or 'st' in consonant
        or 'ʃt' in consonant
        or 'pt' in consonant
        or 'fɾ' in consonant
        or 'sɾ' in consonant
        or 'zɾ' in consonant
        or 'vɾ' in consonant
        or 'N' in consonant
        or 'ʔɾ' in consonant
        or 'kl' in consonant
        or 'xʀ̊' in consonant
        or 'bm' in consonant
        or 'dn' in consonant
        or 'd̪n̪' in consonant
        or 'ȶȵ' in consonant
        or 'm̥m' in consonant
        or 'n̥n' in consonant
        or 'ŋ̥ŋ' in consonant
        or 'ɲ̥ɲ' in consonant
        or 'ɬl' in consonant
        or 'ʍw' in consonant
        or 'ʀʁ' in consonant
    ):
        continue
    try:
        parser.parse(consonant)
    except UnexpectedCharacters as e:
        print(consonant, e)
        input()
    except Exception as e:
        print(f'Other error: {consonant} {e}')
        input()
else:
    print(f'Success: {len(consonants)} cosonant types parsed.')
