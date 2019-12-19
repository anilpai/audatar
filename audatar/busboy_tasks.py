from audatar.extensions import celery

import requests
from celery.result import AsyncResult
from audatar import audatar_config
from audatar.utils.helper import format_time, requests_retry_session
import json
import datetime
import logging

token = audatar_config.token


@celery.task
def vci_status_check_and_update():
    """ Fix vci status issue between flower and postgres."""

    '''Find all the tasks in submitted status in db which are atleast 15 minutes old'''
    t = datetime.datetime.now() + datetime.timedelta(hours=6) - datetime.timedelta(minutes=15)
    s = 'Submitted'
    page_size = '50'
    print('Catch Up tasks stuck in {0} since : {1} '.format(s, t - datetime.timedelta(hours=6)))
    r = requests.get('{0}/vci/?status={1}&end_date={2}&pageSize={3}'.format(audatar_config.api_url, s, t, page_size),
                     headers={'accept': 'application/json', 'Authorization': 'Bearer '+token})

    ids = []
    for i in r.json()['data']:
        ids.insert(0, (i['id'], i['task_id']))
    print(ids)

    print(len(ids))

    started = []
    success = []
    failure = []

    for i in ids:
        t = requests.get('{0}/api/task/info/{1}'.format(audatar_config.flower_api_url, i[1]),
                         auth=(audatar_config.flower_username, audatar_config.flower_password))

        if t.status_code == 404:
            print('Task Id not found')
            failure.append(i[0])

            ''' Error the task. May be the task was not sent to workers or flower was restarted. '''

            fail_status = 'Error'
            parameters = {
                'status': fail_status,
                'time_started': format_time(int(datetime.datetime.now().strftime('%s'))),
                'time_completed': format_time(int(datetime.datetime.now().strftime('%s'))),
                'result_records': 'Message from Audatar: Validation Check went missing. Re-run task. Id = {0} , Slack: #audatar-support'.format(i[0]),
                'result': fail_status,
                'result_count': None,
                'task_id': i[1]
            }

            vci = requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, i[1]),
                                               data=json.dumps(parameters, indent=4),
                                               headers=audatar_config.headers)

            print('VCI Id : {0} , HTTP Status = {1} '.format(i[0], vci.status_code))

            print(vci.text)

        elif t.status_code == 200:
            print(t.json())
            if t.json()['state'].lower() == 'success':
                print('Task was successful')
                success.append(i[0])

                ''' Update the db that task as successful '''
                success_status = 'Success'
                json_dict = t.json()

                result = AsyncResult(json_dict['uuid'])

                parameters = {
                    'status': success_status,
                    'time_started': format_time(json_dict['started']),
                    'time_completed': format_time(json_dict['succeeded']),
                    'result_records': result.result.result_records_json(),
                    'result': json_dict['state'].title(),
                    'result_count': len(result.result.results),
                    'task_id': json_dict['uuid']
                }

                vci = requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, json_dict['uuid']),
                                                   data=json.dumps(parameters, indent=4),
                                                   headers=audatar_config.headers)
                print('VCI Id : {0} , HTTP Status = {1} '.format(i[0], vci.status_code))

            elif t.json()['state'].lower() == 'failure':
                print('Task was failure')
                failure.append(i[0])

                ''' Update the db that task was failure '''
                fail_status = 'Error'
                json_dict = t.json()

                result = AsyncResult(json_dict['uuid'])

                parameters = {
                    'status': fail_status,
                    'time_started': format_time(json_dict['started']),
                    'time_completed': format_time(json_dict['succeeded']),
                    'result_records': str(result.result),
                    'result': fail_status,
                    'result_count': None,
                    'task_id': i[1]
                }

                vci = requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, i[1]),
                                                   data=json.dumps(parameters, indent=4),
                                                   headers=audatar_config.headers)

                print('VCI Id : {0} , HTTP Status = {1} '.format(i[0], vci.status_code))

                print(vci.text)

            else:
                print(t.json()['state'].lower())
                started.append(i[0])
                print('Task is in started. Move on ..')
                ''' TODO: Update the db as Started'''

    return started, success, failure


