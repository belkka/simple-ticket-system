Run postgres in docker:

    docker-compose up

Write a .env file:

    cp example.env .env

Activate virtualenv (and install missing dependencies):

    poetry shell

Create tables in empty db (no migrations, what a shame!):

    flask db_create_all  # inside `poetry shell`
    # or
    poetry run flask db_create_all

Run API (in virtualenv):

    flask run  # inside `poetry shell`
    # or
    poetry run flask run

Access API at localhost:5000 (default port used by Flask)
