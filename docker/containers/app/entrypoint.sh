#!/bin/sh


postgres_ready() {
    $(which curl) http://$DB_HOST:$DB_PORT/ 2>&1 | grep '52'
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 2
done
>&2 echo 'PostgreSQL is available.'

uvicorn src.main:app --host 0.0.0.0 --port 8081 --reload

