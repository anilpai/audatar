#!/bin/bash

env=$1
BASIC_AUTH=$2:$3

if [[ -z "$2" ]];
then
    echo "Flower Username is missing"
fi

if [[ -z "$3" ]];
then
    echo "Flower Password is missing"
fi

if [ "$env" == "prod" ] || [ "$env" == "stage" ] ||  [ "$env" == "dev" ];
then
    export ENV=$env
    PYTHONPATH=`pwd`:$PYTHONPATH OMP_NUM_THREADS=1 exec celery flower -A audatar.task_executor --basic_auth=$BASIC_AUTH &
else
    echo "Missing or invalid environment argument. Valid values are 'prod', 'stage', and 'dev'. Example: 'run.sh stage'"
fi
