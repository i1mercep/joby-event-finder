# Event finder Backend

REST API with SQLite DB

## Requirements

* docker
* docker compose
* make
* python (3.13) (optional: to run `populate_db.py`)

## Run

Environment file `env` must be set.

Example is provided in `env.dist`

```bash
cp env.dist env
```

Run the container

```bash
make run
```

API docs: https://localhost:8000/docs

To populate database with test data:

```bash
python populate_db.py
```
### Endpoint examples

* http://localhost:8000/api/v1/users
* http://localhost:8000/api/v1/venues
* http://localhost:8000/api/v1/events

## Development

### Tests

```bash
make test
```

### Run development image

```bash
make run_dev
```

### Generate migration

When database schema is changed run:

```bash
make migration m="msg"
```


