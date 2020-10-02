import os
import time
from database_util import application_db, get_customer_detail_sql
from application_util import call_initiation
import itertools

# while True:

available_channel = application_db.get_available_channels()

product_to_run = available_channel["running_products"]

for _id, product in enumerate(product_to_run):

    """" mapping the key with available prefixes """
    prefixs_mapping = list(itertools.product(
        available_channel["key"], available_channel["prefix"]))

    for index, prefix_mapping in enumerate(prefixs_mapping):

        prefix_allocated_channels = available_channel["available_channel"]

        """ only the channel is free the aplication will run """
        if prefix_allocated_channels > 0:

            """ no of channel running and no of free channal available logic """
            prefix_running_channels = available_channel["running_channel"]
            prefix_free_channels = prefix_allocated_channels - prefix_running_channels

            if prefix_free_channels > 0:

                """ get the customer data from databse to initiate the call for product wise """
                customer_datas = get_customer_detail_sql.get_customer_five_data_from_database(
                    product, prefix_free_channels)

                if len(customer_datas) > 0:

                    """ initiate the call based on customer data """
                    call_initiate = call_initiation.customer_data_call_initiation_process(
                        customer_datas, prefix_mapping[1])

                    if call_initiate:
                        # To do status maintain details #
                        print("Call initited success")
                        break
                    else:
                        print("Call initited failed")
                        break
                else:
                    raise Exception("Customer data is empty ..")

time.sleep(5)
