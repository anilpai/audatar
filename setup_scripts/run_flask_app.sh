#!/bin/bash

python3 write_secrets_file.py
PYTHONPATH=`pwd`:$PYTHONPATH OMP_NUM_THREADS=1 exec python3 manage.py run