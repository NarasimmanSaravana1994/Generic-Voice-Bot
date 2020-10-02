import os
from pydub import AudioSegment


def number_to_audio(input_number, language, product="hfcl"):
    ''' convert number to its corresponding sound'''
    wav_list = []
    wav_list1 = []
    number_creation_status = 1

    if language in ["english", "hindi"]:
        if product == "hfcl":
            number_wav_path = os.getcwd() + '/audio_files/common_audios/' + \
                language+"_numbers_ashmini/"
        elif "kotaklas" in product or "icicidel" in product or "divya" in product or "bajajwheeler" in product:
            number_wav_path = os.getcwd() + '/audio_files/common_audios/' + \
                language+"_numbers_divya/"
        elif product == "lalitha":
            number_wav_path = os.getcwd() + '/audio_files/common_audios/' + \
                language+"_numbers_lalitha/"
        elif product == "ajitha":
            number_wav_path = os.getcwd() + '/audio_files/common_audios/' + \
                language+"_numbers_ajitha/"
        elif product == "padma":
            number_wav_path = os.getcwd() + '/audio_files/common_audios/' + \
                language+"_numbers_padma/"
        else:
            number_wav_path = os.getcwd() + '/audio_files/common_audios/' + \
                language+"_numbers_ashmini/"
    else:
        if product == "hfcl":
            number_wav_path = os.getcwd() + '/audio_files/HeroFincorp/hero_recordings_' + \
                language+'/numbers/'
        else:
            number_wav_path = os.getcwd() + "/audio_files/products/" + \
                product+"/"+language+"_numbers/"

    input_number_str = str(input_number)
    input_number = int(input_number)

    if len(input_number_str) == 9:
        crore = str(input_number//10000000)
        if input_number % 1000000 == 0:
            wav_list1 = [number_wav_path+crore +
                         ".wav", number_wav_path+"10000000.wav"]
            input_number_str = ""
        else:
            wav_list1 = [number_wav_path+crore +
                         ".wav", number_wav_path+"10000000.wav"]
            input_number_str = str(input_number % 10000000)
            input_number = int(input_number_str)

    if len(input_number_str) == 8:
        crore = str(input_number//10000000)
        if input_number % 1000000 == 0:
            wav_list1.extend([number_wav_path+crore+".wav",
                              number_wav_path+"10000000.wav"])
            input_number_str = ""
        else:
            wav_list1 .extend([number_wav_path+crore+".wav",
                               number_wav_path+"10000000.wav"])
            input_number_str = str(input_number % 10000000)
            input_number = int(input_number_str)

    if len(input_number_str) == 7:
        lakh = str(input_number//100000)
        if input_number % 100000 == 0:
            wav_list1 .extend([number_wav_path+lakh+".wav",
                               number_wav_path+"100000.wav"])
            input_number_str = ""
        else:
            wav_list1 .extend([number_wav_path+lakh+".wav",
                               number_wav_path+"100000.wav"])
            input_number_str = str(input_number % 100000)
            input_number = int(input_number_str)

    if len(input_number_str) == 6:
        lakh = str(input_number//100000)
        if input_number % 100000 == 0:
            wav_list1 .extend([number_wav_path+lakh+".wav",
                               number_wav_path+"100000.wav"])
            input_number_str = ""
        else:
            wav_list1.extend([number_wav_path+lakh+".wav",
                              number_wav_path+"100000.wav"])
            input_number_str = str(input_number % 100000)
            input_number = int(input_number_str)

    if len(input_number_str) == 5:
        thous = str((input_number//1000))
        hun = str(((input_number % 1000)//100)*100)
        hundred_position = str((input_number % 1000)//100)
        ten = str(input_number % 100)
        if int(ten) != 0:
            if int(hundred_position) != 0:
                wav_list = [number_wav_path+thous+".wav", number_wav_path +
                            "1000.wav", number_wav_path+hun+".wav", number_wav_path+ten+".wav"]
            else:
                wav_list = [number_wav_path+thous+".wav", number_wav_path +
                            "1000.wav", number_wav_path+str(int(ten))+".wav"]
        else:
            if int(hundred_position) != 0:
                wav_list = [number_wav_path+thous+".wav",
                            number_wav_path+"1000.wav", number_wav_path+hun+".wav"]
            else:
                wav_list = [number_wav_path+thous +
                            ".wav", number_wav_path+"1000.wav"]

    elif len(input_number_str) == 4:
        thous = str((input_number//1000)*1000)
        hundred_position = str((input_number % 1000)//100)
        hun = str(((input_number % 1000)//100)*100)
        ten = str(input_number % 100)
        if int(thous) == 1000:
            if language in ["hindi", "english"]:
                thous = "1_1000"
            else:
                thos = "1000"
        if int(ten) != 0:
            if int(hundred_position) != 0:
                wav_list = [number_wav_path+thous+".wav",
                            number_wav_path+hun+".wav", number_wav_path+ten+".wav"]
            else:
                wav_list = [number_wav_path+thous+".wav",
                            number_wav_path+str(int(ten))+".wav"]
        else:
            if int(hundred_position) != 0:
                wav_list = [number_wav_path+thous +
                            ".wav", number_wav_path+hun+".wav"]
            else:

                wav_list = [number_wav_path+thous+".wav"]

    elif len(input_number_str) == 3:
        hun = str((input_number//100)*100)
        ten = str(input_number % 100)
        if int(ten) != 0:
            wav_list = [number_wav_path+hun+".wav", number_wav_path+ten+".wav"]
        else:
            wav_list = [number_wav_path+hun+".wav"]
    elif len(input_number_str) == 2:
        wav_list = [number_wav_path+input_number_str+".wav"]
    elif len(input_number_str) == 1:
        wav_list = [number_wav_path+input_number_str+".wav"]

    wav_list1.extend(wav_list)

    soundc = AudioSegment.from_wav(wav_list1[0])

    for i in wav_list1[1:]:
        soundc += AudioSegment.from_wav(i)
    return soundc, number_creation_status


def number_to_audio_malayalam(input_number, language, product=""):
    ''' convert number to its corresponding sound'''
    wav_list = []
    wav_list1 = []
    number_creation_status = 1

    if language == "tamil":
        if "bajajnach" in product or "bajajemi" in product or "lalitha" in product:
            number_wav_path = os.getcwd() + '/common_audios/'+language+"_numbers_lalitha/"

        else:
            number_wav_path = os.getcwd() + '/common_audios/'+language+"_numbers/"
    else:
        number_wav_path = os.getcwd() + '/HeroFincorp/hero_recordings_' + \
            language+'/numbers/'
    input_number_str = str(input_number)
    input_number = int(input_number)

    if len(input_number_str) == 7:

        lakh = str(input_number//100000)
        if input_number % 100000 == 0:
            wav_list1 = [number_wav_path+lakh +
                         ".wav", number_wav_path+"100000.wav"]
            # return number_creation_status
        else:
            wav_list1 = [number_wav_path+lakh+".wav",
                         number_wav_path+"100000_thi.wav"]
            input_number_str = str(input_number % 100000)
            input_number = int(input_number_str)
    if len(input_number_str) == 6:
        lakh = str(input_number//100000)
        if input_number % 100000 == 0:
            wav_list1 = [number_wav_path+lakh +
                         ".wav", number_wav_path+"100000.wav"]
        else:
            wav_list1 = [number_wav_path+lakh+".wav",
                         number_wav_path+"100000_thi.wav"]
            input_number_str = str(input_number % 100000)
            input_number = int(input_number_str)

    if len(input_number_str) == 5:
        thous = str((input_number//1000))
        hundred_position = str((input_number % 1000)//100)
        hun = str(((input_number % 1000)//100)*100)
        ten = str(input_number % 100)
        if int(ten) != 0:
            if int(hundred_position) != 0:
                wav_list = [number_wav_path+thous+".wav", number_wav_path+"1000_thi.wav",
                            number_wav_path+hun+"_thi.wav", number_wav_path+ten+".wav"]
            else:
                wav_list = [number_wav_path+thous+".wav", number_wav_path +
                            "1000_thi.wav", number_wav_path+ten+".wav"]
        else:
            if int(hundred_position) != 0:
                wav_list = [number_wav_path+thous+".wav", number_wav_path +
                            "1000_thi.wav", number_wav_path+hun+".wav"]
            else:
                wav_list = [number_wav_path+thous +
                            ".wav", number_wav_path+"1000.wav"]

    elif len(input_number_str) == 4:
        thous = str((input_number//1000))
        hundred_position = str((input_number % 1000)//100)
        hun = str(((input_number % 1000)//100)*100)
        ten = str(input_number % 100)

        if int(ten) != 0:
            if int(hun) != 0:
                if int(thous) == 1:
                    wav_list = [number_wav_path+"1000_thi.wav",
                                number_wav_path+hun+"_thi.wav", number_wav_path+ten+".wav"]
                else:
                    wav_list = [number_wav_path+thous+".wav", number_wav_path+"1000_thi.wav",
                                number_wav_path+hun+"_thi.wav", number_wav_path+ten+".wav"]
            else:
                if int(thous) == 1:
                    wav_list = [number_wav_path+"1000_thi.wav",
                                number_wav_path+ten+".wav"]
                else:
                    wav_list = [number_wav_path+thous+".wav", number_wav_path +
                                "1000_thi.wav", number_wav_path+ten+".wav"]
        else:
            if int(hun) != 0:
                if int(thous) == 1:
                    wav_list = [number_wav_path+"1000_thi.wav",
                                number_wav_path+hun+"_thi.wav", number_wav_path+ten+".wav"]
                else:
                    wav_list = [number_wav_path+thous+".wav", number_wav_path +
                                "1000_thi.wav", number_wav_path+hun+".wav"]
            else:
                wav_list = [number_wav_path+thous +
                            ".wav", number_wav_path+"1000.wav"]

    elif len(input_number_str) == 3:
        hun = str((input_number//100)*100)
        tens_position = str((input_number % 100)//10)
        ten = str(input_number % 100)
        if int(ten) != 0:
            if int(tens_position) != 0:
                wav_list = [number_wav_path+hun +
                            "_thi.wav", number_wav_path+ten+".wav"]
            else:
                wav_list = [number_wav_path+hun+"_thi.wav",
                            number_wav_path+str(int(ten))+".wav"]
        else:
            wav_list = [number_wav_path+hun+".wav"]

    elif len(input_number_str) == 2:
        wav_list = [number_wav_path+input_number_str+".wav"]
    elif len(input_number_str) == 1 and input_number_str != "0":
        wav_list = [number_wav_path+input_number_str+".wav"]

    wav_list1.extend(wav_list)

    soundc = AudioSegment.from_wav(wav_list1[0])

    for i in wav_list1[1:]:
        soundc += AudioSegment.from_wav(i)
    return soundc, number_creation_status
