import json
import requests
import logging

from audatar.serializers import vci_schema
from audatar import audatar_config
from audatar.models import ValidationCheckInstance, Notification
from audatar.utils import helper

logger = logging.getLogger('audatar')


class Webhook:
    def __init__(self, id):
        self.result = ValidationCheckInstance.query.get(id)
        self.mlist = None
        self.webhook_list = None
        self.vci_record = None
        self.vci = {
            'id': self.result.id,
            'task_id': self.result.task_id,
            'status': self.result.status,
            'count': self.result.result_count,
            'vc_id': self.result.validation_check.id,
            'input': self.result.input,
            'time_started': self.result.time_started,
            'time_submitted': self.result.time_submitted,
            'time_completed': self.result.time_completed,
            'created_by': self.result.created_by,
            'result': self.result.result
        }

    def generate_vci_record(self):
        """Prepares result_records (vci) based on VCI status."""
        self.result.input = json.loads(self.result.input)
        if self.vci['result'] != 'Error' and self.result.result_records is not None:
            self.result.result_records = json.loads(self.result.result_records)
            self.vci_record = vci_schema.dump(self.result).data
        else:
            self.vci_record = vci_schema.dump(self.result).data

    def generate_webhook_list(self):
        """Prepares a webhook list to execute request to subscribers based on
        notification table."""
        self.mlist = []
        self.webhook_list = []
        notify = Notification.query.filter(Notification.validation_check_id ==
                                           self.vci['vc_id'], Notification.type == 'Webhook').all()
        for n in notify:
            if self.vci['result'] == 'Pass' and n.notify_if_success is True:
                self.mlist.append(n.value)
            elif self.vci['result'] == 'Fail' and n.notify_if_failure is True:
                self.mlist.append(n.value)
            elif self.vci['result'] == 'Error' and n.notify_if_error is True:
                self.mlist.append(n.value)

    def trigger_webhook_requests(self):
        """Triggers all the webhook requests."""
        headers = {'content-type': 'application/json'}
        for element in self.mlist:
            requests.post(element, data=json.dumps(self.vci_record, indent=4), headers=headers)

    def send_webhook(self):
        """Send webhook to subscribers."""

        self.generate_vci_record()
        self.generate_webhook_list()

        try:
            self.trigger_webhook_requests()
        except Exception as e:
            logging.info(str(e))

        list_string = ';'.join(map(str, self.mlist))
        completed = self.vci['time_completed'].strftime('%Y-%m-%d %H:%M:%S')

        parameters = {
            'value': list_string,
            'time_completed': completed,
            'type': self.vci['result'],
            'validation_check_id': self.vci['vc_id'],
            'task_id': self.vci['task_id']
        }

        notification = requests.post('{0}/nlog/'.format(audatar_config.api_url), data=json.dumps(parameters, indent=4),
                                     headers=audatar_config.headers)

        logger.info(helper.generate_logging_message('audatar', 'webhook', 'success webhook', notification.json()['id'], 'success',
                                                    'Parameters: {}'.format(parameters)))
