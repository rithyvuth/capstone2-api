import json
import re
import string
import khmernltk

from text_normalization_assets.number_to_khmer_text import number_to_khmer_text, kh_num_to_num, number_with_dot_to_khmer_text, convert_num_format
from text_normalization_assets.english_to_khmer import english_to_khmer


def text_normalize(text):

    """Given a text, normalize it by changing to lower case, removing punctuations, removing words that only contain digits and removing extra spaces

    Args:
        text : The string to be normalized

    Returns:
        normalized_text : the string after all normalization  

    """
    khmer_unicode = r'\u1780-\u17F9'
    khmer_use_text_unicode = r'\u1780-\u17d3\u17dd'
    khmer_num_unicode = r'\u17E0-\u17E9'


    # text = khmernltk.word_tokenize(text)
    #handle number
    text = str(text)
    text = re.sub(r'[' + khmer_num_unicode + ']+', lambda x: kh_num_to_num(x.group()), text)

    text = re.sub(r'\d+\.\d+', lambda x: number_with_dot_to_khmer_text(x.group()), text)

    text = re.sub(r'\d{1,3}(?:,\s?\d{3}?){0,}', lambda x: convert_num_format(x.group()), text)
    text = re.sub(r'\d{1,3}(?:\s\d{3}?){0,}', lambda x: convert_num_format(x.group()), text)
    
    text = re.sub(r'\d+', lambda x: number_to_khmer_text(x.group()), text)

    text = re.sub(r'%', 'ភាគរយ', text)
    text = re.sub(r'\u17db', 'រៀល', text)
    text = re.sub(r'\$', 'ដុល្លា', text)

    #remove links
    text = re.sub(r'http\S+', '', text)

    #remove email
    text = re.sub(r'\S+@[a-zA-Z]+(?:\.[a-zA-Z]+)+', '', text)

    #handle english
    text = re.sub(r'[A-Za-z]{5,}', '', text)
    text = re.sub(r'[A-Za-z]{1,5}', lambda x: english_to_khmer(x.group()), text)

    #remove emoji
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    #handle punctuations
    punct = string.punctuation
    text = re.sub(r'['+punct+']', '', text)

    #remove extra spaces
    text = re.sub(r'\s+', '', text)

    #handdle ៗ
    text = khmernltk.word_tokenize(text)
    tmp_words = text
    i = 0
    for word in tmp_words:
        if word == 'ៗ' and i > 0:
            text[i] = text[i-1]
        i += 1
    text = ''.join(text)

    #remove anything that not in khmer_use_text_unicode
    text = re.sub(r'[^'+khmer_use_text_unicode+']', '', text)

    return text
