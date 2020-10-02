from multiprocessing import Pool
import threading
import ast
from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
from application_util import product_operation, caller_operation
from custome_audio_generation import generate_audio
from database_util import application_db

""" update the channel dedtails once the call initiated """


def update_channel_detail_call_initiated():

    available_channels_details = application_db.get_available_channels()

    available_channel = available_channels_details["available_channel"]
    running_channel = available_channels_details["running_channel"]

    available_channel = available_channel - 1
    running_channel = running_channel + 1

    application_db.update_channel_details(available_channel, running_channel)

    return True


""" call initaition from SPI server """


def call_initiation(transaction_id, mobile_no, product_type, prefix, context="0009"):
    try:
        client = AMIClient(address='10.101.1.184', port=5038)
        client.login(username='gihosp', secret='gihosp123')

        action = SimpleAction(
            'Originate',
            Channel="local/"+"6"+mobile_no+"@from-internal",
            Context="GIVoice",
            Exten=context,
            Priority=1,
            Account=product_type,
            CallerID=transaction_id,
            Async="yes",
            Timeout=50000
        )
        future = client.send_action(action)
        response = future.response

        update_channel_detail_call_initiated()
        return True
    except Exception as ex:
        raise Exception(
            "SIP server is down .. please check eject error {}".format(str(ex)))
        return True


def customer_data_call_initiation_process(customer_datas, prefix):

    try:
        threads = []
        for index, customer_data in enumerate(customer_datas):
            input_list = []
            '''parse the product details from customer data'''
            #caller_data = customer_data.decode().split("$$$")

            caller_data = customer_data

            transaction_id = str(caller_data[0])
            mobile_no = str(caller_data[2])
            language = str(caller_data[3]).strip()
            product_type = str(caller_data[16])

            split_def_product_type = product_type.split()

            product_type = product_type.replace(" ", "_")

            try:
                sub_product = split_def_product_type[0] + \
                    "_" + split_def_product_type[1]
            except:
                sub_product = product_type

            product = split_def_product_type[0]

            ''' insert new caller data while call initiation '''
            if caller_operation.insert_new_caller_data(transaction_id, caller_data):

                ''' get product config details via customer product '''
                product_config = product_operation.get_product_config(product)

                ''' if product is active status means it will initiate the call '''
                if product_config["status"] == 1:

                    ''' check to create custome audio '''
                    if product_config["is_call_initiate_custome_audio"] == 1:

                        ''' generate custome audio while call initiazation itself'''
                        generate_audio.generic_audio_generation(
                            product_config["question_flow"], transaction_id, language, caller_data)

                    # call_initiation(transaction_id, mobile_no,
                    #                 product_type, prefix, product_config["context"])

                    # t = threading.Thread(target=call_initiation, args=(transaction_id, mobile_no,
                    #                                                    product_type, prefix, product_config["context"]),)
                    # threads.append(t)
                    # t.start()
                    input_list.append(transaction_id)
                    input_list.append(mobile_no)
                    input_list.append(product_type)
                    input_list.append(prefix)
                    input_list.append(product_config["context"])
                    threads.append(input_list)
                else:
                    return False
            else:
                return False

        pool = Pool(processes=3)
        pool.starmap(call_initiation, threads)
        pool.close()
        return True
    except Exception as ex:
        return False
