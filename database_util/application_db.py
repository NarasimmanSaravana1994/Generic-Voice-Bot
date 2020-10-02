from pymongo import MongoClient
from bson.json_util import dumps
import json

##### database connection #####

client = MongoClient('localhost', 27017)
db = client.voicebot_

channel_status = db.get_collection('channel_status')
current_caller_datas = db.get_collection('current_caller_datas')
responce_preprocessing = db.get_collection('responce_preprocessing')
voicebot_user_history = db.get_collection('voicebot_user_history')
repeating_logic = db.get_collection('repeating_logic')

# available_products = db.get_collection('products_customized audios')
# product_context = db.get_collection('product_context')
# product_type = db.get_collection('product_type')
# product_xml_flow = db.get_collection('product_xml_flow')
# audio_sequence_mode_choosing = db.get_collection(
#     'audio_sequence_mode_choosing')


product_config = db.get_collection('product_flow')


def update_voice_bot_history(transaction_id, current_audio_no, user_responce):
    """ update the user transaction history in mongo """
    try:
        voicebot_user_history.insert_one(
            {"transaction_id": str(transaction_id), "current_audio_no": current_audio_no, "user_responce": user_responce})
        return True
    except Exception as ex:
        raise Exception("")


def get_product_config(product_name):
    """ get the product flow """
    try:
        product = product_config.find_one({"product_name": product_name})

        product = json.loads(dumps(product))
        del product["_id"]
        return product
    except Exception as ex:
        raise Exception("")


def get_repeating_count(transaction_id, question_no):
    try:
        repeat = repeating_logic.find_one(
            {"transaction_id": transaction_id, "question_no": question_no})

        repeat_ = json.loads(dumps(repeat))
        del repeat_["_id"]
        return repeat_
    except Exception as ex:
        repeat_ = {}
        repeat_["transaction_id"] = transaction_id
        repeat_["question_no"] = question_no
        repeat_["no_of_time_repeating"] = 0
        repeating_logic.insert_one(repeat_)
        return repeat_


def update_repeating_count(transaction_id, question_no, repeating_count):

    repeating_logic.update_one(
        {
            "transaction_id": transaction_id,
            "question_no": question_no
        },
        {
            "$set": {
                "no_of_time_repeating": repeating_count
            }
        }
    )

    return True


def remove_completed_caller_data_beased_on_transaction_id(transaction_id):
    current_caller_datas.remove({"transction_id": transaction_id})
    return True


def remove_repeating_logic_based_on_transaction_id(transaction_id):
    repeating_logic.remove({"transaction_id": transaction_id})
    return True


#####################################################################################################################################
####### database connection #####
""" get the available channel details """


def get_available_channels():
    try:
        available_channels = {}

        channels = channel_status.find_one({})
        channels = json.loads(dumps(channels))

        available_channels["available_channel"] = channels["available_channel"]
        available_channels["running_channel"] = channels["running_channel"]
        available_channels["total_channel"] = channels["total_channel"]
        available_channels["key"] = channels["key"]
        available_channels["prefix"] = channels["prefix"]
        available_channels["running_products"] = channels["running_products"]
        available_channels["total_products"] = channels["total_products"]

        return available_channels
    except Exception as ex:
        raise Exception(
            "Unable to get the channel details .. please check eject error {}".format(str(ex)))


""" update the available channel details """


def update_channel_details(available_channel, running_channel):
    try:
        ## To do ##

        channel_status.update_one(
            {
                "total_channel": 30
            },
            {
                "$set": {
                    "available_channel": available_channel,
                    "running_channel": running_channel
                }
            }
        )
        return True
    except Exception as ex:
        raise Exception(
            "Unable to update the channel details .. please check eject error {}".format(str(ex)))


""" get product details """


def get_product_details_from_db():
    try:
        total_products = []
        products = available_products.find({})
        products = json.loads(dumps(products))
        for index, value in enumerate(products):
            del value["_id"]
            total_products.append(value)
        return total_products
    except Exception as ex:
        raise Exception(
            "Unable to get the product details from db .. please check eject error {}".format(str(ex)))


""" get product context """


def get_product_context_from_db():
    try:
        context = product_context.find({})
        context = json.loads(dumps(context))[0]
        del context["_id"]
        return context
    except Exception as ex:
        raise Exception(
            "Unable to get the product context from db .. please check eject error {}".format(str(ex)))


""" insert new caller data while call initialization """


def insert_new_caller_data(transction_id, caller_data):
    try:
        caller_data_is_exist = current_caller_datas.find(
            {"transction_id": transction_id}).count()

        if caller_data_is_exist == 0:
            current_caller_datas.insert_one(
                {"transction_id": str(transction_id), "caller_data": caller_data})
            return True
        else:
            return False
    except Exception as ex:
        raise Exception(
            " Unable to insert the new caller data.. plase check the eject error {}".format(str(ex)))


""" get current caller data in call from database """


