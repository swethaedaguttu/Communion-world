web: gunicorn community_connect.wsgi --log-file -
worker: celery -A community_connect worker --loglevel=info
