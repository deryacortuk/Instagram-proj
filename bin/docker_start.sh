#!/bin/bash
NAME="web"
DJANGODIR=/app
USER=root
GROUP=root
NUM_WORKERS=10
DJANGO_WSGI_MODULE=Service.wsgi
DJANGO_SETTINGS_MODULE=Service.settings
DJANGO_SECRET_KEY=${SECRET_KEY}
DATABASE_NAME=${POSTGRES_DB}
DATABASE_USER=${POSTGRES_USER}
DATABASE_PASSWORD=${POSTGRES_PASSWORD}
DATABASE_HOST=pgdb
DATABASE_PORT=5432
PROD_USER=${ADMIN}
PROD_USER_EMAIL=${DJANGO_ADMIN_EMAIL}
PROD_USER_PASS=${DJANGO_ADMIN_PASSWORD}
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME}
ADMIN=${ADMIN}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL}
CELERY_BROKER=${CELERY_BROKER}
CELERY_BACKEND=${CELERY_BACKEND}
TIMEOUT=120
PYTHONPATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin



echo "Starting" $NAME as `whoami`
cd $DJANGODIR




export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

export C_FORCE_ROOT='true'



python manage.py makemigrations && \
  python manage.py migrate && \
  python manage.py initadmin && \
  

celery -A Service worker -l --pool=gevent --concurrency=100 --loglevel=info --logfile=logs/celery.log --detach
celery -A Service beat -l  --scheduler django_celery_beat.schedulers:DatabaseScheduler --logfile=logs/celery.log --detach

echo Starting Gunicorn.



exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--timeout $TIMEOUT \
--user=$USER --group=$GROUP \
--bind  0.0.0.0:8000 \
--log-level=debug \
--log-file=- \
--worker-class gevent \
--threads 10 \