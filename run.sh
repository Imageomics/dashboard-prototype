#!/bin/bash
gunicorn -w ${BACKEND_WORKERS:=4} -b :5000 -t 360 dashboard:server
