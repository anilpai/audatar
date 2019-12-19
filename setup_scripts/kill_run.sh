#!/bin/bash

env=$1

if [ "$env" == "prod" ] || [ "$env" == "stage" ] ||  [ "$env" == "dev" ];
then
    # Set environment variable
    export ENV=$env

    # Kill all existing processes
    sudo killall -9 python3
    sudo killall -9 celery
    
    # Run
    PYTHONPATH=`pwd`:$PYTHONPATH OMP_NUM_THREADS=1 exec python3 manage.py run & celery -A audatar.task_executor --loglevel=info worker &
    celery -A audatar.task_executor flower & python3 -m audatar.monitor &
else
    echo "Missing or invalid environment argument. Valid values are 'prod', 'stage', and 'dev'. Example: 'run.sh stage'"
fi


# THIS FILE HAS BEEN DEPRECATED.