#!/bin/bash

python3 ../write_secrets_file.py

yarn install && yarn build && node server.js
