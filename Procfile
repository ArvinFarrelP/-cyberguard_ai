web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn cyberguardai.wsgi:application --bind 0.0.0.0:$PORT --workers 1

web: python start.py