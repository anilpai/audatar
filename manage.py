import multiprocessing
from flask_script import Manager
import logging
from audatar.app import create_app
from gunicorn.app.wsgiapp import WSGIApplication


def get_version():
    with open('./setup_scripts/version.txt', 'rb') as f:
        return f.read().decode()


app = create_app()
manager = Manager(app)


@app.route('/alive.txt', methods=['GET', 'HEAD'])
def health_check():
    logging.info('Health Check - Audatar OK')
    return 'OK', 200


@app.route('/version.txt', methods=['GET'])
def version_check():
    version = get_version()
    logging.info('Version Check - Audatar version : %s', version)
    return version, 200


@app.route('/')
def welcome_to_home():
    logging.debug('index: GET /')
    return 'Welcome to Audatar', 200


@manager.command
def run(host='0.0.0.0', port=8080, workers=1 + (multiprocessing.cpu_count() * 2)):
    """Run the app with Gunicorn."""

    if app.debug:
        app.run(host, int(port), use_reloader=False)
    else:
        gunicorn = WSGIApplication()
        gunicorn.load_wsgiapp = lambda: app
        gunicorn.cfg.set('bind', '%s:%s' % (host, port))
        gunicorn.cfg.set('workers', workers)
        gunicorn.cfg.set('threads', workers)
        gunicorn.cfg.set('pidfile', None)
        gunicorn.cfg.set('worker_class', 'sync')
        gunicorn.cfg.set('keepalive', 10)
        gunicorn.cfg.set('accesslog', '-')
        gunicorn.cfg.set('errorlog', '-')
        gunicorn.cfg.set('reload', True)
        gunicorn.chdir()
        gunicorn.run()


if __name__ == '__main__':
    manager.run()