@celery.task
def stuck_in_started():
    """Stuck in Started Status for an hour."""

    '''Find all tasks stuck in Started for more than an hour from db'''
    t = datetime.datetime.now() + datetime.timedelta(hours=6) - datetime.timedelta(hours=1)
    s = 'Started'
    page_size = '50'
    print('Catch Up tasks stuck in {0} since : {1} '.format(s, t - datetime.timedelta(hours=6)))
    r = requests.get('{0}/vci/?status={1}&end_date={2}&pageSize={3}'.format(audatar_config.api_url, s, t, page_size),
                     headers={'accept': 'application/json', 'Authorization': 'Bearer ' + token})

    ids = []
    for i in r.json()['data']:
        ids.insert(0, (i['id'], i['task_id']))

    print(ids)

    for i in ids:
        t = requests.get('{0}/api/task/info/{1}'.format(audatar_config.flower_api_url, i[1]),
                         auth=(audatar_config.flower_username, audatar_config.flower_password))

        if t.status_code == 404:
            ''' Task Id not found.'''
            ''' Update the db that task was failure. '''
            fail_status = 'Error'

            parameters = {
                'status': fail_status,
                'time_started': format_time(int(datetime.datetime.now().strftime('%s'))),
                'time_completed': format_time(int(datetime.datetime.now().strftime('%s'))),
                'result_records': 'Message from Audatar: Validation Check went missing. Re-run task. Id = {0} , Slack: #audatar-support'.format(i[0]),
                'result': fail_status,
                'result_count': None,
                'task_id': i[1]
            }

            vci = requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, i[1]),
                                               data=json.dumps(parameters, indent=4),
                                               headers=audatar_config.headers)

            print('VCI Id : {0} , HTTP Status = {1} '.format(i[0], vci.status_code))

            print(vci.text)

        elif t.status_code == 200:
            ''' If started, then fail.'''
            print(t.json())

            if t.json()['state'].lower() == 'success':
                print('Task was successful')

                ''' Update the db that task as successful '''
                success_status = 'Success'
                json_dict = t.json()

                result = AsyncResult(json_dict['uuid'])

                parameters = {
                    'status': success_status,
                    'time_started': format_time(json_dict['started']),
                    'time_completed': format_time(json_dict['succeeded']),
                    'result_records': result.result.result_records_json(),
                    'result': json_dict['state'].title(),
                    'result_count': len(result.result.results),
                    'task_id': json_dict['uuid']
                }

                vci = requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, json_dict['uuid']),
                                                   data=json.dumps(parameters, indent=4),
                                                   headers=audatar_config.headers)
                print('VCI Id : {0} , HTTP Status = {1} '.format(i[0], vci.status_code))

            elif t.json()['state'].lower() == 'failure':
                print('Task was failure')

                ''' Update the db that task was failure '''
                fail_status = 'Error'
                json_dict = t.json()

                from celery.result import AsyncResult
                result = AsyncResult(json_dict['uuid'])

                parameters = {
                    'status': fail_status,
                    'time_started': format_time(json_dict['started']),
                    'time_completed': format_time(json_dict['succeeded']),
                    'result_records': str(result.result),
                    'result': fail_status,
                    'result_count': None,
                    'task_id': i[1]
                }

                vci = requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, i[1]),
                                                   data=json.dumps(parameters, indent=4),
                                                   headers=audatar_config.headers)

                print('VCI Id : {0} , HTTP Status = {1} '.format(i[0], vci.status_code))

                print(vci.text)

            else:
                print('Task is in {0} status for a long time. Error the task...'.format(t.json()['state'].lower()))

                ''' Update the db that task was failure '''
                fail_status = 'Error'
                json_dict = t.json()

                parameters = {
                    'status': fail_status,
                    'time_started': format_time(json_dict['started']),
                    'time_completed': format_time(int(datetime.datetime.now().strftime('%s'))),
                    'result_records': 'Message from Audatar : Validation Check ran more than an hour.',
                    'result': fail_status,
                    'result_count': None,
                    'task_id': i[1]
                }

                vci = requests_retry_session().put('{0}/vci/task_id/{1}'.format(audatar_config.api_url, i[1]),
                                                   data=json.dumps(parameters, indent=4),
                                                   headers=audatar_config.headers)

                print('VCI Id : {0} , HTTP Status = {1} '.format(i[0], vci.status_code))

                print(vci.text)

    return ids


@celery.task
def back_fill_validation_registry():
    """Start date is 2 days ago from now."""

    N = 2
    start_date = datetime.datetime.now() - datetime.timedelta(days=N)
    end_date = datetime.datetime.now()
    page_size = 500
    page_number = 1
    vci_id = None
    status = 'Success'

    r = requests.get('{0}/vci/?status={1}&start_date={2}&end_date={3}&pageNumber={4}&pageSize={5}&vr_sent={6}'.format(audatar_config.api_url,
                                                                                                                      status,
                                                                                                                      start_date,
                                                                                                                      end_date,
                                                                                                                      page_number,
                                                                                                                      page_size,
                                                                                                                      False),
                     headers={'accept': 'application/json', 'Authorization': 'Bearer ' + token})

    print(r.status_code)
    count = r.json()['count']
    print(count)

    for i in r.json()['data']:
        try:
            vci_id = i['id']
        except Exception as e:
            print(str(e))

        dr_parameters = {'vci_id': vci_id}
        """ Send Results to Data Registry"""
        backfill = requests.post('{0}/notification/send_ds'.format(audatar_config.api_url),
                                 data=json.dumps(dr_parameters, indent=4), headers=audatar_config.headers)
        print(backfill.status_code)

        """ Update the attribute on success"""

        pg_parameters = {}
        if backfill.status_code == 200:
            pg_parameters['id'] = vci_id
            pg_parameters['sent_to_validation_registry'] = True
            pg_update = requests_retry_session().put('{0}/vci/{1}'.format(audatar_config.api_url, vci_id),
                                                     data=json.dumps(pg_parameters, indent=4),
                                                     headers=audatar_config.headers)

            print(pg_update.status_code)
            logging.info('Sent results to Data Registry.')
