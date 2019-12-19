import logging
import requests

from audatar.connections import *
from audatar.extensions import celery
from audatar.utils import helper
from audatar import audatar_config

from celery.schedules import crontab
from audatar import busboy_tasks


class CallbackTask(celery.Task):

    def on_success(self, retval, task_id, args, kwargs):

        logging.info('Celery Task ran successfully !')

        try:
            success_status = 'Success'
            parameters = {
                'status': success_status,
                'time_started': helper.format_time(helper.get_celery_task_times(task_id)['started']),
                'time_completed': helper.format_time(helper.get_celery_task_times(task_id)['succeeded']),
                'result_records': retval.result_records_json(),
                'result': retval.status,
                'result_count': len(retval.results),
                'task_id': task_id,
                'result_metric': retval.metric_json()
            }

            vci = helper.requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, task_id),
                                                      data=json.dumps(parameters, indent=4), headers=audatar_config.headers)

            logging.info('{0} has status {1}'.format(task_id, retval.status))
            logging.info('Task success updated in database')

            dr_parameters = {'vci_id': vci.json()['id']}

            """ Send Results to Data Registry"""
            ds_response = requests.post('{0}/notification/send_ds'.format(audatar_config.api_url),
                                       data=json.dumps(dr_parameters, indent=4),
                                       headers=audatar_config.headers)
            logging.info('Sent results to Data Registry.')

            """ Update the attribute on success"""

            if ds_response.status_code == 200:
                parameters['sent_to_validation_registry'] = True
                helper.requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, task_id),
                                                    data=json.dumps(parameters, indent=4),
                                                    headers=audatar_config.headers)

            """ Prepare for notifications. """
            notify_parameters = {'result_status': success_status, 'vci_id': vci.json()['id']}

            """ Send Notification Email to subscribers. """
            requests.post('{0}/notification/send_email'.format(audatar_config.api_url),
                          data=json.dumps(notify_parameters, indent=4), headers=audatar_config.headers)
            logging.info('Sent Notification Email to subscribers.')

            """ Send Notification Webhook to subscribers."""
            requests.post('{0}/notification/send_webhook'.format(audatar_config.api_url),
                          data=json.dumps(notify_parameters, indent=4), headers=audatar_config.headers)
            logging.info('Sent Notification Webhook to subscribers.')

        except Exception as e:
            logging.error(str(e))

        return super(CallbackTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):

        logging.info('Celery Task failed due to an error !')

        try:
            fail_status = 'Error'
            parameters = {
                'status': fail_status,
                'time_started': helper.format_time(helper.get_celery_task_times(task_id)['started']),
                'time_completed': helper.format_time(helper.get_celery_task_times(task_id)['failed']),
                'result_records': str(einfo),
                'result': fail_status,
                'result_count': None,
                'task_id': task_id
            }

            vci = helper.requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, task_id),
                                                      data=json.dumps(parameters, indent=4),
                                                      headers=audatar_config.headers)

            logging.info('{0} has status {1}'.format(task_id, fail_status))
            logging.info('Task fail updated in database')

            dr_parameters = {'vci_id': vci.json()['id']}

            """ Send Results to Data Registry"""
            ds_response = requests.post('{0}/notification/send_ds'.format(audatar_config.api_url),
                                        data=json.dumps(dr_parameters, indent=4), headers=audatar_config.headers)
            logging.info('Sent results to Data Registry.')

            """ Update the attribute on success"""

            if ds_response.status_code == 200:
                parameters['sent_to_validation_registry'] = True
                helper.requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, task_id),
                                                    data=json.dumps(parameters, indent=4),
                                                    headers=audatar_config.headers)

            """ Prepare for notifications. """
            notify_parameters = {'result_status': fail_status, 'vci_id': vci.json()['id']}

            """ Send Notification Email to subscribers. """
            requests.post('{0}/notification/send_email'.format(audatar_config.api_url),
                          data=json.dumps(notify_parameters, indent=4), headers=audatar_config.headers)
            logging.info('Sent Notification Email to subscribers.')

            """ Send Notification Webhook to subscribers."""
            requests.post('{0}/notification/send_webhook'.format(audatar_config.api_url),
                          data=json.dumps(notify_parameters, indent=4), headers=audatar_config.headers)
            logging.info('Sent Notification Webhook to subscribers.')

        except Exception as e:
            logging.error(str(e))

        return super(CallbackTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):

        print(exc, task_id, args, kwargs, einfo)

        return super(CallbackTask, self).on_retry(exc, task_id, args, kwargs, einfo)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(minute="*/21"),
        busboy_tasks.vci_status_check_and_update.s(),
        name='runs every 21 minutes'
    )

    sender.add_periodic_task(
        crontab(hour="*", minute=1),
        busboy_tasks.stuck_in_started.s(),
        name='runs first minute of every hour'
    )

    sender.add_periodic_task(
        crontab(hour=11, minute=5),
        busboy_tasks.back_fill_validation_registry.s(),
        name='runs every day once at 5 minutes past eleven'
    )


@celery.task(base=CallbackTask, track_started=True)
def validate(vc_class_path, validation_check_params_dict):

    logging.info('Task ID {0} is running now'.format(validate.request.id))
    task_id = validate.request.id

    try:
        started_status = 'Started'
        parameters = {
            'status': started_status,
            'time_started': helper.format_time(helper.get_celery_task_times(task_id)['started'])
        }

        helper.requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, task_id),
                                            data=json.dumps(parameters, indent=4), headers=audatar_config.headers)

        logging.info('{0} has status {1}'.format(task_id, started_status))
        logging.info('Task STARTED updated in database')

    except Exception as e:
        logging.error(str(e))

    logging.info('Get validator class from class_path')
    validator_class = helper.get_class_by_class_path(vc_class_path)
    logging.info('Validator class obtained !')
    logging.info(validator_class)

    valid_vc_params = validator_class.required_parameters() + validator_class.optional_parameters()
    logging.info('Valid VC params built !')

    valid_vc_params_dict = {}
    for key, value in valid_vc_params:
        valid_vc_params_dict[key] = value

    params_for_validator = {}

    for key, value in validation_check_params_dict.items():
        if key in valid_vc_params_dict:
            if (isinstance(valid_vc_params_dict[key], list) and all([issubclass(i, ConnectionBase) for i in valid_vc_params_dict[key]])) or issubclass(valid_vc_params_dict[key], ConnectionBase):
                logging.info('Get Connection Parameters..')
                r = helper.requests_retry_session().get('{0}/getConnectionParameters/{1}'.format(audatar_config.api_url, value), headers=audatar_config.headers)
                print('Get Connection Parameters Response Code : {0}'.format(r.status_code))
                try:
                    _json = r.json()
                    conn_class = helper.get_class_by_class_path(_json['conn_class_path'])
                    params_for_validator[key] = conn_class(value, _json['parameters'])
                    logging.info('Connection Parameters obtained !')
                except Exception as e:
                    logging.info('Failed to obtain Connection Parameters !')
                    logging.error(str(e))
            elif isinstance(valid_vc_params_dict[key], dict):
                params_for_validator[key] = json.loads(value)
            else:
                params_for_validator[key] = value

    validator = validator_class(params_for_validator)

    return validator.validate()
