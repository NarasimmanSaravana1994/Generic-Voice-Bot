from flask import Flask, request
from flask_cors import CORS
import flask_monitoringdashboard as dashboard
from responce_process import user_based_responce_process
from database_util import application_db


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return " Generic voice bot aplication is working ...."

# play_file


@app.route('/play_file', methods=['GET'])
def check_ivr_responce():

    dtmf = request.args.get("DTMF")
    product_type = str(request.args.get("product_type")).strip()
    transaction_id = str(request.args.get("trans_id")).strip()
    recorded_file = request.args.get("recorded_file")

    if recorded_file:
        current_audio_number = recorded_file.split("_")[-1].strip()
    else:
        current_audio_number = 2

    return user_based_responce_process.next_flow(transaction_id, dtmf, current_audio_number, recorded_file, True)


@app.route('/vb_responce_check', methods=['GET'])
def check_vb_responce():

    product_type = str(request.args.get("product_name")).strip()
    transaction_id = str(request.args.get("trans_id")).strip()
    recorded_file = request.args.get("recorded_file")
    current_audio_number = recorded_file.split("_")[-1].strip()

    return user_based_responce_process.next_flow(transaction_id, dtmf, current_audio_number, recorded_file, True)


@app.route('/end_call', methods=['GET'])
def end_call():
    transaction_id = str(request.args.get("transaction_id")).strip()

    application_db.remove_repeating_logic_based_on_transaction_id(
        transaction_id)
    application_db.remove_completed_caller_data_beased_on_transaction_id(
        transaction_id)

    available_channels_details = application_db.get_available_channels()

    available_channel = available_channels_details["available_channel"]
    running_channel = available_channels_details["running_channel"]

    available_channel = available_channel + 1
    running_channel = running_channel - 1

    application_db.update_channel_details(available_channel, running_channel)

    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4041, threaded=True, debug=True)
