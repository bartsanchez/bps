.PHONY: build start stop logs ps

START_SERVICES ?=
RUN_SERVICE ?=

COMPOSE_EXEC ?= docker compose

build:
	${COMPOSE_EXEC} build

start:
	${COMPOSE_EXEC} up -d $(START_SERVICES)

stop:
	${COMPOSE_EXEC} down

run:
	${COMPOSE_EXEC} run --rm $(RUN_SERVICE)

logs:
	${COMPOSE_EXEC} logs $(ARGS)

ps:
	${COMPOSE_EXEC} ps
