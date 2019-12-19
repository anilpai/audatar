from audatar.extensions import Celery as celery_app


def monitor(app):
    """Configure Controller to monitor celery."""

    state = app.events.State()

    def announce_task_status(event):
        app.event(event)
        try:
            task = state.tasks.get(event['uuid'])
            print(vars(task))
            print('TASK {0}:[{1}] {2}' % (task.state, task.name, task.uuid, task.info()))
        except Exception as e:
            print(str(e))

    def task_succeeded(event):
        announce_task_status(event)
        state.event(event)
        try:
            task = state.tasks.get[event['uuid']]
            print(vars(task))
            print('Task record updated in database')
        except Exception as e:
            print(str(e))

    def worker_offline(event):
        state.event(event)
        print(' Worker just went offline !!')

    def worker_online(event):
        state.event(event)
        print(' Worker is now online !!')

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
            'task-started': announce_task_status,
            'task-sent': announce_task_status,
            'task-received': announce_task_status,
            'task-succeeded': task_succeeded,
            'task-failed': announce_task_status,
            'task-rejected': announce_task_status,
            'task-revoked': announce_task_status,
            'task-retired': announce_task_status,
            'worker-online': worker_online,
            'worker_offline': worker_offline,
            'worker-heartbeat': None
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    monitor(celery_app)
