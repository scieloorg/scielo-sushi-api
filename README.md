SciELO SUSHI API

## Instalation
```shell script
virtualenv -p python3.6 .venv
source .venv/bin/activate
pip install -e .
pip install -e ".[dev]" # only on development environments
```

## Configuration
File `{development|production}.ini` must be configured with the credentials of the Matomo Database and the application url, as follows:

1. `sqlalchemy.url = mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}`
2. `application.url = http://{HOST}:{PORT}`
3. `listen = {HOST}:{PORT}`


## Database
```shell script
initialize_db development.ini
```

## Automatic testing
```shell script
pytest api/tests.py -q
```

## Running
```shell script
pserve development.ini --reload
```
