import os
from multiprocessing import Process
from pydub import AudioSegment
from application_util import caller_data_parsing, product_operation
from custome_audio_generation import number_audio_creation


def generate_audio(final_sounds_generate,
                   transaction_id,
                   product,
                   audio_number,
                   flow_type,
                   next_question_no,
                   is_flow_end=False,
                   extra_audio=''):

    path = os.getcwd()+'/temp_files/temp_audio_files/'+str(transaction_id)+"/"

    if not os.path.exists(path):
        os.mkdir(path)

    ''' this method is used generate combined audio formation '''
    if is_flow_end:
        wav_fname = os.getcwd()+'/temp_files/temp_audio_files/'+str(transaction_id) + "/" +\
            "end"+"_"+str(transaction_id)+"_"+product+"_"+flow_type + \
            "_" + str(audio_number)+"_"+(extra_audio).strip() + \
            "_"+str(next_question_no)+'.wav'
    else:
        wav_fname = os.getcwd()+'/temp_files/temp_audio_files/'+str(transaction_id) + "/" +\
            str(transaction_id)+"_"+product+"_"+flow_type + \
            "_" + str(audio_number)+"_"+(extra_audio).strip() + \
            "_"+str(next_question_no)+'.wav'

    final_sounds_generate = final_sounds_generate.set_frame_rate(
        8000).set_channels(1)
    final_sounds_generate.export(wav_fname, format="wav")

    return True


def is_customazied(final_sounds_generate, flow, type_two_data_object, language, product, transaction_id):
    ''' this method is used get the custome audio file based on the user sequence wise '''
    final_sounds_list = []

    if flow["is_customazied"]:
        customizeds = flow["customizeds"]
        for customized in customizeds:
            if customized["language"] == language:
                sequences = customized["sequence"]
                for sequence in sequences:
                    if sequence["type"] == 1:
                        final_sounds_list.append(AudioSegment.from_wav(
                            os.getcwd() + "/audio_files/generic_audios/"+product+"/"+language+"/"+sequence["audio"]+".wav"))

                    elif sequence["type"] == 2:
                        final_sounds_list.append(AudioSegment.from_wav(
                            os.getcwd() + "/audio_files/generic_audios/"+product+"/"+language+"/"+type_two_data_object[str(sequence["audio"])]+".wav"))

                    elif sequence["type"] == 3:
                        final_sounds_list.append(number_audio_creation.number_to_audio(
                            type_two_data_object[str(sequence["audio"])], language)[0])

        for index_, _final_sound_ in enumerate(final_sounds_list):
            final_sounds_generate = final_sounds_generate + \
                final_sounds_list[index_]

        generate_audio(final_sounds_generate,
                       transaction_id,
                       product,
                       str(flow["audio_number"]),
                       flow["flow_type"],
                       flow["is_ivr_next_question_no"],
                       flow["is_flow_end"])

        return True
    else:
        return False


def ivr_reply_expecting(final_sounds_generate, flow, type_two_data_object, language, product, transaction_id):
    ''' this method is used to get and generate the audio file for ivr products'''
    if flow["ivr_reply_expecting"]:
        ivr_reply = flow["ivr_reply"]
        for reply_ivr in ivr_reply:
            if language == reply_ivr["language"]:
                values = reply_ivr["values"]

                for value in values:
                    final_sounds_generate = AudioSegment.from_wav(
                        os.getcwd() + "/audio_files/generic_audios/"+product+"/"+language+"/"+value["audio"]+".wav")

                    #generate_audio(final_sounds_generate, transaction_id, product,str(flow["audio_number"]),  value["audio"], flow["flow_type"], value["next_question_no"], flow["is_flow_end"])
                    generate_audio(final_sounds_generate,
                                   transaction_id,
                                   product,
                                   str(flow["audio_number"]),
                                   flow["flow_type"],
                                   value["next_question_no"],
                                   flow["is_flow_end"])

        return True
    else:
        return False


