import pypyodbc


def commit_ivr_status(trans_id, dtmf, product):
    '''
        commit the status of IVR
        input : Transaction ID, status string(1.need help, 2.need help, 3.dispute, else wrong digits/ not pressed)
    '''
    try:
        connectionString = 'DRIVER={FreeTDS};SERVER=10.101.1.190\SQL2014;PORT=1433;DATABASE=smartrupee;UID=sa;PWD=gitech123*gitech;TDS_Version=7.2;'
        connection = pyodbc.connect(connectionString, autocommit=True)
        cursor = connection.cursor()
        #cursor.execute("CLI_INS_CustomerIVRTrack ?,?", [trans_id, status])
        connection.close()
    except Exception as ex:
        raise Exception(" Unable to update the ivr status in sql ")
    return True


def commit_user_response(trans_id, mob_no, product, qs_no, qs_text, cus_response, sys_prediction):
    '''
        update the db with user response(speech to text result) and corresponding voicebot prediction
        input : transaction ID, mobile number, question number, customer response, and corresponding  system predictions
    '''
    if len(cus_response) > 150:
        cus_response = ""
        sys_prediction = "unclear"

    try:
        connectionString = 'DRIVER={FreeTDS};SERVER=10.101.1.190\SQL2014;PORT=1433;DATABASE=smartrupee;UID=sa;PWD=gitech123*gitech;TDS_Version=7.2;'
        connection = pyodbc.connect(connectionString, autocommit=True)
        cursor = connection.cursor()
        # cursor.execute("CLI_INS_CustomerSpeechTrack ?,?,?,?,?,?", [
        #                trans_id, mob_no, qs_no, qs_text, cus_response, sys_prediction])
        connection.close()
    except Exception as ex:
        raise Exception(" Unable to update the ivr status in sql ")
    return True
