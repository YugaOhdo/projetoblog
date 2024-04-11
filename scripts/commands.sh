#!/bin/sh

#O shell encerra a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do 
    echo "Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
    sleep 5
done

echo "Postgres Database Started Successsfully ($POSTGRES_HOST:$POSTGRES_PORT)"

collectstatic.sh #uma forma de executar scripts
makemigrations.sh
migrate.sh
runserver.sh
