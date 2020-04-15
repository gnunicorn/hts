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

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn hts.wsgi:application --bind 0.0.0.0:8000 --workers 6