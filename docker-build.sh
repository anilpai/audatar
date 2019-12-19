#!/bin/bash

NAME=dl2.homeawaycorp.com/analyticsengineering/ae-audatar
if [[ $1 != '--no-base' ]]; then
    docker build -t ${NAME}-base -f Dockerfile-base .
fi

docker build -t ${NAME}-flask -f Dockerfile-flask .
docker build -t ${NAME}-node -f Dockerfile-node .
docker build -t ${NAME}-celery -f Dockerfile-celery .
