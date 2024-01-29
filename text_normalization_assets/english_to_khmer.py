import pandas as pd
import os
def english_to_khmer(text):
    text = str(text)
    result = ''
    for letter in text:
        result += engtokh(letter)

    return result

def engtokh(char):
    eng_khmer_dict = pd.read_csv(os.path.join(os.path.dirname(__file__), 'english_to_khmer.csv'), encoding='utf-8')
    capital = eng_khmer_dict['capital']
    small = eng_khmer_dict['small']
    result = ''
    for i in char:
        if i in capital.values:
            result += eng_khmer_dict['khmer'][capital[capital == i].index[0]]
        elif i in small.values:
            result += eng_khmer_dict['khmer'][small[small == i].index[0]]
        else:
            result = ''
        
    return result
   