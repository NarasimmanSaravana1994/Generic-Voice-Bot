from requests import Session
import subprocess


def url(language):
    ''' find the text to speech api url '''
    if language == "tamil":
        url = 'http://10.101.1.245:7070/audio-recognize'
    elif language == "english":
        url = 'http://10.101.1.245:6060/audio-recognize'

    return url


def deepspeech_api(language, audio_file_name):
    ''' deepspeech api '''
    try:
        session.head(url(language))
        response = session.post(
            url=url,
            data={
                'languageCode': language,
                'wavfilename': audio_file_name.split("/")[-1]

            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )

        return response.text
    except Exception as ex:
        raise Exception(
            " Unable predict the text from speech. please find the eject error {}".format(str(ex)))


def responce_preprocessing(responce):
    ''' remove unwanted charected in string '''
    prunned_responce = ""
    for character in responce:
        if character.isalnum():
            prunned_responce += character

    return prunned_responce


def deepspeech_speech_to_text(audio_file_name, language):
    '''
        Performing specch to text 
        input : processed input file, language code
        output : text corresponding to the given speech file
    '''
    ssh_cmd = "sshpass -p gitech123$* scp -r "+audio_file_name + \
        " administrator@10.101.1.245:~/Projects/Voicebot_TempAudios/" + \
        language+"/"+current_date+"/"

    try:
        subprocess.check_output(ssh_cmd, shell=True,
                                stderr=subprocess.STDOUT).decode('utf-8')
    except Exception as ex:
        raise("Unable to paste the audio file for sppech to text server. Please refer the eject error {}".format(str(ex)))

    response = str(deepspeech_api(language, audio_file_name)).strip()
    response = responce_preprocessing(responce).lower()
    return response
