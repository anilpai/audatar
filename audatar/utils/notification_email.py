import json
import requests
import logging

from flask import render_template
from audatar.models import ValidationCheckInstance, Notification, ValidationCheck
from audatar.utils import helper
from audatar.utils.mail import HomeAwayMailer
from audatar import audatar_config

logger = logging.getLogger('audatar')


class NotificationEmail:
    def __init__(self, id):
        self.mailer = HomeAwayMailer()
        self.result = ValidationCheckInstance.query.get(id)
        self.mlist = None
        self.result_records = None
        self.vc_name = None
        self.vci = {
            'id': self.result.id,
            'task_id': self.result.task_id,
            'status': self.result.status,
            'count': self.result.result_count,
            'vc_id': self.result.validation_check.id,
            'input': self.result.input,
            'time_started': helper.convert_time_to_cst(self.result.time_started),
            'time_submitted': helper.convert_time_to_cst(self.result.time_submitted),
            'time_completed': helper.convert_time_to_cst(self.result.time_completed),
            'created_by': self.result.created_by,
            'result': self.result.result
        }

    def generate_result_records(self):
        """Prepares result_records based on VCI status."""
        if self.vci['result'] in ['Pass', 'Fail']:
            self.result_records = json.loads(self.result.result_records)
        else:
            self.result_records = self.result.result_records

    def generate_mailing_list(self):
        """Prepares a mailing list to send email to subscribers based on
        notification table."""
        self.mlist = []
        notify = Notification.query.filter(Notification.validation_check_id ==
                                           self.vci['vc_id'], Notification.type == 'Email').all()
        for n in notify:
            if self.vci['result'] == 'Pass' and n.notify_if_success is True:
                self.mlist.append(n.value)
            elif self.vci['result'] == 'Fail' and n.notify_if_failure is True:
                self.mlist.append(n.value)
            elif self.vci['result'] == 'Error' and n.notify_if_error is True:
                self.mlist.append(n.value)

    def get_vc_name(self):
        """Get a vc name for email template."""
        vc_table = ValidationCheck.query.filter(ValidationCheck.id == self.vci['vc_id']).first()
        self.vc_name = vc_table.name

    def get_table_header(self):
        """Get a list of table columns to build the table header."""
        return json.loads(self.result.result_records)['schema']['colOrder']

    def get_table_data(self):
        """Get a list of lists to build the complete table."""
        data = json.loads(self.result.result_records)['data']
        ordered_data = []
        for i in range(len(data)):
            temp = []
            for k in self.get_table_header():
                temp.append(data[i][k])
            ordered_data.append(temp)
        return ordered_data

    def send_mail_as_html(self):
        """Send Email to subscribers in HTML format using appropriate email
        template."""

        self.get_vc_name()
        self.generate_mailing_list()
        listString = ';'.join(map(str, self.mlist))
        completed = self.result.time_completed.strftime('%Y-%m-%d %H:%M:%S')
        parameters = {
            'value': listString,
            'time_completed': completed,
            'type': self.vci['result'],
            'validation_check_id': self.vci['vc_id'],
            'task_id': self.vci['task_id']
        }

        if self.vci['status'] != 'Error':
            self.mailer.sendhtml(
                '{0} - [Validation Check : {1}] is in {2} state : Audatar Results'.format(audatar_config.env.capitalize(),
                                                                                          self.vc_name,
                                                                                          self.vci['result']),
                render_template(
                    'email/validation_result.html',
                    vci=self.vci,
                    vci_input=json.loads(self.vci['input']),
                    header=self.get_table_header(),
                    data=self.get_table_data()
                ), 'audatar@homeaway.com', 'analyticsengineeringoperations@groups.homeawaycorp.com', self.mlist)
            logging.info('Mail sent successfully!')

            """ Save the Email Notification to Logs."""
            notification_success = requests.post('{0}/nlog/'.format(audatar_config.api_url),
                                                 data=json.dumps(parameters, indent=4), headers=audatar_config.headers)

            logger.info(helper.generate_logging_message('audatar', 'notification_email', 'success email', notification_success.json()['id'], 'success',
                                                        'Parameters: {}'.format(parameters)))

        else:
            self.mailer.sendhtml(
                '{0} - [Validation Check : {1}] is in {2} state : Audatar Results'.format(audatar_config.env.capitalize(),
                                                                                          self.vc_name,
                                                                                          self.vci['result']),
                render_template(
                    'email/validation_failure.html',
                    vci=self.vci,
                    vci_input=json.loads(self.vci['input']),
                    data=self.result.result_records
                ), 'audatar@homeaway.com', 'analyticsengineeringoperations@groups.homeawaycorp.com', self.mlist)
            logging.info('Failure Mail sent successfully!')

            """ Save the Email Notification to Logs."""
            notification_fail = requests.post('{0}/nlog/'.format(audatar_config.api_url),
                                              data=json.dumps(parameters, indent=4), headers=audatar_config.headers)

            logger.info(helper.generate_logging_message('audatar', 'notification_email', 'error email', notification_fail.json()['id'], 'success',
                                                        'Parameters: {}'.format(parameters)))
