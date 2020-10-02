from database_util import application_db


def insert_new_caller_data(transcation_id, caller_data):
    """ This method is user to insert the new caller data from database"""
    application_db.insert_new_caller_data(transcation_id, caller_data)
    return True


def get_product_config(productname):
    """This method is used to get product config info from mongodb"""

    return application_db.get_product_config(productname)


def update_voice_bot_history(transaction_id, current_audio_no, user_responce):
    return application_db.update_voice_bot_history(transaction_id, current_audio_no, user_responce)


def get_repeating_count(transaction_id, question_no):
    return application_db.get_repeating_count(transaction_id, question_no)


def update_repeating_count(transaction_id, question_no, repeating_count):
    return application_db.update_repeating_count(transaction_id, question_no, repeating_count)
##################################################################################################################


def get_product_type():
    """" This method is get the product type from mongodb """
    return application_db.get_product_type()


def get_responce():
    """ This method is used to get the responce normalization """
    return application_db.get_product_responce()


def get_audio_sequence_mode_choosing(product_name):
    """ This method is used to get the audio payment sequence mode """
    return application_db
