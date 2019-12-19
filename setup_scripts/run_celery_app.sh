#!/bin/bash

echo "Step 1: Writing secrets"
python3 write_secrets_file.py
echo "Step 2: Starting workers"
PYTHONPATH=`pwd`:$PYTHONPATH OMP_NUM_THREADS=1 exec celery -A audatar.task_executor worker -l info -c 4 -n worker1@%h & \
celery -A audatar.task_executor worker -l info -c 4 -n worker2@%h & \
celery -A audatar.task_executor worker -l info -c 4 -n worker3@%h & \
celery -A audatar.task_executor worker -l info -c 4 -n worker4@%h &
echo "Step 3: Starting API for Celery"
PYTHONPATH=`pwd`:$PYTHONPATH OMP_NUM_THREADS=1 exec python3 audatar/celery_app.py
