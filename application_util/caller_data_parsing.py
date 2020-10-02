from dateutil import parser


def caller_data_parsing(caller_data):
    ''' parse the data from caller data object '''

    penalty_charges = "2"

    try:
        application_id = str(callee_data[25]).strip().lower()
    except:
        application_id = "1"
    try:
        transaction_id = str(caller_data[0])
    except:
        transaction_id = ""

    try:
        language = str(caller_data[3]).strip().lower()
    except:
        language = ""

    try:
        emi_amount = str(int(float(caller_data[5])))
    except:
        emi_amount = ""

    try:
        loan_type = str(caller_data[8]).strip().lower()
    except:
        loan_type = parser.parse(emi_start_month)

    try:
        product_type = str(caller_data[16]).strip().lower()
    except:
        product_type = ""

    try:
        product = product_type.split()[0]
    except:
        product = ""

    try:
        mobile_no = ""
    except:
        mobile_no = ""

    try:
        account_no = str(caller_data[4]).strip().lower()
        account_no = " ".join(str(acc_no)[-6:])
    except:
        account_no = ""

    try:
        due_date = caller_data[6]
    except:
        due_date = None

    try:
        product_name = str(caller_data[8]).strip().lower()
    except:
        product_name = ""

    try:
        emi_start_month = str(caller_data[22]).strip().lower()
        try:
            if type(emi_start_month) == "datetime.datetime":
                temp = [str(due_date.year), str(
                    due_date.month), str(due_date.day)]
                emi_start_month = temp
            else:
                dt_due_date = parser.parse(emi_start_month)
                temp = [str(dt_due_date.year), str(
                    dt_due_date.month), str(dt_due_date.day)]
                emi_start_month = temp
        except:
            emi_start_month = []
    except:
        emi_start_month = []

    try:
        loan_amount = str(caller_data[23]).strip().lower()
    except:
        loan_amount = ""

    try:
        tenure = str(caller_data[24]).strip().lower()
    except:
        tenure = ""

    try:
        bounce_charges = str(caller_data[26]).split(".")[0].lower()
    except:
        bounce_charges = ""

    try:
        disbursal_date = caller_data[27]

        if type(disbursal_date) == "datetime.datetime":
            temp = [str(due_date.year), str(due_date.month), str(due_date.day)]
            disbursal_date = temp
        else:
            dt_due_date = parser.parse(disbursal_date)
            temp = [str(dt_due_date.year), str(
                dt_due_date.month), str(dt_due_date.day)]
            disbursal_date = temp
    except:
        disbursal_date = []

    try:
        dealer_name = str(caller_data[21])
        dealer_name = dealer_name.replace(" ", "_")
    except:
        dealer_name = dealer_name

    return transaction_id, language, loan_type, product_type, product, mobile_no, account_no, due_date, product_name, emi_start_month, loan_amount, tenure, bounce_charges, penalty_charges, disbursal_date, application_id, emi_amount, dealer_name
