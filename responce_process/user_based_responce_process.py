import os
from application_util import caller_data_parsing, caller_operation, product_operation
from database_util import sql_db_opration_utils
from responce_process import text_response_process
from speech_to_text import speech_text_deepspeech, speech_text_google_api
from configparser import ConfigParser

''' read config file for speech to text api '''
configur = ConfigParser()


def check_repeating_logic(transaction_id, question_no, repeating_counts):
    ''' get the repeating logic based on trasaction id and question no'''
    repeating_count = product_operation.get_repeating_count(
        transaction_id, question_no)

    ''' repeating count exceded the limit checking'''
    if repeating_count["no_of_time_repeating"] <= repeating_counts:
        return True
    else:
        return False


def update_repeating_count(transaction_id, question_no):
    ''' get the repeating logic based on trasaction id and question no'''
    repeating_count = product_operation.get_repeating_count(
        transaction_id, question_no)

    ''' increment the exceded count with actual count '''
    increment_count = repeating_count["no_of_time_repeating"]+1

    return product_operation.update_repeating_count(transaction_id, question_no, increment_count)


def update_history(transaction_id, current_audio_no, user_responce):
    return product_operation.update_voice_bot_history(transaction_id, current_audio_no, user_responce)


def download_recording(filename):
    ''' download the audio file for predicting the text from audio file '''
    try:
        recording_path = "/var/lib/asterisk/sounds/en/custom/"
        filename = filename+"-in"
        save_path = "voicebot/recordings/"
        record_fname = os.path.join(recording_path, filename)
        command = "cp "+record_fname+".wav" + " "+save_path
        os.system(command)

        return save_path+filename+".wav"
    except:
        return ""


def vb_file_return_logic(runned_process):
    empty_string = ""
    temp = []
    final_temp = []

    for res_pro in runned_process:
        temp = []
        for val in res_pro:
            temp.append(val["satisfied"])

        final_temp.append(temp)

    for index, val in enumerate(final_temp):
        if len(val) == 1:
            if True in val:
                return runned_process[index][0]['audio_name'], runned_process[index][0]['satisfied'], runned_process[index][0]['is_run_time_dynamic_audio']
        else:
            if False not in val:
                return runned_process[index][0]['audio_name'], runned_process[index][0]['satisfied'], runned_process[index][0]['is_run_time_dynamic_audio']

    return "", False, False


def vb_responce_process(input_text, values):
    runned_process = []
    normalized_responces = []
    for value in values:
        normalized_responces = []
        responce_categorys = value["responce_category"]
        for responce_category in responce_categorys:
            normalized_responce = {}
            normalized_responce["mode"] = responce_category
            res, is_satisfide = text_response_process.generic_process_identification(
                responce_category, input_text)
            normalized_responce["responce"] = res
            normalized_responce["satisfied"] = is_satisfide
            normalized_responce["is_run_time_dynamic_audio"] = value["is_run_time_dynamic_audio"]
            normalized_responce["audio_name"] = value["next_question_no"]

            normalized_responces.append(normalized_responce)

        runned_process.append(normalized_responces)

    return vb_file_return_logic(runned_process)


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


def iv_vb_file_return(current_flow, transaction_id, dtmf, product, language, accno, emi_amount,  application_id, dealer_name, loan_amount, tenure, emi_start_month, user_responce=''):
    try:
        if current_flow["vb_reply_expecting"]:
            vb_reply = current_flow["vb_reply"]
            for reply_vb in vb_reply:
                if reply_vb["language"] == language:
                    file_name, is_satisfide, is_run_time_dynamic_audio = vb_responce_process(
                        user_responce, reply_vb["values"])

                    if is_run_time_dynamic_audio:
                        if current_flow["is_flow_end"]:
                            if os.path.exists(os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/" + "end"+"_"+str(transaction_id)+"_"+product+"_"+current_flow["flow_type"] + "_" + str(current_flow["audio_number"]) + "_" + "run_time_dynamic_audios" + "_" + str(file_name) + '.wav'):
                                return wav_fname
                            else:
                                return "end"
                        else:
                            wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/" + str(transaction_id)+"_"+product+"_"+current_flow["flow_type"] + "_" + str(
                                current_flow["audio_number"]) + "_" + "run_time_dynamic_audios" + "_" + str(file_name) + '.wav'

                            if os.path.exists(wav_fname):
                                return wav_fname
                            else:
                                return "end"
                    else:
                        if current_flow["is_flow_end"]:
                            wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/" + \
                                "end"+"_"+str(transaction_id)+"_"+product+"_"+current_flow["flow_type"] + \
                                "_" + str(current_flow["audio_number"]) + \
                                "_"+str(extra_audio).strip()+"_" + \
                                str(file_name)+'.wav'

                            if os.path.exists(wav_fname):
                                return wav_fname
                            else:
                                return "end"
                        else:
                            wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/" + str(transaction_id)+"_"+product+"_" + \
                                current_flow["flow_type"] + "_" + str(current_flow["audio_number"]) + "_"+(
                                    extra_audio).strip()+"_" + str(file_name)+'.wav'

                            if os.path.exists(wav_fname):
                                return wav_fname
                            else:
                                return "end"
                else:
                    pass

        elif current_flow["ivr_reply_expecting"]:
            vb_reply = current_flow["ivr_reply"]
            for reply_vb in vb_reply:
                if reply_vb["language"] == language:
                    values = reply_vb["values"]
                    for value in values:
                        if str(dtmf) in value["responce_category"]:
                            if current_flow["is_flow_end"]:
                                wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/" + "end"+"_"+str(transaction_id)+"_"+product+"_" + \
                                    current_flow["flow_type"] + "_" + str(current_flow["audio_number"]) + "_"+(
                                        extra_audio).strip()+"_" + str(value["next_question_no"])+'.wav'

                                if os.path.exists(wav_fname):
                                    return wav_fname
                                else:
                                    return "end"
                            else:
                                wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/" + str(transaction_id)+"_"+product+"_" + \
                                    current_flow["flow_type"] + "_" + str(current_flow["audio_number"]) + "_"+(
                                        extra_audio).strip()+"_" + str(value["next_question_no"])+'.wav'

                                if os.path.exists(wav_fname):
                                    return wav_fname
                                else:
                                    return "end"
                else:
                    pass
    except Exception as ex:
        print(ex)


