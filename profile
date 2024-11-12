web: gunicorn community_connect.wsgi --log-file -
worker: celery -A community_connect_backend worker --log level=info