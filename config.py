import os
NUM_WORKERS=2
NUM_THREADS=4
keepalive = 100
# worker_class = 'gevent'
workers = int(os.environ.get('GUNICORN_PROCESSES', NUM_WORKERS))
threads = int(os.environ.get('GUNICORN_THREADS', NUM_THREADS))
# workers = 2
# threads = 4
timeout = 120
forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
loglevel = 'debug'
