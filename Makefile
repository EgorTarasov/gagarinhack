# check if we have .env file and load it
ifneq ("$(wildcard .env)","")
    include .env
    export
endif

POSTGRES_SETUP_TEST := user=${POSTGRES_USER} password=${POSTGRES_PASSWORD} dbname=${POSTGRES_DB} host=${POSTGRES_HOST} port=${POSTGRES_PORT} sslmode=disable
MIGRATION_FOLDER=$(CURDIR)/migrations

.PHONY: pip
pip:
	pip install -r requirements/dev.txt

.PHONY: pip-prod
pip-prod:
	pip install -r requirements/prod.txt

.PHONY: run-in-docker
run-in-docker:
	docker-compose up -d --build
.PHONY: proto-py
proto-py:
	python -m grpc_tools.protoc -Iproto --python_out=src/grpc --pyi_out=src/grpc --grpc_python_out=src/grpc proto/search.proto

.PHONY: redis
redis:
	docker-compose up redis -d --build

.PHONY: createdb
createdb:
	docker-compose up postgres -d --build

.PHONY: rabbitmq
rabbitmq:
	docker-compose up rabbitmq -d --build

.PHONY: worker
worker: rabbitmq
	celery -A src.worker worker --loglevel=info

.PHONY: fastapi
fastapi:
	python3 -m uvicorn --app-dir ./src/ main:app --reload

.PHONY: migration-create
migration-create:
	goose -dir "$(MIGRATION_FOLDER)" create "$(name)" sql

.PHONY: migration-up
migration-up:
	goose -dir "$(MIGRATION_FOLDER)" postgres "$(POSTGRES_SETUP_TEST)" up

.PHONY: migration-down
migration-down:
	goose -dir "$(MIGRATION_FOLDER)" postgres "$(POSTGRES_SETUP_TEST)" down


# запуск на сервере, с докером
move:



deploy:
	ssh -i $(SERVER_USERNAME):$(SERVER_PASSWORD)@$(SERVER_URL) "cd gagarinhach && git pull && "

stop_deploy:
	ssh -i $(SERVER_USERNAME)@$(SERVER_URL) "cd gagarinhach && docker compose -f deployment/docker-compose.yaml down"