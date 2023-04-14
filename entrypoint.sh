#!/bin/sh

echo "*** Starting entrypoint.sh ***"
echo "*** Running collectstatic ***"

# python manage.py collectstatic --noinput --settings=cognied.settings.prod

echo "*** Running migrations ***"
python manage.py wait_for_db --settings=cognied.settings.prod
# python manage.py migrate --settings=cognied.settings.prod

echo "*** Starting server ***"
gunicorn --env DJANGO_SETTINGS_MODULE=cognied.settings.prod cognied.wsgi:application --bind 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000 --settings=cognied.settings.dev
echo "*** Server listo ***"