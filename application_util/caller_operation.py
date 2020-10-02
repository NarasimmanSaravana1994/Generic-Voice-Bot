from database_util import application_db


def insert_new_caller_data(transcation_id, caller_data):
    """ This method is user to insert the new caller data from database """
    application_db.insert_new_caller_data(transcation_id, caller_data)
    return True


def get_caller_data(transcation_id):
    """ This method is user get the caller data from databases based on transaction id """
    return application_db.get_current_caller_data(transcation_id)["caller_data"]
