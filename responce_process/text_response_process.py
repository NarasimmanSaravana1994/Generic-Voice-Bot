import re
import itertools
import datetime
import datefinder
from dateutil import parser
from application_util import product_operation


def responce_words(responce_category, is_multiple=False):
    """ This method is used to get the all responce words based in responce category """
    responces = product_operation.get_responce()

    for index, responce in enumerate(responces):
        if responce_category == responce["responce_category"]:
            return responce
        else:
            pass

    return {}


def word_tokenization(input_text):
    ''' This method is used word preprocessing and tokenizing the word '''
    input_text = input_text.replace("\n", "")
    input_text = re.sub('[^a-zA-Z0-9  ]', "", input_text)
    input_text = input_text.strip().lower()

    text_tokenization = input_text.split()

    return [" ".join(
        text_tokenization[i:j]) for i, j in itertools.combinations(range(len(text_tokenization)+1), 2)]


def responce_mapping(responce, mapped_database_responces):
    """ This method is used to map the appropriate responce based on user responce """

    if len(mapped_database_responces["keyword_lists"]) > 0:
        responce_lists = mapped_responce["keyword_lists"]
        for responce_list in responce_lists:
            if responce in responce_list["sub_category_keyword_lists"]:
                return responce, True
            else:
                pass
    else:
        if responce in mapped_database_responces["keyword_list"]:
            return responce, True

    return "", False


def check_unclear_responce(responce, initial_check=False):
    ''' This method is used to check the unclear responce '''

    if initial_check:
        if not responce or responce == "":
            return "unclear", True
        else:
            return responce, False
    else:
        if not responce or responce == "":
            return "unclear"
        else:
            return responce


def generic_process_identification(mode, input_text):
    try:
        ''' This method is used consolidate the overall text processing '''
        mapped_database_responces = responce_words(str(mode))

        word_combinations = word_tokenization(input_text)

        for word_combination in word_combinations:
            responce, is_responce_exist = responce_mapping(
                word_combination, mapped_database_responces)
            if is_responce_exist:
                return check_unclear_responce(responce), True
            else:
                return check_unclear_responce(responce), False
    except:
        return "", False
