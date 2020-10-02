import pypyodbc
import datetime


def get_customer_five_data_from_database(client_id, no_of_record_to_get=5):
    """
        return 5 records for the given client ID
        input : client ID
    """
    rows = []
    try:
        # connectionString = 'DRIVER={FreeTDS};SERVER=10.101.1.190\SQL2014;DATABASE=smartrupee;UID=sa;PWD=gitech123*gitech;TDS_Version=7.2;'
        # connection = pypyodbc.connect(connectionString, autocommit=True)
        # cursor = connection.cursor()
        # query = cursor.execute("CLI_GET_voiceblastdata_V3 ?", [client_id])
        # rows = cursor.fetchall()
        # connection.close()
        # 04466506031
        rows = [(1, u'Narasimman', u'9787411068', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
                 1, 1, None, None, u'equitasfixeddeposit', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456')]
        #  ,
        # (2, u'Narasimman', u'04466506032', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (3, u'Narasimman', u'04466506033', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (4, u'PINAKIN CHORASIYA', u'04466506034', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (5, u'PINAKIN CHORASIYA', u'04466506035', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (6, u'PINAKIN CHORASIYA', u'04466506036', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (7, u'PINAKIN CHORASIYA', u'04466506009', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (8, u'PINAKIN CHORASIYA', u'04466506026', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (9, u'PINAKIN CHORASIYA', u'04466506037', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (10, u'PINAKIN CHORASIYA', u'04466506003', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456'),
        # (11, u'PINAKIN CHORASIYA', u'04466506012', u'english', None, 1000, None, None, u'Welcome call', None, None, datetime.datetime(2018, 11, 27, 12, 40, 58, 20000),
        #  1, 1, None, None, u'hfcl welcome call', u'10.101.1.147', u'1044', u'gihosp123', u'6', u'electric two wheeler', u'2018-11-08T00:00:00+05:30', 101031, 24, u'123456')]
    except Exception as ex:
        raise Exception(
            "Unable to get the client details .. please check eject error {}".format(str(ex)))

    return rows
