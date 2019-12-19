#!/bin/bash

python3 write_secrets_file.py
BASIC_AUTH=$(head -n 1 ./setup_scripts/flower_creds.txt)
PYTHONPATH=`pwd`:$PYTHONPATH OMP_NUM_THREADS=1 exec flower -A audatar.task_executor --port=5555 -l info --basic_auth=$BASIC_AUTH

# THIS FILE HAS BEEN DEPRECATED.