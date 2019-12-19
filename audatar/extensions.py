from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
import datadog

from algoliasearch import algoliasearch
from audatar import audatar_config
from celery import Celery

import os

db = SQLAlchemy(session_options={'autoflush': False})
rest = APIManager()
ma = Marshmallow()
mail = Mail()
celery = Celery('audatar.task_executor',
                backend=audatar_config.CELERY_SETTINGS['result_backend'],
                broker=audatar_config.CELERY_SETTINGS['broker_url'])
auth = HTTPBasicAuth()
swagger = Swagger()

client = algoliasearch.Client(audatar_config.algolia_app_id, audatar_config.algolia_api_key)
index = client.init_index(audatar_config.algolia_index)


def init_datadog():
    """DataDog integration setup."""
    datadog.initialize(**audatar_config.DATADOG_SETTINGS)

    stats = datadog.ThreadStats()

    stats.start(flush_interval=10, roll_up_interval=10, device=None, flush_in_thread=True,
                flush_in_greenlet=False, disabled=False)

    return stats


stats = init_datadog()

datadog_tags = ['audatar_app_name:{}'.format(os.getenv('MPAAS_APPLICATION_NAME')),
                'audatar_env:{}'.format(os.getenv('MPAAS_ENVIRONMENT')),
                'audatar_app_version:{}'.format(os.getenv('MPAAS_APPLICATION_VERSION'))]
