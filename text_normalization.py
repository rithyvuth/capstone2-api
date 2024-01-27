import json
import re
import unicodedata
import khmernltk

from norm_config import norm_config


def text_normalize(text):

    """Given a text, normalize it by changing to lower case, removing punctuations, removing words that only contain digits and removing extra spaces

    Args:
        text : The string to be normalized

    Returns:
        normalized_text : the string after all normalization  

    """

    # text = khmernltk.word_tokenize(text)

    config = norm_config["*"]

    for field in ["lower_case", "punc_set","del_set", "mapping", "digit_set", "unicode_norm"]:
        if field not in config:
            config[field] = norm_config["*"][field]


    text = unicodedata.normalize(config["unicode_norm"], text)


    # brackets
    # always text inside brackets with numbers in them. Usually corresponds to "(Sam 23:17)"
    text = re.sub(r"\([^\)]*\d[^\)]*\)", " ", text)

    # Apply mappings

    for old, new in config["mapping"].items():
        text = re.sub(old, new, text)

    # Replace punctutations with nothings

    punct_pattern = r"[" + config["punc_set"]

    punct_pattern += "]"

    normalized_text = re.sub(punct_pattern, "", text)

    # remove characters in delete list

    delete_patten = r"[" + config["del_set"] + "]"

    normalized_text = re.sub(delete_patten, "", normalized_text)

    

    if config["rm_diacritics"]:
        from unidecode import unidecode
        normalized_text = unidecode(normalized_text)

    # Remove spaces
    normalized_text = re.sub(r"\s+", "", normalized_text).strip()

    return normalized_text

def num_to_text(number):
    """Given a number, convert it to text

    Args:
        number : The number to be converted

    Returns:
        text : the text after conversion  

    """
    return ''