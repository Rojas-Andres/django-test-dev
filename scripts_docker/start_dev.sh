#!/usr/bin/env bash

echo "Executing start_dev.sh"
bash /tmp/postgres-healthy.sh
python manage.py migrate --noinput
python manage.py runserver 0:8000
