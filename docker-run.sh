#!/bin/bash

CONTAINER_NAME=ae-audatar
IMAGE_NAME=dl2.homeawaycorp.com/analyticsengineering/$CONTAINER_NAME

docker run --rm -it --name ${CONTAINER_NAME}-base -p 8080:8080 \
    -p 10080:10080 \
    -e MPAAS_APPLICATION_NAME="ae-audatar-base" \
    -e MPAAS_ENVIRONMENT="dev" \
    -e HOST="127.0.0.1" \
    -e PORT_8080="8080" \
    -e PORT_10080="10080" \
    ${IMAGE_NAME}-base $@

docker run --rm -it --name ${CONTAINER_NAME}-flask -p 8080:8080 \
    -p 10080:10080 \
    -e MPAAS_APPLICATION_NAME="ae-audatar-flask" \
    -e MPAAS_ENVIRONMENT="dev" \
    -e HOST="127.0.0.1" \
    -e PORT_8080="8080" \
    -e PORT_10080="10080" \
    ${IMAGE_NAME}-flask $@

docker run --name ${CONTAINER_NAME}-node -p 5000:5000 \
    -p 10080:10080 \
    -e MPAAS_APPLICATION_NAME="ae-audatar-node" \
    -e MPAAS_ENVIRONMENT="dev" \
    -e HOST="127.0.0.1" \
    -e PORT_5000="5000" \
    -e PORT_10080="10080" \
    ${IMAGE_NAME}-node $@

docker run --name ${CONTAINER_NAME}-celery --rm -p 8080:8080 \
    -p 10080:10080 \
    -e MPAAS_APPLICATION_NAME="ae-audatar-celery" \
    -e MPAAS_ENVIRONMENT="dev" \
    -e HOST="127.0.0.1" \
    -e PORT_8080="8080" \
    -e PORT_10080="10080" \
    ${IMAGE_NAME}-celery $@

