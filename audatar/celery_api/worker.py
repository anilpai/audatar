from sanic import Blueprint
from sanic.response import json
from audatar.extensions import celery as celery_app
import os

worker_bp = Blueprint('worker', url_prefix='/api/workers')

inspect = celery_app.control.inspect()


@worker_bp.route('/ping')
async def ping(request):
    """Ping worker(s)."""
    err_msg = 'No workers are alive !'
    result = inspect.ping()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/active', methods=['GET'])
async def active(request):
    """List of tasks currently being executed."""
    err_msg = 'No workers are active !'
    result = inspect.active()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/stats', methods=['GET'])
async def stats(request):
    """Request worker statistics/information."""
    err_msg = 'No workers available for stats !'
    result = inspect.stats()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=404)


@worker_bp.route('/registered', methods=['GET'])
async def registered(request):
    """List of registered tasks."""
    err_msg = 'No workers are registered !'
    result = inspect.registered()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/reserved', methods=['GET'])
async def reserved(request):
    """List of currently reserved tasks, not including scheduled/active."""
    err_msg = 'No workers are registered !'
    result = inspect.reserved()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/scheduled', methods=['GET'])
async def scheduled(request):
    """List of currently scheduled ETA/countdown tasks."""
    err_msg = 'No workers are scheduled !'
    result = inspect.scheduled()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/revoked', methods=['GET'])
async def revoked(request):
    """List of revoked task-ids."""
    err_msg = 'No workers are revoked !'
    result = inspect.revoked()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/active_queues', methods=['GET'])
async def active_queues(request):
    """List the task queues a worker is currently consuming from."""
    err_msg = 'No queues are active !'
    result = inspect.active_queues()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/clock', methods=['GET'])
async def clock(request):
    """Get current logical clock value."""
    err_msg = 'No clock !'
    result = inspect.clock()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/memsample', methods=['GET'])
async def memsample(request):
    """Sample current RSS memory usage."""
    err_msg = 'No mem sample !'
    result = inspect.memsample()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)


@worker_bp.route('/memdump', methods=['GET'])
async def memdump(request):
    """Dump statistics of previous memsample requests."""
    err_msg = 'No mem dump !'
    result = inspect.memdump()
    if result is None:
        return json({'msg': err_msg}, status=503)
    hostname = os.uname().nodename
    result = {k: v for k, v in result.items() if k.endswith('@{0}'.format(hostname))}
    result['count'] = len(result)
    if result['count'] == 0:
        return json({'msg': err_msg}, status=503)
    return json(result, status=200)
