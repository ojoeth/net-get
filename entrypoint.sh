#!/bin/ash
set -e
redis-server --daemonize yes
sleep 1
celery worker --detach -B -l info -A net_get
gunicorn -b :80 wsgi:webapp
exec "$@"