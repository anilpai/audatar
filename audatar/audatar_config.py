import os
from audatar.utils.jprops_reader import *

'''
Get environment from environment variable.
Default 'local' if variable not found.
'''
env = os.getenv('MPAAS_ENVIRONMENT') or 'local'

'''
Datadog Instrumentation Setup
'''

DATADOG_SETTINGS = {
    'prefix': 'ae-audatar',
    'api_key': '632496f81d14f8408cb9570fb4b3465a',
    'app_key': 'f2cb1dd7019dc8e8268e6e71051a42c3ceed7e9c',
    'stats_host': 'dockerhost'
}


'''
API URL
'''
api_url = properties['react_app.base_api_url']

'''
Mail Server
'''
mail_server = properties['smtp_mail.server_name']

'''
Postgres SQL Credentials on AWS RDS
'''
pg_username = properties['postgres.username']
pg_password = properties['postgres.password']
pg_hostname = properties['postgres.hostname']
pg_port_num = properties['postgres.port']
pg_db_name = properties['postgres.database']

'''
RabbitMQ Credentials on AWS
'''
rabbit_username = properties['rabbit.username']
rabbit_password = properties['rabbit.password']
rabbit_hostname = properties['rabbit.hostname']
rabbit_port_num = properties['rabbit.port']

''''
SQLAlchemy Settings
'''

SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    pg_username, pg_password, pg_hostname, pg_port_num, pg_db_name)

'''
Celery Settings
'''
PROD_CELERY_BROKER_URI = 'amqp://{0}:{1}@{2}:{3}'.format(rabbit_username,
                                                         rabbit_password, rabbit_hostname, rabbit_port_num)


CELERY_SETTINGS = {
    'broker_url': PROD_CELERY_BROKER_URI,
    'result_backend': 'db+' + SQLALCHEMY_DATABASE_URI,
    'task_track_started': True,
    'database_table_names': {
        'task': 'celery_taskmeta',
        'group': 'celery_groupmeta',
    },
}

secret_key = properties['secret.key']

LDAP_URI = properties['ldap.uri']

token = properties['jwt.token']

headers = {'accept': 'application/json', 'Authorization': 'Bearer {0}'.format(properties['jwt.token'])}

""" Flower Credentials"""

flower_username = properties['flower.username']
flower_password = properties['flower.password']
flower_api_url = properties['flower.api_url']

'''
data explorer register validation check api url 
'''
data_explorer_api_url = os.getenv('DATA_EXPLORER_API_URL')
data_explorer_algolia_url = os.getenv('DATA_EXPLORER_ALGOLIA_URL')
# data_explorer_api_url = properties['data.explorer.api.url']
# data_explorer_algolia_url = properties['data.explorer.algolia.url']
audatar_vci_url = api_url+'/'
headers_data_explorer = {'Content-type': 'application/json', 'Accept': 'application/json'}


'''
algolia related secrets
'''

algolia_app_id = properties['algolia.appId']
algolia_index = properties['algolia.index']
algolia_api_key = properties['algolia.apiKey']
