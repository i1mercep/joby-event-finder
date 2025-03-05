.PHONY: build run down build_dev down_dev test build_migration migration local_migration format requirements local_test

build:
	docker compose build --build-arg PIP_REQUIREMENTS_FILE=requirements.txt

run: build
	docker compose up

down:
	docker compose down --remove-orphans

# Development commands
build_dev:
	DEVELOPMENT=true USER=$(shell id -u) docker compose -f docker-compose.dev.yml build --build-arg PIP_REQUIREMENTS_FILE=requirements_dev.txt

run_dev: build_dev
	docker compose -f docker-compose.dev.yml up
	docker compose -f docker-compose.dev.yml down --remove-orphans

down_dev:
	docker compose docker-compose.dev.yml down --remove-orphans

test: build_dev
	DEVELOPMENT=true USER=$(shell id -u) docker compose -f docker-compose.dev.yml run --rm eventfinder_backend_dev \
		./scripts/test.sh $(TEST_ARGS)
	docker compose -f docker-compose.dev.yml down -v --remove-orphans

build_migration:
	DEVELOPMENT=true USER=$(shell id -u) docker compose -f docker-compose.migrations.yml build --build-arg PIP_REQUIREMENTS_FILE=requirements_dev.txt

migration: build_migration # call example: `make migration m="migration message"`
	DEVELOPMENT=true USER=$(shell id -u) docker compose -f docker-compose.migrations.yml run --rm eventfinder_backend_migrations \
		./scripts/migration.sh "$m" --abort-on-container-exit
	docker compose -f docker-compose.migrations.yml down -v --remove-orphans

# Local development commands
local_migration: # call example: `make generate_migration m="migration message"`
	./scripts/migration.sh "$m"

format:
	./scripts/format.sh

requirements:
	./scripts/requirements.sh

local_test:
	./scripts/test.sh
