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
fi

if [ "$1" = 'start' ]; then
  gunicorn hts.wsgi:application --bind 0.0.0.0:8000 --workers 6
fi

exec "$@"