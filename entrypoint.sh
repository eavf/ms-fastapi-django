#!/bin/bash

RUN_PORT=${PORT:-8000}

/usr/local/bin/gunicorn --worker-tmp-dir /dev/shm -k uvicorn.workers.UvicornWorker main.py --bind "0.0.0.0:${RUN_PORT}"