def get_current_caller_data(transction_id):
    try:
        caller_data_is_exist = current_caller_datas.find(
            {"transction_id": transction_id}).count()

        if caller_data_is_exist == 1:
            caller_data = current_caller_datas.find(
                {"transction_id": transction_id})
            caller_data = json.loads(dumps(caller_data))[0]
            del caller_data["_id"]
            return caller_data
        else:
            raise Exception(
                " No caller data available in database against the mentioned trasaction id {}".format(transction_id))
    except Exception as ex:
        raise Exception(
            "Unable to get the current caller from db .. please check eject error {}".format(str(ex)))


""" update current caller data in call from databse """


def update_current_caller_data(transction_id, caller_data):
    try:
        caller_data_is_exist = current_caller_datas.find(
            {"transction_id": transction_id}).count()

        if caller_data_is_exist == 1:
            session.update_one(
                {
                    "transction_id": str(transction_id)},
                {
                    "$push": {
                        "caller_data": caller_data
                    }
                }
            )
            return True
        else:
            raise Exception(
                " No caller data available in database against the mentioned trasaction id {}".format(transction_id))
    except Exception as ex:
        raise Exception(
            "Unable to update the current caller data from db .. please check eject error {}".format(str(ex)))


""" get product type"""


def get_product_type():
    try:
        product_types = product_type.find()
        product_types = json.loads(dumps(product_types))[0]
        del product_types["_id"]
        return product_types
    except Exception as ex:
        raise Exception(
            " Unable to get product type in from db.. please check eject error {}".format(str(ex)))


""" get product_xml_flow """


def get_product_xml_flow(product_name):
    try:
        _product_xml_flow = product_xml_flow.find(
            {"product_name": product_name})

        _product_xml_flow = json.loads(dumps(_product_xml_flow))[0]

        del _product_xml_flow["_id"]
        return _product_xml_flow

    except Exception as ex:
        raise Exception(
            " Unable to get the product xml flow from db.. please check eject error {}".format(str(ex)))


""" get product responce """


def get_product_responce():
    try:
        all_responces = []
        product_responces = responce_preprocessing.find()

        product_responces = json.loads(dumps(product_responces))

        for index, product_responce in enumerate(product_responces):
            responce = {}
            del product_responce["_id"]
            responce["responce_category"] = product_responce["responce_category"]
            responce["keyword_list"] = product_responce["keyword_list"]
            responce["keyword_lists"] = product_responce["keyword_lists"]
            # responce["responce"] = product_responce["responce"]
            all_responces.append(responce)

        return all_responces

    except Exception as ex:
        raise Exception(
            " Unable to get the product xml flow from db.. please check eject error {}".format(str(ex)))


def get_audio_sequence_mode_choosing(product_name):
    try:

        _audio_sequence_mode_choosing = audio_sequence_mode_choosing.find(
            {"product_name": product_name})

        _audio_sequence_mode_choosing = json.loads(dumps(_product_xml_flow))[0]

        del _audio_sequence_mode_choosing["_id"]
        return _audio_sequence_mode_choosing

    except Exception as ex:
        raise Exception(
            " Unable to get the product audio sequence mode selection from db.. please check eject error {}".format(str(ex)))


# def insert_collection(session_id):
#     try:
#         session.insert_one({"session_id": str(session_id),
#                             "status": "True", "chat_flow": []})
#         return True
#     except Exception as ex:
#         print("Error : ", ex)
#         return False


# def is_sessionid_exists(session_id):
#     try:
#         count = session.find({"session_id": session_id}).count()
#         if count == 1:
#             return True
#         else:
#             return False
#     except Exception as ex:
#         print("Error : ", ex)
#         return False


# def get_value_with_session_id(session_id):
#     try:
#         value = session.find_one({"session_id": session_id}, {"_id": 0})
#         value = json.loads(dumps(value))
#         return value
#     except Exception as ex:
#         print("Error : ", ex)
#         return {}

# def chat_flow_session_update(session_id, chat_flow):
#     try:

#         # is_exit = session.find({"$and": [{"session_id": session_id}, {
#         #                        "chat_flow.question_id": chat_flow['question_id']}]}).count()

#         # if is_exit == 1:
#         #     session.update({"$and": [{"session_id": session_id}, {"chat_flow.question_id": chat_flow['question_id']}]}, {
#         #                    "$set": {"chat_flow.$.answer": chat_flow['answer']}})
#         # else:
#         session.update_one(
#             {
#                 "session_id": str(session_id)},
#             {
#                 "$push": {
#                     "chat_flow": chat_flow
#                 }
#             }
#         )

#     except Exception as ex:
#         print("Error : ", ex)
#         return False


# def get_question_chat(company_id, domain_id):
#     chat_flow = question_flow.find_one(
#         {"company_id": company_id, "domain_id": domain_id})
#     chat_flow = json.loads(dumps(chat_flow))
#     return chat_flow
