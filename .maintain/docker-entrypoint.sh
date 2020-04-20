#!/bin/sh
set -e

until psql $DATABASE_URL -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
	python manage.py load_initial_data
fi

if [ "$1" = 'migrate' ]; then
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  exit 0
fi


if [ "$1" = 'worker' ]; then
  celery -A hts worker --loglevel=info
  exit 0
fi

uwsgi --ini /code/hts-uwsgi.ini
