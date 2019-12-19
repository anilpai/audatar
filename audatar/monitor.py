import logging
import requests
import json
from audatar import audatar_config
from celery.result import AsyncResult
from audatar.extensions import celery
from audatar.utils import helper
from multiprocessing import Process

logger = logging.getLogger('audatar')

# THIS FILE HAS BEEN DEPRECATED.


def monitor(celery_app):
    """Monitors the status of the celery worker tasks, and update db to
    indicate task has started.

    :param celery_app: celery app instance from audatar extensions.
    :return: None
    """
    state = celery_app.events.State()

    def task_started(event):
        """Announces that task was started, updates the Validation Check
        Instance table."""
        state.event(event)
        task_id = event['uuid']
        try:
            result = AsyncResult(task_id)

            parameters = {
                'status': 'Started',
                'time_started': helper.format_time(helper.get_celery_task_times(task_id)['started'])
            }

            requests.put('{0}/api/vci/task_id/{1}'.format(audatar_config.api_url, task_id),
                         data=json.dumps(parameters, indent=4), headers=audatar_config.headers)

            logger.info(helper.generate_logging_message('audatar', 'monitor', 'started', task_id,
                                                        'success', '{0} has status {1}'.format(result.task_id, result.state)))
            logging.info('Task started updated in database')

        except Exception as e:
            logger.info(helper.generate_logging_message('audatar', 'monitor', 'started', task_id, 'fail', str(e)))

    with celery_app.connection() as connection:
        recv = celery_app.events.Receiver(connection, handlers={
            'task-started': task_started
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    p = Process(target=monitor, args=(celery,))
    p.start()
