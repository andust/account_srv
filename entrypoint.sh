#!/bin/sh


postgres_ready() {
    $(which curl) http://$DB_HOST:$DB_PORT/ 2>&1 | grep '52'
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 2
done
>&2 echo 'PostgreSQL is available.'

cd src/infra/database/ && alembic upgrade head && cd ../../../


uvicorn src.main:app --host 0.0.0.0 --port $UVICORN_MAP_PORT --reload
