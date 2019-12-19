#!/bin/bash

CONTAINER_NAME=ae-audatar

IMAGE_NAME=dl2.homeawaycorp.com/analyticsengineering/${CONTAINER_NAME}

docker run --rm -i \
    --name ${CONTAINER_NAME}-base \
     ${IMAGE_NAME}-base


docker run --rm -i \
    --name ${CONTAINER_NAME}-flask \
     ${IMAGE_NAME}-flask


docker run --rm -i \
    --name ${CONTAINER_NAME}-ui \
     ${IMAGE_NAME}-ui

docker run --rm -i \
    --name ${CONTAINER_NAME}-celery \
     ${IMAGE_NAME}-celery