def generic_audio_generation(current_flow, transaction_id, dtmf, product, language, accno, emi_amount,  application_id, dealer_name, loan_amount, tenure, emi_start_month, user_responce=''):
    ''' generate final custome audio to play '''

    empty_string = ""
    extra_audio = ""
    wav_fname = ""

    if current_flow["is_customazied"]:

        if current_flow["is_flow_end"]:

            wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/" + \
                "end"+"_"+str(transaction_id)+"_"+product+"_"+current_flow["flow_type"] + \
                "_" + str(current_flow["audio_number"]) + \
                "_"+(extra_audio).strip()+"_" + \
                str(current_flow["is_ivr_next_question_no"])+'.wav'

            return wav_fname
        else:
            wav_fname = os.getcwd()+'/temp_files/temp_audio_files/' + str(transaction_id)+"/"+str(transaction_id)+"_"+product+"_"+current_flow["flow_type"] + \
                "_" + str(current_flow["audio_number"]) + \
                "_"+(extra_audio).strip() + "_" + \
                str(current_flow["is_ivr_next_question_no"])+'.wav'

            return wav_fname

    else:
        return iv_vb_file_return(current_flow, transaction_id, dtmf, product, language, accno, emi_amount,  application_id, dealer_name, loan_amount, tenure, emi_start_month, user_responce='')


def audio_generation(current_flow, transaction_id, dtmf, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name, emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name, recorded_file_name):

    response = ''

    ''' if voicebot responce is expected means it will send the audio for STT conversion '''
    if current_flow["vb_reply_expecting"]:
        ''' downloading the audio file from astrick server '''
        recorded_file_name = download_recording(recorded_file_name)

        configur.read(os.getcwd() + '/config/app_config.ini')

        ''' to convert speech to text based on configuartion '''
        if configur.get('speech_api', 'speech_api') == "google":
            # to do for google api
            response = 'yes'
        else:
            ''' send the recording file for STT conversion '''
            response = speech_text_deepspeech.deepspeech_speech_to_text(
                recorded_file_name, language)

    ''' normalize the responce and return the next audio file for the flow'''
    recorded_file_name = generic_audio_generation(current_flow,
                                                  transaction_id, dtmf, product, language, account_no, emi_amount, application_id, dealer_name, loan_amount, tenure, emi_start_month, response)

    ''' update the flow history for internal application maintain '''
    update_history(
        transaction_id, current_flow["audio_number"], response)

    return recorded_file_name, response


def next_flow(transaction_id, dtmf=0, current_recording_no=0, recorded_file_name='', is_ivr=False):

    caller_data = get_caller_data(transaction_id)

    transaction_id, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name, emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name = caller_data_parsing.caller_data_parsing(
        caller_data)

    ''' get the question flow based on the product '''
    current_flow = get_product_based_current_flow(
        product, current_recording_no)

    ''' check the audio repeating logic based on audio no if reating exceded it will end the call or flow ..'''
    is_check_repeating_logic = check_repeating_logic(
        transaction_id, current_recording_no, current_flow["no_of_repeating"])

    if is_check_repeating_logic:
        file_name, response = audio_generation(current_flow, transaction_id, dtmf, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name,
                                               emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name, recorded_file_name)

        ''' update the repeating count based on the user transaction id and question no'''
        update_repeating_count(transaction_id, current_recording_no)

        ''' update the status in sql database '''
        if is_ivr and current_flow["ivr_reply_expecting"]:
            sql_db_opration_utils.commit_ivr_status(
                transaction_id, dtmf, product)
        elif current_flow["vb_reply_expecting"]:
            sql_db_opration_utils.commit_user_response(
                transaction_id, mobile_no, product, current_recording_no, "", response, response)

        return file_name
    else:
        return "end_"+str(transaction_id)
