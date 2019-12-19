from flask import Flask, request, Response, render_template, g, after_this_request
from flask_admin import Admin

import os
import logging
import datadog
import time
import uuid
from logging.handlers import RotatingFileHandler

from audatar import audatar_config
from audatar.admin import admin_routes

from audatar.api import api_bp, connection_bp, connectiontype_bp, validation_check_bp, validation_check_instance_bp, \
    validation_check_parameters_bp, validator_bp, notification_bp, notification_log_bp, team_bp, \
    heartbeat_bp, severitylevel_bp, dimension_bp, workers_bp, dataset_bp
from audatar.extensions import db, celery, ma, mail, auth, swagger, stats, datadog_tags
from audatar.models import User

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    connection_bp,
    connectiontype_bp,
    validation_check_bp,
    validation_check_instance_bp,
    validation_check_parameters_bp,
    validator_bp,
    notification_bp,
    notification_log_bp,
    team_bp,
    heartbeat_bp,
    api_bp,
    severitylevel_bp,
    dimension_bp,
    workers_bp,
    dataset_bp
)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a flask app."""

    if app_name is None:
        app_name = 'audatar'
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_relative_config=True)
    app.config['SECRET_KEY'] = '123456790'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s:%s/%s' % (
        audatar_config.pg_username, audatar_config.pg_password, audatar_config.pg_hostname, audatar_config.pg_port_num, audatar_config.pg_db_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'Audatar API Documentation',
        'uiversion': 2    # uiversion3 is still experimental, hence using ver2
    }
    app.config['JWT_AUTH_URL_RULE'] = '/api/auth'

    configure_app(config)
    configure_hook(app)
    configure_logging(app)
    configure_celery_app(app, celery)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_error_handlers(app)
    configure_logging(app)
    datadog.api.Event.create(title='Audatar API service has started',
                             text='Audatar API service started and ready to respond to requests',
                             tags=datadog_tags)
    app.logger.info('Audatar has started in the {0} environment'.format(audatar_config.env))
    return app


def configure_logging(app):
    """Configure info logging to splunk."""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    app.logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s|%(asctime)s|%(filename)s|%(lineno)s|%(message)s')
    file_name = 'logs/stdout.log'
    time_handler = logging.handlers.TimedRotatingFileHandler(file_name, when='midnight', backupCount=5)
    time_handler.setFormatter(formatter)
    time_handler.suffix = '%Y%m%d.log'
    app.logger.addHandler(time_handler)


def configure_app(app, config=None):
    """Different ways of configurations."""
    if config:
        app.config.from_object(config)


def configure_extensions(app):
    """flask-alchemy."""
    db.init_app(app)

    """swagger docs"""
    swagger.init_app(app)

    """ flask basic auth """
    @auth.verify_password
    def verify_password(username_or_token, password):
        user = User.verify_auth_token(username_or_token)
        if not user:
            user = User.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        return True

    """ flask-admin """

    admin = Admin(name='Audatar: Admin View', template_mode='bootstrap3')
    admin.init_app(app)
    admin_routes(admin)

    """ celery"""
    # celery.config_from_object(app.config)

    """" flask-marshmallow """
    ma.init_app(app)

    """ Flask-Mail """
    mail.init_app(app)


def configure_celery_app(app, celery):
    """Configure the celery app."""
    celery.conf.update(app.config)
    app.config.update(audatar_config.CELERY_SETTINGS)
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_hook(app):
    @app.before_request
    def add_request_id():

        g.request_id = request.headers.get('X-HomeAway-Request-Marker', 'audatar-{}'.format(uuid.uuid4().hex[:7]))

        method = request.path[1:].replace('/', '_')
        request_metric = 'audatar.requests.' + method

        start = time.time()

        @after_this_request
        def record_request_time(response):
            end = time.time()
            elapsed = (end - start) * 1000

            try:
                stats.timing(request_metric + '.total.time', elapsed, timestamp=start, tags=datadog_tags)
                stats.timing(request_metric + '.' + str(response.status_code)[0] + 'XX.time', elapsed, timestamp=start,
                             tags=datadog_tags)
                stats.increment(request_metric + '.total', tags=datadog_tags)
                stats.increment(request_metric + '.' + str(response.status_code)[0] + 'XX', tags=datadog_tags)

                stats.timing('audatar.requests.total.time', elapsed, timestamp=start, tags=datadog_tags)
                stats.timing('audatar.requests.' + str(response.status_code)
                             [0] + 'XX.time', elapsed, timestamp=start, tags=datadog_tags)
                stats.increment('audatar.requests.total', tags=datadog_tags)
                stats.increment('audatar.requests.' + str(response.status_code)[0] + 'XX', tags=datadog_tags)
            except Exception as e:
                logging.warning('Exception when sending metrics: ' + str(e))
                pass

            return response


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/forbidden_page.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/page_not_found.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/server_error.html'), 500
