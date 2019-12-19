from flask import Blueprint, jsonify, request, json
import requests
from audatar import audatar_config
from audatar.utils.notification_email import NotificationEmail
from audatar.utils.webhook import Webhook
from audatar.utils.helper import get_results_dict

from audatar.api import token_required
from flask_cors import CORS

notification_bp = Blueprint('notification_bp', __name__, url_prefix='/api/notification')

CORS(notification_bp)


@notification_bp.route('/send_email', methods=['POST'])
@token_required
def send_notification_email():
    """Sends a Notification email to subscribers.

    :param result_status: the celery task result status.
    :param vci_id: the id of the Validation Check Instance.
    :return: None
    """

    parameters = json.loads(request.data.decode('utf-8'))
    result_status = parameters.get('result_status', None)
    vci_id = parameters.get('vci_id', None)

    try:
        mail = NotificationEmail(vci_id)
        mail.send_mail_as_html()
        return jsonify(msg='Mail notification sent successfully !', id=vci_id, result_status=result_status), 200
    except Exception as e:
        return jsonify(msg=str(e)), 404


@notification_bp.route('/send_webhook', methods=['POST'])
@token_required
def send_notification_webhook():
    """Sends a Notification webhook to subscribers.

    :param result_status: the celery task result status.
    :param vci_id: the id of the Validation Check Instance.
    :return: None
    """

    parameters = json.loads(request.data.decode('utf-8'))
    result_status = parameters.get('result_status', None)
    vci_id = parameters.get('vci_id', None)

    try:
        webhook = Webhook(vci_id)
        webhook.send_webhook()
        return jsonify(msg='Webhook notification sent successfully !', id=vci_id, result_status=result_status), 200
    except Exception as e:
        return jsonify(msg=str(e)), 404


@notification_bp.route('/send_ds', methods=['POST'])
@token_required
def send_to_data_registry():
    """Sends results to Data Registry.

    :param vci_id: the id of the Validation Check Instance.
    :return: None
    """

    parameters = json.loads(request.data.decode('utf-8'))
    vci_id = parameters.get('vci_id', None)

    try:
        dr_params = get_results_dict(vci_id)
        dr_success = requests.post(audatar_config.data_explorer_api_url,
                                   data=json.dumps(dr_params, indent=4), headers=audatar_config.headers_data_explorer)
        if dr_success.status_code == 200:
            return jsonify(msg='Submitted to Data Registry successfully !', id=vci_id), 200
        else:
            return jsonify(msg='Something went wrong during posting data results to registry', id=vci_id), \
                   dr_success.status_code
    except Exception as e:
        return jsonify(msg=str(e)), 404
