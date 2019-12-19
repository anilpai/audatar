from sanic import Sanic
from sanic.response import json
from audatar.celery_api import worker_bp
from audatar.extensions import celery as celery_app
import os

"""Create Sanic app."""

app = Sanic(__name__)

"""Configure API Blueprints."""

app.blueprint(worker_bp)


@app.get('/alive.txt')
def get_alive(request):
    result = celery_app.control.inspect().ping()
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': 'No workers are alive !'}, status=503)
    return json('OK', status=200)


@app.head('/alive.txt')
def get_alive(request):
    result = celery_app.control.inspect().ping()
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': 'No workers are alive !'}, status=503)
    return json('OK', status=200)


@app.route('/')
def home(request):
    return json(
        {'message': 'Welcome to Audatar - API for Celery Health!'},
        headers={'X-Served-By': 'sanic'},
        status=200
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, workers=4, debug=False)
