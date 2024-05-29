# Local setup

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


## Query API using HTTPie

Generate a ticket (remember the ticket id and randomly generated group id):

    http POST localhost:5000/tickets/
    # repeat to create more tickets

Register analyst (role must be `group_analyst:<group id>`):

    http localhost:5000/me email=analyst1@example.com password=1 roles=group_analyst:1

Above command line sends application/json document using HTTP POST method to /me:

```json
{
    "email": "analyst1@example.com",
    "password": 1,
    "roles": "group_analyst:1"
}
```

Update ticket status:

    # -a 'analyst1@example.com:1' is `<username>:<password>` for BASIC AUTHENTICATION
    # endpoint is /tickets/<ticket id>/status
    # JSON is {"value": "in_review"}
    http -a 'analyst1@example.com:1' PUT localhost:5000/tickets/1/status value=in_review
