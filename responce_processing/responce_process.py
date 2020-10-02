import os
from application_util import caller_data_parsing, caller_operation, product_operation
from responce_process import response_processing_
from speech_to_text import speech_text_deepspeech, speech_text_google_api
from configparser import ConfigParser

''' read config file for speech to text api '''
configur = ConfigParser()


def download_recording(filename):
    ''' download the audio file for predicting the text from audio file '''

    recording_path = "/var/lib/asterisk/sounds/en/custom/"
    filename = filename+"-in"
    save_path = "voicebot/recordings/"
    record_fname = os.path.join(recording_path, filename)
    command = "cp "+record_fname+".wav" + " "+save_path
    os.system(command)

    return save_path+filename+".wav"


def vb_file_return_logic(runned_process):
    empty_string = ""
    for index, value in enumerate(runned_process):
        temp_responce = []
        for val in value:
            if val["satisfied"] == False:
                break

            temp_responce.append(val["satisfied"])

        if False in temp_responce:
            pass
        else:
            if len(temp_responce) > 1:
                return val["audio_name"]


def vb_responce_process(input_text, values):
    runned_process = []
    normalized_responces = []
    for value in values:
        normalized_responces = []
        responce_categorys = value["responce_category"]
        for responce_category in responce_categorys:
            normalized_responce = {}
            normalized_responce["mode"] = responce_category
            res, is_satisfide = response_processing_.generic_audio_generation(responce_category,
                                                                              input_text)
            normalized_responce["responce"] = res
            normalized_responce["satisfied"] = is_satisfide
            normalized_responce["audio_name"] = value["audio_name"]
            normalized_responce["mode_length"] = len(
                value["responce_category"])

            normalized_responces.append(normalized_responce)

        runned_process.append(normalized_responces)

    return vb_file_return_logic(runned_process, values)


def get_caller_data(transaction_id):
    ''' get current caller data '''

    return caller_operation.get_caller_data(transaction_id)


def get_product_based_current_flow(product, current_recording_no):
    ''' get product flow based on product name '''
    product_configuration = product_operation.get_product_config(product)

    ''' if product is active status means it will initiate the call '''
    if product_configuration["status"] == 1:

        for config in product_configuration["question_flow"]:
            if current_recording_no == config["audio_number"]:
                return config

    return None


def generic_audio_generation(current_flow, trans_id, dtmf, language, accno, emi_amount,  application_id, dealer_name, loan_amount, tenure, emi_start_month, user_responce=''):
    ''' generate final custome audio to play '''

    empty_string = ""

    if current_flow["is_customazied"]:

        if current_flow["is_flow_end"]:
            wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + \
                "end"+"_"+str(trans_id)+"_"+current_flow["flow_type"] + \
                "_"+str(current_flow["audio_number"])+'.wav'
            return wav_fname
        else:
            wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + \
                str(trans_id)+"_"+current_flow["flow_type"] + \
                "_"+str(current_flow["audio_number"])+"_"+'.wav'

            return wav_fname

    else:
        if current_flow["vb_reply_expecting"]:
            vb_reply = current_flow["vb_reply"]
            for reply_vb in vb_reply:
                if reply_vb["language"] == language:
                    values = reply_vb["values"]
                    return vb_responce_process(user_responce, values)

        elif current_flow["ivr_reply_expecting"]:
            vb_reply = current_flow["ivr_reply"]
            for reply_vb in vb_reply:
                if reply_vb["language"] == language:
                    values = reply_vb["values"]
                    for value in values:
                        if str(dtmf) in value["responce_category"]:
                            return str(trans_id)+"_"+str(current_flow["flow_type"])+"_"+str(current_flow["audio_number"])+'.wav'
                        else:
                            pass


def audio_generation_(current_flow, transaction_id, dtmf, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name, emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name, recorded_file_name):

    response = ''

    if current_flow["vb_reply_expecting"]:
        ''' downloading the audio file from astrick server '''
        recorded_file_name = download_recording(recorded_file_name)

        configur.read(os.getcwd() + '/config/app_config.ini')

        ''' to convert speech to text based on configuartion '''
        if configur.get('speech_api', 'speech_api') == "google":
            # to do for google api
            pass
        else:
            response = speech_text_deepspeech.deepspeech_speech_to_text(
                recorded_file_name, language)

    return generic_audio_generation(current_flow,
                                    transaction_id, dtmf, language, account_no, emi_amount, application_id, dealer_name, loan_amount, tenure, emi_start_month, response)


def next_flow(transaction_id, dtmf=0, current_recording_no=0, recorded_file_name=''):

    caller_data = get_caller_data(transaction_id)

    transaction_id, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name, emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name = caller_data_parsing.caller_data_parsing(
        caller_data)

    current_flow = get_product_based_current_flow(
        'icic', current_recording_no)

    return audio_generation_(current_flow, transaction_id, dtmf, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name, emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name, recorded_file_name)