def vb_reply_expecting(final_sounds_generate, flow, type_two_data_object, language, product, transaction_id):
    ''' this method is used to get and generate the audio file for voicebot products'''
    try:
        if flow["vb_reply_expecting"]:
            vb_reply = flow["vb_reply"]
            for reply_vb in vb_reply:
                if language == reply_vb["language"]:
                    values = reply_vb["values"]

                    for value in values:
                        if value["is_run_time_dynamic_audio"]:
                            dynamic_audios = value["run_time_dynamic_audios"]
                            final_sounds_generate = AudioSegment.empty()
                            for dynamci_audio in dynamic_audios:
                                if language == dynamci_audio["language"]:
                                    dynamic_audio_sequences = dynamci_audio["sequence"]
                                    final_sounds_list = []
                                    for dynamic_audio_sequence in dynamic_audio_sequences:
                                        if dynamic_audio_sequence["type"] == 1:
                                            final_sounds_list.append(AudioSegment.from_wav(
                                                os.getcwd() + "/audio_files/generic_audios/"+product+"/"+language+"/"+dynamic_audio_sequence["audio"]+".wav"))

                                        elif dynamic_audio_sequence["type"] == 2:
                                            final_sounds_list.append(AudioSegment.from_wav(
                                                os.getcwd() + "/audio_files/generic_audios/"+product+"/"+language+"/"+type_two_data_object[str(dynamic_audio_sequence["audio"])]+".wav"))

                                        elif dynamic_audio_sequence["type"] == 3:
                                            final_sounds_list.append(number_audio_creation.number_to_audio(
                                                type_two_data_object[str(dynamic_audio_sequence["audio"])], language)[0])

                                    for index_, _final_sound_ in enumerate(final_sounds_list):
                                        final_sounds_generate = final_sounds_generate + \
                                            final_sounds_list[index_]

                                    generate_audio(final_sounds_generate,
                                                   transaction_id,
                                                   product,
                                                   str(flow["audio_number"]),
                                                   flow["flow_type"],
                                                   value["next_question_no"],
                                                   flow["is_flow_end"], "run_time_dynamic_audios")
                        else:
                            final_sounds_generate = AudioSegment.from_wav(
                                os.getcwd() + "/audio_files/generic_audios/"+product+"/"+language+"/"+value["audio"]+".wav")

                            # generate_audio(final_sounds_generate, transaction_id, product,str(flow["audio_number"]),  value["audio"], flow["flow_type"], , flow["is_flow_end"])

                            generate_audio(final_sounds_generate,
                                           transaction_id,
                                           product,
                                           str(flow["audio_number"]),
                                           flow["flow_type"],
                                           value["next_question_no"],
                                           flow["is_flow_end"])
            return True
        else:
            return False
    except Exception as ex:
        print(ex)


def generic_audio_generation(question_flow, transacyion_id, language, caller_data):
    ''' this method is used get the all basic caller data and initiate the custome audio generation based on the product type '''
    transaction_id, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name, emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name = caller_data_parsing.caller_data_parsing(
        caller_data)

    ###########################
    type_two_data_object = {}
    type_two_data_object["transaction_id"] = transaction_id
    type_two_data_object["language"] = language
    type_two_data_object["loan_type"] = loan_type
    type_two_data_object["product_type"] = product_type
    type_two_data_object["product"] = product
    type_two_data_object["mobile_no"] = mobile_no
    type_two_data_object["account_no"] = account_no
    type_two_data_object["due_date"] = due_date
    type_two_data_object["product_name"] = product_name
    type_two_data_object["emi_start_month"] = emi_start_month
    type_two_data_object["loan_amount"] = loan_amount
    type_two_data_object["tenure"] = tenure
    type_two_data_object["bounce_charges"] = bounce_charges
    type_two_data_object["penalty_charges"] = penalty_charges
    type_two_data_object["disbursal_date"] = disbursal_date
    type_two_data_object["application_id"] = application_id
    type_two_data_object["emi_amount"] = emi_amount
    type_two_data_object["dealer_name"] = dealer_name

    ###########################
    ''' create empty file for generate audio '''
    final_sounds_generate = AudioSegment.empty()

    ''' generate the audio files based on the question wise using thread logic '''
    for index, flow in enumerate(question_flow):
        p1 = Process(target=ivr_reply_expecting,
                     args=(final_sounds_generate, flow, type_two_data_object, language, product, transaction_id))
        p1.start()

        p2 = Process(target=is_customazied,
                     args=(final_sounds_generate, flow, type_two_data_object, language, product, transaction_id))
        p2.start()

        p3 = Process(target=vb_reply_expecting,
                     args=(final_sounds_generate, flow, type_two_data_object, language, product, transaction_id))
        p3.start()

        p1.join()
        p2.join()
        p3.join()
        # vb_reply_expecting(final_sounds_generate, flow,
        #                    type_two_data_object, language, product, transaction_id)
    return True
