.PHONY: tests

# buildkit is more efficient
DOCKER_BUILDKIT=1
DOCKER_RUN=docker-compose run --rm --no-deps facets-api


docker_build:
	docker-compose build

docker_up:
	docker-compose up

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