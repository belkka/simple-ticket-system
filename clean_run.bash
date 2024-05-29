docker-compose down
docker-compose up -d

echo 'Sleeping 5 seconds...'
sleep 5
poetry run flask db_create_all
poetry run flask run --debug
