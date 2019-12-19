import time
from datetime import datetime

import requests
from audatar.app import create_app
from celery.result import AsyncResult

from audatar.extensions import db
from audatar.utils import helper
from audatar.utils.notification_email import NotificationEmail
from audatar.models import ValidationCheckInstance
from requests.auth import HTTPBasicAuth

from audatar import audatar_config


if __name__ == '__main__':
    app = create_app('controller')
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    while True:
        status = 'Submitted'
        validations = requests.get('{0}/api/vci/status/{1}'.format(audatar_config.api_url, status),
                                   verify=False, headers=audatar_config.headers).json()
        for v in validations['data']:
            result = AsyncResult(v['task_id'])
            if result.state == 'SUCCESS':
                ValidationCheckInstance.query.filter(ValidationCheckInstance.task_id == result.task_id). \
                    update({ValidationCheckInstance.status: result.status,
                            ValidationCheckInstance.time_started: helper.format_time(
                                helper.get_celery_task_times(v['task_id'])['started']),
                            ValidationCheckInstance.time_completed: helper.format_time(
                                helper.get_celery_task_times(v['task_id'])['succeeded']),
                            ValidationCheckInstance.result_records: result.result.result_records_json(),
                            ValidationCheckInstance.result: result.result.status,
                            ValidationCheckInstance.result_count: len(result.result.results)
                            })
                db.session.commit()
                vci = ValidationCheckInstance.query.filter(ValidationCheckInstance.task_id == result.task_id).all()
                db.session.commit()
                print('{0} has status {1}'.format(result.task_id, result.state))
                print('Task {0} was successful hence db updated'.format(result.task_id))
                mail = NotificationEmail(vci[0].id)
                mail.send_mail_as_html()
                print('{0} Mail notification sent successfully !'.format(result.status))

            elif result.state == 'FAILURE':
                status = 'Error'
                data = result.traceback
                result.time_completed = datetime.now()
                vci_id = ValidationCheckInstance.query.filter(ValidationCheckInstance.task_id == result.task_id). \
                    update({ValidationCheckInstance.status: status,
                            ValidationCheckInstance.time_started: helper.format_time(
                                helper.get_celery_task_times(v['task_id'])['started']),
                            ValidationCheckInstance.time_completed: helper.format_time(
                                helper.get_celery_task_times(v['task_id'])['failed']),
                            ValidationCheckInstance.result_records: data,
                            ValidationCheckInstance.result: status,
                            ValidationCheckInstance.result_count: None
                            })
                db.session.commit()
                vci = ValidationCheckInstance.query.filter(ValidationCheckInstance.task_id == result.task_id).all()
                db.session.commit()
                print('{0} has status {1}'.format(result.task_id, result.state))
                print('Task {0} was failure hence db updated'.format(result.task_id))
                mail = NotificationEmail(vci[0].id)
                mail.send_mail_as_html()
                print('{0} Mail notification sent successfully !'.format(result.status))

            else:
                print('{} has status {}'.format(result.task_id, result.state))
        time.sleep(5)
