.PHONY: tests

# buildkit is more efficient
DOCKER_BUILDKIT=1
DOCKER_COMPOSE=docker compose
DOCKER_RUN=${DOCKER_COMPOSE} run --rm --no-deps facets-api


build:
	${DOCKER_COMPOSE} build

up:
	${DOCKER_COMPOSE} up

# recompile languages files
build_lang:
	${DOCKER_RUN} find i18n -name \*.po -execdir msgfmt knowledge-panel.po -o knowledge-panel.mo \;

# lint code
lint:
	${DOCKER_RUN} isort .
	${DOCKER_RUN} black .

# check code quality
quality:
	${DOCKER_RUN} flake8 .
	${DOCKER_RUN} isort --check-only .
	${DOCKER_RUN} black --check .

tests:
	${DOCKER_RUN} pytest .

checks: quality tests

# To ease the process for contributors
all: build_lang lint checks