#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
    echo "$ENV"
    echo "Cassandra Server(Flask)"
    exec python "/home/uwsgi/app/cassandra_server.py"
else
    echo "Cassandra Server(uWSGI)"
    exec uwsgi --http 0.0.0.0:9090 --wsgi-file /home/uwsgi/app/cassandra_server.py --callable app --stats 0.0.0.0:9191
fi


